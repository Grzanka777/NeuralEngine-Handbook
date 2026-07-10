# Observation

## Responsibility

An Observation captures a raw, bounded fact or signal before interpretation.

## Owns

- source reference,
- observed content,
- capture metadata,
- identity,
- creation timestamp when applicable.

## Must not own

- derived meaning,
- reusable guidance,
- playbook execution logic,
- evaluation logic.

## Architectural role

Observation is the entry point of the NeuralEngine knowledge chain.

## Invariants

- Identity is explicit.
- Source/provenance is preserved.
- Content is not silently rewritten into interpretation.
- Validation occurs before persistence.

## Typical transitions

`Observation` → `Experience`

The transition must be performed by an application use case, not a repository adapter.
