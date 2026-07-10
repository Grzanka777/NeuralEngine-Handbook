# Anti-pattern: Business Logic in Adapter

## Symptom

An infrastructure adapter decides validation, eligibility, transition, or policy.

## Risk

- behavior changes when adapters change,
- domain rules become untestable in isolation,
- persistence becomes the source of truth.

## Correction

Move policy into domain or application services. Keep the adapter focused on translation and external interaction.
