# PlaybookRun

## Responsibility

A PlaybookRun is the caller's explicit record that one existing Playbook was manually or
externally applied to a concrete situation. NeuralEngine does not execute Playbook steps.

## Owns

- playbook reference,
- execution state,
- runtime inputs and outputs where modeled,
- identity.

## Must not own

- reusable playbook definition,
- evaluation policy,
- proposal approval logic.

## Invariants

- A run references exactly one playbook identity.
- `playbook_id` is the exact persisted relation to that Playbook.
- Runtime state must not mutate the playbook definition.
- Evaluation is modeled separately.
- A Run has no PlaybookRevision relation, so it cannot prove which revision was executed.

## Typical transitions

`PlaybookRun` → `PlaybookEvaluation`
