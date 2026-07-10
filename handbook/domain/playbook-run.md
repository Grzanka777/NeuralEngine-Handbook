# PlaybookRun

## Responsibility

A PlaybookRun represents one execution instance of a playbook.

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
- Runtime state must not mutate the playbook definition.
- Evaluation is modeled separately.

## Typical transitions

`PlaybookRun` → `PlaybookEvaluation`
