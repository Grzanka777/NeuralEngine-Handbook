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

## Neural home path selection

Source commit `f7bdd1dceb6b848c67b8acf2552ddd18cda51a34` implements one fail-closed
operational path-selection contract. `NEURAL_HOME` is the sole public selector. When it is absent,
the selected home remains exactly:

```text
Path.home() / ".neural"
```

Presence is distinct from absence. A supplied value must be non-blank, have no leading or trailing
whitespace, contain neither `~` nor NUL, be absolute, and strictly resolve to an existing,
accessible directory. A valid directory symlink is accepted only after strict resolution.
Malformed, missing, dangling, non-directory, inaccessible, or otherwise unavailable overrides
fail closed. Once `NEURAL_HOME` is present, no failure path falls back to `~/.neural`.

Each resolution returns one immutable `NeuralPaths` value. Its resolved home derives the Brain,
all 15 default JSON record-store directories, projects, logs, `config.toml`, and `VERSION`.
`Brain`, `Container`, CLI preflight, and every default JSON repository consume that selected path
set. Environment-derived defaults are not frozen at module import.

`Brain` distinguishes default initialization from override initialization. Default `neural init`
may create `Path.home() / ".neural"`. Override init requires the selected root itself to
pre-exist and be writable; it creates only approved children below that root. It does not
recursively recreate a vanished selected root. Existing initialization content is preserved by
the bounded idempotent initialization behavior.

`neural status` is read-only. It reports the resolution source, configured value, resolved home,
resolved Brain path, home and Brain availability, initialization state, and a bounded failure
reason. Normal commands preflight the selected root; with an override they also require an
available initialized Brain before service use. An unavailable override is not represented as an
empty Brain, and the error explicitly states that no fallback was used.

## Neural Doctor readiness diagnostics

`neural doctor` is the bounded, intrinsically read-only readiness companion to `neural status`.
It diagnoses the selected Neural home and Brain without initializing, repairing, migrating,
configuring, or writing state. It accepts no command flags. The selected home is the authority
for every check; an unavailable override fails closed and never falls back to `~/.neural`.

Doctor checks home and Brain existence, directory and read/write access, package `VERSION`,
`config.toml`, and the exact 15 canonical JSON stores. It counts records and validates each
record's UTF-8 decoding, JSON structure, domain schema, filename UUID/payload-ID consistency,
and duplicate IDs within a store. It also computes a deterministic relative-path aggregate
SHA-256 manifest without printing payloads, configuration contents, individual IDs, or per-file
hashes.

The report has the fixed sections `Selection`, `Home`, `Brain`, `Stores`, `Integrity`, `Manifest`,
and `Readiness`. Checks use the states `PASS`, `WARN`, `FAIL`, and `SKIP`. A `READY` report exits
`0`; `NOT READY` exits `1`; invalid invocation or an unexpected internal failure exits `2`.
Doctor provides evidence only: it does not repair, initialize, migrate, back up, mount or inspect
devices/processes, manage locks, validate relationship graphs, inspect project behavior, manage
agent configuration, or write Brain records. It complements `neural status`: status explains
selection and availability, while Doctor explains operational readiness of the selected state.

For a pre-existing portable home, an environment override may be used for one process:

```bash
NEURAL_HOME=/path/to/NeuralEngine-State neural doctor
```

This is an operational example, not a universal product default or a migration/synchronization
mechanism. The default remains `Path.home() / ".neural"` when the override is absent.

Explicit `directory=...` repository injection remains supported and bypasses the default
root-selection guard for that injected directory. Domain models, application-service interfaces,
repository ports, JSON schemas, and existing default-home data do not change.

This capability is path selection only. It does not migrate, copy, back up, restore, synchronize,
merge, lock, export, or import a Brain. It provides no mount or device management, filesystem
identity or health policy, multi-host writer coordination, MCP integration, project partitioning
or inference, or agent integration. When `NEURAL_HOME` points to a directory on
portable storage, a user-managed portable Neural home is supported provided the same
path is available and accessible. Storage lifecycle, device management, and deployment
remain user and operator responsibilities.

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

