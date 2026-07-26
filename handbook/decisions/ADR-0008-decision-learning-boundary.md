# ADR-0008: Decision Learning boundary

Status: Accepted

## Decision

Development decision tracking uses implemented separate immutable `Decision`,
`DecisionAcceptance`, `DecisionAction`, `DecisionOutcome`, and `DecisionReview` records with
embedded immutable `EvidenceReference` values. Outcome owns factual results; Review owns
authorized interpretation over an explicit ordered outcome set. Lifecycle state is derived from
acceptance, actions, and the latest factual outcome, not stored as mutable status or duplicated in
a generic event stream. Review is orthogonal append-only history.

Selected Review interpretation becomes Experience only through an explicit authorized use case.
Promotion provenance is embedded immutably in the existing Experience rather than represented by
a link aggregate, second write, new repository, or new lifecycle state. Experience-to-Knowledge
generalization remains explicit through the existing generic Knowledge paths.

Knowledge uses `Knowledge.experience_ids` as its durable relation. Every supplied or returned
Experience relation is read through a narrow `ExperienceReader` implemented by
`ExperienceService.get_by_id()`, preserving one canonical owner for persisted Review-promotion
integrity. KnowledgeService does not read ExperienceRepository directly or copy Review provenance.

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
- Source commit `12097feb0159cc8e8831000ab04c290b56ecfc8e` implements Decision proposal,
  acceptance, action, outcome, and review recording; outcome history/summary; review history; their
  CLI; and the canonical `DecisionLifecycleService`.
- The same checkpoint implements explicit ordered DecisionReview statement promotion into one
  existing Experience with embedded immutable provenance, fail-closed read integrity, and scoped
  application-layer idempotency. It does not implement automatic learning.
- Source commit `1b45beb9b595b650a48ad00ba3ea38f7eebd02b6` hardens explicit Knowledge
  creation and all Knowledge read/navigation modes through the validated Experience reader. The
  container injects ExperienceService; canonical missing-Experience and DecisionReview/promotion
  errors fail closed without a parallel Knowledge error taxonomy.
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
- A Review may produce multiple Experiences under distinct keys, but one promoted Experience
  references exactly one Review. Corrections append and ordinary Experience remains compatible.
- Automatic promotion and a separate promotion/link aggregate were rejected because authority and
  provenance belong in one explicit Experience write. Repository-order duplicate selection was
  rejected in favor of a dedicated fail-closed ambiguity error.
- No Knowledge schema, authority, idempotency, repository, adapter, or command changed. Duplicate
  Experience IDs remain supported, and read validation performs one validated read per relation.
- `neural knowledge add` and `neural knowledge from-experience` are explicit creation;
  `neural experience knowledge` is read-only navigation.
- Source commit `ebab369f24385494da5906f523368d81eb08d639` documents the implemented
  Playbook-scoped contract from exact `Playbook.knowledge_ids` through Run, Evaluation, and
  Proposal relations, plus the optional DecisionAction/DecisionOutcome bridge.
- Source commit `18788adacf75ff7f11d0dd6f28e5da8cf143081b` adds zero-or-one explicit
  caller-supplied `PlaybookRun.revision_id`, validated writes and fail-closed linked reads,
  revision-to-Runs navigation, and validated downstream Run-reader composition.
- Storing Knowledge alone proves durable capture, not later use or improvement. Playbook-scoped
  Knowledge use and Run feedback exist, while Knowledge-specific causality, durable retrieval or
  recommendation events, and demonstrated improvement remain unsupported. Revision-specific
  execution provenance exists only when a Run caller supplies one exact same-Playbook revision;
  it is never inferred from activation or application state.
- PlaybookEvaluation, EvolutionProposal, and DecisionAction preserve optional revision provenance
  transitively through exact Run relations and do not store a revision ID directly.
- Old Run JSON without `revision_id` remains valid without migration, backfill, or inference.
