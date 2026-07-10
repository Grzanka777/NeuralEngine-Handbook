# Experience

## Responsibility

An Experience represents interpreted learning derived from one or more observations.

## Owns

- interpreted outcome,
- contextual meaning,
- provenance back to observations,
- identity.

## Must not own

- generalized reusable knowledge,
- execution instructions,
- evaluation policy.

## Invariants

- Provenance is preserved.
- Interpretation is explicit.
- Creation does not erase source observations.

## Typical transitions

`Experience` → `Knowledge`

The application layer coordinates this transformation.
