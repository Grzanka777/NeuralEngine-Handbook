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

Source commit `1b45beb9b595b650a48ad00ba3ea38f7eebd02b6` preserves the separate immutable
`Decision`, `DecisionAcceptance`, `DecisionAction`, `DecisionOutcome`, and `DecisionReview`
records, persistence-focused ports and JSON adapters, application services, container wiring,
thin proposal/acceptance/action/outcome/review CLI commands, and the canonical
`DecisionLifecycleService`. An action records work performed; only a linked outcome records
factual results and validation evidence; a review records authorized interpretation.

`DecisionOutcome` links one Decision, its acceptance, and one or more ordered unique actions. Its
result is exactly `succeeded`, `failed`, `partial`, or `unknown`; scalar metrics are immutable.
Multiple outcomes form history, and the non-persisted `DecisionOutcomeSummary` derives counts and
the latest outcome using `(validated_at, outcome.id)` rather than repository order.
`DecisionReview` targets an explicit ordered non-empty set of outcomes for one Decision and
acceptance. Multiple reviews form immutable history ordered by `(reviewed_at, review.id)`.

The same checkpoint implements explicit Review-to-Experience promotion. One Experience may embed
optional immutable `DecisionReviewPromotion` provenance containing ordered copied Review
statements. `ExperienceService` uses the validated Review service boundary and existing Experience
repository; no promotion aggregate, repository, adapter, path, Brain collection, or automatic
learning exists. Old and ordinary Experiences remain compatible.

The checkpoint also hardens the existing explicit Knowledge slice. `KnowledgeService` depends on
the narrow application-facing `ExperienceReader.get_by_id()` protocol, and the container supplies
`ExperienceService` as its implementation. Knowledge creation and returned Knowledge relations
therefore reuse `ExperienceService.get_by_id()` as the single owner of persisted Review-promotion
provenance validation. The dependency remains acyclic because `ExperienceService` has no
KnowledgeService dependency.

`KnowledgeService.add()` rejects empty evidence before relation reads, validates IDs in caller
order, preserves duplicates, and writes only after every read succeeds. `add_from_experience()`
uses the same boundary. Complete list and present single-item reads validate every stored
Experience relation; the scoped Experience navigation validates its requested Experience and all
relations of matching Knowledge records while leaving unrelated records outside the query.
Missing Experiences retain `ExperienceNotFoundError`, while canonical DecisionReview and
promotion errors propagate unchanged.

The canonical lifecycle states remain exactly `proposed`, `accepted`, `in_progress`, `succeeded`,
`failed`, `partial`, and `outcome_unknown`. Review is orthogonal append-only history; there is no
`reviewed`, `promoted`, or `learned` state. Outcome or review creation does not create learning;
only the explicit promotion use case creates an Experience, which remains distinct from Knowledge.
There is no execution engine, lifecycle reversal, ingestion, automatic learning or evolution,
generic event replay, or
Consigliere integration. The authoritative implemented contract and future boundary are defined
in `handbook/architecture/decision-learning.md`. Generic Knowledge creation is already explicit;
`neural experience knowledge` is read-only navigation. Durable operational Knowledge use and
feedback remain a separate future gap, and storing Knowledge does not prove later improvement.

---

# Decision Learning Architecture

## Status and purpose

NeuralEngine source commit `1b45beb9b595b650a48ad00ba3ea38f7eebd02b6` implements the Decision,
DecisionAcceptance, DecisionAction, DecisionOutcome, and DecisionReview foundations plus the
canonical `DecisionLifecycleService` projection. They record an immutable proposed choice,
explicit authorization, work performed under that authorization, factual results, and authorized
interpretation, plus explicit promotion of selected Review statements into an existing Experience.
Each foundation persists its durable records, exposes application use cases, is wired through the
container, and provides a thin CLI.

The wider Decision Learning lifecycle remains accepted future architecture. Decision tracking
complements the existing Observation-to-Playbook chain; it does not replace it.

## Implemented foundation

The implemented foundations are exactly:

```text
Decision
EvidenceReference
DecisionAcceptance
DecisionAction
DecisionOutcome
DecisionReview
DecisionReviewPromotion
DecisionReviewPromotionSourceStatement
DecisionRepository
DecisionAcceptanceRepository
DecisionActionRepository
DecisionOutcomeRepository
DecisionReviewRepository
JsonDecisionRepository
JsonDecisionAcceptanceRepository
JsonDecisionActionRepository
JsonDecisionOutcomeRepository
JsonDecisionReviewRepository
DecisionService
DecisionAcceptanceService
DecisionActionService
DecisionOutcomeService
DecisionOutcomeSummary
DecisionReviewService
ExperienceService.add_from_decision_review
ExperienceReader
KnowledgeService
DecisionLifecycleService
container wiring
neural decision add/list/show
neural decision accept
neural decision acceptance-history
neural decision action add
neural decision action-history
neural decision action-show
neural decision outcome add
neural decision outcome-history
neural decision outcome-show
neural decision outcome-summary
neural decision review add
neural decision review history
neural decision review show
neural experience from-review
neural knowledge add/list/show
neural knowledge from-experience
neural experience knowledge
neural decision state
```

Creating a Decision records a proposal. Creating a DecisionAcceptance explicitly authorizes that
proposal for possible future work. Creating a DecisionAction records work performed under that
acceptance. Creating a DecisionOutcome records factual results and validation evidence for one or
more linked actions. Creating a DecisionReview records authorized interpretation over an explicit
ordered outcome set. None of these operations automatically creates learning.
Only the separate authorized Review-to-Experience promotion use case creates one Experience from
selected copied Review interpretation; that Experience remains distinct from Knowledge.

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

`EvidenceReference` is an implemented immutable value embedded in a Decision,
DecisionAcceptance, DecisionAction, DecisionOutcome, or DecisionReview:

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

## DecisionAcceptance foundation

`DecisionAcceptance` is an immutable domain model with these implemented fields:

```text
id
accepted_at
decision_id
accepted_by
reason
evidence_references
idempotency_key
tags
```

Its implemented invariants are:

1. `decision_id` is a valid UUID.
2. `accepted_by` is trimmed and non-blank.
3. `reason` is trimmed and non-blank.
4. `idempotency_key` is trimmed and non-blank.
5. `accepted_at` is timezone-aware and normalized to UTC.
6. Tags are trimmed, reject blanks, and remove case-insensitive duplicates while preserving
   first-seen order.
7. Evidence references reuse the existing immutable `EvidenceReference`.
8. The model is immutable.
9. No mutable lifecycle status exists.
10. Acceptance does not embed or mutate the Decision payload.

The semantic boundary is exact:

```text
Decision
= proposed choice

DecisionAcceptance
= explicit authorization for possible future execution
```

Acceptance does not mean execution occurred, a DecisionAction exists, a DecisionOutcome exists, a
DecisionReview exists, or learning was created.

## DecisionAction foundation

`DecisionAction` is an immutable domain model with these exact implemented fields:

```text
id
recorded_at
decision_id
acceptance_id
action_type
summary
performed_by
started_at
completed_at
evidence_references
playbook_run_id
idempotency_key
tags
```

Its implemented invariants are:

1. Decision and acceptance IDs are valid UUIDs.
2. `action_type`, `summary`, `performed_by`, and `idempotency_key` are trimmed and non-blank.
3. `action_type` is bounded to 64 characters.
4. `recorded_at`, `started_at`, and optional `completed_at` are timezone-aware and normalized to
   UTC.
5. `completed_at` cannot precede `started_at`.
6. Tags are normalized like Decision tags.
7. Evidence reuses immutable embedded `EvidenceReference`.
8. Optional `playbook_run_id` is a UUID.
9. The model is immutable.
10. No mutable status field exists.
11. Decision and DecisionAcceptance payloads are not embedded or mutated.

The semantic boundary is exact:

```text
DecisionAction
= work was performed under an explicitly accepted Decision
```

It does not mean the work succeeded, validation passed, an intended result occurred,
DecisionOutcome exists, DecisionReview exists, or learning was created. `completed_at` means only
that the described work interval ended. It does not by itself produce a `completed`, `executed`,
or `succeeded` lifecycle state.

## DecisionOutcome foundation

`DecisionOutcome` is an immutable factual result and validation record with these exact
implemented fields:

```text
id
recorded_at
decision_id
acceptance_id
action_ids
result
summary
validated_by
validated_at
evidence_references
metrics
idempotency_key
tags
```

Its implemented invariants are:

1. Decision, acceptance, and action IDs are valid UUIDs.
2. At least one action ID is required; action IDs are ordered and unique.
3. `result` is exactly `succeeded`, `failed`, `partial`, or `unknown`.
4. `summary`, `validated_by`, and `idempotency_key` are trimmed and non-blank.
5. `recorded_at` and `validated_at` are timezone-aware and normalized to UTC.
6. Metrics contain at most 100 scalar `int | float | str | bool` values.
7. Metric keys are trimmed, non-blank, at most 64 characters, and case-insensitively unique.
8. Float metrics are finite, string metrics are bounded to 1000 characters, and nested values are
   rejected.
