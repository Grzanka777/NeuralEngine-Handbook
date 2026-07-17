# ADR-0008: Decision Learning boundary

Status: Accepted

## Decision

Development decision tracking uses implemented separate immutable `Decision`,
`DecisionAcceptance`, and `DecisionAction` records with embedded immutable `EvidenceReference`
values. `DecisionOutcome` and `DecisionReview` remain separate future-only records. Lifecycle state
is derived from semantic records, not stored as mutable status or duplicated in a generic event
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
- Source commit `1964356` implements Decision proposal, acceptance, action recording, and their
  CLI plus the canonical `DecisionLifecycleService`.
- Only proposed, accepted, and in-progress states can currently be derived. Action completion time
  does not imply lifecycle completion, success, failure, outcome, or review.
- Acceptance is authorization for possible future execution; it is not execution or reversal and
  creates no later lifecycle or learning record.
- The one recommended next milestone is `DecisionOutcome foundation`, kept separate from
  DecisionReview.
