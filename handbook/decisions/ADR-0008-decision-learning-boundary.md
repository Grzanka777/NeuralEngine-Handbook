# ADR-0008: Decision Learning boundary

Status: Accepted

## Decision

Development decision tracking uses an implemented immutable `Decision` with embedded immutable
`EvidenceReference` values. `DecisionAcceptance`, `DecisionAction`, `DecisionOutcome`, and
`DecisionReview` remain separate future-only records. Any future lifecycle state is derived from
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
- Source commit `7724342` implements only the Decision foundation and `neural decision
  add/list/show`; it does not implement the later lifecycle.
- The one recommended next milestone is `DecisionAcceptance foundation`, kept separate from
  DecisionAction and DecisionOutcome.
