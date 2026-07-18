# ADR-0008: Decision Learning boundary

Status: Accepted

## Decision

Development decision tracking uses implemented separate immutable `Decision`,
`DecisionAcceptance`, `DecisionAction`, `DecisionOutcome`, and `DecisionReview` records with
embedded immutable `EvidenceReference` values. Outcome owns factual results; Review owns
authorized interpretation over an explicit ordered outcome set. Lifecycle state is derived from
acceptance, actions, and the latest factual outcome, not stored as mutable status or duplicated in
a generic event stream. Review is orthogonal append-only history.

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
- Source commit `910f481e27302daa6d3f15bde30d678ffc9e5d2f` implements Decision proposal,
  acceptance, action, outcome, and review recording; outcome history/summary; review history; their
  CLI; and the canonical `DecisionLifecycleService`.
- The canonical states are exactly proposed, accepted, in-progress, succeeded, failed, partial,
  and outcome-unknown. Latest outcome selection uses validation time and outcome UUID, not
  repository order. No generic completed, resolved, or reviewed state exists.
- Acceptance is authorization for possible future execution; it is not execution or reversal and
  creates no later lifecycle or learning record.
- Multiple immutable outcomes may be appended for one Decision. Outcome creation is factual only
  and creates no review or learning record.
- Multiple immutable reviews may cover one Decision, outcome, or ordered outcome set. Corrections
  append, action provenance remains transitive through outcomes, and no `current`, replacement,
  supersession, deletion, lifecycle transition, or automatic learning behavior exists.
- Outcome and review idempotency both fail closed when more than one persisted record matches a
  scoped key: their distinct ambiguity errors replace arbitrary first-match selection and no write
  occurs regardless of repository order or payload equivalence.
- The recommended next controlled slice is separate explicit Experience creation from review
  findings or candidate lessons; downstream Experience, Knowledge, or Playbook creation remains
  explicit.
