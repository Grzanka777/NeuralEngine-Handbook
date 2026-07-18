# ADR-0008: Decision Learning boundary

Status: Accepted

## Decision

Development decision tracking uses implemented separate immutable `Decision`,
`DecisionAcceptance`, `DecisionAction`, and `DecisionOutcome` records with embedded immutable
`EvidenceReference` values. `DecisionReview` remains a separate future-only record. Lifecycle
state is derived from semantic records, not stored as mutable status or duplicated in a generic
event stream.

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
- Source commit `5befd7c` implements Decision proposal, acceptance, action and outcome recording,
  outcome history/summary, their CLI, and the canonical `DecisionLifecycleService`.
- The canonical states are exactly proposed, accepted, in-progress, succeeded, failed, partial,
  and outcome-unknown. Latest outcome selection uses validation time and outcome UUID, not
  repository order. No generic completed, resolved, or reviewed state exists.
- Acceptance is authorization for possible future execution; it is not execution or reversal and
  creates no later lifecycle or learning record.
- Multiple immutable outcomes may be appended for one Decision. Outcome creation is factual only
  and creates no review or learning record.
- The one recommended next milestone is `DecisionReview foundation`, kept separate from automatic
  learning and downstream Experience, Knowledge, or Playbook creation.
