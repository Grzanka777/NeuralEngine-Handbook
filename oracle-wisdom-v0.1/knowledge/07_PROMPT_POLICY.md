# Prompt Policy

## Generate an agent prompt only when

- repository inspection or modification is required;
- an agent materially reduces error risk;
- scope and authority can be explicit;
- validation can be defined.

## Prefer manual commands when

- operation is deterministic;
- few known paths are affected;
- no architectural judgment is required;
- verification is immediate.

## Prompt structure

1. classification;
2. objective;
3. authoritative checkpoint;
4. compact scope;
5. exclusions;
6. validation;
7. review artifact;
8. NeuralEngine usage;
9. completion response.

## Efficiency

One task per fresh session; one newest checkpoint; no broad repository/history reading; combine mechanical work; no standard post-push agent without concrete risk; do not repeat global rules.

## Safety

Agents do not commit or push without explicit separate authorization. Token savings never weaken Brain, data, migration, security, schema, public behavior or release controls.
