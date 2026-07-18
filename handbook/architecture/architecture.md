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

Source commit `910f481e27302daa6d3f15bde30d678ffc9e5d2f` implements separate immutable
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

The canonical lifecycle states remain exactly `proposed`, `accepted`, `in_progress`, `succeeded`,
`failed`, `partial`, and `outcome_unknown`. Review is orthogonal append-only history; there is no
`reviewed` state. Outcome or review creation does not create learning. There is no execution
engine, lifecycle reversal, ingestion, automatic learning or evolution, generic event replay, or
Consigliere integration. The authoritative implemented contract and future boundary are defined
in `handbook/architecture/decision-learning.md`; the recommended next controlled slice is
separate explicit Experience creation from review findings or candidate lessons.
