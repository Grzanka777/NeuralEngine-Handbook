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

Source commit `62c0dcb` accepts a future self-observation and Decision Learning architecture based
on separate immutable `Decision`, `DecisionAcceptance`, `DecisionAction`, `DecisionOutcome`, and
`DecisionReview` records. Lifecycle state is derived from these semantic records rather than a
mutable status or duplicate generic event stream.

Decision tracking complements the existing domain chain. Consigliere remains a future advisory
layer, while NeuralEngine remains the durable system of record. The full design, evidence model,
dogfooding workflow, future-only CLI sketch, implementation milestone, and explicit non-behavior
are defined in `handbook/architecture/decision-learning.md`.
