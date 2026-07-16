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
