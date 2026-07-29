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

Development-evidence dogfooding adds no evidence or candidate repository port. Durable apply
continues through the existing Decision-family and Experience repository contracts; the
non-persisted candidate and source snapshot have no save, load, query, lifecycle, or approval
surface.

Confirmed rule:

`PlaybookRevisionService.list_for_playbook(UUID)` owns playbook revision navigation.

`PlaybookRevisionRepository` remains limited to `save()`, `load_all()`, and `get_by_id()`.
Its `save()` contract is create-once: create an absent Revision UUID without replacement, accept
an identical complete same-ID replay as a byte-preserving no-op, and reject a different same-ID
payload as `PlaybookRevisionPersistenceConflictError` without writing.
`PlaybookRevisionRepositoryError` is the base persistence failure category;
`PlaybookRevisionStoredDataError` identifies malformed or invalid stored data and non-UUID
filename stems, while `PlaybookRevisionIdentityMismatchError` identifies filename/request versus
embedded UUID disagreement. A missing `get_by_id()` returns `None`. Relation filtering and normal
fresh-ID creation remain application-service responsibilities.

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
Its `save()` contract is create-once: create an absent Knowledge UUID, accept an identical
complete same-ID replay as a no-op, and reject a different same-ID payload as
`KnowledgePersistenceConflictError` without writing. Persistence conflict, invalid stored data,
and filename/request-to-payload identity mismatch are distinct repository failures.
Knowledge membership filtering and complete relation validation remain in `KnowledgeService`.
KnowledgeService does not use `ExperienceRepository` directly; its separate application-facing
`ExperienceReader` exposes only validated `get_by_id()` behavior implemented by
`ExperienceService`. No Knowledge/Experience relation query or promotion-integrity method is added
to either repository port.

`PlaybookRunRepository` remains limited to `save()`, `load_all()`, and `get_by_id()`.
Its `save()` contract is create-once: create an absent Run UUID without replacement, accept an
identical complete same-ID replay as a metadata-preserving no-op, and reject a different same-ID
payload as `PlaybookRunPersistenceConflictError` without writing.
`PlaybookRunRepositoryError` is the base persistence failure category;
`PlaybookRunStoredDataError` identifies malformed or invalid stored data and non-UUID filename
stems, while `PlaybookRunIdentityMismatchError` identifies filename/request versus embedded UUID
disagreement. A missing `get_by_id()` returns `None`.

Optional revision validation, complete and scoped relation integrity, ordinary fresh-ID creation,
and revision-to-Runs filtering belong to `PlaybookRunService`. The separate application-facing
`PlaybookRunReader` exposes its validated `get_by_id()` behavior to downstream services. No
revision-specific repository query method, update/delete surface, or content-level idempotency
operation is added.

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
