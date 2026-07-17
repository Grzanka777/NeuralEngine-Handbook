# NeuralEngine Decision Engine

# Decision Engine

Use this document before implementation.

## Agent selection

### Use Codex GPT-5.5 medium when any answer is yes

- Does the task add a feature?
- Does it change the domain model?
- Does it touch more than one architectural layer?
- Does it add or change a port?
- Does it add or change an adapter?
- Does it change a repository interface?
- Does it change dependency injection?
- Does it add a CLI command?
- Does it change persisted schema?
- Does it change public behavior?
- Does it change validation order?
- Does it change provenance semantics?
- Does it add architecture documentation?

### DeepSeek is allowed only when all are true

- The task is a concrete post-review correction.
- The change is normally limited to one to three files.
- No feature is added.
- No architecture changes.
- No persisted schema changes.
- No public behavior changes.
- No validation-order changes.
- No provenance changes.

## Layer decision tree

```text
Does the behavior express a domain invariant?
├── Yes → Domain
└── No
    └── Does it coordinate a use case?
        ├── Yes → Application service
        └── No
            └── Does it define an external contract?
                ├── Yes → Port
                └── No
                    └── Does it implement an external concern?
                        ├── Yes → Infrastructure adapter
                        └── No
                            └── Is it user interaction/rendering?
                                ├── Yes → CLI
                                └── No → Reassess the design
```

## Repository decision tree

```text
Is the requested operation persistence?
├── No → Do not add it to a repository
└── Yes
    └── Is it generic persistence behavior?
        ├── Yes → Repository port may own it
        └── No
            └── Can application services compose it?
                ├── Yes → Keep it in the service
                └── No → Require architecture review
```

## New feature decision tree

```text
New behavior
├── Domain concept changed?
│   ├── Yes → Domain + tests
│   └── No
├── Persistence required?
│   ├── Yes → Port + adapter + tests
│   └── No
├── Use-case orchestration required?
│   ├── Yes → Application service + tests
│   └── No
├── Dependency wiring changed?
│   ├── Yes → Container + tests
│   └── No
└── User-facing command required?
    ├── Yes → CLI + tests
    └── No
```

## Priority order

1. Correctness.
2. Domain integrity.
3. Architecture.
4. Maintainability.
5. Testability.
6. Performance.
7. Convenience.

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
