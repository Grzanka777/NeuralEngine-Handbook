# NeuralEngine Engineering Handbook

# NeuralEngine Constitution

## Mission

Build an engine that transforms observations into reusable knowledge, executable playbooks, evaluated outcomes, and controlled evolution.

## Core principles

1. Correctness before speed.
2. Domain before persistence.
3. Explicit dependencies before convenience.
4. Architecture before implementation shortcuts.
5. Deterministic behavior where practical.
6. Validation before persistence.
7. Small coherent changes.
8. Tests as executable specifications.
9. Review evidence before success claims.
10. No commits or pushes by agents.

## Forbidden

- Business logic in CLI handlers.
- Business logic in infrastructure adapters.
- Hidden dependencies.
- Global mutable state.
- Silent validation failure.
- Scope expansion.
- Unrelated refactoring.
- Repository interfaces used as service APIs.
- Manual edits to generated handbook outputs.

---

# Architecture

NeuralEngine follows a hexagonal architecture.

## Layers

- Domain
- Application
- Ports
- Infrastructure
- CLI

## Dependency rules

- Domain depends on no outer layer.
- Application depends on domain and ports.
- Infrastructure implements ports.
- CLI invokes application services.
- Dependency construction belongs in the container.
- Infrastructure must never depend on CLI.

## Responsibility rules

- Entities and value objects own domain invariants.
- Application services own use cases.
- Repository ports define persistence contracts.
- Adapters implement persistence contracts.
- CLI translates input and renders output.
- Relationship navigation should be composed in services when it does not belong in persistence.

## Revision lifecycle and application boundary

The current end of the domain chain is deliberately split across three immutable records:

```text
PlaybookRevision
→ PlaybookRevisionActivation
→ PlaybookRevisionApplication
```

`PlaybookRevision` is a candidate snapshot. `PlaybookRevisionActivation` records lifecycle and
audit decisions. `PlaybookRevisionApplication` records application intent and audit state.
Activation does not imply application.

`PlaybookRevisionActivationService.get_active_revision_for_playbook(playbook_id)` is the canonical
owner of active-revision resolution. `PlaybookRevisionApplicationService` delegates to it and must
not duplicate activation-history replay.

The application foundation has a domain model, repository port, JSON adapter at
`NeuralPaths.PLAYBOOK_REVISION_APPLICATIONS`, and container wiring for both repository and service.
`PlaybookRevisionApplicationService.add(...)` validates that the Playbook, revision, and proposal
exist; the proposal is still accepted; the revision belongs to the supplied Playbook and proposal;
an optional source activation exists and matches the same relation; and the requested revision is
currently active.

Read-only application navigation verifies the source entity, calls
`PlaybookRevisionApplicationRepository.load_all()`, filters in the application layer, and preserves
repository order. No relation-specific repository query methods exist.

Activation inspection and lifecycle-write CLI commands exist. Application CLI commands do not.
Records created by the current application service have `content_changed=False`; there is no
Playbook content mutation, revision materialization, proposal mutation or application, proposal
status change, or automatic evolution.

This architecture snapshot corresponds to source commit `88921c5` (`feat: add playbook revision
application foundation`). Source validation for that milestone reported 537 passing tests; this is
a milestone snapshot, not a timeless guarantee.

## Decision Learning boundary

Source commit `7724342` implements the immutable `Decision` and embedded `EvidenceReference`, a
persistence-focused repository port and JSON adapter, `DecisionService`, container wiring, and
thin `neural decision add/list/show` commands. The service owns Observation and supersession
validation plus load-and-filter idempotency; the CLI constructs no repositories.

`DecisionAcceptance`, `DecisionAction`, `DecisionOutcome`, and `DecisionReview` remain future-only.
There is no ingestion, automatic learning, lifecycle replay, or Consigliere integration. The
authoritative implemented contract and future boundary are defined in
`handbook/architecture/decision-learning.md`.

---

# Decision Learning Architecture

## Status and purpose

NeuralEngine source commit `7724342` implements the Decision foundation. It records an immutable
proposed choice and bounded evidence references, persists Decisions, exposes application use
cases, wires them through the container, and provides a thin CLI.

The wider Decision Learning lifecycle remains accepted future architecture. Decision tracking
complements the existing Observation-to-Playbook chain; it does not replace it.

## Implemented foundation

The implemented slice is exactly:

```text
Decision
EvidenceReference
DecisionRepository
JsonDecisionRepository
DecisionService
container wiring
neural decision add/list/show
```

Creating a Decision records a proposal. It does not accept or execute the proposal and does not
create any downstream learning record. `DecisionAcceptance`, `DecisionAction`, `DecisionOutcome`,
and `DecisionReview` are future-only records.

## Decision model

`Decision` is an immutable domain model with these implemented fields:

```text
id
created_at
project_key
title
objective
context_summary
alternatives
proposed_option
rationale
observation_ids
evidence_references
proposed_by
supersedes_decision_id
idempotency_key
tags
```

Its implemented invariants are:

1. Required text is trimmed and non-blank.
2. At least two meaningful alternatives are required.
3. Alternatives reject case-insensitive duplicates.
4. `proposed_option` exactly matches one stored alternative.
5. Observation IDs are unique.
6. An optional superseded Decision must not equal the new Decision.
7. Tags are trimmed; case-insensitive duplicates are removed while first-seen order is preserved.
8. `created_at` is timezone-aware and normalized to UTC.
9. The model is immutable.
10. No mutable lifecycle status exists.

A material correction creates another Decision linked through `supersedes_decision_id`; it does
not rewrite the earlier record.

