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
- `run_id` is the exact persisted relation to that Run.
- Evaluation semantics are explicit.
- Evaluation does not silently mutate a playbook.

Through `PlaybookEvaluation.run_id → PlaybookRun.playbook_id →
Playbook.knowledge_ids`, an Evaluation provides durable feedback at Playbook and declared
Knowledge-set scope. It does not attribute an outcome to one Knowledge item or prove causal or
comparative improvement.

## Typical transitions

`PlaybookEvaluation` → `EvolutionProposal`
