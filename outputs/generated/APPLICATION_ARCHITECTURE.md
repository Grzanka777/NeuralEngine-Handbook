# NeuralEngine Application Architecture

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

## Decision acceptance service ownership

`DecisionAcceptanceService.accept()` validates Decision existence, constructs an immutable
candidate, and uses `DecisionAcceptanceRepository.load_all()` for idempotency and first-acceptance
eligibility. The scope is `(decision_id, "decision_acceptance", idempotency_key)`. Equivalent
semantic replay returns the existing record; conflicting reuse of the key and a distinct second
acceptance both fail visibly without writing.

`list_for_decision()` verifies the Decision, filters acceptance records in the application layer,
and preserves repository order. `show()` owns explicit acceptance not-found behavior. Acceptance
does not mutate Decision or create actions, outcomes, reviews, execution, or learning.

## Decision action ownership

`DecisionActionService.add()` validates the Decision, matching acceptance, and optional
PlaybookRun before creating an immutable action. It uses
`(decision_id, "decision_action", idempotency_key)` for application-layer idempotency, permits
multiple distinct actions, and mutates no related record. PlaybookRun and Playbook expose no
`project_key`, so the service can validate only run existence without a schema change.

`list_for_decision()` validates the Decision, filters `load_all()` in repository order, and
`show()` owns explicit action-not-found behavior. The service creates no Outcome, Review, or
learning record.

## Decision outcome and lifecycle ownership

`DecisionOutcomeService.add()` validates the Decision, matching acceptance, one or more unique
actions, each action's Decision and acceptance relations, and validation time against the earliest
linked action start before constructing or saving an immutable outcome. It uses
`(decision_id, "decision_outcome", idempotency_key)` for application-layer idempotency. Zero
matches creates normally; exactly one equivalent match returns the existing outcome; exactly one
different match conflicts. More than one persisted scoped match raises
`DecisionOutcomeIdempotencyAmbiguityError`, regardless of payload equivalence or repository order,
without selecting a duplicate or writing. Another key may append another outcome for the same
Decision.

`list_for_decision()` validates the Decision and returns all matching outcomes in repository order.
`show()` owns explicit outcome-not-found behavior. `summary_for_decision()` validates persisted
outcome relations and returns an immutable, non-persisted `DecisionOutcomeSummary` with outcome
count, deterministic latest result/time, distinct linked-action count, counts by result, and
success/failure presence. Latest selection uses `(validated_at, outcome.id)` rather than repository
order.

`DecisionLifecycleService` is the only canonical projection owner. It validates persisted
Decision/acceptance/action/outcome relations and derives exactly `proposed`, `accepted`,
`in_progress`, `succeeded`, `failed`, `partial`, or `outcome_unknown`. When outcomes exist, the
latest is selected by `(validated_at, outcome.id)`. It writes no status and exposes no generic
`completed`, `resolved`, or reviewed state. Outcome creation and projection create no Review or
learning record.

## Decision review ownership

`DecisionReviewService.add()` first constructs the immutable candidate, then validates Decision,
matching acceptance, every explicit ordered outcome relation, and that `reviewed_at` is not earlier
than the latest referenced outcome validation. It writes only after all validation. The scope is
`(decision_id, "decision_review", idempotency_key)`: zero matches creates, exactly one equivalent
match replays, and exactly one different match raises `DecisionReviewIdempotencyConflictError`.
More than one match raises `DecisionReviewIdempotencyAmbiguityError` with identifying details,
independent of repository order and duplicate payload equivalence, without arbitrary selection,
semantic comparison against a selected duplicate, or a write.

Semantic comparison for the exactly-one-match case excludes generated review ID and recording
time plus evidence capture times. It includes ordered outcome IDs, findings, candidate lessons,
evidence, tags, and every other caller-supplied semantic field, so ordered collections remain order
sensitive. `list_for_decision()` validates the Decision and every persisted review relation, then
sorts by `(reviewed_at, review.id)`. `show()` validates persisted relations and owns explicit
review-not-found behavior.

Multiple reviews may cover one Decision, one outcome, or the same ordered outcome set under
different keys. Corrections append; the service has no replacement, supersession, deletion, or
`current` behavior. It creates no Experience, Knowledge, Playbook, proposal, or Consigliere work
and does not participate in `DecisionLifecycleService`.

The DecisionOutcome and DecisionReview duplicate-key rules are the same reusable fail-closed
application-service invariant: more than one persisted match for a scoped key is corruption or
ambiguity to surface, never an ordering problem to resolve by choosing the first record. Their
scopes and controlled ambiguity error types remain separate.

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