## EvidenceReference

`EvidenceReference` is an implemented immutable value embedded in a Decision:

```text
kind
locator
repository_or_project
content_hash
captured_at
source
summary
```

`kind` and `locator` are required, trimmed, non-blank, and bounded. Optional text is trimmed,
bounded, and cannot be blank when supplied. `captured_at` is timezone-aware and normalized to UTC.
The complete value is serialized inside Decision JSON.

There is no Evidence repository, service, or CLI. A locator is retained as provenance only: the
Decision CLI does not open it, verify it, or ingest its content.

## Persistence

The persistence-focused `DecisionRepository` port implements only:

```text
save()
load_all()
get_by_id()
```

No relation, project, or idempotency query was added. `JsonDecisionRepository` stores one JSON
file per Decision under `NeuralPaths.DECISIONS`. UUIDs, UTC-aware timestamps, embedded evidence,
and optional values round-trip through the domain model. `load_all()` sorts file names for
deterministic order. Malformed stored data surfaces domain validation errors; the adapter does not
silently repair it. No migration, evidence ingestion, file ingestion, or git ingestion behavior
exists.

## Application service

`DecisionService` implements:

```text
add()
list_decisions()
show()
```

`add()` constructs an immutable Decision candidate first, validates every referenced Observation,
then validates an optional superseded Decision. A superseded Decision must exist and have the same
`project_key`. Only after these checks does the service perform idempotency detection and, when
needed, persist the candidate. It creates no other record, performs no lifecycle transition, and
does not trigger learning.

The implemented idempotency scope is:

```text
(project_key, "decision", idempotency_key)
```

The `"decision"` record type is implicit because the operation is owned by `DecisionService`.
Detection uses `DecisionRepository.load_all()` followed by application-layer filtering; there is
no repository idempotency query.

```text
same key + equivalent semantic payload
→ return existing Decision

same key + different semantic payload
→ visible conflict, no write
```

Semantic equivalence excludes generated identity and time values:

```text
Decision.id
Decision.created_at
EvidenceReference.captured_at
```

`list_decisions()` preserves repository order. Its optional project filter is trimmed and applied
in the application layer; a blank filter fails visibly. `show()` loads by UUID and raises the
existing explicit not-found error when no Decision exists.

## Container

The composition root constructs and connects:

```text
JsonDecisionRepository
JsonObservationRepository
DecisionService
```

The CLI resolves `DecisionService` from the container. It does not construct repositories or own
validation, relation checks, persistence, or idempotency policy.

## Implemented CLI

These commands exist at commit `7724342`:

```text
neural decision add
neural decision list
neural decision show DECISION_UUID
```

`neural decision add` requires these scalar options:

```text
--project-key
--title
--objective
--context-summary
--proposed-option
--rationale
--proposed-by
--idempotency-key
```

It accepts these repeatable options:

```text
--alternative
--observation-id
--evidence
--tag
```

The optional supersession argument is:

```text
--supersedes-decision-id
```

Evidence is supplied as a bounded JSON value, for example:

```bash
neural decision add \
  --project-key NeuralEngine \
  --title "Canonical lifecycle ownership" \
  --objective "Choose one active-revision owner" \
  --context-summary "Two services could derive the same state" \
  --alternative "Activation service owns derivation" \
  --alternative "Application service replays records" \
  --proposed-option "Activation service owns derivation" \
  --rationale "One owner prevents semantic drift" \
  --proposed-by architecture-review \
  --idempotency-key decision-active-revision-owner \
  --evidence '{"kind":"agent_review","locator":".agent-work/reviews/review.md"}'
```

The CLI parses and validates this JSON value as `EvidenceReference`. It does not read the locator
or ingest any referenced file content.

`neural decision list --project PROJECT_KEY` filters through the service and renders:

```text
ID
Created
Project
Title
Proposed option
Proposed by
```

`neural decision show DECISION_UUID` renders the full Decision details, including alternatives,
Observation IDs, embedded evidence references, optional supersession, idempotency key, and tags.

## Future lifecycle boundary

The accepted future record family remains deliberately separate:

```text
Decision
→ DecisionAcceptance
→ DecisionAction
→ DecisionOutcome
→ DecisionReview
```

- `Decision` is the implemented proposed choice.
- `DecisionAcceptance` would explicitly authorize execution.
- `DecisionAction` would record work performed under an accepted Decision.
- `DecisionOutcome` would record factual results and validation evidence.
- `DecisionReview` would assess outcomes and hold candidate lessons.

Only the first record exists. The future records must remain immutable semantic records rather
than fields on a mutable Decision or a duplicate generic event stream. A proposed option is not an
acceptance, an outcome is not an Experience, and candidate lessons are not automatically Knowledge
or a Playbook change.

The intended future projection is `proposed → accepted → executed → reviewed`, derived by an
application service from future records. Commit `7724342` implements no lifecycle replay or
projection service.

## Relationship to the domain chain

The implemented Decision may reference existing Observations as context. Everything after the
Decision remains an explicit future bridge:

```text
Observation
→ Decision
→ future DecisionAcceptance
→ future DecisionAction
→ future DecisionOutcome
→ future DecisionReview
→ explicitly created Experience
→ explicitly created Knowledge
```

`DecisionOutcome` remains distinct from Experience, and Decision review must never mutate a
Playbook. Any future connection to PlaybookRun, PlaybookEvaluation, EvolutionProposal, or the
revision lifecycle requires a separate reviewed use case.

## Self-observation and Consigliere boundaries

The future dogfooding flow remains a design direction:

