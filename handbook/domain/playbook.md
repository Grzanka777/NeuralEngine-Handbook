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
- Revision navigation is owned by `PlaybookRevisionService`.
- Persistence concerns remain outside the domain object.

## Typical transitions

`Playbook` → `PlaybookRun`
