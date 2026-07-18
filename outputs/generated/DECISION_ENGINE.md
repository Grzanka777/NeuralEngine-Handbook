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

NeuralEngine source commit `12097feb0159cc8e8831000ab04c290b56ecfc8e` implements the Decision,
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

At source commit `12097fe`, `Experience` has optional immutable
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

## Implemented CLI

These commands exist at commit `12097fe`:

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

Commit `12097fe` does not capture or ingest those events automatically. Automatic candidates and
manual confirmation remain future concepts; no automatic persistence, ingestion, or learning
exists.

Consigliere also remains future-only. It may later advise. No Consigliere integration exists, and
no recommendation can directly mutate NeuralEngine or authorize a durable record.

## Current non-behavior

Commit `12097fe` does not implement:

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
Experience-to-Knowledge promotion
automatic Playbook creation or mutation
automatic evolution
Consigliere integration
```

It also does not execute commands referenced by evidence, open locators, automatically accept
Decisions, materialize Playbook revisions, or infer outcomes from `completed_at`. Explicit user
requests are required to create Decision, DecisionAcceptance, DecisionAction, DecisionOutcome, or
DecisionReview records and to promote Review statements into Experience.

## Recommended next milestone

The recommended next controlled slice is:

```text
separate explicit Experience-to-Knowledge decision or use case
```

It must preserve explicit authority and remain separate from automatic Knowledge, Playbook,
PlaybookEvaluation, EvolutionProposal, lifecycle, or Consigliere behavior.

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

Development decision tracking uses implemented separate immutable `Decision`,
`DecisionAcceptance`, `DecisionAction`, `DecisionOutcome`, and `DecisionReview` records with
embedded immutable `EvidenceReference` values. Outcome owns factual results; Review owns
authorized interpretation over an explicit ordered outcome set. Lifecycle state is derived from
acceptance, actions, and the latest factual outcome, not stored as mutable status or duplicated in
a generic event stream. Review is orthogonal append-only history.

Selected Review interpretation becomes Experience only through an explicit authorized use case.
Promotion provenance is embedded immutably in the existing Experience rather than represented by
a link aggregate, second write, new repository, or new lifecycle state. Experience-to-Knowledge
remains a separate explicit decision.

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
- The next controlled downstream step remains a separate explicit Experience-to-Knowledge decision
  or use case; Knowledge, Playbook, and evolution creation remain explicit.