```text
prompt
→ agent execution
→ review finding
→ decision/correction
→ implementation
→ validation
→ commit
→ push
→ post-work lesson
```

Commit `7724342` does not capture or ingest those events. Automatic candidates and manual
confirmation remain future concepts; no automatic persistence, ingestion, or learning exists.

Consigliere also remains future-only. It may later advise. No Consigliere integration exists, and
no recommendation can directly mutate NeuralEngine or authorize a durable record.

## Current non-behavior

Commit `7724342` does not implement:

```text
DecisionAcceptance
DecisionAction
DecisionOutcome
DecisionReview
decision lifecycle replay
evidence repository
file ingestion
git ingestion
automatic Observation creation
automatic Experience creation
automatic Knowledge creation
automatic Playbook creation or mutation
automatic evolution
Consigliere integration
```

It also does not execute commands referenced by evidence, open locators, accept Decisions,
materialize Playbook revisions, or create any record other than the explicitly requested Decision.

## Recommended next milestone

The one recommended next controlled slice is:

```text
DecisionAcceptance foundation
```

It must remain separate from `DecisionAction` and `DecisionOutcome`.

## Handbook synchronization policy

Generated Handbook outputs are rebuilt from source documents and templates and are never edited
manually. Copying the generated skill back to NeuralEngine is outside this synchronization task.

---

# Responsibility Matrix

| Concern | Owning layer | Forbidden locations |
|---|---|---|
| Domain invariant | Domain | CLI, adapter |
| Use-case orchestration | Application | CLI, repository adapter |
| Persistence contract | Port | Domain, CLI |
| Persistence implementation | Infrastructure | Domain, application |
| Dependency construction | Container | Domain entity, service |
| Input parsing | CLI | Domain entity |
| Output rendering | CLI | Repository |
| Relationship navigation | Application service by default | Repository unless persistence-owned |
| Validation of domain state | Domain/application as appropriate | Infrastructure-only |
| Provenance policy | Domain/application architecture | CLI-only |

---

# Domain Chain

The confirmed NeuralEngine chain is:

`Observation`
→ `Experience`
→ `Knowledge`
→ `Playbook`
→ `PlaybookRun`
→ `PlaybookEvaluation`
→ `EvolutionProposal`
→ `PlaybookRevision`
→ `PlaybookRevisionActivation`
→ `PlaybookRevisionApplication`

The final three stages are separate records with separate responsibilities:

- `PlaybookRevision` is an immutable candidate snapshot.
- `PlaybookRevisionActivation` is an immutable lifecycle and audit decision.
- `PlaybookRevisionApplication` is an immutable application-intent and audit record.

Creating a revision does not activate or apply it. Activation does not imply application.
The current application foundation records intent only: it does not materialize revision
content into a Playbook or mutate any related record.

## Relationship ownership

Relationship navigation belongs in application services unless persistence itself owns the concern.

Confirmed example:

- `PlaybookRevisionService.list_for_playbook(UUID)` owns playbook revision navigation.
- `PlaybookRevisionActivationService` owns activation navigation and canonical active-revision
  derivation through `get_active_revision_for_playbook(playbook_id)`.
- `PlaybookRevisionApplicationService` owns application-record navigation and delegates active
  revision resolution to `PlaybookRevisionActivationService`.
- Repository interfaces remain persistence-focused.
- `PlaybookService` should not gain unrelated persistence dependencies.

## Complementary Decision Learning chain

The implemented Decision foundation records a bounded proposed choice after Observation context:

```text
Observation
→ Decision
→ future DecisionAcceptance
→ future DecisionAction
→ future DecisionOutcome
→ future DecisionReview
→ Experience
→ Knowledge
```

This is a complementary provenance path, not a replacement for the canonical domain chain.
DecisionOutcome is factual; Experience is interpreted; Knowledge is generalized; Playbook remains
a separately created repeatable procedure. Only Decision and its embedded EvidenceReference exist
at source commit `7724342`; no transition in this path is automatic.

---

# Observation

## Responsibility

An Observation captures a raw, bounded fact or signal before interpretation.

## Owns

- source reference,
- observed content,
- capture metadata,
- identity,
- creation timestamp when applicable.

## Must not own

- derived meaning,
- reusable guidance,
- playbook execution logic,
- evaluation logic.

## Architectural role

Observation is the entry point of the NeuralEngine knowledge chain.

## Invariants

- Identity is explicit.
- Source/provenance is preserved.
- Content is not silently rewritten into interpretation.
- Validation occurs before persistence.

## Typical transitions

`Observation` → `Experience`

The transition must be performed by an application use case, not a repository adapter.

---

# Experience

## Responsibility

An Experience represents interpreted learning derived from one or more observations.

## Owns

- interpreted outcome,
- contextual meaning,
- provenance back to observations,
- identity.

## Must not own

- generalized reusable knowledge,
- execution instructions,
- evaluation policy.

## Invariants

- Provenance is preserved.
- Interpretation is explicit.
- Creation does not erase source observations.

## Typical transitions

`Experience` → `Knowledge`

The application layer coordinates this transformation.

---

# Knowledge

## Responsibility

Knowledge is reusable, generalized understanding derived from experience.

## Owns

- normalized insight,
- reusable statement,
- provenance to source experiences,
- identity.

## Must not own

- executable workflow steps,
- runtime execution state,
- evaluation outcome.

## Invariants

- Knowledge must be sufficiently generalized to be reusable.
- Provenance remains available.
- Domain validation precedes persistence.

## Typical transitions

`Knowledge` → `Playbook`

---

# Playbook

## Responsibility

A Playbook defines an executable or operationalized procedure derived from knowledge.