9. The metric mapping is immutable and serialized in deterministic key order.
10. Tags and evidence use the existing normalization and immutable `EvidenceReference` rules.
11. The model is immutable and has no mutable lifecycle status.

One Decision may have multiple outcomes. Each outcome appends factual history and may link one or
more actions; no outcome replaces or mutates an earlier record. An outcome does not mean review,
Experience, Knowledge, Playbook change, or automatic learning occurred.

## DecisionReview foundation

`DecisionReview` is an immutable, append-only authorized interpretation record with these exact
implemented fields:

```text
id
recorded_at
decision_id
acceptance_id
outcome_ids
reviewed_by
reviewed_at
assessment
summary
findings
candidate_lessons
evidence_references
confidence
idempotency_key
tags
```

Assessment is exactly `sound`, `flawed`, `mixed`, or `inconclusive`; confidence is exactly `low`,
`medium`, or `high`. Assessment is not the outcome result vocabulary: successful factual outcomes
may support a flawed review, and failed outcomes may support a sound review.

`outcome_ids` is ordered, unique, and non-empty. Findings are required ordered text; findings and
candidate lessons each allow at most 100 case-insensitively unique entries of at most 1000
characters. Candidate lessons may be empty and have no promotion authority. Reviewer is bounded to
255 characters and summary to 1000; required text is trimmed and non-blank. Tags preserve
first-seen order while removing case-insensitive duplicates. UTC-aware timestamps are normalized
to UTC, and `reviewed_at` cannot be later than `recorded_at`.

Every outcome must exist and belong to the same Decision and acceptance. Review time cannot
precede the latest `validated_at` among selected outcomes. Action IDs are not persisted: provenance
is transitive through `DecisionReview → DecisionOutcome[] → DecisionAction[]`. Multiple reviews
may cover one Decision, outcome, or ordered outcome set under different keys. Corrections append;
there is no replacement, supersession, deletion, or persisted `current` behavior.

## DecisionReview-to-Experience promotion foundation

At source commit `1b45beb`, `Experience` has optional immutable
`decision_review_promotion: DecisionReviewPromotion | None`. Plain direct and
Observation-derived Experiences retain `None`. Promotion contains exactly one Review ID, ordered
non-empty immutable source statements, promoter, reason, and idempotency key. Each statement stores
exactly `kind`, zero-based non-negative `index`, and exact copied `text`; kind is exactly `finding`
or `candidate_lesson`, and `(kind, index)` pairs are unique.

Promoter and key are bounded to 255 characters; reason and copied text are bounded to 1000. All are
trimmed and non-blank. Reviewer and promoter are separate explicit authorities. Promotion copies no
Decision, acceptance, action, outcome, reviewer, assessment, confidence, or evidence fields into
Experience. One Experience references one Review and one or more selected statements; one Review
and one source statement may produce multiple Experiences under different keys. Corrections append.

The implemented chain is:

```text
Observation
→ Decision
→ DecisionAcceptance
→ DecisionAction
→ DecisionOutcome
→ DecisionReview
→ explicitly promoted Experience
→ separately and explicitly created Knowledge
```

Review save does not promote. Promotion does not create Knowledge or change Decision lifecycle.
`DecisionReview.assessment`, `DecisionOutcome.result`, and `Experience.result` remain distinct.

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

The persistence-focused `DecisionAcceptanceRepository` likewise implements only:

```text
save()
load_all()
get_by_id()
```

It has no relation, project, or idempotency query methods. Relation and eligibility filtering
belong to `DecisionAcceptanceService`. `JsonDecisionAcceptanceRepository` stores one JSON file per
acceptance under `NeuralPaths.DECISION_ACCEPTANCES`, and Brain initialization creates that
directory. `load_all()` sorts file names for deterministic order. UUIDs, UTC-aware timestamps,
embedded evidence, and normalized tags round-trip through domain validation. Malformed stored data
surfaces validation errors. No migration or ingestion behavior exists.

The persistence-focused `DecisionActionRepository` implements only:

```text
save()
load_all()
get_by_id()
```

It has no relation, idempotency, or lifecycle query methods. Filtering and relation validation
remain in application services. `JsonDecisionActionRepository` stores one JSON file per action
under `NeuralPaths.DECISION_ACTIONS`, and Brain initialization creates that directory.
`load_all()` sorts file names for deterministic order. The complete domain record round-trips
through validation, and malformed stored data fails visibly. The adapter performs no migration,
ingestion, or command execution.

The persistence-focused `DecisionOutcomeRepository` also implements only:

```text
save()
load_all()
get_by_id()
```

It has no relation, idempotency, latest-outcome, summary, or lifecycle query methods.
`JsonDecisionOutcomeRepository` stores one deterministic JSON file per outcome under
`NeuralPaths.DECISION_OUTCOMES`, and Brain initialization creates that directory. Complete records
and immutable scalar metrics round-trip through domain validation; malformed data fails visibly.
The adapter performs no relation filtering, lifecycle projection, review, learning, migration, or
ingestion.

The persistence-focused `DecisionReviewRepository` implements only:

```text
save()
load_all()
get_by_id()
```

It has no relation, idempotency, chronology, or lifecycle query methods.
`JsonDecisionReviewRepository` stores one deterministic sorted-key JSON file per review under
`NeuralPaths.DECISION_REVIEWS`, and Brain initialization creates that directory. `load_all()` sorts
filenames and every record round-trips through domain validation. Filtering, relation validation,
history ordering, ambiguity detection, and semantic comparison remain in the application service.

The existing `ExperienceRepository` also remains limited to:

```text
save()
load_all()
get_by_id()
```

`JsonExperienceRepository` continues to store one JSON file per Experience under
`NeuralPaths.EXPERIENCES` and round-trips the optional embedded promotion through domain
validation. Old JSON without the field loads with `None`. No migration, new path, Brain directory,
link record, promotion repository, second write, or production adapter rewrite was introduced.
Idempotency and Review integrity remain application policy.

The existing `KnowledgeRepository` remains limited to:

```text
save()
load_all()
get_by_id()
```

No Knowledge relation or provenance query was added. `JsonKnowledgeRepository` and the Knowledge
JSON schema are unchanged. Knowledge membership filtering and relation validation remain
application policy.

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

### DecisionAcceptanceService

`DecisionAcceptanceService` implements:

```text
accept()
list_for_decision()
show()
```

`accept()` validates that the referenced Decision exists, constructs an immutable candidate, loads
all acceptance records, handles an equivalent idempotent replay, rejects conflicting key reuse,
rejects a second distinct acceptance, and persists only after validation. It does not mutate the
Decision and creates no action, outcome, review, or learning record.

The initial monotonic eligibility rule is:

```text
Decision exists
and no DecisionAcceptance exists
→ eligible for first acceptance
```

Only one acceptance per Decision is allowed. A superseding Decision does not invalidate an
existing acceptance. There is no rejection, withdrawal, reversal, reopening, cancellation, or
replacement behavior.

The implemented idempotency scope is:

```text
(decision_id, "decision_acceptance", idempotency_key)
```

```text
same scoped key + equivalent semantic payload
→ return existing DecisionAcceptance

same scoped key + different semantic payload
→ visible idempotency conflict, no write

different key + Decision already accepted
→ visible already-accepted conflict, no write
```

Semantic equivalence excludes:

```text
DecisionAcceptance.id
DecisionAcceptance.accepted_at
EvidenceReference.captured_at
```

`list_for_decision()` validates Decision existence, loads all acceptance records, filters in the
application layer, and preserves repository order without adding a repository query. `show()`
raises an explicit acceptance not-found error.

### DecisionActionService

`DecisionActionService` implements:

```text
add()
list_for_decision()
show()
```

`add()` validates Decision existence, acceptance existence, and that the acceptance belongs to the
same Decision. It validates an optional PlaybookRun exists, constructs an immutable candidate,
performs idempotency detection, returns an equivalent replay, rejects conflicting key reuse,
allows multiple distinct actions, and persists only after every validation. It mutates neither
Decision nor DecisionAcceptance and creates no Outcome, Review, Experience, Knowledge, Playbook,
or EvolutionProposal.

The current PlaybookRun limitation is explicit:

```text
PlaybookRun and Playbook currently expose no project_key,
so only existence can be validated without a separately reviewed schema change.
```

Action idempotency is scoped by:

```text
(decision_id, "decision_action", idempotency_key)
```

```text
same scoped key + equivalent semantic payload
→ return existing DecisionAction

same scoped key + different semantic payload
→ visible conflict, no write

different key
→ another action may be recorded
```

Semantic equivalence excludes:

```text
DecisionAction.id
DecisionAction.recorded_at
EvidenceReference.captured_at
```

`list_for_decision()` validates the Decision, filters `load_all()` in the application layer, and
preserves repository order. `show()` raises an explicit action-not-found error.

### DecisionOutcomeService

`DecisionOutcomeService` implements:

```text
add()
list_for_decision()
show()
summary_for_decision()
```

`add()` validates Decision existence, acceptance existence and ownership, at least one unique
action, and every action's Decision and acceptance relations. `validated_at` cannot precede the
earliest linked action start. Only after relation validation does the service construct and save
the immutable outcome. It mutates no related record and creates no Review or learning artifact.

Outcome idempotency is scoped by:

```text
(decision_id, "decision_outcome", idempotency_key)
```

```text
same scoped key + equivalent semantic payload
→ return existing DecisionOutcome

same scoped key + different semantic payload
→ visible conflict, no write

more than one persisted scoped match
→ `DecisionOutcomeIdempotencyAmbiguityError`, no arbitrary selection, no write

different key
→ another outcome may be recorded
```

Semantic equivalence excludes `DecisionOutcome.id`, `DecisionOutcome.recorded_at`, and embedded
`EvidenceReference.captured_at`. It includes the linked relations, result, validation data,
metrics, and other caller-supplied semantic fields.

`list_for_decision()` validates the Decision, filters `load_all()` in the application layer, and
preserves repository order so the complete multiple-outcome history remains visible. `show()`
raises an explicit outcome-not-found error.

`DecisionOutcomeSummary` is an immutable, non-persisted application read model returned by
`summary_for_decision()`. It reports outcome count, latest result and validation time, distinct
linked-action count, counts for each result value, and success/failure presence. Summary derivation
validates every persisted outcome-to-acceptance/action relation. Latest selection is deterministic
by `(validated_at, outcome.id)` and never depends on repository order. The summary is derived on
demand and is neither persisted nor cached.

More than one matching persisted outcome always raises ambiguity before selecting or semantically
comparing a record. This is independent of repository enumeration order and applies to equivalent
and different duplicate payloads. Zero matches follows normal creation; exactly one match retains
the equivalent-replay or conflict behavior. This hardening changes no outcome fields, vocabulary,
relations, ordering, summary, CLI, stored schema, or lifecycle behavior.

### DecisionReviewService

`DecisionReviewService` implements:

```text
add()
list_for_decision()
show()
```

`add()` constructs the candidate first, so local domain validation precedes repository reads. It
then requires the Decision, validates the acceptance belongs to it, loads every caller-ordered
outcome by ID, validates Decision and acceptance ownership, and requires `reviewed_at` to be at or
after the latest selected outcome validation. Missing or mismatched relations and invalid time all
fail before persistence.

Review idempotency is scoped by:

```text
(decision_id, "decision_review", idempotency_key)
```

```text
zero scoped matches
→ save the validated candidate

exactly one equivalent match
→ validate persisted relations and return existing DecisionReview

exactly one different match
→ `DecisionReviewIdempotencyConflictError`, no write

more than one persisted scoped match
→ `DecisionReviewIdempotencyAmbiguityError`, no arbitrary selection or comparison, no write
```

The ambiguity error carries Decision ID, idempotency key, and match count. Ambiguity is independent
of repository order and applies to semantically equivalent or different duplicates. For exactly
one match, semantic equivalence excludes generated review ID and recording time and embedded
evidence capture times; it includes every caller-supplied semantic field. Ordered outcome IDs,
findings, candidate lessons, evidence, and tags therefore remain order sensitive.

`list_for_decision()` requires the Decision, validates every persisted relation, and sorts by
`(reviewed_at, review.id)`. `show()` loads by ID and validates its relations. Controlled errors
cover missing Decision, acceptance, outcome, or review; acceptance/Decision mismatch;
outcome/Decision or outcome/acceptance mismatch; review before outcome; idempotency conflict; and
duplicate-key ambiguity. No failing path writes.

DecisionReview and DecisionOutcome share the reusable fail-closed invariant that multiple matches
for a scoped idempotency key must be surfaced, never resolved through `next()`, first-match
selection, repository order, or comparison with an arbitrarily chosen record. Their scopes and
ambiguity error types remain separate.

### ExperienceService Review promotion

`ExperienceService.add_from_decision_review(...)` validates selectors and bounded authority
metadata before calling `DecisionReviewService.show()`. It then copies caller-ordered exact Review
items, validates optional Observations, constructs one promoted Experience, loads all Experiences,
and applies this scope:

```text
(decision_review_id, "review_experience_promotion", idempotency_key)
```

```text
zero matches
→ save and return one promoted Experience

exactly one equivalent match
→ validate its provenance and return original ID/timestamp, no write

exactly one different match
→ `DecisionReviewPromotionIdempotencyConflictError`, no write

more than one match
→ `DecisionReviewPromotionIdempotencyAmbiguityError`, no selection or comparison, no write
```

Equivalence excludes only generated `Experience.id` and `Experience.timestamp`; every ordinary
Experience field, optional Observation ID, tag, and ordered promotion value remains semantic.
Ambiguity is repository-order independent.

Replay, `get_by_id()`, complete list, and Observation-linked list revalidate the referenced Review
graph, selector bounds, and exact copied text. Missing or malformed provenance fails closed without
repair or skipping; plain records bypass promotion validation. The use case owns no Knowledge,
Playbook, evolution, lifecycle, evidence, or Consigliere behavior.

### KnowledgeService validated Experience boundary

The existing generic `KnowledgeService` implements:

```text
add()
add_from_experience()
list_knowledge()
list_for_experience()
get_by_id()
```

It depends on `KnowledgeRepository` and the application-facing `ExperienceReader.get_by_id()`
protocol defined beside the service. `ExperienceService` implements the protocol, so
`ExperienceService.get_by_id()` remains the single owner of persisted Review graph, promotion
selector, and copied-text validation. KnowledgeService no longer reads `ExperienceRepository`
directly, loads DecisionReview, or duplicates another service's validation. ExperienceService has
no KnowledgeService dependency, so the graph is acyclic.

`add()` rejects empty evidence before relation reads, validates supplied Experience IDs in caller
order, preserves duplicates, and saves only after every validation succeeds.
`add_from_experience()` validates its source through the same reader and performs no save when it
is missing or corrupt.

`list_knowledge()` validates every Experience relation of every loaded record in repository and
relation order and fails closed without partial results. `get_by_id()` performs no Experience read
when Knowledge is absent and validates every relation of a present record.
`list_for_experience()` validates the requested Experience first, filters Knowledge in repository
order, validates every relation of every matching record, and deliberately leaves unrelated
Knowledge records outside this scoped validation.

Missing relations continue to raise `ExperienceNotFoundError`. Existing `DecisionReviewError` and
`DecisionReviewPromotionError` instances propagate unchanged. The five affected CLI surfaces
render those failures as controlled nonzero errors without tracebacks. Validation is exactly the
existing ExperienceService read contract; it does not recursively revalidate every Observation or
DecisionAction ancestry relation.

This hardening changes no Knowledge or Experience schema, authority, cardinality, duplicate-ID
behavior, Knowledge idempotency, repository, adapter, JSON format, command, or automatic behavior.
It performs one validated Experience read per stored relation, including duplicates. The linear
read amplification is accepted in favor of fail-closed integrity; no caching, batching, or
deduplication was added.

### Canonical DecisionLifecycleService

`DecisionLifecycleService` is the only canonical owner of the current lifecycle projection. It
depends on:

```text
DecisionRepository
DecisionAcceptanceRepository
DecisionActionRepository
DecisionOutcomeRepository
```

It derives exactly:

```text
Decision exists, no acceptance
→ proposed

Decision exists, one valid acceptance, no action
→ accepted

Decision exists, one valid acceptance, at least one valid action
→ in_progress

latest valid outcome has result succeeded
→ succeeded

latest valid outcome has result failed
→ failed

latest valid outcome has result partial
→ partial

latest valid outcome has result unknown
→ outcome_unknown
```

No mutable status is written and no generic event stream exists. The latest outcome is selected by
`(validated_at, outcome.id)`, never repository order. Multiple persisted acceptances fail visibly,
as do invalid action or outcome relations. Multiple valid actions with no outcome derive
`in_progress`; multiple outcomes retain history while the latest valid one drives the projection.
There is no generic `executed`, `completed`, `resolved`, or `reviewed` state.

## Container

The composition root constructs and connects:

```text
JsonDecisionRepository
JsonObservationRepository
DecisionService
JsonDecisionAcceptanceRepository
DecisionAcceptanceService
JsonDecisionActionRepository
JsonPlaybookRunRepository
DecisionActionService
JsonDecisionOutcomeRepository
DecisionOutcomeService
JsonDecisionReviewRepository
DecisionReviewService
JsonExperienceRepository
ExperienceService
JsonKnowledgeRepository
KnowledgeService
DecisionLifecycleService
```

