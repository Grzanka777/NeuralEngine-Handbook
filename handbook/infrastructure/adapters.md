# Infrastructure Adapters

## Responsibility

Adapters implement ports using concrete external mechanisms.

Examples:

- filesystem persistence,
- SQL persistence,
- JSON serialization,
- clock providers,
- UUID providers.

## Adapter rules

Adapters may:

- translate between persistence and domain representations,
- handle external resource lifecycle,
- convert external failures into stable adapter/application errors,
- enforce storage-level constraints that mirror domain requirements.

Adapters must not:

- decide business policy,
- change validation order,
- infer domain transitions,
- render CLI output,
- orchestrate use cases,
- silently repair invalid domain state.

## Mapping rule

Mapping code should be explicit and testable.

Persistence models must not leak into application services.