## Owns

- executable intent,
- ordered guidance or steps,
- identity,
- revision-related semantics through dedicated services.

## Must not own

- execution state,
- evaluation outcome,
- repository traversal logic,
- infrastructure-specific behavior.

## Invariants

- A playbook is distinct from a run.
- Revision navigation is owned by `PlaybookRevisionService`.
- Persistence concerns remain outside the domain object.

## Typical transitions

`Playbook` → `PlaybookRun`

---

# PlaybookRun

## Responsibility

A PlaybookRun represents one execution instance of a playbook.

## Owns

- playbook reference,
- execution state,
- runtime inputs and outputs where modeled,
- identity.

## Must not own

- reusable playbook definition,
- evaluation policy,
- proposal approval logic.

## Invariants

- A run references exactly one playbook identity.
- Runtime state must not mutate the playbook definition.
- Evaluation is modeled separately.

## Typical transitions

`PlaybookRun` → `PlaybookEvaluation`

---

# PlaybookEvaluation

## Responsibility

A PlaybookEvaluation records the assessment of a completed or assessable playbook run.

## Owns

- run reference,
- evaluation result,
- evidence or rationale where modeled,
- identity.

## Must not own

- playbook execution,
- revision persistence,
- evolution proposal application.

## Invariants

- Evaluation targets a specific run.
- Evaluation semantics are explicit.
- Evaluation does not silently mutate a playbook.

## Typical transitions

`PlaybookEvaluation` → `EvolutionProposal`

---

# EvolutionProposal

## Responsibility

An EvolutionProposal expresses a controlled suggestion for changing a playbook based on evaluation evidence.

## Owns

- source evaluation reference,
- proposed change,
- rationale,
- lifecycle state where modeled,
- identity.

## Must not own

- direct mutation of the playbook,
- revision persistence implementation,
- approval side effects outside application services.

## Invariants

- Proposal provenance is preserved.
- Proposal and applied revision are distinct concepts.
- Public behavior changes require architectural review.

## Typical transitions

`EvolutionProposal` → `PlaybookRevision`

---

# PlaybookRevision

## Responsibility

A PlaybookRevision is an immutable candidate snapshot of explicitly supplied revised Playbook
content. It is linked to one existing Playbook and one accepted EvolutionProposal.

## Owns

- playbook reference,
- revised content and metadata,
- source proposal reference,
- identity.

## Must not own

- repository navigation,
- unrelated playbook service responsibilities,
- infrastructure-specific persistence behavior.
- activation state,
- application state.

## Lifecycle boundary

Creating a revision does not mutate the Playbook, apply the proposal, activate the revision, or
perform automatic evolution. Activation and application are represented by separate immutable
records.

## Confirmed application rule

`PlaybookRevisionService.list_for_playbook(UUID)` owns revision navigation for a playbook.

The repository port remains persistence-focused and should not gain a broad `find_by_playbook_id` method solely to move application navigation into persistence.

## Invariants

- Revision identity is explicit.
- Parent playbook identity is explicit.
- Provenance to proposal is preserved.
- Revision creation does not change proposal status.
- Revision creation does not apply proposal changes.

---

# PlaybookRevisionActivation

## Responsibility

A PlaybookRevisionActivation is a separate immutable lifecycle and audit record for an explicit
manual or external-system decision about one PlaybookRevision.

Supported decisions are:

- `active`,
- `superseded`,
- `rejected`.

Activation does not imply application. It does not materialize revision content into a Playbook,
mutate a Playbook or PlaybookRevision, change EvolutionProposal status, apply a proposal, or
perform automatic evolution.

## Application ownership

`PlaybookRevisionActivationService` owns read-only lifecycle navigation by Playbook,
PlaybookRevision, and EvolutionProposal. It also owns canonical active-revision derivation through:

```python
PlaybookRevisionActivationService.get_active_revision_for_playbook(playbook_id)
```

Activation records are replayed in repository order only inside this service. Consumers must
delegate active-revision resolution rather than duplicate lifecycle replay.

Each relation-list method verifies its source entity, loads all activation records through
`PlaybookRevisionActivationRepository.load_all()`, filters in the application layer, and preserves
repository order. No relation-specific repository query methods are added.

## Current CLI

Read-only lifecycle inspection exists through:

```text
neural playbook revision-history PLAYBOOK_UUID
neural playbook active-revision PLAYBOOK_UUID
neural revision activation-history REVISION_UUID
neural proposal activation-history PROPOSAL_UUID
```

Explicit lifecycle decisions can be recorded through:

```text
neural revision activate ...
neural revision supersede ...
neural revision reject ...
```

These write only PlaybookRevisionActivation records.

---

# PlaybookRevisionApplication

## Responsibility

A PlaybookRevisionApplication is an immutable application-intent and audit record. The current
foundation records that an active revision reached an explicit application boundary; it does not
materialize or copy revision content into a Playbook.

Current fields are:

```text
id
applied_at
playbook_id
revision_id
proposal_id
reason
applied_by
notes
tags
source_activation_id
idempotency_key
content_changed
```

`content_changed` defaults to `False`.

## Current foundation

The implemented vertical-slice foundation includes:

- the `PlaybookRevisionApplication` domain model,
- `PlaybookRevisionApplicationRepository`,
- `JsonPlaybookRevisionApplicationRepository`,
- `NeuralPaths.PLAYBOOK_REVISION_APPLICATIONS`,
- container repository and service wiring,
- `PlaybookRevisionApplicationService.add(...)`,
- read-only `list_for_playbook(...)`, `list_for_revision(...)`, and
  `list_for_proposal(...)` navigation.