Source commit `6303abe56e8362478f7cc60dc9d841658ee815d8` adds create-once persistence
integrity for `PlaybookRun`. Under supported repository operations, one Run UUID is published
without replacement. One Run UUID binds to one complete validated modeled payload.

Equality covers `id`, `timestamp`, `playbook_id`, `revision_id`, `situation`, ordered
`actions_taken`, `outcome`, `success`, ordered `evidence`, `notes`, and ordered `tags`.

`JsonPlaybookRunRepository` validates the candidate, writes and `fsync`s a repository-owned
same-directory temporary file, and publishes it without replacing an existing UUID path. An absent
UUID is created once. An identical complete same-ID replay is a successful no-op that preserves
bytes, inode, size, mtime, and ctime. Any different complete same-ID payload raises
`PlaybookRunPersistenceConflictError` without overwrite. Malformed JSON or invalid modeled data
raises `PlaybookRunStoredDataError`; a filename or requested UUID that differs from embedded
`PlaybookRun.id` raises `PlaybookRunIdentityMismatchError`.

`get_by_id()` returns `None` when the file is absent; present data is validated and identity
checked. `load_all()` validates every filename stem as a UUID, validates every complete Run, and
rejects identity mismatches rather than skipping invalid records. Valid existing JSON remains
readable without migration. Repository-owned temporary files are cleaned up.

Repository replay is not ordinary creation. `PlaybookRunService.add()` and `neural run add`
continue to generate a fresh Run UUID and timestamp and expose no same-ID or semantic replay.
Content equality under different generated UUIDs is not idempotent or deduplicated. The repository
adds no update, delete, replace, version, migration, repair, transaction, generalized
crash-recovery, or tamper-proof guarantee; direct filesystem mutation remains out-of-band.

Optional Revision provenance is unchanged. `playbook_id` names the base Playbook; caller-supplied
`revision_id` may name one exact Revision, while omission makes no revision-specific claim.
Activation, application, timestamps, tags, and repository order never infer that relation.
No other record automatically creates a Run. Persistence creates no automatic additional Run,
Evaluation, DecisionAction, Outcome, Review, Experience, Knowledge, or evolution record.

The canonical lifecycle states remain exactly `proposed`, `accepted`, `in_progress`, `succeeded`,
`failed`, `partial`, and `outcome_unknown`. Review is orthogonal append-only history; there is no
`reviewed`, `promoted`, or `learned` state. Outcome or review creation does not create learning;
only the explicit promotion use case creates an Experience, which remains distinct from Knowledge.
Source commit `25599655d0b1483eb37f88d379f6ca99afaf828d` adds one specialized local
development-evidence boundary. `DevelopmentEvidenceSource` exposes bounded source facts;
`LocalDevelopmentEvidenceSource` owns local file, Git, and conservative Markdown reads;
`DevelopmentEvidenceService` owns correlation, non-persisted preview, authority-confirmed apply,
replay, and dependency-ordered delegation. Existing Decision-family services continue to own all
durable semantics and persistence, and the CLI remains parsing, delegation, rendering, and
controlled-error handling only.

This is not a generic ingestion framework. There is no execution engine, lifecycle reversal,
automatic learning or evolution, generic event replay, persisted evidence or candidate aggregate,
or Consigliere integration. The authoritative implemented contract and future boundary are
defined in `handbook/architecture/decision-learning.md`. Generic Knowledge creation is already
explicit; `neural experience knowledge` is read-only navigation. Storing Knowledge alone does not
prove later use or improvement.

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

## Package and Brain format version contracts

NeuralEngine package/application version and persisted Brain format version are independent
contracts.

For NeuralEngine v1.1.0:

- package/application version is 1.1.0,
- persisted Brain format version remains 1.0.0.

A package release does not imply a Brain-format migration. Brain compatibility is determined by
the persisted Brain format contract, not by the package version.

The authority for the package/application version is the NeuralEngine `pyproject.toml` and the
`neuralengine.__version__` module attribute. The authority for the persisted Brain format version
is the Brain `VERSION` file produced by Brain initialization.

Package upgrade does not automatically migrate Brain format. Compatibility checks use the
persisted format contract, not the package version. Only behavior supported by NeuralEngine source
determines actual format support.
