# Execution Profiles

## critical

Strongest available reasoning, conservative scope, explicit uncertainty and full evidence. Use for architecture, persistence, migration, security, data integrity, public contracts and release decisions.

## review

Independent skeptical analysis, read-only behavior, evidence before conclusions and findings ordered by severity.

## balanced

Default medium reasoning for standard implementation, documentation and bounded technical work.

## light

Minimal reasoning for deterministic mechanical tasks with exact instructions and no scope expansion.

## Separation

Task class defines workflow rigor. Execution profile defines reasoning for one stage.

A critical change may use `critical` for implementation, `review` for independent review and `light` for an authorized exact-copy publication step.