## Invariants and non-behavior

Creating an application record does not mutate Playbook, PlaybookRevision, EvolutionProposal, or
PlaybookRevisionActivation records. It does not change proposal status, apply a proposal, or
perform automatic evolution.

There is currently:

- no CLI apply command,
- no CLI application-history commands,
- no Playbook content mutation,
- no PlaybookRevision materialization,
- no proposal application,
- no application-specific repository query method.

---

# Application Services

## Responsibility

Application services coordinate use cases across domain objects and ports.

They own orchestration, not persistence implementation or user-interface rendering.

## Required properties

Every application service should:

- expose one coherent responsibility,
- depend on ports rather than concrete adapters,
- preserve domain validation order,
- coordinate provenance explicitly,
- remain testable without CLI, database, filesystem, or network,
- avoid constructing dependencies internally,
- return domain/application results rather than rendered text.

## Service boundary rules

A service may:

- load entities through repository ports,
- invoke domain behavior,
- coordinate multiple domain objects,
- persist results through ports,
- raise explicit application errors,
- compose relationship navigation.

A service must not:

- instantiate repositories,
- import CLI modules,
- render Rich tables,
- parse command-line strings,
- depend on concrete SQL/filesystem adapters,
- silently change public behavior,
- absorb unrelated use cases.

## Public method design

Prefer explicit methods named after use cases.

Good:

```python
revision_service.list_for_playbook(playbook_id)
```

Avoid generic, ambiguous methods:

```python
service.process(data)
service.handle(value)
```

## Service growth rule

When a service gains unrelated responsibilities, split by use case or domain ownership.

Do not split merely to reduce line count. Split when reasons to change diverge.

## Revision lifecycle ownership

`PlaybookRevisionActivationService` owns active-revision derivation through
`get_active_revision_for_playbook(playbook_id)`.

`PlaybookRevisionApplicationService.add(...)` validates the Playbook, revision, accepted proposal,
relation consistency, optional source activation, and current active revision before saving one
application audit record. It delegates active-revision resolution to the activation service.

Its relation-list methods verify the source entity, load all application records, filter in the
application layer, preserve repository order, and perform no mutation.

## Decision service ownership

`DecisionService.add()` creates an immutable candidate, validates referenced Observations and an
optional same-project superseded Decision, then performs idempotency detection through repository
`load_all()` and application-layer filtering. Its scope is
`(project_key, "decision", idempotency_key)`; no repository query method exists.

An equivalent replay returns the existing Decision. Reusing the same key with a different semantic
payload fails visibly without writing. Generated Decision identity and timestamps, including
embedded `EvidenceReference.captured_at`, are excluded from semantic comparison.

`list_decisions()` preserves repository order and may filter by a non-blank project key in the
application layer. `show()` owns the explicit not-found behavior. No lifecycle transition,
automatic learning, or downstream record creation is part of this service.

---

# Application Errors

## Purpose

Application errors communicate expected use-case failures across layer boundaries.

## Rules

- Use explicit error types.
- Include stable contextual identifiers.
- Preserve the original cause when wrapping infrastructure errors.
- Keep rendering outside the error type.
- Avoid leaking adapter-specific exception classes into CLI.

Good:

```python
raise PlaybookNotFoundError(playbook_id)
```

Avoid:

```python
raise Exception("something failed")
```

## Mapping

- Domain violations remain domain errors.
- Missing application resources use application errors.
- Infrastructure failures are translated at adapter/application boundaries.
- CLI maps application errors to user-facing messages and exit codes.

---

# Ports

## Responsibility

Ports define the contracts required by the application layer from external systems.

## Port design rules

A port must:

- describe application needs, not adapter capabilities,
- use domain/application types,
- avoid database-specific concepts,
- remain minimal,
- have behaviorally meaningful method names,
- be mockable or replaceable in tests.

A port must not expose:

- SQL,
- ORM sessions,
- filesystem paths unless the application concept requires them,
- HTTP response objects,
- CLI rendering concerns,
- concrete adapter classes.

## Change policy

Changing a port is architectural work.

A port change requires:

- Codex GPT-5.5 medium,
- review of all implementations,
- review of service call sites,
- updated contract tests,
- full validation.

---

# Repository Ports

## Responsibility

Repository ports define persistence operations needed by application services.

## Allowed operations

Typical operations include:

- add/save,
- get by identity,
- list,
- delete when domain policy allows it,
- narrowly justified persistence queries.

## Forbidden expansion

Do not add repository methods merely because a relationship exists.

First ask whether the application service can compose the navigation from existing persistence operations.

Confirmed rule:

`PlaybookRevisionService.list_for_playbook(UUID)` owns playbook revision navigation.

`PlaybookRevisionApplicationRepository` remains limited to `save()`, `load_all()`, and
`get_by_id()`. Navigation by Playbook, PlaybookRevision, or EvolutionProposal is composed by
`PlaybookRevisionApplicationService`; no relation-specific query methods are part of the port.

`DecisionRepository` is likewise limited to `save()`, `load_all()`, and `get_by_id()`.
Project filtering and idempotency detection belong to `DecisionService`; no project or idempotency
query method is part of the port.

## Repository return types

Prefer:

- domain entities,
- value objects,
- explicit optional results,
- application-facing collections.

Avoid:

- ORM models,
- database rows,
- SQL tuples,
- adapter-specific pagination objects.

## Not-found behavior

Choose one consistent contract:

- return `None`, or
- raise an explicit port/application error.

Do not mix behavior across implementations.

---

# Infrastructure Adapters

## Responsibility

