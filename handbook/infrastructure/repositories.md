# Repository Adapters

## Responsibility

Repository adapters implement repository ports.

## Implementation rules

- Preserve domain identity exactly.
- Preserve provenance fields.
- Make serialization round-trippable.
- Keep ordering deterministic when public behavior depends on ordering.
- Handle missing records according to the port contract.
- Do not broaden the port from inside the adapter.
- Do not add business filtering without an application requirement.

## Testing requirements

Repository adapters require tests for:

- save and load,
- missing identity,
- list behavior,
- ordering where relevant,
- serialization round trip,
- invalid/corrupted persisted data,
- provenance preservation.
