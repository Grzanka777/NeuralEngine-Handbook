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