Adapters implement ports using concrete external mechanisms.

Examples:

- filesystem persistence,
- SQL persistence,
- JSON serialization,
- clock providers,
- UUID providers.

## Adapter rules

Adapters may:

- translate between persistence and domain representations,
- handle external resource lifecycle,
- convert external failures into stable adapter/application errors,
- enforce storage-level constraints that mirror domain requirements.

Adapters must not:

- decide business policy,
- change validation order,
- infer domain transitions,
- render CLI output,
- orchestrate use cases,
- silently repair invalid domain state.

## Mapping rule

Mapping code should be explicit and testable.

Persistence models must not leak into application services.

---

# Repository Adapters

## Responsibility

Repository adapters implement repository ports.

## Implementation rules

- Preserve domain identity exactly.
- Preserve provenance fields.
- Make serialization round-trippable.
- Keep ordering deterministic when public behavior depends on ordering.
- Handle missing records according to the port contract.
- Do not broaden the port from inside the adapter.
- Do not add business filtering without an application requirement.

## Testing requirements

Repository adapters require tests for:

- save and load,
- missing identity,
- list behavior,
- ordering where relevant,
- serialization round trip,
- invalid/corrupted persisted data,
- provenance preservation.

## Revision application adapter

`JsonPlaybookRevisionApplicationRepository` implements
`PlaybookRevisionApplicationRepository` and stores application audit records under
`NeuralPaths.PLAYBOOK_REVISION_APPLICATIONS`. It supplies only the port's basic save, load-all, and
identity lookup operations; relation filtering remains in the application layer.

## Decision adapter

`JsonDecisionRepository` implements `DecisionRepository` and stores one JSON file per Decision
under `NeuralPaths.DECISIONS`. UUIDs, timestamps, optional values, and embedded
`EvidenceReference` values round-trip through domain validation. `load_all()` sorts file names for
deterministic order, and malformed data surfaces validation errors. The adapter performs no
project filtering, idempotency query, migration, or ingestion.

---

# Dependency Injection and Container

## Responsibility

The container is the composition root.

It constructs concrete adapters and injects them into application services.

## Rules

The container may:

- instantiate repositories,
- instantiate infrastructure providers,
- instantiate application services,
- define lifecycle and sharing policy,
- expose configured services to CLI.

The container must not:

- contain business logic,
- perform use-case orchestration,
- parse CLI arguments,
- hide mutable global state,
- create cyclic dependencies.

## Constructor injection

Prefer constructor injection.

Good:

```python
service = PlaybookRevisionService(repository=revision_repository)
```

Avoid service locator access inside services:

```python
repository = container.get("revision_repository")
```

## Change policy

Any container or registration change is architectural work owned by Codex.

The current revision application foundation is wired through
`Container.playbook_revision_application_repository()` and
`Container.playbook_revision_application_service()`. The service receives its repositories and a
`PlaybookRevisionActivationService`, preserving canonical ownership of active-revision resolution.

The Decision foundation is wired through `Container.decision_repository()` and
`Container.decision_service()`. The container supplies `JsonDecisionRepository` and
`JsonObservationRepository` to `DecisionService`; Decision CLI handlers resolve the service and do
not construct repositories.

---

# Dependency Lifecycle

## Default policy

Prefer explicit, simple lifetimes.

- Stateless services may be reused.
- Repositories may be reused when their adapter is safe to share.
- Per-operation resources must be scoped explicitly.
- Global mutable singletons are forbidden.

## Resource ownership

The component that opens an external resource must have a defined closing strategy.

Examples:

- database connection/session,
- file handle,
- transaction,
- network client.

Resource cleanup must not depend on process termination.

---

# Cookbook: Add an Application Service

1. Identify the exact use case.
2. Confirm no existing service already owns it.
3. Identify required domain entities and value objects.
4. Identify required ports.
5. Define explicit application errors.
6. Implement constructor-injected dependencies.
7. Implement one coherent public method.
8. Add service-level tests using fakes.
9. Wire the service in the container.
10. Add CLI integration only if requested.
11. Run full validation.
12. Produce the review artifact.

---

# Cookbook: Add a Repository

1. Confirm the domain concept requires persistence.
2. Confirm a repository is the correct abstraction.
3. Define the minimal repository port.
4. Use domain/application types in the contract.
5. Implement the adapter.
6. Add mapping and round-trip tests.
7. Add missing-record behavior tests.
8. Register the adapter in the container.
9. Inject the repository into the owning service.
10. Run full validation.
11. Produce the review artifact.

---

# Cookbook: Add an Adapter

1. Start from an existing port.
2. Do not design from the external library API.
3. Map external types to domain/application types.
4. Translate external failures.
5. Define resource lifecycle.
6. Add adapter contract tests.
7. Register the adapter in the container.
8. Verify no concrete adapter leaks inward.
9. Run full validation.
10. Produce the review artifact.

---

# Cookbook: Wire the Container

1. Identify new concrete dependencies.
2. Confirm service constructors remain explicit.
3. Instantiate adapters before services.
4. Inject ports through constructor arguments.
5. Avoid service-locator access.
6. Keep lifecycle policy explicit.
7. Add or update container tests.
8. Verify CLI resolves the service, not the adapter.
9. Run full validation.
10. Produce the review artifact.

---

# Anti-pattern: Fat Service

## Symptom

One application service coordinates unrelated use cases and depends on many unrelated ports.

## Risk

- high coupling,
- difficult testing,
- unclear ownership,
- unrelated changes collide.

## Correction

Split by use-case responsibility or domain ownership.

Do not split solely by file length.

---