`DecisionAcceptanceService` receives `JsonDecisionAcceptanceRepository` and
`JsonDecisionRepository`. The CLI resolves services from the container. It does not construct
repositories or own validation, relation checks, persistence, eligibility, or idempotency policy.

`DecisionActionService` receives `JsonDecisionActionRepository`, `JsonDecisionRepository`,
`JsonDecisionAcceptanceRepository`, and `JsonPlaybookRunRepository`. `DecisionOutcomeService`
receives `JsonDecisionOutcomeRepository` plus Decision, acceptance, and action repositories.
`DecisionLifecycleService` receives the Decision, acceptance, action, and outcome repositories.
`DecisionReviewService` receives `JsonDecisionReviewRepository` plus Decision, acceptance, and
outcome repositories. `Container.decision_review_repository()` and
`Container.decision_review_service()` expose the review composition. CLI handlers resolve services
from the container and construct no repositories.
`Container.experience_service()` injects `JsonExperienceRepository`,
`JsonObservationRepository`, and that validated `DecisionReviewService` boundary into
`ExperienceService`; the container owns no promotion policy.
`Container.knowledge_service()` injects `JsonKnowledgeRepository` and the constructed
`ExperienceService` as `ExperienceReader`; it does not supply a raw `JsonExperienceRepository` to
KnowledgeService.

## Implemented CLI

These commands exist at commit `1b45beb`:

```text
neural decision add
neural decision list
neural decision show DECISION_UUID
neural decision accept DECISION_UUID
neural decision acceptance-history DECISION_UUID
neural decision action add DECISION_UUID
neural decision action-history DECISION_UUID
neural decision action-show ACTION_UUID
neural decision outcome add DECISION_UUID
neural decision outcome-history DECISION_UUID
neural decision outcome-show OUTCOME_UUID
neural decision outcome-summary DECISION_UUID
neural decision review add DECISION_UUID
neural decision review history DECISION_UUID
neural decision review show REVIEW_UUID
neural experience add
neural experience from-observation OBSERVATION_UUID
neural experience from-review REVIEW_UUID
neural experience list
neural experience show EXPERIENCE_UUID
neural experience knowledge EXPERIENCE_UUID
neural knowledge add
neural knowledge from-experience EXPERIENCE_UUID
neural knowledge list
neural knowledge show KNOWLEDGE_UUID
neural observation experiences OBSERVATION_UUID
neural decision state DECISION_UUID
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

### Decision acceptance commands

`neural decision accept DECISION_UUID` requires:

```text
DECISION_UUID
--accepted-by
--reason
--idempotency-key
```

It accepts repeatable optional values:

```text
--evidence
--tag
```

For example:

```bash
neural decision accept DECISION_UUID \
  --accepted-by architecture-owner \
  --reason "Approved after architecture review" \
  --idempotency-key decision-acceptance-1 \
  --evidence '{"kind":"manual_decision","locator":"approval:architecture-review"}' \
  --tag architecture
```

The CLI parses and validates `EvidenceReference`, but does not read the locator or ingest locator
content. Business rules remain in `DecisionAcceptanceService`. Success prints the stored
acceptance ID.

`neural decision acceptance-history DECISION_UUID` validates the Decision through the service and
renders:

```text
ID
Accepted
Decision ID
Accepted by
Reason
```

An existing Decision with no acceptance produces a controlled empty state.

### Decision action commands

`neural decision action add DECISION_UUID` requires:

```text
--acceptance-id
--action-type
--summary
--performed-by
--started-at
--idempotency-key
```

It accepts these optional values; evidence and tags are repeatable:

```text
--completed-at
--playbook-run-id
--evidence
--tag
```

The CLI parses timestamps as ISO-8601 values and parses evidence as embedded
`EvidenceReference` values. It does not execute commands or open evidence locators. Business rules
remain in `DecisionActionService`, and success prints the stored action ID.

`neural decision action-history DECISION_UUID` renders:

```text
ID
Recorded
Action type
Performed by
Started
Completed
Summary
```

An existing Decision with no actions produces a controlled empty state.
`neural decision action-show ACTION_UUID` renders every DecisionAction field.

### Decision outcome and state commands

`neural decision outcome add DECISION_UUID` requires:

```text
--acceptance-id
--action-id (one or more)
--result
--summary
--validated-by
--validated-at
--idempotency-key
```

Repeated `--evidence`, `--metric KEY=VALUE`, and `--tag` values are optional. Result accepts only
`succeeded`, `failed`, `partial`, or `unknown`. Metrics parse unambiguous booleans, integers, and
finite floats; other values remain strings and domain validation enforces the scalar bounds. The
CLI reads no evidence locator and executes no referenced command.

`neural decision outcome-history DECISION_UUID` renders all matching outcomes in repository order,
including their result, validation time, linked action IDs, validator, and summary. An existing
Decision with no outcomes produces a controlled empty state. `outcome-show OUTCOME_UUID` renders
every stored field, including evidence, metrics, idempotency key, and tags.

`neural decision outcome-summary DECISION_UUID` renders the derived count, deterministic latest
result/time, distinct linked-action count, counts by result, and success/failure presence. It does
not persist the summary.

### Decision review commands

`neural decision review add DECISION_UUID` requires:

```text
--acceptance-id
--outcome-id (one or more, repeatable and ordered)
--reviewed-by
--reviewed-at
--assessment
--summary
--finding (one or more, repeatable and ordered)
--confidence
--idempotency-key
```

Optional repeatable inputs are `--candidate-lesson`, `--evidence` JSON, and `--tag`. Assessment
accepts `sound`, `flawed`, `mixed`, or `inconclusive`; confidence accepts `low`, `medium`, or
`high`. The CLI parses ISO-8601 review time and embedded evidence but never opens evidence
locators. Validation errors render their first message; `ValueError` and controlled
`DecisionReviewError` failures render visibly and exit nonzero. Success prints the stored review ID
and every review field.

`neural decision review history DECISION_UUID` renders deterministic service history with columns
`ID`, `Reviewed`, `Reviewed by`, `Assessment`, `Confidence`, `Outcome IDs`, and `Summary`. An
existing Decision with no reviews renders `No review history found for Decision: ...`.
`neural decision review show REVIEW_UUID` renders every field after persisted relation validation.

### Review-to-Experience promotion command

`neural experience from-review REVIEW_UUID` requires repeatable ordered `--source`, plus:

```text
--promoted-by
--promotion-reason
--idempotency-key
--title
--context
--action
--outcome
--result
```

Optional repeatable inputs are `--observation-id` and `--tag`. Selectors use exact syntax such as
`--source finding:1 --source candidate_lesson:2`. CLI ordinals are positive and one-based; they
become durable zero-based indexes `0` and `1` without caller-supplied text. Invalid selector syntax,
kind, ordinal, Review, source index, Observation, conflict, ambiguity, or read integrity renders a
controlled error.

Success and equivalent replay print the stored Experience ID and complete auditable Experience
details. Promotion source rendering shows kind, user ordinal, stored index, and copied text, plus
promoter, reason, and key. Reviewer and promoter remain separate authorities.

Ordinary Experience commands keep their existing contracts. Direct `add` requires title, context,
action, outcome, and result; `from-observation` derives context from the required Observation and
requires title, action, outcome, and result. Observation IDs and tags remain optional where already
supported. List, show, Experience-to-Knowledge navigation, and Observation-to-Experience navigation
remain read-only. Ordinary Experience creation requires no promotion metadata or idempotency key.

### Knowledge commands and controlled integrity failures

`neural knowledge add` and `neural knowledge from-experience EXPERIENCE_UUID` are the existing
explicit creation paths. They accept caller-supplied Knowledge content and do not infer, promote,
or automatically create it. `neural experience knowledge EXPERIENCE_UUID` is read-only navigation.

All five Knowledge-to-Experience surfaces are protected by the validated reader:

```text
neural knowledge add
neural knowledge from-experience EXPERIENCE_UUID
neural knowledge list
neural knowledge show KNOWLEDGE_UUID
neural experience knowledge EXPERIENCE_UUID
```

Missing Experience and canonical DecisionReview/promotion-integrity errors render controlled
messages and exit nonzero without a traceback. No Knowledge-specific promotion error taxonomy,
new command, or success-output change exists.

`neural decision state DECISION_UUID` renders exactly one of:

```text
proposed
accepted
in_progress
succeeded
failed
partial
outcome_unknown
```

## Review and learning boundary

The record family remains deliberately separate:

```text
Decision
→ DecisionAcceptance
→ DecisionAction
→ DecisionOutcome
→ DecisionReview
```

- `Decision` is the implemented proposed choice.
- `DecisionAcceptance` is the implemented explicit authorization for possible future execution.
- `DecisionAction` is the implemented record of work performed under an accepted Decision.
- `DecisionOutcome` is the implemented factual result and validation evidence record.
- `DecisionReview` is the implemented authorized interpretation over explicit ordered outcomes.

All five decision records and the explicit Review-to-Experience promotion use case exist. Records
remain immutable semantic records rather than fields on a mutable
Decision or a duplicate generic event stream. A proposed option is not an acceptance, acceptance
is not execution, an outcome is not a review or Experience, and review findings or candidate
lessons are not Experience until promotion succeeds and are never automatically Knowledge or a
Playbook change.

Explicit Knowledge capture is a later, separate act through the existing generic Knowledge
commands. Its durable transitive provenance is:

```text
Knowledge.experience_ids
→ Experience.decision_review_promotion
→ DecisionReview
```

The Review provenance is not copied into Knowledge. `neural experience knowledge` only navigates
this relation; it does not create or promote Knowledge. Storing Knowledge proves explicit durable
capture, not that the Knowledge was used in, or improved, a later Decision.

The currently derivable projection is only:

```text
Decision without acceptance
→ proposed

