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
- `knowledge_ids` contains the exact Knowledge UUIDs selected by the caller.
- `PlaybookService.add()` requires at least one Knowledge ID and validates every referenced
  Knowledge item before persistence.
- Revision navigation is owned by `PlaybookRevisionService`.
- Persistence concerns remain outside the domain object.

Knowledge selection is explicit. It is not durable retrieval history, a recommendation event,
execution, evaluation, or proof that any individual Knowledge item caused an outcome.

The Playbook retains exact Knowledge UUIDs rather than Knowledge payload snapshots. Supported
create-once Knowledge repository writes give each referenced UUID stable payload meaning going
forward. This does not add a Knowledge snapshot, version relation, content hash, historical
reconstruction, or protection from direct filesystem mutation.

## Typical transitions

`Playbook` → `PlaybookRun`