# Anti-pattern: God Repository

## Symptom

A repository exposes relationship navigation, filtering, reporting, validation, and business operations.

## Risk

- persistence controls application behavior,
- services become thin wrappers,
- adapters become difficult to replace,
- domain decisions leak outward.

## Correction

Keep persistence methods minimal. Move orchestration and navigation into application services.

---

# Anti-pattern: Service Locator

## Symptom

Application code fetches dependencies from a global container at runtime.

## Risk

- hidden dependencies,
- brittle tests,
- runtime failures,
- cyclic coupling.

## Correction

Use constructor injection and keep the container at the composition root.

---

# Anti-pattern: Business Logic in Adapter

## Symptom

An infrastructure adapter decides validation, eligibility, transition, or policy.

## Risk

- behavior changes when adapters change,
- domain rules become untestable in isolation,
- persistence becomes the source of truth.

## Correction

Move policy into domain or application services. Keep the adapter focused on translation and external interaction.

---

# Application Service Checklist

- Is the use case explicit?
- Does one service clearly own it?
- Are dependencies constructor-injected?
- Are dependencies ports rather than adapters?
- Is business logic outside CLI and infrastructure?
- Are errors explicit?
- Is validation order preserved?
- Is provenance preserved?
- Can the service be tested without external systems?
- Are tests written with fakes?
- Is container wiring updated?
- Is Codex assigned when architecture changes?

---

# Repository Checklist

- Does the domain concept require persistence?
- Is the port minimal?
- Are method names persistence-focused?
- Are domain/application types used?
- Is relationship navigation better owned by a service?
- Is missing-record behavior consistent?
- Are adapters covered by round-trip tests?
- Is ordering deterministic where observable?
- Is provenance preserved?
- Are all implementations updated after a port change?

---

# Adapter Checklist

- Does the adapter implement an existing port?
- Are external types translated?
- Are external failures mapped?
- Is resource lifecycle explicit?
- Is business policy absent?
- Is validation order unchanged?
- Are adapter contract tests present?
- Does no adapter type leak inward?
- Is container registration explicit?

---

# Container Checklist

- Is the container only composing dependencies?
- Are constructors explicit?
- Are adapters instantiated before services?
- Are lifetimes clear?
- Is mutable global state absent?
- Are cyclic dependencies absent?
- Does CLI resolve services rather than repositories?
- Are container tests updated?

---

# ADR-0005: Constructor injection

Status: Accepted

## Decision

Application services receive dependencies through constructors.

The dependency container remains the composition root.

## Consequences

- Dependencies are visible.
- Services are testable with fakes.
- Service-locator access inside application code is prohibited.

---

# ADR-0006: Minimal application-driven ports

Status: Accepted

## Decision

Ports describe the minimum contracts required by application use cases.

They do not mirror every capability of an external library or persistence technology.

## Consequences

- Adapters remain replaceable.
- Port changes require architectural review.
- External types do not leak into application code.

---

# ADR-0007: Adapters contain no business policy

Status: Accepted

## Decision

Infrastructure adapters translate and interact with external systems but do not own business rules or use-case orchestration.

## Consequences

- Business behavior remains stable across adapter changes.
- Domain and service tests can run without infrastructure.
- Adapter tests focus on contracts and translation.

---

# Development Workflow

## Before work

1. Read `AGENTS.md`.
2. Read `.agent-work/project-state.md` when present.
3. Run `./scripts/validate.sh`.
4. Inspect affected code and tests.
5. Define the smallest complete scope.
6. Create a task prompt under `.agent-work/prompts/`.

## During work

- Implement a coherent vertical slice.
- Follow current patterns.
- Add tests with implementation.
- Preserve public behavior unless explicitly changing it.
- Preserve persisted schemas unless explicitly changing them.
- Avoid unrelated cleanup.

## After work

1. Run `./scripts/validate.sh`.
2. Create a review file under `.agent-work/reviews/`.
3. Include validation output, diff stat, diff check, git status, and full diff.
4. Stop without committing or pushing.

## Future self-observation workflow

NeuralEngine development is intended to become a dogfooding source through:

```text
prompt
→ agent execution
→ review finding
→ decision/correction
→ implementation
→ validation
→ commit
→ push
→ post-work lesson
```

Automatic capture produces candidates only. Manual confirmation authorizes durable records;
immutable records preserve the audit trail; derived summaries remain replaceable views. No
automatic persistence, ingestion, or learning exists.

## Handbook synchronization

```text
major NeuralEngine milestone
→ commit/push NeuralEngine
→ sync NeuralEngine-Handbook
→ generate SKILL.md
→ copy generated SKILL.md back to NeuralEngine
→ commit/push skill sync
```

Each repository change is separate and reviewable. Generated outputs are rebuilt from Handbook
sources and are never edited manually.

---

# Validation Policy

Preferred command:

```bash
./scripts/validate.sh
```

Required checks:

```bash
ruff format --check .
ruff check .
mypy src tests
pytest
```

Never claim success unless all required checks pass.

When validation fails:

- show the failing command,
- include relevant output,
- identify whether the failure is pre-existing,
- do not bypass or suppress the failure.

---

# Agent Assignment Policy

## Codex GPT-5.5 medium

Use for:

- new features,
- domain models,
- vertical slices,
- ports and adapters,
- repositories and services,
- dependency injection,
- CLI additions,
- persisted schema changes,
- public behavior changes,
- validation-order changes,
- provenance decisions,
- architectural documentation.

## DeepSeek

Use only for small controlled post-review fixes, normally one to three files:

