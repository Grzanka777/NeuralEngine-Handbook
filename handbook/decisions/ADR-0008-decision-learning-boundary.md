# ADR-0008: Decision Learning boundary

Status: Accepted

## Decision

Future development decision tracking uses separate immutable `Decision`, `DecisionAcceptance`,
`DecisionAction`, `DecisionOutcome`, and `DecisionReview` records. Lifecycle state is derived from
those semantic records, not stored as mutable `Decision.status` or duplicated in a generic event
stream.

Decision tracking complements the existing Observation-to-Playbook chain. Evidence uses bounded
embedded references, durable writes require explicit authority, and Consigliere remains a future
advisory layer rather than authoritative storage.

## Consequences

- Recommendation, acceptance, execution, factual outcome, review, and learning remain distinct.
- Corrections append records instead of rewriting history.
- Application services own cross-record validation, derived state, and initial load-and-filter
  idempotency checks; repository ports remain persistence-focused.
- No automatic ingestion, persistence, learning, Playbook evolution, or Consigliere integration is
  implied.
- The first recommended implementation milestone is the immutable Decision foundation with only
  future `add`, `list`, and `show` CLI behavior.
