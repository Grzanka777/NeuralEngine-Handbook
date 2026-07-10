# PlaybookEvaluation

## Responsibility

A PlaybookEvaluation records the assessment of a completed or assessable playbook run.

## Owns

- run reference,
- evaluation result,
- evidence or rationale where modeled,
- identity.

## Must not own

- playbook execution,
- revision persistence,
- evolution proposal application.

## Invariants

- Evaluation targets a specific run.
- Evaluation semantics are explicit.
- Evaluation does not silently mutate a playbook.

## Typical transitions

`PlaybookEvaluation` → `EvolutionProposal`
