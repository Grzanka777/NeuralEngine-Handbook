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

## Decision action and lifecycle ownership

`DecisionActionService.add()` validates the Decision, matching acceptance, and optional
PlaybookRun before creating an immutable action. It uses
`(decision_id, "decision_action", idempotency_key)` for application-layer idempotency, permits
multiple distinct actions, and mutates no related record. PlaybookRun and Playbook expose no
`project_key`, so the service can validate only run existence without a schema change.

`list_for_decision()` validates the Decision, filters `load_all()` in repository order, and
`show()` owns explicit action-not-found behavior. The service creates no Outcome, Review, or
learning record.

`DecisionLifecycleService` is the only canonical projection owner. It validates persisted
Decision/acceptance/action relations and derives only `proposed`, `accepted`, or `in_progress`.
It writes no status, ignores repository order for state, and exposes no completed, succeeded,
failed, or reviewed state.