Decision with one valid acceptance
→ accepted

Decision with one valid acceptance and at least one valid action
→ in_progress

latest valid outcome succeeded
→ succeeded

latest valid outcome failed
→ failed

latest valid outcome partial
→ partial

latest valid outcome unknown
→ outcome_unknown
```

The lifecycle projection uses the latest valid outcome selected by `(validated_at, outcome.id)`.
There is no generic executed, completed, resolved, or reviewed state and no generic full lifecycle
event replay service.

## Relationship to the domain chain

The implemented Decision may reference existing Observations as context. The implemented path and
future learning bridge remain explicit:

```text
Observation
→ Decision
→ DecisionAcceptance
→ DecisionAction
→ DecisionOutcome
→ DecisionReview
→ explicitly promoted Experience
→ separately and explicitly created Knowledge
```

DecisionAction may optionally reference an existing PlaybookRun, with existence-only validation
because PlaybookRun and Playbook expose no project key. `DecisionOutcome` remains distinct from
Experience. The promotion use case copies selected Review text into optional immutable Experience
provenance and never mutates a Playbook. Any connection from an action to
PlaybookEvaluation, EvolutionProposal, or the revision lifecycle requires a separate reviewed use
case.

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

Commit `1b45beb` does not capture or ingest those events automatically. Automatic candidates and
manual confirmation remain future concepts; no automatic persistence, ingestion, or learning
exists.

Consigliere also remains future-only. It may later advise. No Consigliere integration exists, and
no recommendation can directly mutate NeuralEngine or authorize a durable record.

## Current non-behavior

Commit `1b45beb` does not implement:

```text
execution engine
command/shell execution
rejection
withdrawal
reversal
reopening
cancellation
replacement
executed/completed/resolved/reviewed states
file ingestion
git ingestion
automatic Observation creation
automatic Experience creation
automatic Knowledge creation
special DecisionReview-to-Knowledge promotion
durable Knowledge use in a later Decision
Knowledge effectiveness feedback
automatic Playbook creation or mutation
automatic evolution
Consigliere integration
```

It also does not execute commands referenced by evidence, open locators, automatically accept
Decisions, materialize Playbook revisions, or infer outcomes from `completed_at`. Explicit user
requests are required to create Decision, DecisionAcceptance, DecisionAction, DecisionOutcome, or
DecisionReview records and to promote Review statements into Experience.

## Remaining learning-loop gap

The remaining controlled learning-loop gap is:

```text
durable operational Knowledge use and feedback
```

Explicit generic Knowledge creation is already implemented. The future slice must distinguish
retrieval from durable use, record evidence rather than infer improvement from storage, preserve
explicit authority, and remain separate from automatic Knowledge, Playbook, PlaybookEvaluation,
EvolutionProposal, lifecycle, or Consigliere behavior.

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
| Validated cross-service relation read | Narrow application-facing reader protocol | Raw repository bypass or duplicated provenance validation |
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

The implemented Decision, DecisionAcceptance, DecisionAction, DecisionOutcome, and DecisionReview
foundations record a bounded proposed choice, explicit authorization, work performed, factual
results, and authorized interpretation after Observation context:

```text
Observation
→ Decision
→ DecisionAcceptance
→ DecisionAction
→ DecisionOutcome
→ DecisionReview
→ explicitly promoted Experience
→ separately and explicitly created Knowledge
```

This is a complementary provenance path, not a replacement for the canonical domain chain.
DecisionOutcome is factual; DecisionReview is authorized interpretation; Experience captures
explicitly promoted operational learning; Knowledge is separately generalized; Playbook remains a
separately created repeatable procedure. A Decision may have multiple immutable outcomes and
reviews, and one Review may explicitly produce multiple Experiences under different promotion
keys. A promoted Experience selects ordered Review statements and cannot combine Reviews. Review
action provenance remains transitive through explicit outcomes; promoted Experience provenance
remains transitive through its one Review. These records exist at source commit `12097fe`; no
Review save, promotion, lifecycle transition, or later Knowledge record in this path is automatic.

At source commit `1b45beb`, explicit Knowledge capture keeps its existing durable relation:

```text
Knowledge.experience_ids
→ Experience.decision_review_promotion
→ DecisionReview
```

KnowledgeService traverses every returned or newly supplied Experience relation through the
validated `ExperienceService.get_by_id()` boundary. This preserves transitive Review provenance
without copying it into Knowledge. `neural knowledge add` and `neural knowledge from-experience`
create explicit Knowledge; `neural experience knowledge` only navigates the relation. Durable
capture is not a durable record that Knowledge informed or improved a later decision.

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

An Experience represents explicitly recorded operational learning. It may be created directly,
derived from one Observation, or explicitly promoted from selected DecisionReview statements.

## Owns

- interpreted outcome,
- contextual meaning,
- provenance back to observations,
- optional immutable DecisionReview promotion provenance,
- identity.

## Must not own

- generalized reusable knowledge,
- execution instructions,
- evaluation policy.

## Invariants

- Provenance is preserved.
- Interpretation is explicit.
- Creation does not erase source observations.
- Plain and Observation-derived Experiences have `decision_review_promotion is None`.
- A promoted Experience contains one optional `DecisionReviewPromotion`; it remains Experience,
  not generalized Knowledge.

## Typical transitions

`Experience` → `Knowledge`

The application layer coordinates this separate explicit transformation. Experience creation does
not create Knowledge automatically.

Knowledge creation and reads consume Experience through the narrow application-facing
`ExperienceReader` implemented by `ExperienceService.get_by_id()`. For promoted Experiences this
reuses the existing Review graph, selector-index, and copied-source-text validation before the
Experience can support returned or newly created Knowledge. It does not add recursive Observation
validation to ordinary Experience reads.

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
- At least one Experience ID is required by `KnowledgeService.add()`.
- Every supplied or returned Experience relation is validated through the narrow
  application-facing `ExperienceReader` implemented by `ExperienceService.get_by_id()`.
- Provenance remains transitively available through `Knowledge.experience_ids`; Review provenance
  is not copied into Knowledge.
- Domain and relation validation precede persistence.

## Typical transitions

`Knowledge` → `Playbook`

## Explicit capture and navigation

Knowledge creation remains available through:

```text
neural knowledge add
neural knowledge from-experience EXPERIENCE_UUID
```

Both commands store caller-supplied statement, rationale, confidence, Experience IDs, and tags.
They do not infer or automatically promote Knowledge. `neural experience knowledge
EXPERIENCE_UUID` is read-only navigation through `KnowledgeService.list_for_experience()` and does
not create Knowledge.

## Validated Experience boundary

`KnowledgeService` depends on `KnowledgeRepository` and the `ExperienceReader.get_by_id()`
protocol, not on `ExperienceRepository`. The container injects `ExperienceService`, whose
`get_by_id()` remains the canonical validation owner for promoted Experience ancestry.
The dependency is acyclic: ExperienceService has no KnowledgeService dependency.

Creation behavior is exact:

- `add()` rejects empty evidence before any Experience read, validates IDs in caller order,
  preserves order and duplicates, and saves only after all reads succeed;
- `add_from_experience()` validates its one source through the same reader and performs no save
  when that source is missing or corrupt.

Read behavior is exact:

- `list_knowledge()` validates every Experience relation of every record in repository and
  relation order and fails closed without partial results;
- `get_by_id()` performs no Experience read when Knowledge is absent and validates every relation
  when it is present;
- `list_for_experience()` validates the requested Experience first, preserves repository-order
  membership filtering, validates every relation of every matching Knowledge record, and does not
  validate unrelated Knowledge records.

Missing relations continue to raise `ExperienceNotFoundError`. Existing canonical
`DecisionReviewError` and `DecisionReviewPromotionError` instances propagate unchanged for missing
or malformed Review ancestry, invalid promotion selectors/indexes, or copied text that no longer
matches the Review. The guarantee is limited to validation already owned by
`ExperienceService.get_by_id()`; it does not recursively validate every possible Observation or
DecisionAction relation.

## Compatibility and learning boundary

The hardening adds no Knowledge field, Review provenance copy, authority marker, idempotency
behavior, repository method, adapter format, command, or automatic creation. Knowledge may still
reference one or more Experiences, mix ordinary and promoted sources, combine different Reviews,
and retain duplicate Experience IDs. Knowledge creation itself remains non-idempotent.

Durable provenance is:

```text
Knowledge.experience_ids
→ Experience.decision_review_promotion
→ DecisionReview
```

Storing Knowledge proves explicit durable capture only. It does not prove the Knowledge was used
in, or improved, a later decision. Durable operational use and feedback remain a separate future
gap.

Read validation performs one validated Experience read per stored relation, including duplicates.
The resulting linear read amplification is an intentional fail-closed trade-off; this milestone
adds no cache, batch reader, or deduplication.

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

# DecisionOutcome

## Responsibility

A DecisionOutcome is an immutable factual result and validation record for one or more actions
performed under one accepted Decision. It records what happened; it does not interpret lessons or
create learning.

## Implemented fields

- `id`
- `recorded_at`
- `decision_id`
- `acceptance_id`
- ordered unique `action_ids`
- `result`
- `summary`
- `validated_by`
- `validated_at`
- embedded `evidence_references`
- immutable scalar `metrics`
- `idempotency_key`
- normalized `tags`

The result values are exactly `succeeded`, `failed`, `partial`, and `unknown`. A Decision can have
multiple outcomes; new factual results append history instead of replacing an earlier outcome.

## Invariants and relations

- The Decision and DecisionAcceptance must exist, and the acceptance must belong to the Decision.
- At least one action is required. Action IDs are ordered and unique.
- Every action must exist and belong to the same Decision and acceptance.
- `validated_at` cannot precede the earliest linked action start.
- Required text is trimmed and non-blank; timestamps are timezone-aware and normalized to UTC.
- The record and exposed metrics mapping are immutable.

Metrics contain at most 100 `str -> int | float | str | bool` entries. Keys are trimmed,
non-blank, at most 64 characters, and case-insensitively unique. Floats must be finite, strings are
bounded to 1000 characters, and nested values are rejected. JSON serialization sorts metric keys.

## History, idempotency, and summary

Idempotency is scoped by `(decision_id, "decision_outcome", idempotency_key)`. Equivalent replay
returns the existing outcome. Reusing the same scoped key with a different semantic payload fails
without a write. If more than one persisted outcome matches the scoped key,
`DecisionOutcomeIdempotencyAmbiguityError` is raised whether their payloads are equivalent or
different. The service never chooses an arbitrary duplicate, the result is independent of
repository enumeration order, and no write occurs. Generated outcome ID, recording time, and
evidence capture times are excluded from the exactly-one-match semantic comparison; a different
key may append another outcome for the same Decision.

`DecisionOutcomeSummary` is an immutable, non-persisted read model derived on demand. It reports
outcome count, latest result and validation time, distinct linked-action count, counts for every
result value, and success/failure presence. Summary derivation validates stored acceptance/action
relations. Latest selection is deterministic by `(validated_at, outcome.id)`, never repository
order.

## Lifecycle and learning boundary

`DecisionLifecycleService` maps the latest valid outcome to `succeeded`, `failed`, `partial`, or
`outcome_unknown`. Earlier outcomes remain available as history. No `completed` or `resolved`
lifecycle state exists.

Recording an outcome does not review a Decision and does not create Observation, Experience,
Knowledge, Playbook, PlaybookEvaluation, EvolutionProposal, or automatic learning. The separately
implemented DecisionReview foundation interprets explicit outcomes without rewriting them or
changing lifecycle state.

---

# DecisionReview

## Responsibility

A DecisionReview is an immutable, append-only authorized interpretation record over one Decision,
one DecisionAcceptance, and an explicit ordered set of DecisionOutcome records. It owns assessment,
findings, candidate lessons, review evidence, and reviewer confidence. It does not own factual
execution results, rewrite outcomes, execute evidence, mutate lifecycle state, create learning
records, or call Consigliere.

## Implemented fields and vocabularies

- `id`
- `recorded_at`
- `decision_id`
- `acceptance_id`
- ordered unique `outcome_ids`
- `reviewed_by`
- `reviewed_at`
- `assessment`
- `summary`
- ordered `findings`
- ordered `candidate_lessons`
- embedded `evidence_references`
- `confidence`
- `idempotency_key`
- normalized `tags`

Assessment is exactly `sound`, `flawed`, `mixed`, or `inconclusive`. Confidence is exactly `low`,
`medium`, or `high`. These are independent of `DecisionOutcomeResult`, whose values remain
`succeeded`, `failed`, `partial`, and `unknown`: a successful outcome can support a flawed review,
and a failed outcome can support a sound review.

## Validation and provenance

- `outcome_ids` is ordered, unique, and non-empty; every outcome must exist and belong to the same
  Decision and acceptance.
- Action IDs are not persisted on a review. Provenance is transitive through
  `DecisionReview → DecisionOutcome[] → DecisionAction[]`.
- `reviewed_by` is trimmed, non-blank, and at most 255 characters; `summary` is trimmed, non-blank,
  and at most 1000 characters. The idempotency key is trimmed and non-blank.
- Findings are required, ordered, trimmed, non-blank, case-insensitively unique, and limited to 100
  entries of at most 1000 characters each.
- Candidate lessons use the same ordering, normalization, uniqueness, count, and length bounds, but
  may be empty. They are not Experience or Knowledge until a separate authorized use case succeeds.
- Tags are trimmed and case-insensitively deduplicated while first-seen order is preserved.
- `recorded_at` and `reviewed_at` must be timezone-aware and are normalized to UTC. Locally,
  `reviewed_at` cannot be later than `recorded_at`; the service also requires it not to precede the
  latest `validated_at` among the explicitly selected outcomes.
- The candidate's local validation occurs before repository reads. Decision, acceptance, outcome,
  cross-record, and time validation all fail closed before a write.

Repository enumeration order never defines review scope or chronology. The caller supplies the
ordered outcome scope, and history is sorted deterministically by `(reviewed_at, review.id)`.

## History, corrections, and idempotency

Multiple reviews are allowed for a Decision, an outcome, or the same ordered outcome set when they
use different idempotency keys. Reassessment and correction append another review. This foundation
has no mutation, replacement, supersession, deletion, or persisted `current` behavior.

Idempotency is scoped by `(decision_id, "decision_review", idempotency_key)`:

- zero matches creates the validated candidate;
- exactly one semantically equivalent match returns the existing review;
- exactly one different match raises `DecisionReviewIdempotencyConflictError` without a write;
- more than one match raises `DecisionReviewIdempotencyAmbiguityError` with the Decision ID, key,
  and match count, without selecting or comparing an arbitrary duplicate and without a write.

Ambiguity is independent of repository enumeration order and applies whether duplicates are
semantically equivalent or different. For the exactly-one-match comparison, semantic payload
excludes generated `id`, generated `recorded_at`, and each evidence reference's `captured_at`; it
includes all caller-supplied fields and preserves the order sensitivity of `outcome_ids`, findings,
candidate lessons, evidence references, and tags.

## Persistence, service, and CLI

`DecisionReviewRepository` exposes exactly `save()`, `load_all()`, and `get_by_id()`.
`JsonDecisionReviewRepository` stores one deterministic, sorted-key JSON file per review under
`NeuralPaths.DECISION_REVIEWS`; `load_all()` sorts filenames and reconstructs records through domain
validation. Brain initialization creates the directory. `Container.decision_review_repository()`
and `Container.decision_review_service()` wire the JSON review repository together with Decision,
acceptance, and outcome repositories.

`DecisionReviewService` implements `add()`, `list_for_decision()`, and `show()`. Its controlled
errors cover missing Decision, acceptance, outcome, or review; acceptance/Decision mismatch;
outcome/Decision or outcome/acceptance mismatch; review before the latest outcome; idempotency
conflict; and duplicate-key ambiguity. Read operations validate persisted relations before
returning records.

The CLI group is `neural decision review` with exact commands `add DECISION_UUID`,
`history DECISION_UUID`, and `show REVIEW_UUID`. Add requires `--acceptance-id`, repeatable
`--outcome-id`, `--reviewed-by`, `--reviewed-at`, `--assessment`, `--summary`, repeatable
`--finding`, `--confidence`, and `--idempotency-key`. Optional repeatable inputs are
`--candidate-lesson`, `--evidence` JSON, and `--tag`. Success prints the stored ID and every field.
History renders `ID`, `Reviewed`, `Reviewed by`, `Assessment`, `Confidence`, `Outcome IDs`, and
`Summary`; its controlled empty message is `No review history found for Decision: ...`. Show
renders every field. Evidence locators are retained but not opened.

## Lifecycle and learning boundary

DecisionReview is orthogonal interpretive history. Saving one never creates Experience. The
separate `ExperienceService.add_from_decision_review()` use case may explicitly copy selected
findings or candidate lessons into one Experience without mutating the Review.
DecisionReview does not affect `DecisionLifecycleService`.
The lifecycle remains exactly `proposed`, `accepted`, `in_progress`, `succeeded`, `failed`,
`partial`, and `outcome_unknown`; no `reviewed` state exists. A review never automatically creates
Observation, Knowledge, Playbook, PlaybookEvaluation, EvolutionProposal, revision records, or
Consigliere work. Promotion remains explicit and a promoted Experience is not Knowledge.

---

# DecisionReview-to-Experience Promotion

## Responsibility and chain

The implemented promotion foundation converts selected immutable DecisionReview interpretation
into one existing `Experience` record only through the explicitly authorized
`ExperienceService.add_from_decision_review(...)` use case:

```text
DecisionReview
→ explicitly promoted Experience
→ separately and explicitly created Knowledge
```

A finding or candidate lesson is not Experience before promotion succeeds. A promoted Experience
is still not Knowledge. Reviewer and promoter are separate authorities and may be different people;
this foundation introduces no RBAC or approval system.

## Durable schema

`Experience` now has one optional field:

```text
decision_review_promotion: DecisionReviewPromotion | None
```

`DecisionReviewPromotion` contains exactly:

```text
decision_review_id
source_statements
promoted_by
promotion_reason
idempotency_key
```

Each ordered `DecisionReviewPromotionSourceStatement` contains exactly:

```text
kind
index
text
```

The source-kind vocabulary is exactly `finding | candidate_lesson`. Durable indexes are zero-based
and non-negative. Source statements are ordered and non-empty, and each `(kind, index)` pair is
unique. Promotion and source-statement values are immutable.

`promoted_by` and `idempotency_key` are trimmed, non-blank, and at most 255 characters;
`promotion_reason` is trimmed, non-blank, and at most 1000 characters. Copied statement text is
trimmed, non-blank, and at most 1000 characters. The service stores the normalized exact immutable
Review item at the selected index; callers and the CLI never supply independent source text.

Plain direct and Observation-derived Experiences retain `decision_review_promotion is None`. A
promotion copies no Decision, DecisionAcceptance, DecisionAction, DecisionOutcome, reviewer,
assessment, confidence, or evidence fields into Experience. Their provenance remains transitive
through the referenced Review.

## Cardinality and corrections

- One promoted Experience references exactly one DecisionReview.
- One promoted Experience selects one or more ordered statements from that Review.
- One DecisionReview may produce multiple Experiences.
- One source statement may be promoted repeatedly under different idempotency keys.
- One promoted Experience cannot combine multiple DecisionReviews.

Corrections append another Experience under a different key. There is no replacement,
supersession, deletion, status, ranking, scoring, or current/best promotion behavior.

## Explicit application and read integrity

`ExperienceService.add_from_decision_review(...)` performs this sequence:

1. validate the non-empty, unique, non-negative caller selectors and normalize bounded promotion
   authority metadata;
2. call the existing validated `DecisionReviewService.show(review_id)` boundary;
3. validate each ordered finding or candidate-lesson index and copy exact Review text;
4. validate optional Observation references through the existing behavior;
5. construct one promoted Experience;
6. scan `ExperienceRepository.load_all()` for the scoped idempotency key;
7. save exactly one Experience only after every validation and idempotency check.

Validation failure, conflict, or ambiguity performs no write. The service creates no second link
record and performs no transaction emulation.

Equivalent replay validates the existing promoted Experience before returning it. `get_by_id()`,
the complete Experience list, and the Observation-linked Experience list also revalidate promoted
records. Validation calls the referenced Review's existing `show()` boundary, which revalidates its
persisted Decision, acceptance, outcome, and time relations, then checks selector bounds and exact
copied text. Missing or malformed provenance fails closed without repair or skipping. Plain
Experience reads are unaffected; Observation-linked listing validates only returned linked records.

## Idempotency

Promotion idempotency is application-layer policy scoped by:

```text
(decision_review_id, "review_experience_promotion", idempotency_key)
```

| Matches | Implemented behavior |
| ---: | --- |
| 0 | Save and return one promoted Experience. |
| 1 equivalent | Return the existing Experience with its original ID and timestamp; no write. |
| 1 conflicting | Raise `DecisionReviewPromotionIdempotencyConflictError`; no write. |
| More than 1 | Raise `DecisionReviewPromotionIdempotencyAmbiguityError`; do not select or compare an arbitrary duplicate; no write. |

Ambiguity is independent of repository enumeration order. Semantic equivalence excludes only
generated `Experience.id` and `Experience.timestamp`. It includes every caller-supplied Experience
field, optional Observation IDs, tags, and every ordered promotion field, including copied text,
promoter, reason, and key.

## Persistence compatibility

`ExperienceRepository` remains limited to `save()`, `load_all()`, and `get_by_id()`; scanning and
relation policy remain in the application layer. Existing `JsonExperienceRepository` already
round-trips plain and promoted records through domain validation under `NeuralPaths.EXPERIENCES`.
Old JSON without `decision_review_promotion` remains valid and loads with `None`.

No migration, inferred provenance, second write, separate aggregate, repository, adapter, path, or
Brain collection was introduced. The production adapter required no rewrite.

## CLI and boundaries

The implemented command is `neural experience from-review REVIEW_UUID`. It requires repeatable
ordered `--source KIND:ORDINAL`, `--promoted-by`, `--promotion-reason`, `--idempotency-key`,
`--title`, `--context`, `--action`, `--outcome`, and `--result`. Optional repeatable inputs are
`--observation-id` and `--tag`.

For example, `--source finding:1 --source candidate_lesson:2` uses one-based user ordinals and is
converted deterministically to durable indexes `0` and `1`. Invalid syntax, kind, non-positive
ordinal, Review, source index, Observation, conflict, ambiguity, or persisted integrity renders a
controlled error. Success and equivalent replay render the stored Experience identity and complete
promotion provenance, including user ordinal, stored index, copied text, actor, reason, and key.

Ordinary `neural experience add`, `from-observation`, `list`, `show`, `knowledge`, and
`neural observation experiences` retain their existing inputs and behavior. Ordinary creation does
not require promotion data or an idempotency key.

Promotion changes no canonical Decision lifecycle state and adds no `reviewed`, `promoted`, or
`learned` state. It creates no Knowledge, Playbook, PlaybookEvaluation, EvolutionProposal,
revision, evidence execution, automatic learning, or Consigliere work. `DecisionReview.assessment`,
`DecisionOutcome.result`, and `Experience.result` remain distinct meanings. A later explicit
Knowledge generalization uses the existing generic Knowledge commands and validated Experience
reader boundary; `neural experience knowledge` remains read-only navigation. Durable Knowledge use
and feedback remain separate future work.

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

## DecisionReview-to-Experience promotion ownership

`ExperienceService.add_from_decision_review(...)` is the one implemented explicit promotion use
case. It validates selectors and bounded promoter/reason/key metadata before relation reads, calls
the existing validated `DecisionReviewService.show(review_id)` boundary, validates ordered finding
and candidate-lesson indexes, copies exact Review text, validates optional Observation IDs,
constructs one Experience, then loads Experiences for application-layer idempotency. Only a fully
validated zero-match candidate is saved.

The scope is `(decision_review_id, "review_experience_promotion", idempotency_key)`. Exactly one
equivalent match returns the original Experience identity and timestamp without writing; exactly
one different match raises `DecisionReviewPromotionIdempotencyConflictError`; more than one match
raises `DecisionReviewPromotionIdempotencyAmbiguityError` without repository-order selection or
arbitrary semantic comparison. Semantic equivalence excludes only generated Experience ID and
timestamp and includes every caller-supplied Experience and ordered promotion field.

Equivalent replay validates the existing provenance. `get_by_id()`, `list_experiences()`, and
`list_for_observation()` also fail closed for promoted records when the Review graph is invalid, an
index is out of range, or copied text differs. Plain Experience reads remain unaffected. Direct and
Observation-derived `add` paths keep their existing inputs and do not acquire idempotency or
promotion requirements.

One Review may produce multiple Experiences under different keys, and the same statement may be
promoted repeatedly. Each Experience references only one Review. Corrections append; no promotion
replacement, ranking, deletion, lifecycle state, Knowledge creation, or Consigliere behavior is
owned here.

## Knowledge-to-Experience integrity ownership

`KnowledgeService` keeps its existing public methods:

```text
add()
add_from_experience()
list_knowledge()
list_for_experience()
get_by_id()
```

It depends on `KnowledgeRepository` plus a narrow application-facing `ExperienceReader` protocol
that exposes only `get_by_id()`. `ExperienceService` implements that reader, and its
`get_by_id()` remains the single owner of persisted DecisionReview-promotion provenance
validation. KnowledgeService does not depend on `ExperienceRepository`, inspect promotion fields,
load DecisionReview directly, or translate canonical DecisionReview and promotion errors.

`add()` rejects an empty Experience ID list before any relation read. It validates supplied IDs in
caller order through the reader, preserves order and duplicates, constructs Knowledge only after
all reads succeed, and then saves once. `add_from_experience()` validates its one source through
the same reader and performs no save for a missing or corrupt source.

`list_knowledge()` validates every relation of every loaded record in repository and relation
order, then returns the complete list; it does not skip, repair, filter, or partially return
invalid records. `get_by_id()` performs no Experience read for an absent Knowledge item and
validates every relation of a present item. `list_for_experience()` validates the requested
Experience first, filters in repository order, validates every relation of every matching record,
and deliberately does not validate unrelated Knowledge records.

Missing Experience relations retain `ExperienceNotFoundError`. Existing `DecisionReviewError` and
`DecisionReviewPromotionError` instances propagate unchanged. The validation guarantee is exactly
the existing `ExperienceService.get_by_id()` contract, including Review graph, selector, and
copied-text integrity; it does not recursively revalidate every Observation or DecisionAction
relation. One validated Experience read occurs per stored relation, including duplicates. This
linear fail-closed cost is accepted; no caching, batching, or deduplication is implemented.

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

## Knowledge-to-Experience integrity errors

KnowledgeService retains `ExperienceNotFoundError` for missing Experience relations. It propagates
existing `DecisionReviewError` and `DecisionReviewPromotionError` instances unchanged when
`ExperienceService.get_by_id()` finds corrupt promoted ancestry. It does not wrap them or create a
parallel Knowledge-specific taxonomy.

The CLI renders controlled nonzero failures without tracebacks for:

```text
neural knowledge add
neural knowledge from-experience
neural knowledge list
neural knowledge show
neural experience knowledge
```

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

## Narrow application reader boundary

`ExperienceReader` is defined beside `KnowledgeService` because it describes one application
service's validated read need rather than a persistence contract. It exposes only:

```text
get_by_id(experience_id)
```

`ExperienceService` satisfies the protocol structurally. The protocol prevents KnowledgeService
from depending on the broader raw `ExperienceRepository` surface or duplicating promoted
Experience validation. No repository port changed for this boundary.

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

`ExperienceRepository` remains limited to `save()`, `load_all()`, and `get_by_id()` for both plain
and promoted Experiences. Review validation, copied-text integrity, Observation validation, and
`(decision_review_id, "review_experience_promotion", idempotency_key)` scanning belong to
`ExperienceService`; no promotion, relation, or idempotency query belongs to the port.

`KnowledgeRepository` also remains limited to `save()`, `load_all()`, and `get_by_id()`.
Knowledge membership filtering and complete relation validation remain in `KnowledgeService`.
KnowledgeService does not use `ExperienceRepository` directly; its separate application-facing
`ExperienceReader` exposes only validated `get_by_id()` behavior implemented by
`ExperienceService`. No Knowledge/Experience relation query or promotion-integrity method is added
to either repository port.

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

## Experience adapter and promotion compatibility

`JsonExperienceRepository` continues to implement the unchanged `ExperienceRepository` under
`NeuralPaths.EXPERIENCES`, storing one JSON file per Experience and sorting filenames for
deterministic `load_all()`. Domain validation round-trips both ordinary records and the optional
embedded `DecisionReviewPromotion`. Old JSON without that field loads with `None` and remains plain.

No migration or production adapter rewrite was required. The adapter performs no Review lookup,
source copying, integrity repair, idempotency decision, promotion policy, second write, or inferred
provenance. No promotion adapter, repository, path, or Brain directory exists.

## Knowledge adapter compatibility

`JsonKnowledgeRepository` and `KnowledgeRepository` remain unchanged. Knowledge-to-Experience
integrity is enforced by application composition through `ExperienceReader` and
`ExperienceService.get_by_id()`, not by either JSON adapter. No Knowledge or Experience JSON field,
format, migration, relation index, second write, or repair-on-read behavior was added.

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

`Container.experience_service()` supplies `JsonExperienceRepository`,
`JsonObservationRepository`, and the existing validated `DecisionReviewService` boundary to
`ExperienceService`. The container adds no promotion policy, link repository, path, or lifecycle
behavior; `neural experience from-review` resolves this service like the ordinary Experience
commands.

`Container.knowledge_service()` supplies `JsonKnowledgeRepository` and the constructed
`ExperienceService` as the narrow `ExperienceReader`. It does not inject a raw
`JsonExperienceRepository` into KnowledgeService. This keeps promoted-Experience validation in
one owner and preserves an acyclic graph:

```text
KnowledgeService
→ ExperienceReader
→ ExperienceService
→ ExperienceRepository + ObservationRepository + DecisionReviewService
```

ExperienceService has no KnowledgeService dependency, and the container adds no Knowledge
validation or learning policy.

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

Development decision tracking uses implemented separate immutable `Decision`,
`DecisionAcceptance`, `DecisionAction`, `DecisionOutcome`, and `DecisionReview` records with
embedded immutable `EvidenceReference` values. Outcome owns factual results; Review owns
authorized interpretation over an explicit ordered outcome set. Lifecycle state is derived from
acceptance, actions, and the latest factual outcome, not stored as mutable status or duplicated in
a generic event stream. Review is orthogonal append-only history.

Selected Review interpretation becomes Experience only through an explicit authorized use case.
Promotion provenance is embedded immutably in the existing Experience rather than represented by
a link aggregate, second write, new repository, or new lifecycle state. Experience-to-Knowledge
generalization remains explicit through the existing generic Knowledge paths.

Knowledge uses `Knowledge.experience_ids` as its durable relation. Every supplied or returned
Experience relation is read through a narrow `ExperienceReader` implemented by
`ExperienceService.get_by_id()`, preserving one canonical owner for persisted Review-promotion
integrity. KnowledgeService does not read ExperienceRepository directly or copy Review provenance.

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
- Source commit `12097feb0159cc8e8831000ab04c290b56ecfc8e` implements Decision proposal,
  acceptance, action, outcome, and review recording; outcome history/summary; review history; their
  CLI; and the canonical `DecisionLifecycleService`.
- The same checkpoint implements explicit ordered DecisionReview statement promotion into one
  existing Experience with embedded immutable provenance, fail-closed read integrity, and scoped
  application-layer idempotency. It does not implement automatic learning.
- Source commit `1b45beb9b595b650a48ad00ba3ea38f7eebd02b6` hardens explicit Knowledge
  creation and all Knowledge read/navigation modes through the validated Experience reader. The
  container injects ExperienceService; canonical missing-Experience and DecisionReview/promotion
  errors fail closed without a parallel Knowledge error taxonomy.
- The canonical states are exactly proposed, accepted, in-progress, succeeded, failed, partial,
  and outcome-unknown. Latest outcome selection uses validation time and outcome UUID, not
  repository order. No generic completed, resolved, or reviewed state exists.
- Acceptance is authorization for possible future execution; it is not execution or reversal and
  creates no later lifecycle or learning record.
- Multiple immutable outcomes may be appended for one Decision. Outcome creation is factual only
  and creates no review or learning record.
- Multiple immutable reviews may cover one Decision, outcome, or ordered outcome set. Corrections
  append, action provenance remains transitive through outcomes, and no `current`, replacement,
  supersession, deletion, lifecycle transition, or automatic learning behavior exists.
- Outcome and review idempotency both fail closed when more than one persisted record matches a
  scoped key: their distinct ambiguity errors replace arbitrary first-match selection and no write
  occurs regardless of repository order or payload equivalence.
- A Review may produce multiple Experiences under distinct keys, but one promoted Experience
  references exactly one Review. Corrections append and ordinary Experience remains compatible.
- Automatic promotion and a separate promotion/link aggregate were rejected because authority and
  provenance belong in one explicit Experience write. Repository-order duplicate selection was
  rejected in favor of a dedicated fail-closed ambiguity error.
- No Knowledge schema, authority, idempotency, repository, adapter, or command changed. Duplicate
  Experience IDs remain supported, and read validation performs one validated read per relation.
- `neural knowledge add` and `neural knowledge from-experience` are explicit creation;
  `neural experience knowledge` is read-only navigation.
- Storing Knowledge proves durable capture, not later operational use or improved decisions. That
  use-and-feedback gap remains future work; Knowledge, Playbook, and evolution creation remain
  explicit.