- one concrete bug,
- targeted regression tests,
- Ruff or MyPy corrections,
- small message, type, validation, or CLI-option fixes,
- minor refactors without behavior change.

Every DeepSeek prompt must begin with reading `AGENTS.md`.

Required scope guard:

> Do not add features. Do not broaden scope. Do not change architecture, persisted schemas, public behavior, validation order, or provenance rules. Modify only the files required for the specified fix.

---

# Pattern: New Feature

1. Identify the owning domain concept.
2. Decide whether the change requires a new entity or extends an existing one.
3. Define or update ports.
4. Implement adapters.
5. Implement the application service.
6. Wire dependencies in the container.
7. Add CLI only when required.
8. Add unit, service, adapter, and CLI tests as applicable.
9. Run full validation.
10. Produce the review artifact.

---

# Pattern: Controlled Bug Fix

1. Reproduce the problem.
2. Add a regression test when practical.
3. Fix the root cause.
4. Run targeted tests.
5. Run full validation.
6. Produce the review artifact.
7. Stop without committing or pushing.

---

# Definition of Done

A task is complete only when:

- requested behavior is implemented,
- scope has not expanded,
- architectural boundaries are preserved,
- tests cover the change,
- all required validation passes,
- prompt and review artifacts exist,
- review includes complete evidence,
- no commit or push was performed.

---

# Review Checklist

- Is the requested scope complete?
- Were unrelated changes avoided?
- Are layer responsibilities preserved?
- Is business logic in the correct layer?
- Are repository interfaces persistence-focused?
- Are tests sufficient?
- Did validation pass?
- Does the review include diff stat, diff check, git status, and full diff?
- Were persisted schemas or public behavior changed?
- Was any commit or push performed?

---

# Domain Change Checklist

- Which entity or value object owns the new responsibility?
- Does the change preserve the canonical domain chain?
- Is provenance preserved?
- Is validation placed before persistence?
- Does the change require a new port?
- Does it require an adapter?
- Does it require application orchestration?
- Does container wiring change?
- Does public behavior change?
- Does persisted schema change?
- Are unit and service tests sufficient?
- Is Codex assigned?

---

# New CLI Command Checklist

- Does an application service already expose the required use case?
- Is business logic absent from the command handler?
- Is dependency resolution delegated to the container?
- Are UUID inputs validated consistently?
- Are errors mapped to useful user-facing messages?
- Are CLI tests included?
- Is public output intentionally specified?
- Is the task assigned to Codex?

---

# ADR-0001: Service-owned relationship navigation

Status: Accepted

## Decision

Relationship navigation that can be composed from persistence operations belongs in application services rather than repository interfaces.

## Context

Playbook revision navigation previously risked expanding repository responsibilities and coupling unrelated services.

## Consequences

- Repository ports remain persistence-focused.
- Application services own use-case navigation.
- Service tests describe the relationship behavior.

---

# ADR-0002: Canonical domain chain

Status: Accepted

## Decision

The canonical NeuralEngine chain is:

`Observation`
→ `Experience`
→ `Knowledge`
→ `Playbook`
→ `PlaybookRun`
→ `PlaybookEvaluation`
→ `EvolutionProposal`
→ `PlaybookRevision`
→ `PlaybookRevisionActivation`
→ `PlaybookRevisionApplication`

## Consequences

- New features must identify their position in the chain.
- Transitions are application use cases.
- Provenance must not be lost between stages.
- A later-stage object must not silently absorb the responsibility of an earlier-stage object.
- Revision, activation, and application remain separate explicit records.
- Activation does not imply application, and application intent does not imply materialization.

---

# ADR-0003: Agent assignment policy

Status: Accepted

## Decision

Codex GPT-5.5 medium owns architectural and feature work.

DeepSeek is restricted to small, controlled, post-review fixes, normally one to three files.

## Consequences

- New features are never delegated to DeepSeek.
- Repository, service, container, CLI, schema, public behavior, validation-order, and provenance changes belong to Codex.
- DeepSeek prompts require an explicit scope guard.

---

# ADR-0004: Mandatory prompt and review artifacts

Status: Accepted

## Decision

Every agent task must have:

- a prompt in `.agent-work/prompts/`,
- a review in `.agent-work/reviews/`.

The review must contain validation output, diff stat, diff check, git status, and full diff.

## Consequences

- Agent work is inspectable before commit.
- Success claims require evidence.
- Agents do not commit or push.

---

# ADR-0008: Decision Learning boundary

Status: Accepted

## Decision

Development decision tracking uses an implemented immutable `Decision` with embedded immutable
`EvidenceReference` values. `DecisionAcceptance`, `DecisionAction`, `DecisionOutcome`, and
`DecisionReview` remain separate future-only records. Any future lifecycle state is derived from
those semantic records, not stored as mutable `Decision.status` or duplicated in a generic event
stream.

Decision tracking complements the existing Observation-to-Playbook chain. Evidence uses bounded
embedded references, durable writes require explicit authority, and Consigliere remains a future
advisory layer rather than authoritative storage.

## Consequences

- Recommendation, acceptance, execution, factual outcome, review, and learning remain distinct.
- Corrections append records instead of rewriting history.
- Application services own cross-record validation, derived state, and initial load-and-filter
  idempotency checks; repository ports remain persistence-focused.
- No automatic ingestion, persistence, learning, Playbook evolution, or Consigliere integration is
  implied.
- Source commit `7724342` implements only the Decision foundation and `neural decision
  add/list/show`; it does not implement the later lifecycle.
- The one recommended next milestone is `DecisionAcceptance foundation`, kept separate from
  DecisionAction and DecisionOutcome.
