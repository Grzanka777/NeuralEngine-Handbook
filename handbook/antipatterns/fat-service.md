# Anti-pattern: Fat Service

## Symptom

One application service coordinates unrelated use cases and depends on many unrelated ports.

## Risk

- high coupling,
- difficult testing,
- unclear ownership,
- unrelated changes collide.

## Correction

Split by use-case responsibility or domain ownership.

Do not split solely by file length.