`DecisionAcceptanceRepository` is also limited to `save()`, `load_all()`, and `get_by_id()`.
Decision relation filtering, eligibility, and idempotency belong to
`DecisionAcceptanceService`; no relation, project, or idempotency query method is part of the port.

`DecisionActionRepository` is limited to `save()`, `load_all()`, and `get_by_id()`.
Relation validation, Decision filtering, idempotency, and lifecycle projection belong to
application services; no relation, idempotency, or lifecycle query method is part of the port.

`DecisionOutcomeRepository` is limited to `save()`, `load_all()`, and `get_by_id()`.
Decision filtering, acceptance/action relation validation, multiple-outcome history, idempotency,
summary derivation, and lifecycle projection belong to application services; no relation,
idempotency, summary, latest-outcome, or lifecycle query method is part of the port.

`DecisionReviewRepository` is likewise limited to `save()`, `load_all()`, and `get_by_id()`.
Decision filtering, cross-record validation, history ordering, and scoped idempotency—including
fail-closed duplicate-match ambiguity—belong to `DecisionReviewService`; no relation,
idempotency, chronology, or lifecycle query method is part of the port.

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

## Decision acceptance adapter

`JsonDecisionAcceptanceRepository` implements `DecisionAcceptanceRepository` and stores one JSON
file per acceptance under `NeuralPaths.DECISION_ACCEPTANCES`; Brain initialization creates the
directory. UUIDs, timestamps, embedded evidence, and tags round-trip through domain validation.
`load_all()` sorts file names for deterministic order, and malformed data surfaces validation
errors. The adapter performs no relation filtering, eligibility decision, migration, or ingestion.

## Decision action adapter

`JsonDecisionActionRepository` implements `DecisionActionRepository` and stores one JSON file per
action under `NeuralPaths.DECISION_ACTIONS`; Brain initialization creates the directory. Complete
DecisionAction records round-trip through domain validation. `load_all()` sorts file names for
deterministic order, and malformed data surfaces validation errors. The adapter performs no
relation filtering, lifecycle projection, migration, ingestion, or command execution.

## Decision outcome adapter

`JsonDecisionOutcomeRepository` implements `DecisionOutcomeRepository` and stores one JSON file
per outcome under `NeuralPaths.DECISION_OUTCOMES`; Brain initialization creates the directory.
Complete DecisionOutcome records, including immutable scalar metrics, round-trip through domain
validation. JSON object keys and metric keys are serialized deterministically, `load_all()` sorts
file names, and malformed data surfaces validation errors. The adapter performs no relation
validation or filtering, latest-outcome selection, summary or lifecycle projection, idempotency
decision, migration, ingestion, review, or learning.

## Decision review adapter

`JsonDecisionReviewRepository` implements `DecisionReviewRepository` and stores one JSON file per
review under `NeuralPaths.DECISION_REVIEWS`; Brain initialization creates the directory. Complete
DecisionReview records round-trip through domain validation. JSON object keys are serialized with
`indent=2` and `sort_keys=True`, `load_all()` sorts filenames, and malformed data surfaces
validation errors. The adapter performs no Decision filtering, relation validation, chronology,
idempotency selection, lifecycle projection, evidence ingestion, learning, or Consigliere work.

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

The acceptance foundation is wired through `Container.decision_acceptance_repository()` and
`Container.decision_acceptance_service()`. The container supplies
`JsonDecisionAcceptanceRepository` and `JsonDecisionRepository` to
`DecisionAcceptanceService`; acceptance CLI handlers construct no repositories.

The action foundation is wired through `Container.decision_action_repository()` and
`Container.decision_action_service()`. The action service receives JSON action, Decision,
acceptance, and PlaybookRun repositories.

The outcome foundation is wired through `Container.decision_outcome_repository()` and
`Container.decision_outcome_service()`. The outcome service receives JSON outcome, Decision,
acceptance, and action repositories. `Container.decision_lifecycle_service()` receives those same
four repository categories so it can validate relations and derive the canonical state. Decision
action, outcome, summary, and state CLI handlers resolve services and construct no repositories.

The review foundation is wired through `Container.decision_review_repository()` and
`Container.decision_review_service()`. The service receives `JsonDecisionReviewRepository`,
`JsonDecisionRepository`, `JsonDecisionAcceptanceRepository`, and
`JsonDecisionOutcomeRepository`. Brain initialization creates `NeuralPaths.DECISION_REVIEWS`.
Decision review CLI handlers resolve the service and construct no repositories.

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
