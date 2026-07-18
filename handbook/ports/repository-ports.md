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
