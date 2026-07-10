# Anti-pattern: God Repository

## Symptom

A repository exposes relationship navigation, filtering, reporting, validation, and business operations.

## Risk

- persistence controls application behavior,
- services become thin wrappers,
- adapters become difficult to replace,
- domain decisions leak outward.

## Correction

Keep persistence methods minimal. Move orchestration and navigation into application services.
