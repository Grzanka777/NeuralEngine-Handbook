# DecisionOutcome

## Responsibility

A DecisionOutcome is an immutable factual result and validation record for one or more actions
performed under one accepted Decision. It records what happened; it does not interpret lessons or
create learning.

## Implemented fields

- `id`
- `recorded_at`
- `decision_id`
- `acceptance_id`
- ordered unique `action_ids`
- `result`
- `summary`
- `validated_by`
- `validated_at`
- embedded `evidence_references`
- immutable scalar `metrics`
- `idempotency_key`
- normalized `tags`

The result values are exactly `succeeded`, `failed`, `partial`, and `unknown`. A Decision can have
multiple outcomes; new factual results append history instead of replacing an earlier outcome.

## Invariants and relations

- The Decision and DecisionAcceptance must exist, and the acceptance must belong to the Decision.
- At least one action is required. Action IDs are ordered and unique.
- Every action must exist and belong to the same Decision and acceptance.
- `validated_at` cannot precede the earliest linked action start.
- Required text is trimmed and non-blank; timestamps are timezone-aware and normalized to UTC.
- The record and exposed metrics mapping are immutable.

Metrics contain at most 100 `str -> int | float | str | bool` entries. Keys are trimmed,
non-blank, at most 64 characters, and case-insensitively unique. Floats must be finite, strings are
bounded to 1000 characters, and nested values are rejected. JSON serialization sorts metric keys.

## History, idempotency, and summary

Idempotency is scoped by `(decision_id, "decision_outcome", idempotency_key)`. Equivalent replay
returns the existing outcome. Reusing the same scoped key with a different semantic payload fails
without a write. If more than one persisted outcome matches the scoped key,
`DecisionOutcomeIdempotencyAmbiguityError` is raised whether their payloads are equivalent or
different. The service never chooses an arbitrary duplicate, the result is independent of
repository enumeration order, and no write occurs. Generated outcome ID, recording time, and
evidence capture times are excluded from the exactly-one-match semantic comparison; a different
key may append another outcome for the same Decision.

`DecisionOutcomeSummary` is an immutable, non-persisted read model derived on demand. It reports
outcome count, latest result and validation time, distinct linked-action count, counts for every
result value, and success/failure presence. Summary derivation validates stored acceptance/action
relations. Latest selection is deterministic by `(validated_at, outcome.id)`, never repository
order.

## Lifecycle and learning boundary

`DecisionLifecycleService` maps the latest valid outcome to `succeeded`, `failed`, `partial`, or
`outcome_unknown`. Earlier outcomes remain available as history. No `completed` or `resolved`
lifecycle state exists.

Recording an outcome does not review a Decision and does not create Observation, Experience,
Knowledge, Playbook, PlaybookEvaluation, EvolutionProposal, or automatic learning. The separately
implemented DecisionReview foundation interprets explicit outcomes without rewriting them or
changing lifecycle state.
