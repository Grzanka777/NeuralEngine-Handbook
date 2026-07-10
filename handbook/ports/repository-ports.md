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
