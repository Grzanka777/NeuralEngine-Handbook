# Architecture

NeuralEngine follows a hexagonal architecture.

## Layers

- Domain
- Application
- Ports
- Infrastructure
- CLI

## Dependency rules

- Domain depends on no outer layer.
- Application depends on domain and ports.
- Infrastructure implements ports.
- CLI invokes application services.
- Dependency construction belongs in the container.
- Infrastructure must never depend on CLI.

## Responsibility rules

- Entities and value objects own domain invariants.
- Application services own use cases.
- Repository ports define persistence contracts.
- Adapters implement persistence contracts.
- CLI translates input and renders output.
- Relationship navigation should be composed in services when it does not belong in persistence.

## Revision lifecycle and application boundary

The current end of the domain chain is deliberately split across three immutable records:

```text
PlaybookRevision
→ PlaybookRevisionActivation
→ PlaybookRevisionApplication
```

`PlaybookRevision` is a candidate snapshot. `PlaybookRevisionActivation` records lifecycle and
audit decisions. `PlaybookRevisionApplication` records application intent and audit state.
Activation does not imply application.

`PlaybookRevisionActivationService.get_active_revision_for_playbook(playbook_id)` is the canonical
owner of active-revision resolution. `PlaybookRevisionApplicationService` delegates to it and must
not duplicate activation-history replay.

The application foundation has a domain model, repository port, JSON adapter at
`NeuralPaths.PLAYBOOK_REVISION_APPLICATIONS`, and container wiring for both repository and service.
`PlaybookRevisionApplicationService.add(...)` validates that the Playbook, revision, and proposal
exist; the proposal is still accepted; the revision belongs to the supplied Playbook and proposal;
an optional source activation exists and matches the same relation; and the requested revision is
currently active.

Read-only application navigation verifies the source entity, calls
`PlaybookRevisionApplicationRepository.load_all()`, filters in the application layer, and preserves
repository order. No relation-specific repository query methods exist.

Activation inspection and lifecycle-write CLI commands exist. Application CLI commands do not.
Records created by the current application service have `content_changed=False`; there is no
Playbook content mutation, revision materialization, proposal mutation or application, proposal
status change, or automatic evolution.

This architecture snapshot corresponds to source commit `88921c5` (`feat: add playbook revision
application foundation`). Source validation for that milestone reported 537 passing tests; this is
a milestone snapshot, not a timeless guarantee.

## Decision Learning boundary

Source commit `0ffdda6bfdbadd5952c1066fddd303185939d643` preserves the separate immutable
`Decision`, `DecisionAcceptance`, `DecisionAction`, `DecisionOutcome`, and `DecisionReview`
records, persistence-focused ports and JSON adapters, application services, container wiring,
thin proposal/acceptance/action/outcome/review CLI commands, and the canonical
`DecisionLifecycleService`. An action records work performed; only a linked outcome records
factual results and validation evidence; a review records authorized interpretation.

`DecisionOutcome` links one Decision, its acceptance, and one or more ordered unique actions. Its
result is exactly `succeeded`, `failed`, `partial`, or `unknown`; scalar metrics are immutable.
Multiple outcomes form history, and the non-persisted `DecisionOutcomeSummary` derives counts and
the latest outcome using `(validated_at, outcome.id)` rather than repository order.
`DecisionReview` targets an explicit ordered non-empty set of outcomes for one Decision and
acceptance. Multiple reviews form immutable history ordered by `(reviewed_at, review.id)`.

The same checkpoint implements explicit Review-to-Experience promotion. One Experience may embed
optional immutable `DecisionReviewPromotion` provenance containing ordered copied Review
statements. `ExperienceService` uses the validated Review service boundary and existing Experience
repository; no promotion aggregate, repository, adapter, path, Brain collection, or automatic
learning exists. Old and ordinary Experiences remain compatible.

The checkpoint also hardens the existing explicit Knowledge slice. `KnowledgeService` depends on
the narrow application-facing `ExperienceReader.get_by_id()` protocol, and the container supplies
`ExperienceService` as its implementation. Knowledge creation and returned Knowledge relations
therefore reuse `ExperienceService.get_by_id()` as the single owner of persisted Review-promotion
provenance validation. The dependency remains acyclic because `ExperienceService` has no
KnowledgeService dependency.

`KnowledgeService.add()` rejects empty evidence before relation reads, validates IDs in caller
order, preserves duplicates, and writes only after every read succeeds. `add_from_experience()`
uses the same boundary. Complete list and present single-item reads validate every stored
Experience relation; the scoped Experience navigation validates its requested Experience and all
relations of matching Knowledge records while leaving unrelated records outside the query.
Missing Experiences retain `ExperienceNotFoundError`, while canonical DecisionReview and
promotion errors propagate unchanged.

The same checkpoint hardens Knowledge persistence without changing the Knowledge schema.
`KnowledgeRepository.save()` is create-once: one Knowledge UUID binds to one complete modeled
payload under supported repository operations. An identical complete same-ID replay succeeds
without rewriting existing bytes; a different same-ID payload conflicts without writing.
`JsonKnowledgeRepository` publishes a validated same-directory temporary file through a
non-replacing local filesystem operation. Malformed stored data and filename/request UUID
mismatches fail visibly without overwrite or repair, while a missing `get_by_id()` still returns
`None`.

Complete payload equality includes `id`, `timestamp`, `statement`, `rationale`, `confidence`,
ordered `experience_ids`, and ordered `tags`. This is exact modeled equality, not semantic
equivalence or content deduplication. Valid old JSON remains readable without migration or
backfill; an existing valid payload is authoritative for its UUID going forward.

