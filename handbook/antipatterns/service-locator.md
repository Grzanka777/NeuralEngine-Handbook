# Anti-pattern: Service Locator

## Symptom

Application code fetches dependencies from a global container at runtime.

## Risk

- hidden dependencies,
- brittle tests,
- runtime failures,
- cyclic coupling.

## Correction

Use constructor injection and keep the container at the composition root.