Playbook and PlaybookRevision continue to retain exact Knowledge UUIDs. Under supported
create-once writes those identities now retain stable payload meaning going forward, but neither
record snapshots Knowledge. Direct filesystem mutation remains out-of-band corruption. The
contract is not tamper-proof storage, cryptographic immutability, Knowledge versioning,
historical reconstruction, payload snapshotting, or hash-based integrity.

Source commit `49db077c00e67c1d3b5f25ec92b46c83518a30bb` adds the corresponding
create-once persistence contract for `PlaybookRevision`. Under supported repository operations,
one Revision UUID binds to one complete validated modeled payload. Complete equality covers every
modeled field and ordered collection: `id`, `timestamp`, `playbook_id`, `proposal_id`, `title`,
`situation`, `objective`, ordered `steps`, ordered `success_criteria`, ordered `knowledge_ids`,
`notes`, and ordered `tags`.

`JsonPlaybookRevisionRepository` validates the candidate and publishes a same-directory temporary
file through a non-replacing operation. An absent UUID path is created once. An identical complete
same-ID replay succeeds without rewriting the existing bytes; any different same-ID payload
raises `PlaybookRevisionPersistenceConflictError` without overwrite. Malformed or invalid stored
data raises `PlaybookRevisionStoredDataError`. A filename or requested UUID that differs from the
embedded payload UUID raises `PlaybookRevisionIdentityMismatchError`. `load_all()` also validates
filename UUID syntax and embedded identity, while a missing `get_by_id()` still returns `None`.
Valid old JSON remains readable without migration.

This gives exact Revision UUID relations stable payload meaning going forward under supported
repository operations. It does not deeply freeze nested in-memory lists, prove pre-hardening
payload history, snapshot Revision content into Run or related records, add versioning,
supersession, hashes, content-addressed IDs, migration, backfill, repair, backup/restore, or
filesystem tamper evidence. Direct filesystem mutation remains out-of-band corruption; the
contract is not tamper-proof or cryptographically immutable.

The canonical lifecycle states remain exactly `proposed`, `accepted`, `in_progress`, `succeeded`,
`failed`, `partial`, and `outcome_unknown`. Review is orthogonal append-only history; there is no
`reviewed`, `promoted`, or `learned` state. Outcome or review creation does not create learning;
only the explicit promotion use case creates an Experience, which remains distinct from Knowledge.
There is no execution engine, lifecycle reversal, ingestion, automatic learning or evolution,
generic event replay, or
Consigliere integration. The authoritative implemented contract and future boundary are defined
in `handbook/architecture/decision-learning.md`. Generic Knowledge creation is already explicit;
`neural experience knowledge` is read-only navigation. Storing Knowledge alone does not prove
later use or improvement.

## Durable operational Knowledge use and feedback

Durable Playbook-scoped Knowledge use and Run feedback already exist:

```text
PlaybookRun -> zero or one PlaybookRevision
PlaybookRevision -> zero or many PlaybookRuns
authority -> explicit Run caller
```

Run write validation requires actions, then the base Playbook, then a supplied revision, then
same-Playbook revision ownership; only then may one Run be saved. `get_by_id()`, complete lists,
Playbook-scoped lists, and revision-scoped lists validate linked revision existence and ownership.
Corrupt linked provenance fails closed, while old Run JSON without `revision_id` loads as `None`
without migration, backfill, or inference.

```text
Knowledge
→ Playbook.knowledge_ids
→ PlaybookRun(playbook_id, revision_id?)
→ PlaybookEvaluation.run_id
→ EvolutionProposal(playbook_id, evaluation_ids)
```

The caller explicitly selects exact Knowledge UUIDs into a Playbook, declares that the Playbook
was manually or externally applied by recording a Run, and may additionally declare zero or one
exact immutable PlaybookRevision whose content was used. The Run caller is the authority for that
optional declaration. The caller then evaluates that exact Run and may create an EvolutionProposal
from exact Evaluation IDs. `EvolutionProposalService` verifies that every referenced Evaluation's
Run belongs to the target Playbook.

The exact persisted feedback path is:

```text
PlaybookEvaluation.run_id
→ PlaybookRun(revision_id?, playbook_id)
→ Playbook.knowledge_ids
→ Knowledge.id
```

Decision learning provides an optional persisted bridge:

```text
DecisionOutcome.action_ids
→ DecisionAction.playbook_run_id?
→ PlaybookRun(revision_id?, playbook_id)
→ Playbook.knowledge_ids
```

The bridge is optional because `DecisionAction.playbook_run_id` is optional. A DecisionOutcome
references exact DecisionAction IDs, but an action without a Run relation supplies no Playbook or
Knowledge-use provenance.

These relations provide feedback at Playbook and declared Knowledge-set scope and preserve an
explicit Run revision relation transitively. Evaluation, EvolutionProposal, and DecisionAction do
not store a revision ID directly. The relations do not record durable retrieval history or
recommendation events, prove that one Knowledge item caused an outcome, attribute contributions
within a multi-Knowledge Playbook, or demonstrate causal or comparative improvement.

Revision provenance is never inferred from current active revision, activation history,
repository order, timestamps, `PlaybookRevisionApplication`, or application-intent records. A
revision need not be active or applied for the caller to truthfully declare that its content was
used. `revision_id=None` covers base Playbook execution, legacy records, and unknown revision
provenance and makes no revision-specific claim. Selection, Run recording, Evaluation, Proposal
creation, and decision linkage remain explicit caller actions; none triggers automatic learning,
mutation, materialization, activation, application, or evolution.
