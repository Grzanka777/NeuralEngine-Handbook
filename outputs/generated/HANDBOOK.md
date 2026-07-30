# NeuralEngine Engineering Handbook

# NeuralEngine Constitution

## Mission

Build an engine that transforms observations into reusable knowledge, executable playbooks, evaluated outcomes, and controlled evolution.

## Core principles

1. Correctness before speed.
2. Domain before persistence.
3. Explicit dependencies before convenience.
4. Architecture before implementation shortcuts.
5. Deterministic behavior where practical.
6. Validation before persistence.
7. Small coherent changes.
8. Tests as executable specifications.
9. Review evidence before success claims.
10. No commits or pushes by agents.

## Forbidden

- Business logic in CLI handlers.
- Business logic in infrastructure adapters.
- Hidden dependencies.
- Global mutable state.
- Silent validation failure.
- Scope expansion.
- Unrelated refactoring.
- Repository interfaces used as service APIs.
- Manual edits to generated handbook outputs.

---

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

---

# Decision Learning Architecture

## Status and purpose

NeuralEngine source commit `0ffdda6bfdbadd5952c1066fddd303185939d643` implements the Decision,
DecisionAcceptance, DecisionAction, DecisionOutcome, and DecisionReview foundations plus the
canonical `DecisionLifecycleService` projection. They record an immutable proposed choice,
explicit authorization, work performed under that authorization, factual results, and authorized
interpretation, plus explicit promotion of selected Review statements into an existing Experience.
Each foundation persists its durable records, exposes application use cases, is wired through the
container, and provides a thin CLI.

The wider Decision Learning lifecycle remains accepted future architecture. Decision tracking
complements the existing Observation-to-Playbook chain; it does not replace it.

## Implemented foundation

The implemented foundations are exactly:

```text
Decision
EvidenceReference
DecisionAcceptance
DecisionAction
DecisionOutcome
DecisionReview
DecisionReviewPromotion
DecisionReviewPromotionSourceStatement
DecisionRepository
DecisionAcceptanceRepository
DecisionActionRepository
DecisionOutcomeRepository
DecisionReviewRepository
JsonDecisionRepository
JsonDecisionAcceptanceRepository
JsonDecisionActionRepository
JsonDecisionOutcomeRepository
JsonDecisionReviewRepository
DecisionService
DecisionAcceptanceService
DecisionActionService
DecisionOutcomeService
DecisionOutcomeSummary
DecisionReviewService
ExperienceService.add_from_decision_review
ExperienceReader
KnowledgeService
DecisionLifecycleService
container wiring
neural decision add/list/show
neural decision accept
neural decision acceptance-history
neural decision action add
neural decision action-history
neural decision action-show
neural decision outcome add
neural decision outcome-history
neural decision outcome-show
neural decision outcome-summary
neural decision review add
neural decision review history
neural decision review show
neural experience from-review
neural knowledge add/list/show
neural knowledge from-experience
neural experience knowledge
neural decision state
```

Creating a Decision records a proposal. Creating a DecisionAcceptance explicitly authorizes that
proposal for possible future work. Creating a DecisionAction records work performed under that
acceptance. Creating a DecisionOutcome records factual results and validation evidence for one or
more linked actions. Creating a DecisionReview records authorized interpretation over an explicit
ordered outcome set. None of these operations automatically creates learning.
Only the separate authorized Review-to-Experience promotion use case creates one Experience from
selected copied Review interpretation; that Experience remains distinct from Knowledge.

## Decision model

`Decision` is an immutable domain model with these implemented fields:

```text
id
created_at
project_key
title
objective
context_summary
alternatives
proposed_option
rationale
observation_ids
evidence_references
proposed_by
supersedes_decision_id
idempotency_key
tags
```

Its implemented invariants are:

1. Required text is trimmed and non-blank.
2. At least two meaningful alternatives are required.
3. Alternatives reject case-insensitive duplicates.
4. `proposed_option` exactly matches one stored alternative.
5. Observation IDs are unique.
6. An optional superseded Decision must not equal the new Decision.
7. Tags are trimmed; case-insensitive duplicates are removed while first-seen order is preserved.
8. `created_at` is timezone-aware and normalized to UTC.
9. The model is immutable.
10. No mutable lifecycle status exists.

A material correction creates another Decision linked through `supersedes_decision_id`; it does
not rewrite the earlier record.

## EvidenceReference

`EvidenceReference` is an implemented immutable value embedded in a Decision,
DecisionAcceptance, DecisionAction, DecisionOutcome, or DecisionReview:

```text
kind
locator
repository_or_project
content_hash
captured_at
source
summary
```

`kind` and `locator` are required, trimmed, non-blank, and bounded. Optional text is trimmed,
bounded, and cannot be blank when supplied. `captured_at` is timezone-aware and normalized to UTC.
The complete value is serialized inside Decision JSON.

There is no persisted Evidence aggregate or Evidence repository. The ordinary Decision-family CLI
retains a locator as provenance only and does not open, verify, or ingest it. The separate,
specialized `neural development-evidence` surface described below reads only its deliberately
bounded local prompt/review/commit topology and embeds bounded `EvidenceReference` values in the
existing records.

## DecisionAcceptance foundation

`DecisionAcceptance` is an immutable domain model with these implemented fields:

```text
id
accepted_at
decision_id
accepted_by
reason
evidence_references
idempotency_key
tags
```

Its implemented invariants are:

1. `decision_id` is a valid UUID.
2. `accepted_by` is trimmed and non-blank.
3. `reason` is trimmed and non-blank.
4. `idempotency_key` is trimmed and non-blank.
5. `accepted_at` is timezone-aware and normalized to UTC.
6. Tags are trimmed, reject blanks, and remove case-insensitive duplicates while preserving
   first-seen order.
7. Evidence references reuse the existing immutable `EvidenceReference`.
8. The model is immutable.
9. No mutable lifecycle status exists.
10. Acceptance does not embed or mutate the Decision payload.

The semantic boundary is exact:

```text
Decision
= proposed choice

DecisionAcceptance
= explicit authorization for possible future execution
```

Acceptance does not mean execution occurred, a DecisionAction exists, a DecisionOutcome exists, a
DecisionReview exists, or learning was created.

## DecisionAction foundation

`DecisionAction` is an immutable domain model with these exact implemented fields:

```text
id
recorded_at
decision_id
acceptance_id
action_type
summary
performed_by
started_at
completed_at
evidence_references
playbook_run_id
idempotency_key
tags
```

Its implemented invariants are:

1. Decision and acceptance IDs are valid UUIDs.
2. `action_type`, `summary`, `performed_by`, and `idempotency_key` are trimmed and non-blank.
3. `action_type` is bounded to 64 characters.
4. `recorded_at`, `started_at`, and optional `completed_at` are timezone-aware and normalized to
   UTC.
5. `completed_at` cannot precede `started_at`.
6. Tags are normalized like Decision tags.
7. Evidence reuses immutable embedded `EvidenceReference`.
8. Optional `playbook_run_id` is a UUID.
9. The model is immutable.
10. No mutable status field exists.
11. Decision and DecisionAcceptance payloads are not embedded or mutated.

The semantic boundary is exact:

```text
DecisionAction
= work was performed under an explicitly accepted Decision
```

It does not mean the work succeeded, validation passed, an intended result occurred,
DecisionOutcome exists, DecisionReview exists, or learning was created. `completed_at` means only
that the described work interval ended. It does not by itself produce a `completed`, `executed`,
or `succeeded` lifecycle state.

## DecisionOutcome foundation

`DecisionOutcome` is an immutable factual result and validation record with these exact
implemented fields:

```text
id
recorded_at
decision_id
acceptance_id
action_ids
result
summary
validated_by
validated_at
evidence_references
metrics
idempotency_key
tags
```

Its implemented invariants are:

1. Decision, acceptance, and action IDs are valid UUIDs.
2. At least one action ID is required; action IDs are ordered and unique.
3. `result` is exactly `succeeded`, `failed`, `partial`, or `unknown`.
4. `summary`, `validated_by`, and `idempotency_key` are trimmed and non-blank.
5. `recorded_at` and `validated_at` are timezone-aware and normalized to UTC.
6. Metrics contain at most 100 scalar `int | float | str | bool` values.
7. Metric keys are trimmed, non-blank, at most 64 characters, and case-insensitively unique.
8. Float metrics are finite, string metrics are bounded to 1000 characters, and nested values are
   rejected.
9. The metric mapping is immutable and serialized in deterministic key order.
10. Tags and evidence use the existing normalization and immutable `EvidenceReference` rules.
11. The model is immutable and has no mutable lifecycle status.

One Decision may have multiple outcomes. Each outcome appends factual history and may link one or
more actions; no outcome replaces or mutates an earlier record. An outcome does not mean review,
Experience, Knowledge, Playbook change, or automatic learning occurred.

## DecisionReview foundation

`DecisionReview` is an immutable, append-only authorized interpretation record with these exact
implemented fields:

```text
id
recorded_at
decision_id
acceptance_id
outcome_ids
reviewed_by
reviewed_at
assessment
summary
findings
candidate_lessons
evidence_references
confidence
idempotency_key
tags
```

Assessment is exactly `sound`, `flawed`, `mixed`, or `inconclusive`; confidence is exactly `low`,
`medium`, or `high`. Assessment is not the outcome result vocabulary: successful factual outcomes
may support a flawed review, and failed outcomes may support a sound review.

`outcome_ids` is ordered, unique, and non-empty. Findings are required ordered text; findings and
candidate lessons each allow at most 100 case-insensitively unique entries of at most 1000
characters. Candidate lessons may be empty and have no promotion authority. Reviewer is bounded to
255 characters and summary to 1000; required text is trimmed and non-blank. Tags preserve
first-seen order while removing case-insensitive duplicates. UTC-aware timestamps are normalized
to UTC, and `reviewed_at` cannot be later than `recorded_at`.

Every outcome must exist and belong to the same Decision and acceptance. Review time cannot
precede the latest `validated_at` among selected outcomes. Action IDs are not persisted: provenance
is transitive through `DecisionReview → DecisionOutcome[] → DecisionAction[]`. Multiple reviews
may cover one Decision, outcome, or ordered outcome set under different keys. Corrections append;
there is no replacement, supersession, deletion, or persisted `current` behavior.

## DecisionReview-to-Experience promotion foundation

At source commit `1b45beb`, `Experience` has optional immutable
`decision_review_promotion: DecisionReviewPromotion | None`. Plain direct and
Observation-derived Experiences retain `None`. Promotion contains exactly one Review ID, ordered
non-empty immutable source statements, promoter, reason, and idempotency key. Each statement stores
exactly `kind`, zero-based non-negative `index`, and exact copied `text`; kind is exactly `finding`
or `candidate_lesson`, and `(kind, index)` pairs are unique.

Promoter and key are bounded to 255 characters; reason and copied text are bounded to 1000. All are
trimmed and non-blank. Reviewer and promoter are separate explicit authorities. Promotion copies no
Decision, acceptance, action, outcome, reviewer, assessment, confidence, or evidence fields into
Experience. One Experience references one Review and one or more selected statements; one Review
and one source statement may produce multiple Experiences under different keys. Corrections append.

The implemented chain is:

```text
Observation
→ Decision
→ DecisionAcceptance
→ DecisionAction
→ DecisionOutcome
→ DecisionReview
→ explicitly promoted Experience
→ separately and explicitly created Knowledge
```

Review save does not promote. Promotion does not create Knowledge or change Decision lifecycle.
`DecisionReview.assessment`, `DecisionOutcome.result`, and `Experience.result` remain distinct.

## Persistence

The persistence-focused `DecisionRepository` port implements only:

```text
save()
load_all()
get_by_id()
```

No relation, project, or idempotency query was added. `JsonDecisionRepository` stores one JSON
file per Decision under `NeuralPaths.DECISIONS`. UUIDs, UTC-aware timestamps, embedded evidence,
and optional values round-trip through the domain model. `load_all()` sorts file names for
deterministic order. Malformed stored data surfaces domain validation errors; the adapter does not
silently repair it. No migration, evidence ingestion, file ingestion, or git ingestion behavior
exists.

The persistence-focused `DecisionAcceptanceRepository` likewise implements only:

```text
save()
load_all()
get_by_id()
```

It has no relation, project, or idempotency query methods. Relation and eligibility filtering
belong to `DecisionAcceptanceService`. `JsonDecisionAcceptanceRepository` stores one JSON file per
acceptance under `NeuralPaths.DECISION_ACCEPTANCES`, and Brain initialization creates that
directory. `load_all()` sorts file names for deterministic order. UUIDs, UTC-aware timestamps,
embedded evidence, and normalized tags round-trip through domain validation. Malformed stored data
surfaces validation errors. No migration or ingestion behavior exists.

The persistence-focused `DecisionActionRepository` implements only:

```text
save()
load_all()
get_by_id()
```

It has no relation, idempotency, or lifecycle query methods. Filtering and relation validation
remain in application services. `JsonDecisionActionRepository` stores one JSON file per action
under `NeuralPaths.DECISION_ACTIONS`, and Brain initialization creates that directory.
`load_all()` sorts file names for deterministic order. The complete domain record round-trips
through validation, and malformed stored data fails visibly. The adapter performs no migration,
ingestion, or command execution.

The persistence-focused `DecisionOutcomeRepository` also implements only:

```text
save()
load_all()
get_by_id()
```

It has no relation, idempotency, latest-outcome, summary, or lifecycle query methods.
`JsonDecisionOutcomeRepository` stores one deterministic JSON file per outcome under
`NeuralPaths.DECISION_OUTCOMES`, and Brain initialization creates that directory. Complete records
and immutable scalar metrics round-trip through domain validation; malformed data fails visibly.
The adapter performs no relation filtering, lifecycle projection, review, learning, migration, or
ingestion.

The persistence-focused `DecisionReviewRepository` implements only:

```text
save()
load_all()
get_by_id()
```

It has no relation, idempotency, chronology, or lifecycle query methods.
`JsonDecisionReviewRepository` stores one deterministic sorted-key JSON file per review under
`NeuralPaths.DECISION_REVIEWS`, and Brain initialization creates that directory. `load_all()` sorts
filenames and every record round-trips through domain validation. Filtering, relation validation,
history ordering, ambiguity detection, and semantic comparison remain in the application service.

The existing `ExperienceRepository` also remains limited to:

```text
save()
load_all()
get_by_id()
```

`JsonExperienceRepository` continues to store one JSON file per Experience under
`NeuralPaths.EXPERIENCES` and round-trips the optional embedded promotion through domain
validation. Old JSON without the field loads with `None`. No migration, new path, Brain directory,
link record, promotion repository, second write, or production adapter rewrite was introduced.
Idempotency and Review integrity remain application policy.

The existing `KnowledgeRepository` remains limited to:

```text
save()
load_all()
get_by_id()
```

No Knowledge relation or provenance query was added. The Knowledge JSON schema is unchanged.
`save()` now defines create-once persistence: an absent UUID is created once, an identical
complete same-ID replay is a no-op without byte rewrite, and a different same-ID payload
conflicts without writing. `JsonKnowledgeRepository` enforces this with validated same-directory
temporary data and non-replacing local publication. Malformed stored data and filename/request
identity mismatch fail visibly on collisions and reads without repair. Knowledge membership
filtering and Experience relation validation remain application policy.

## Application service

`DecisionService` implements:

```text
add()
list_decisions()
show()
```

`add()` constructs an immutable Decision candidate first, validates every referenced Observation,
then validates an optional superseded Decision. A superseded Decision must exist and have the same
`project_key`. Only after these checks does the service perform idempotency detection and, when
needed, persist the candidate. It creates no other record, performs no lifecycle transition, and
does not trigger learning.

The implemented idempotency scope is:

```text
(project_key, "decision", idempotency_key)
```

The `"decision"` record type is implicit because the operation is owned by `DecisionService`.
Detection uses `DecisionRepository.load_all()` followed by application-layer filtering; there is
no repository idempotency query.

```text
same key + equivalent semantic payload
→ return existing Decision

same key + different semantic payload
→ visible conflict, no write
```

Semantic equivalence excludes generated identity and time values:

```text
Decision.id
Decision.created_at
EvidenceReference.captured_at
```

`list_decisions()` preserves repository order. Its optional project filter is trimmed and applied
in the application layer; a blank filter fails visibly. `show()` loads by UUID and raises the
existing explicit not-found error when no Decision exists.

### DecisionAcceptanceService

`DecisionAcceptanceService` implements:

```text
accept()
list_for_decision()
show()
```

`accept()` validates that the referenced Decision exists, constructs an immutable candidate, loads
all acceptance records, handles an equivalent idempotent replay, rejects conflicting key reuse,
rejects a second distinct acceptance, and persists only after validation. It does not mutate the
Decision and creates no action, outcome, review, or learning record.

The initial monotonic eligibility rule is:

```text
Decision exists
and no DecisionAcceptance exists
→ eligible for first acceptance
```

Only one acceptance per Decision is allowed. A superseding Decision does not invalidate an
existing acceptance. There is no rejection, withdrawal, reversal, reopening, cancellation, or
replacement behavior.

The implemented idempotency scope is:

```text
(decision_id, "decision_acceptance", idempotency_key)
```

```text
same scoped key + equivalent semantic payload
→ return existing DecisionAcceptance

same scoped key + different semantic payload
→ visible idempotency conflict, no write

different key + Decision already accepted
→ visible already-accepted conflict, no write
```

Semantic equivalence excludes:

```text
DecisionAcceptance.id
DecisionAcceptance.accepted_at
EvidenceReference.captured_at
```

`list_for_decision()` validates Decision existence, loads all acceptance records, filters in the
application layer, and preserves repository order without adding a repository query. `show()`
raises an explicit acceptance not-found error.

### DecisionActionService

`DecisionActionService` implements:

```text
add()
list_for_decision()
show()
```

`add()` validates Decision existence, acceptance existence, and that the acceptance belongs to the
same Decision. It validates an optional PlaybookRun exists, constructs an immutable candidate,
performs idempotency detection, returns an equivalent replay, rejects conflicting key reuse,
allows multiple distinct actions, and persists only after every validation. It mutates neither
Decision nor DecisionAcceptance and creates no Outcome, Review, Experience, Knowledge, Playbook,
or EvolutionProposal.

The current PlaybookRun limitation is explicit:

```text
PlaybookRun and Playbook currently expose no project_key,
so only existence can be validated without a separately reviewed schema change.
```

Action idempotency is scoped by:

```text
(decision_id, "decision_action", idempotency_key)
```

```text
same scoped key + equivalent semantic payload
→ return existing DecisionAction

same scoped key + different semantic payload
→ visible conflict, no write

different key
→ another action may be recorded
```

Semantic equivalence excludes:

```text
DecisionAction.id
DecisionAction.recorded_at
EvidenceReference.captured_at
```

`list_for_decision()` validates the Decision, filters `load_all()` in the application layer, and
preserves repository order. `show()` raises an explicit action-not-found error.

### DecisionOutcomeService

`DecisionOutcomeService` implements:

```text
add()
list_for_decision()
show()
summary_for_decision()
```

`add()` validates Decision existence, acceptance existence and ownership, at least one unique
action, and every action's Decision and acceptance relations. `validated_at` cannot precede the
earliest linked action start. Only after relation validation does the service construct and save
the immutable outcome. It mutates no related record and creates no Review or learning artifact.

Outcome idempotency is scoped by:

```text
(decision_id, "decision_outcome", idempotency_key)
```

```text
same scoped key + equivalent semantic payload
→ return existing DecisionOutcome

same scoped key + different semantic payload
→ visible conflict, no write

more than one persisted scoped match
→ `DecisionOutcomeIdempotencyAmbiguityError`, no arbitrary selection, no write

different key
→ another outcome may be recorded
```

Semantic equivalence excludes `DecisionOutcome.id`, `DecisionOutcome.recorded_at`, and embedded
`EvidenceReference.captured_at`. It includes the linked relations, result, validation data,
metrics, and other caller-supplied semantic fields.

`list_for_decision()` validates the Decision, filters `load_all()` in the application layer, and
preserves repository order so the complete multiple-outcome history remains visible. `show()`
raises an explicit outcome-not-found error.

`DecisionOutcomeSummary` is an immutable, non-persisted application read model returned by
`summary_for_decision()`. It reports outcome count, latest result and validation time, distinct
linked-action count, counts for each result value, and success/failure presence. Summary derivation
validates every persisted outcome-to-acceptance/action relation. Latest selection is deterministic
by `(validated_at, outcome.id)` and never depends on repository order. The summary is derived on
demand and is neither persisted nor cached.

More than one matching persisted outcome always raises ambiguity before selecting or semantically
comparing a record. This is independent of repository enumeration order and applies to equivalent
and different duplicate payloads. Zero matches follows normal creation; exactly one match retains
the equivalent-replay or conflict behavior. This hardening changes no outcome fields, vocabulary,
relations, ordering, summary, CLI, stored schema, or lifecycle behavior.

### DecisionReviewService

`DecisionReviewService` implements:

```text
add()
list_for_decision()
show()
```

`add()` constructs the candidate first, so local domain validation precedes repository reads. It
then requires the Decision, validates the acceptance belongs to it, loads every caller-ordered
outcome by ID, validates Decision and acceptance ownership, and requires `reviewed_at` to be at or
after the latest selected outcome validation. Missing or mismatched relations and invalid time all
fail before persistence.

Review idempotency is scoped by:

```text
(decision_id, "decision_review", idempotency_key)
```

```text
zero scoped matches
→ save the validated candidate

exactly one equivalent match
→ validate persisted relations and return existing DecisionReview

exactly one different match
→ `DecisionReviewIdempotencyConflictError`, no write

more than one persisted scoped match
→ `DecisionReviewIdempotencyAmbiguityError`, no arbitrary selection or comparison, no write
```

The ambiguity error carries Decision ID, idempotency key, and match count. Ambiguity is independent
of repository order and applies to semantically equivalent or different duplicates. For exactly
one match, semantic equivalence excludes generated review ID and recording time and embedded
evidence capture times; it includes every caller-supplied semantic field. Ordered outcome IDs,
findings, candidate lessons, evidence, and tags therefore remain order sensitive.

`list_for_decision()` requires the Decision, validates every persisted relation, and sorts by
`(reviewed_at, review.id)`. `show()` loads by ID and validates its relations. Controlled errors
cover missing Decision, acceptance, outcome, or review; acceptance/Decision mismatch;
outcome/Decision or outcome/acceptance mismatch; review before outcome; idempotency conflict; and
duplicate-key ambiguity. No failing path writes.

DecisionReview and DecisionOutcome share the reusable fail-closed invariant that multiple matches
for a scoped idempotency key must be surfaced, never resolved through `next()`, first-match
selection, repository order, or comparison with an arbitrarily chosen record. Their scopes and
ambiguity error types remain separate.

### ExperienceService Review promotion

`ExperienceService.add_from_decision_review(...)` validates selectors and bounded authority
metadata before calling `DecisionReviewService.show()`. It then copies caller-ordered exact Review
items, validates optional Observations, constructs one promoted Experience, loads all Experiences,
and applies this scope:

```text
(decision_review_id, "review_experience_promotion", idempotency_key)
```

```text
zero matches
→ save and return one promoted Experience

exactly one equivalent match
→ validate its provenance and return original ID/timestamp, no write

exactly one different match
→ `DecisionReviewPromotionIdempotencyConflictError`, no write

more than one match
→ `DecisionReviewPromotionIdempotencyAmbiguityError`, no selection or comparison, no write
```

Equivalence excludes only generated `Experience.id` and `Experience.timestamp`; every ordinary
Experience field, optional Observation ID, tag, and ordered promotion value remains semantic.
Ambiguity is repository-order independent.

Replay, `get_by_id()`, complete list, and Observation-linked list revalidate the referenced Review
graph, selector bounds, and exact copied text. Missing or malformed provenance fails closed without
repair or skipping; plain records bypass promotion validation. The use case owns no Knowledge,
Playbook, evolution, lifecycle, evidence, or Consigliere behavior.

### KnowledgeService validated Experience boundary

The existing generic `KnowledgeService` implements:

```text
add()
add_from_experience()
list_knowledge()
list_for_experience()
get_by_id()
```

It depends on `KnowledgeRepository` and the application-facing `ExperienceReader.get_by_id()`
protocol defined beside the service. `ExperienceService` implements the protocol, so
`ExperienceService.get_by_id()` remains the single owner of persisted Review graph, promotion
selector, and copied-text validation. KnowledgeService no longer reads `ExperienceRepository`
directly, loads DecisionReview, or duplicates another service's validation. ExperienceService has
no KnowledgeService dependency, so the graph is acyclic.

`add()` rejects empty evidence before relation reads, validates supplied Experience IDs in caller
order, preserves duplicates, and saves only after every validation succeeds.
`add_from_experience()` validates its source through the same reader and performs no save when it
is missing or corrupt.

`list_knowledge()` validates every Experience relation of every loaded record in repository and
relation order and fails closed without partial results. `get_by_id()` performs no Experience read
when Knowledge is absent and validates every relation of a present record.
`list_for_experience()` validates the requested Experience first, filters Knowledge in repository
order, validates every relation of every matching record, and deliberately leaves unrelated
Knowledge records outside this scoped validation.

Missing relations continue to raise `ExperienceNotFoundError`. Existing `DecisionReviewError` and
`DecisionReviewPromotionError` instances propagate unchanged. The five affected CLI surfaces
render those failures as controlled nonzero errors without tracebacks. Validation is exactly the
existing ExperienceService read contract; it does not recursively revalidate every Observation or
DecisionAction ancestry relation.

This hardening changes no Knowledge or Experience schema, authority, cardinality, duplicate-ID
behavior, Knowledge idempotency, repository, adapter, JSON format, command, or automatic behavior.
It performs one validated Experience read per stored relation, including duplicates. The linear
read amplification is accepted in favor of fail-closed integrity; no caching, batching, or
deduplication was added.

### Canonical DecisionLifecycleService

`DecisionLifecycleService` is the only canonical owner of the current lifecycle projection. It
depends on:

```text
DecisionRepository
DecisionAcceptanceRepository
DecisionActionRepository
DecisionOutcomeRepository
```

It derives exactly:

```text
Decision exists, no acceptance
→ proposed

Decision exists, one valid acceptance, no action
→ accepted

Decision exists, one valid acceptance, at least one valid action
→ in_progress

latest valid outcome has result succeeded
→ succeeded

latest valid outcome has result failed
→ failed

latest valid outcome has result partial
→ partial

latest valid outcome has result unknown
→ outcome_unknown
```

No mutable status is written and no generic event stream exists. The latest outcome is selected by
`(validated_at, outcome.id)`, never repository order. Multiple persisted acceptances fail visibly,
as do invalid action or outcome relations. Multiple valid actions with no outcome derive
`in_progress`; multiple outcomes retain history while the latest valid one drives the projection.
There is no generic `executed`, `completed`, `resolved`, or `reviewed` state.

## Container

The composition root constructs and connects:

```text
JsonDecisionRepository
JsonObservationRepository
DecisionService
JsonDecisionAcceptanceRepository
DecisionAcceptanceService
JsonDecisionActionRepository
JsonPlaybookRunRepository
DecisionActionService
JsonDecisionOutcomeRepository
DecisionOutcomeService
JsonDecisionReviewRepository
DecisionReviewService
JsonExperienceRepository
ExperienceService
JsonKnowledgeRepository
KnowledgeService
DecisionLifecycleService
```

`DecisionAcceptanceService` receives `JsonDecisionAcceptanceRepository` and
`JsonDecisionRepository`. The CLI resolves services from the container. It does not construct
repositories or own validation, relation checks, persistence, eligibility, or idempotency policy.

`DecisionActionService` receives `JsonDecisionActionRepository`, `JsonDecisionRepository`,
`JsonDecisionAcceptanceRepository`, and `PlaybookRunService` as a validated `PlaybookRunReader`.
`PlaybookEvaluationService` and `EvolutionProposalService` use the same validated Run boundary.
`PlaybookRunService` receives JSON Run, Playbook, and PlaybookRevision repositories, with no
activation or application dependency. `DecisionOutcomeService`
receives `JsonDecisionOutcomeRepository` plus Decision, acceptance, and action repositories.
`DecisionLifecycleService` receives the Decision, acceptance, action, and outcome repositories.
`DecisionReviewService` receives `JsonDecisionReviewRepository` plus Decision, acceptance, and
outcome repositories. `Container.decision_review_repository()` and
`Container.decision_review_service()` expose the review composition. CLI handlers resolve services
from the container and construct no repositories.
`Container.experience_service()` injects `JsonExperienceRepository`,
`JsonObservationRepository`, and that validated `DecisionReviewService` boundary into
`ExperienceService`; the container owns no promotion policy.
`Container.knowledge_service()` injects `JsonKnowledgeRepository` and the constructed
`ExperienceService` as `ExperienceReader`; it does not supply a raw `JsonExperienceRepository` to
KnowledgeService.

## Implemented CLI

These commands exist at commit `1b45beb`:

```text
neural decision add
neural decision list
neural decision show DECISION_UUID
neural decision accept DECISION_UUID
neural decision acceptance-history DECISION_UUID
neural decision action add DECISION_UUID
neural decision action-history DECISION_UUID
neural decision action-show ACTION_UUID
neural decision outcome add DECISION_UUID
neural decision outcome-history DECISION_UUID
neural decision outcome-show OUTCOME_UUID
neural decision outcome-summary DECISION_UUID
neural decision review add DECISION_UUID
neural decision review history DECISION_UUID
neural decision review show REVIEW_UUID
neural experience add
neural experience from-observation OBSERVATION_UUID
neural experience from-review REVIEW_UUID
neural experience list
neural experience show EXPERIENCE_UUID
neural experience knowledge EXPERIENCE_UUID
neural knowledge add
neural knowledge from-experience EXPERIENCE_UUID
neural knowledge list
neural knowledge show KNOWLEDGE_UUID
neural observation experiences OBSERVATION_UUID
neural decision state DECISION_UUID
```

The current source checkpoint `0ffdda6` additionally exposes explicit revision execution
provenance through:

```text
neural run add --revision-id REVISION_UUID ...
neural run list
neural run show RUN_UUID
neural revision runs REVISION_UUID
```

Run list and show output render the revision ID or `-` when absent. CLI handlers delegate relation
validation to `PlaybookRunService` and render missing or cross-Playbook provenance as controlled
exit-code-1 errors.

`neural decision add` requires these scalar options:

```text
--project-key
--title
--objective
--context-summary
--proposed-option
--rationale
--proposed-by
--idempotency-key
```

It accepts these repeatable options:

```text
--alternative
--observation-id
--evidence
--tag
```

The optional supersession argument is:

```text
--supersedes-decision-id
```

Evidence is supplied as a bounded JSON value, for example:

```bash
neural decision add \
  --project-key NeuralEngine \
  --title "Canonical lifecycle ownership" \
  --objective "Choose one active-revision owner" \
  --context-summary "Two services could derive the same state" \
  --alternative "Activation service owns derivation" \
  --alternative "Application service replays records" \
  --proposed-option "Activation service owns derivation" \
  --rationale "One owner prevents semantic drift" \
  --proposed-by architecture-review \
  --idempotency-key decision-active-revision-owner \
  --evidence '{"kind":"agent_review","locator":".agent-work/reviews/review.md"}'
```

The CLI parses and validates this JSON value as `EvidenceReference`. It does not read the locator
or ingest any referenced file content.

`neural decision list --project PROJECT_KEY` filters through the service and renders:

```text
ID
Created
Project
Title
Proposed option
Proposed by
```

`neural decision show DECISION_UUID` renders the full Decision details, including alternatives,
Observation IDs, embedded evidence references, optional supersession, idempotency key, and tags.

### Decision acceptance commands

`neural decision accept DECISION_UUID` requires:

```text
DECISION_UUID
--accepted-by
--reason
--idempotency-key
```

It accepts repeatable optional values:

```text
--evidence
--tag
```

For example:

```bash
neural decision accept DECISION_UUID \
  --accepted-by architecture-owner \
  --reason "Approved after architecture review" \
  --idempotency-key decision-acceptance-1 \
  --evidence '{"kind":"manual_decision","locator":"approval:architecture-review"}' \
  --tag architecture
```

The CLI parses and validates `EvidenceReference`, but does not read the locator or ingest locator
content. Business rules remain in `DecisionAcceptanceService`. Success prints the stored
acceptance ID.

`neural decision acceptance-history DECISION_UUID` validates the Decision through the service and
renders:

```text
ID
Accepted
Decision ID
Accepted by
Reason
```

An existing Decision with no acceptance produces a controlled empty state.

### Decision action commands

`neural decision action add DECISION_UUID` requires:

```text
--acceptance-id
--action-type
--summary
--performed-by
--started-at
--idempotency-key
```

It accepts these optional values; evidence and tags are repeatable:

```text
--completed-at
--playbook-run-id
--evidence
--tag
```

The CLI parses timestamps as ISO-8601 values and parses evidence as embedded
`EvidenceReference` values. It does not execute commands or open evidence locators. Business rules
remain in `DecisionActionService`, and success prints the stored action ID.

`neural decision action-history DECISION_UUID` renders:

```text
ID
Recorded
Action type
Performed by
Started
Completed
Summary
```

An existing Decision with no actions produces a controlled empty state.
`neural decision action-show ACTION_UUID` renders every DecisionAction field.

### Decision outcome and state commands

`neural decision outcome add DECISION_UUID` requires:

```text
--acceptance-id
--action-id (one or more)
--result
--summary
--validated-by
--validated-at
--idempotency-key
```

Repeated `--evidence`, `--metric KEY=VALUE`, and `--tag` values are optional. Result accepts only
`succeeded`, `failed`, `partial`, or `unknown`. Metrics parse unambiguous booleans, integers, and
finite floats; other values remain strings and domain validation enforces the scalar bounds. The
CLI reads no evidence locator and executes no referenced command.

`neural decision outcome-history DECISION_UUID` renders all matching outcomes in repository order,
including their result, validation time, linked action IDs, validator, and summary. An existing
Decision with no outcomes produces a controlled empty state. `outcome-show OUTCOME_UUID` renders
every stored field, including evidence, metrics, idempotency key, and tags.

`neural decision outcome-summary DECISION_UUID` renders the derived count, deterministic latest
result/time, distinct linked-action count, counts by result, and success/failure presence. It does
not persist the summary.

### Decision review commands

`neural decision review add DECISION_UUID` requires:

```text
--acceptance-id
--outcome-id (one or more, repeatable and ordered)
--reviewed-by
--reviewed-at
--assessment
--summary
--finding (one or more, repeatable and ordered)
--confidence
--idempotency-key
```

Optional repeatable inputs are `--candidate-lesson`, `--evidence` JSON, and `--tag`. Assessment
accepts `sound`, `flawed`, `mixed`, or `inconclusive`; confidence accepts `low`, `medium`, or
`high`. The CLI parses ISO-8601 review time and embedded evidence but never opens evidence
locators. Validation errors render their first message; `ValueError` and controlled
`DecisionReviewError` failures render visibly and exit nonzero. Success prints the stored review ID
and every review field.

`neural decision review history DECISION_UUID` renders deterministic service history with columns
`ID`, `Reviewed`, `Reviewed by`, `Assessment`, `Confidence`, `Outcome IDs`, and `Summary`. An
existing Decision with no reviews renders `No review history found for Decision: ...`.
`neural decision review show REVIEW_UUID` renders every field after persisted relation validation.

### Review-to-Experience promotion command

`neural experience from-review REVIEW_UUID` requires repeatable ordered `--source`, plus:

```text
--promoted-by
--promotion-reason
--idempotency-key
--title
--context
--action
--outcome
--result
```

Optional repeatable inputs are `--observation-id` and `--tag`. Selectors use exact syntax such as
`--source finding:1 --source candidate_lesson:2`. CLI ordinals are positive and one-based; they
become durable zero-based indexes `0` and `1` without caller-supplied text. Invalid selector syntax,
kind, ordinal, Review, source index, Observation, conflict, ambiguity, or read integrity renders a
controlled error.

Success and equivalent replay print the stored Experience ID and complete auditable Experience
details. Promotion source rendering shows kind, user ordinal, stored index, and copied text, plus
promoter, reason, and key. Reviewer and promoter remain separate authorities.

Ordinary Experience commands keep their existing contracts. Direct `add` requires title, context,
action, outcome, and result; `from-observation` derives context from the required Observation and
requires title, action, outcome, and result. Observation IDs and tags remain optional where already
supported. List, show, Experience-to-Knowledge navigation, and Observation-to-Experience navigation
remain read-only. Ordinary Experience creation requires no promotion metadata or idempotency key.

### Knowledge commands and controlled integrity failures

`neural knowledge add` and `neural knowledge from-experience EXPERIENCE_UUID` are the existing
explicit creation paths. They accept caller-supplied Knowledge content and do not infer, promote,
or automatically create it. `neural experience knowledge EXPERIENCE_UUID` is read-only navigation.

All five Knowledge-to-Experience surfaces are protected by the validated reader:

```text
neural knowledge add
neural knowledge from-experience EXPERIENCE_UUID
neural knowledge list
neural knowledge show KNOWLEDGE_UUID
neural experience knowledge EXPERIENCE_UUID
```

Missing Experience and canonical DecisionReview/promotion-integrity errors render controlled
messages and exit nonzero without a traceback. No Knowledge-specific promotion error taxonomy,
new command, or success-output change exists.

Repository persistence conflicts, invalid stored data, and filename/request UUID mismatches also
render controlled exit-code-1 errors on the applicable Knowledge surfaces. This changes no
command, option, or success output.

`neural decision state DECISION_UUID` renders exactly one of:

```text
proposed
accepted
in_progress
succeeded
failed
partial
outcome_unknown
```

## Review and learning boundary

The record family remains deliberately separate:

```text
Decision
→ DecisionAcceptance
→ DecisionAction
→ DecisionOutcome
→ DecisionReview
```

- `Decision` is the implemented proposed choice.
- `DecisionAcceptance` is the implemented explicit authorization for possible future execution.
- `DecisionAction` is the implemented record of work performed under an accepted Decision.
- `DecisionOutcome` is the implemented factual result and validation evidence record.
- `DecisionReview` is the implemented authorized interpretation over explicit ordered outcomes.

All five decision records and the explicit Review-to-Experience promotion use case exist. Records
remain immutable semantic records rather than fields on a mutable
Decision or a duplicate generic event stream. A proposed option is not an acceptance, acceptance
is not execution, an outcome is not a review or Experience, and review findings or candidate
lessons are not Experience until promotion succeeds and are never automatically Knowledge or a
Playbook change.

Explicit Knowledge capture is a later, separate act through the existing generic Knowledge
commands. Its durable transitive provenance is:

```text
Knowledge.experience_ids
→ Experience.decision_review_promotion
→ DecisionReview
```

The Review provenance is not copied into Knowledge. `neural experience knowledge` only navigates
this relation; it does not create or promote Knowledge. Storing Knowledge proves explicit durable
capture, not that the Knowledge was used in, or improved, a later Decision.

The currently derivable projection is only:

```text
Decision without acceptance
→ proposed

Decision with one valid acceptance
→ accepted

Decision with one valid acceptance and at least one valid action
→ in_progress

latest valid outcome succeeded
→ succeeded

latest valid outcome failed
→ failed

latest valid outcome partial
→ partial

latest valid outcome unknown
→ outcome_unknown
```

The lifecycle projection uses the latest valid outcome selected by `(validated_at, outcome.id)`.
There is no generic executed, completed, resolved, or reviewed state and no generic full lifecycle
event replay service.

## Relationship to the domain chain

The implemented Decision may reference existing Observations as context. The implemented path and
future learning bridge remain explicit:

```text
Observation
→ Decision
→ DecisionAcceptance
→ DecisionAction
→ DecisionOutcome
→ DecisionReview
→ explicitly promoted Experience
→ separately and explicitly created Knowledge
```

DecisionAction may optionally reference an existing PlaybookRun, with existence-only validation
because PlaybookRun and Playbook expose no project key. `DecisionOutcome` remains distinct from
Experience. The promotion use case copies selected Review text into optional immutable Experience
provenance and never mutates a Playbook.

At source commit `6303abe56e8362478f7cc60dc9d841658ee815d8`, the implemented operational path is:

```text
Knowledge
→ Playbook.knowledge_ids
→ PlaybookRun(playbook_id, revision_id?)
→ PlaybookEvaluation.run_id
→ EvolutionProposal(playbook_id, evaluation_ids)
```

Knowledge exists before use. A caller explicitly selects exact Knowledge UUIDs into a Playbook,
explicitly declares manual or external Playbook application by recording a Run, evaluates that
exact Run, and may create a Proposal from exact Evaluation IDs. The same Run caller may declare
zero or one exact immutable PlaybookRevision whose content was used. Omission covers base Playbook
execution, legacy data, or unknown provenance and makes no revision-specific claim.
`EvolutionProposalService` verifies every referenced Evaluation's Run belongs to the target
Playbook.

Exact persisted feedback provenance is:

```text
PlaybookEvaluation.run_id
→ PlaybookRun(revision_id?, playbook_id)
→ Playbook.knowledge_ids
→ Knowledge.id
```

The optional decision-learning bridge is:

```text
DecisionOutcome.action_ids
→ DecisionAction.playbook_run_id?
→ PlaybookRun(revision_id?, playbook_id)
→ Playbook.knowledge_ids
```

It is optional because `playbook_run_id` is optional. `DecisionOutcome` preserves provenance
through exact DecisionAction IDs, but an action without the Run relation provides no Playbook or
Knowledge-use provenance.

## PlaybookRevision persistence integrity

At the same checkpoint, supported `PlaybookRevisionRepository.save()` operations are create-once.
One persisted Revision UUID identifies one complete validated modeled payload. Initial creation is
non-replacing; an identical complete same-ID replay preserves existing bytes; a different
same-ID payload conflicts without overwrite. Malformed or invalid stored data and
filename/request-to-payload UUID mismatches fail visibly without repair. `load_all()` validates
filename UUID syntax and embedded identity, and missing `get_by_id()` retains `None`.

This is exact modeled equality, including every scalar and ordered collection. It is not semantic
deduplication: the same content under a new UUID remains a distinct valid Revision. Normal
`PlaybookRevisionService.add()` continues to create a fresh UUID and is non-idempotent. No update,
replace, edit, delete, repair, replay, version, or supersession service is introduced.

`PlaybookRun.revision_id` remains optional, explicit, caller-supplied execution provenance. When
present, it retains stable Revision payload meaning going forward under supported writes.
Evaluation and EvolutionProposal preserve that identity transitively through their exact Run
relations; activation and application records preserve it through their exact Revision UUID
relations. None snapshots the Revision payload. Activation or application state is not required
to record a truthful Run, and no automatic selection or Run-to-application binding exists.

The guarantee is prospective and limited to supported repository operations. Top-level model
freezing does not deeply freeze nested lists. Pre-hardening payload history cannot be proven or
reconstructed. There are no Revision snapshots, hashes, digests, content-addressed IDs, versions,
migration, backfill, repair, backup/restore, direct-filesystem protection, tamper evidence, or
cryptographic immutability.

## PlaybookRun persistence integrity

At the current checkpoint, supported `PlaybookRunRepository.save()` operations are create-once.
One persisted Run UUID identifies one complete validated modeled payload across every Run field.
Initial publication cannot replace an existing UUID path. An identical complete same-ID replay
preserves bytes and filesystem metadata; a different same-ID payload conflicts without overwrite.
Malformed or invalid stored data and filename/request-to-payload UUID mismatches fail visibly
without repair. `load_all()` validates filename UUID syntax and all records instead of skipping
invalid data, and missing `get_by_id()` retains `None`.

This repository exact replay is not the public creation use case. `PlaybookRunService.add()` and
`neural run add` continue to generate a fresh UUID and timestamp for each ordinary creation. They
have no caller-supplied Run identity, semantic replay, or content-level deduplication. A matching
payload under a newly generated UUID is a distinct Run.

The optional Revision relation is unchanged: `playbook_id` identifies the base Playbook;
`revision_id` identifies only an exact Revision explicitly supplied by the Run caller. Omission
makes no revision claim. No activation, application, timestamp, tag, or repository ordering
infers it. No other record automatically creates a Run. Repository replay creates no additional
Run, Evaluation, DecisionAction, Outcome, Review, Experience, Knowledge, or evolution record.

The guarantee is limited to supported repository writes. There is no Run update, delete,
replacement, versioning, migration, repair, transaction, generalized crash-recovery,
tamper-proofing, cryptographic integrity, or protection from direct filesystem mutation.

## Local development evidence dogfooding

Source commit `25599655d0b1483eb37f88d379f6ca99afaf828d` implements NeuralEngine's first real
local ingestion and dogfooding path within the wider development workflow:

```text
prompt
→ agent execution
→ review finding
→ decision/correction
→ implementation
→ validation
→ commit
→ push
→ post-work lesson
```

The implemented topology is narrower:

```text
one NeuralEngine Git worktree
+ one distinct repository-relative prompt
+ one distinct repository-relative review
+ one exact lowercase full non-merge commit SHA
→ source validation and correlation
→ frozen non-persisted candidate preview
→ separate explicit authority-confirmed apply
→ Decision
→ DecisionAcceptance
→ DecisionAction
→ DecisionOutcome
→ DecisionReview
→ optional explicit Review-to-Experience promotion
```

It rejects path escape, absolute prompt/review paths, the wrong repository, Handbook input,
cross-repository bundles, identical prompt and review files, missing or insufficient Markdown,
short SHAs or aliases, merge commits, multiple prompts/reviews/commits, checkpoint mismatch,
changed-path mismatch, duplicate review paths, and patch mismatch. The adapter does not search for
artifacts or support a generic ingestion framework.

### Source ownership and correlation

Ownership is explicit:

- `DevelopmentEvidenceSource` exposes only bounded source facts.
- `LocalDevelopmentEvidenceSource` owns local file reads, SHA-256 hashing, Git reads, and
  conservative Markdown parsing.
- `DevelopmentEvidenceService` owns correlation, candidate construction, validation-tree
  strength, authority/apply, replay, and service-call ordering.
- Existing Decision-family services own durable validation, idempotency, relations, and
  persistence.
- The CLI owns parsing, delegation, JSON rendering, and controlled error conversion only.

The implemented order is:

1. validate the NeuralEngine repository root, repository-relative paths, and Git availability;
2. read each selected file once and calculate its SHA-256;
3. parse only the required conservative Markdown sections;
4. resolve the exact lowercase full commit SHA;
5. require exactly one parent;
6. read parent, bounded subject, tree, changed paths, and patch;
7. compare prompt and review starting checkpoints;
8. compare the review checkpoint with the commit parent;
9. compare review inventory with commit changed paths;
10. compare the review diff with the commit patch;
11. classify validation-tree strength;
12. locally validate the caller-supplied domain payload;
13. render the candidate;
14. require explicit apply;
15. rebuild the preview and compare fresh source facts;
16. call existing services in dependency order.

No durable write occurs before step 16. The adapter does not execute validation commands. Missing
exit codes or test counts remain unknown rather than being inferred.

### Candidate, preview, and authority

`DevelopmentEvidenceCandidate` is a frozen application result. It is non-persisted, replaceable,
side-effect free to produce, not truth, and not durable authority. It carries the repository
identity and root; prompt/review paths and hashes; prompt/review checkpoints; review outcome,
changed paths, patch hash, validation claims, and bounded risks; commit SHA, parent, subject, tree,
changed paths, and patch hash; correlation; validation-tree strength; caller interpretation;
uncertainty; EvidenceReferences; proposed and excluded writes; replay identity; and partial-apply
semantics.

Preview is the default and performs no durable write:

```text
neural development-evidence preview ... --records-json '<caller semantics>'
```

Apply is a separate surface:

```text
neural development-evidence apply ... --records-json '<caller semantics>' \
  --confirm-authority
```

Apply rebuilds the preview from fresh prompt, review, and Git facts. Changed source facts reject
the stale candidate before any write. `--confirm-authority` confirms the caller's explicit use of
the supplied semantic actors; it is not authentication. Git authors, operating-system users,
Markdown identities, and review outcomes do not confer authority. No RBAC or signatures exist.
Review-to-Experience promotion remains optional and requires explicit statement selectors,
promoter, promotion reason, and Experience semantics.

Source evidence, normalized source facts, caller interpretation, the candidate, accepted durable
records, authority, provenance, replay, and partial apply remain distinct. In particular, review
outcome `completed` does not mean `DecisionOutcome.result=succeeded`; the caller supplies the
outcome classification.

### Provenance and validation-tree strength

Apply uses the existing embedded `EvidenceReference` value for four bounded references:

```text
prompt path + NeuralEngine + prompt SHA-256
review path + NeuralEngine + review SHA-256
full commit SHA + NeuralEngine + Git tree + bounded commit subject
review validation section + review SHA-256
```

Full prompt/review bodies, diffs, and unrestricted validation output are not persisted. The commit
SHA locates the committed paths and patch. Prompt/review hashes are necessary because
`.agent-work` files are mutable and may be ignored or untracked. A hash proves byte identity, not
truth, authorship, authenticity, or causality.

Validation-tree strength is exactly one of:

```text
exact committed tree attested
review diff matches commit but validation was pre-commit
review claim only
absent
contradictory
```

An exact-tree classification requires recorded zero exit codes and a review attestation matching
the Git tree. Any recorded nonzero exit is contradictory. A matching review patch plus all
recorded zero exit codes is pre-commit diff match when no exact-tree attestation exists. Missing
exit codes remain review claims only.

### Durable writes, replay, and partial apply

Apply may create or replay only:

```text
Decision
DecisionAcceptance
DecisionAction
DecisionOutcome
DecisionReview
optional Experience through existing explicit promotion
```

It explicitly does not create:

```text
Observation
Knowledge
Playbook
PlaybookRevision
PlaybookRun
PlaybookEvaluation
EvolutionProposal
PlaybookRevisionActivation
PlaybookRevisionApplication
persisted evidence
persisted candidate
```

The replay identity is `NeuralEngine:<full commit SHA>`. The orchestrator derives deterministic
service idempotency keys; callers cannot override per-record keys through this surface. Equivalent
replay returns existing records. Changed source hashes or caller semantics conflict. An amended
commit SHA is a new identity.

Apply is resumable, not transactional. Existing services are called in dependency order and no
rollback is promised. If a later call fails, the already-written prefix remains visible; an exact
rerun resumes through existing semantic idempotency. This is deterministic orchestration
idempotency, not an atomic multi-record transaction.

### Controlled failures and explicit non-behavior

The source boundary reports invalid, missing, insufficient, and unsupported evidence. The
orchestrator reports mismatched, unauthorized, stale, or semantically conflicting evidence and
translates existing Decision-family idempotency conflicts. CLI paths render controlled exit-code-1
messages without tracebacks.

There is no automatic truth, automatic Observation or Knowledge creation, automatic Playbook
evolution, GitHub or CI integration, webhook, watcher, background ingestion, actor authentication,
multi-repository ingestion, causal proof, or autonomous learning. Full source bodies and patches
are not durable records. No persisted evidence or candidate aggregate, repository, lifecycle, or
approval state exists. It performs no automatic persistence, ingestion, or learning.

## Consigliere boundary

Consigliere also remains future-only. It may later advise. No Consigliere integration exists, and
no recommendation can directly mutate NeuralEngine or authorize a durable record.

## Current non-behavior

Commit `6303abe56e8362478f7cc60dc9d841658ee815d8` does not implement:

```text
execution engine
command/shell execution
rejection
withdrawal
reversal
reopening
cancellation
replacement
executed/completed/resolved/reviewed states
generic file ingestion
generic or multi-repository git ingestion
GitHub or CI ingestion
background ingestion
persisted evidence or candidate aggregates
candidate lifecycle or approval state
actor authentication, RBAC, or signatures
automatic Observation creation
automatic Experience creation
automatic Knowledge creation
Knowledge update/edit/delete
Knowledge supersession or revision/version lifecycle
content-addressed Knowledge IDs or content hashes
Knowledge payload snapshots or historical reconstruction
filesystem tamper evidence or automatic repair
PlaybookRevision edit/update/delete
PlaybookRevision correction/supersession/version lifecycle
PlaybookRevision payload snapshots or historical reconstruction
PlaybookRevision content hashes, digests, or content-addressed IDs
PlaybookRevision migration, backfill, repair, or backup/restore
deep PlaybookRevision collection immutability
special DecisionReview-to-Knowledge promotion
durable Knowledge retrieval history
durable recommendation events
per-Knowledge contribution attribution
causal or comparative proof of improvement
automatic Playbook creation or mutation
automatic evolution
Consigliere integration
automatic active-revision selection
Run-to-PlaybookRevisionApplication binding
Playbook materialization
revision content execution
service/CLI Run idempotency or semantic replay
content-level Run deduplication across generated UUIDs
PlaybookRun update/delete/replace
PlaybookRun versioning, migration, or repair
PlaybookRun transactions or generalized crash recovery
PlaybookRun tamper-proofing or direct-filesystem protection
mixed or partial revision execution
multiple revisions per Run
automatic activation or application
```

It also does not execute validation commands, automatically accept Decisions, materialize Playbook
revisions, or infer outcomes from review `completed` text or action `completed_at`. The specialized
local source adapter opens only the explicitly selected bounded prompt/review/commit bundle.
Explicit authority-confirmed apply is required to create Decision, DecisionAcceptance,
DecisionAction, DecisionOutcome, or DecisionReview records and to promote Review statements into
Experience.

## Remaining learning-loop limits

Durable Playbook-scoped Knowledge use and Run feedback already exist. The remaining limits are
Knowledge-specific causal attribution, per-Knowledge contribution attribution within a
multi-Knowledge Playbook, durable retrieval or recommendation events, and demonstrated causal or
comparative improvement.

`PlaybookRun` references exactly one base Playbook and may reference zero or one exact
PlaybookRevision. A supplied relation is the Run caller's factual declaration, not a lifecycle
projection. Reads validate revision existence and same-Playbook ownership and fail closed for
corrupt linked provenance; old Runs without the field remain valid.
`PlaybookRevisionApplication` records application intent and audit with
`content_changed=False`; it is not execution and is not bound to a Run. The implementation never
infers revision provenance from active-revision state, activation or application history,
co-existence, timestamps, tags, text similarity, or repository order. A revision need not be
active or applied for the caller to declare that its content was used. All selection, Run,
Evaluation, Proposal, and decision-link writes require explicit caller action and trigger no
automatic learning, mutation, materialization, activation, application, or evolution.

## Handbook synchronization policy

Generated Handbook outputs are rebuilt from source documents and templates and are never edited
manually. Copying the generated skill back to NeuralEngine is outside this synchronization task.

---

# Responsibility Matrix

| Concern | Owning layer | Forbidden locations |
|---|---|---|
| Domain invariant | Domain | CLI, adapter |
| Use-case orchestration | Application | CLI, repository adapter |
| Persistence contract | Port | Domain, CLI |
| Persistence implementation | Infrastructure | Domain, application |
| Dependency construction | Container | Domain entity, service |
| Input parsing | CLI | Domain entity |
| Output rendering | CLI | Repository |
| Relationship navigation | Application service by default | Repository unless persistence-owned |
| Validated cross-service relation read | Narrow application-facing reader protocol | Raw repository bypass or duplicated provenance validation |
| Validation of domain state | Domain/application as appropriate | Infrastructure-only |
| Provenance policy | Domain/application architecture | CLI-only |

---

# Domain Chain

The confirmed NeuralEngine chain is:

`Observation`
→ `Experience`
→ `Knowledge`
→ `Playbook`
→ `PlaybookRun`
→ `PlaybookEvaluation`
→ `EvolutionProposal`
→ `PlaybookRevision`
→ `PlaybookRevisionActivation`
→ `PlaybookRevisionApplication`

The final three stages are separate records with separate responsibilities:

- `PlaybookRevision` is an immutable candidate snapshot.
- `PlaybookRevisionActivation` is an immutable lifecycle and audit decision.
- `PlaybookRevisionApplication` is an immutable application-intent and audit record.

Creating a revision does not activate or apply it. Activation does not imply application.
The current application foundation records intent only: it does not materialize revision
content into a Playbook or mutate any related record.

## Relationship ownership

Relationship navigation belongs in application services unless persistence itself owns the concern.

Confirmed example:

- `PlaybookRevisionService.list_for_playbook(UUID)` owns playbook revision navigation.
- `PlaybookRevisionActivationService` owns activation navigation and canonical active-revision
  derivation through `get_active_revision_for_playbook(playbook_id)`.
- `PlaybookRevisionApplicationService` owns application-record navigation and delegates active
  revision resolution to `PlaybookRevisionActivationService`.
- `PlaybookRunService` owns optional explicit Run-to-Revision validation and reverse
  `list_for_revision(UUID)` navigation without consulting activation or application state.
- Repository interfaces remain persistence-focused.
- `PlaybookService` should not gain unrelated persistence dependencies.

## Complementary Decision Learning chain

The implemented Decision, DecisionAcceptance, DecisionAction, DecisionOutcome, and DecisionReview
foundations record a bounded proposed choice, explicit authorization, work performed, factual
results, and authorized interpretation after Observation context:

```text
Observation
→ Decision
→ DecisionAcceptance
→ DecisionAction
→ DecisionOutcome
→ DecisionReview
→ explicitly promoted Experience
→ separately and explicitly created Knowledge
```

This is a complementary provenance path, not a replacement for the canonical domain chain.
DecisionOutcome is factual; DecisionReview is authorized interpretation; Experience captures
explicitly promoted operational learning; Knowledge is separately generalized; Playbook remains a
separately created repeatable procedure. A Decision may have multiple immutable outcomes and
reviews, and one Review may explicitly produce multiple Experiences under different promotion
keys. A promoted Experience selects ordered Review statements and cannot combine Reviews. Review
action provenance remains transitive through explicit outcomes; promoted Experience provenance
remains transitive through its one Review. These records exist at source commit `12097fe`; no
Review save, promotion, lifecycle transition, or later Knowledge record in this path is automatic.

At source commit `1b45beb`, explicit Knowledge capture keeps its existing durable relation:

```text
Knowledge.experience_ids
→ Experience.decision_review_promotion
→ DecisionReview
```

KnowledgeService traverses every returned or newly supplied Experience relation through the
validated `ExperienceService.get_by_id()` boundary. This preserves transitive Review provenance
without copying it into Knowledge. `neural knowledge add` and `neural knowledge from-experience`
create explicit Knowledge; `neural experience knowledge` only navigates the relation. Durable
capture is not a durable record that Knowledge informed or improved a later decision.

---

# Observation

## Responsibility

An Observation captures a raw, bounded fact or signal before interpretation.

## Owns

- source reference,
- observed content,
- capture metadata,
- identity,
- creation timestamp when applicable.

## Must not own

- derived meaning,
- reusable guidance,
- playbook execution logic,
- evaluation logic.

## Architectural role

Observation is the entry point of the NeuralEngine knowledge chain.

## Invariants

- Identity is explicit.
- Source/provenance is preserved.
- Content is not silently rewritten into interpretation.
- Validation occurs before persistence.

## Typical transitions

`Observation` → `Experience`

The transition must be performed by an application use case, not a repository adapter.

---

# Experience

## Responsibility

An Experience represents explicitly recorded operational learning. It may be created directly,
derived from one Observation, or explicitly promoted from selected DecisionReview statements.

## Owns

- interpreted outcome,
- contextual meaning,
- provenance back to observations,
- optional immutable DecisionReview promotion provenance,
- identity.

## Must not own

- generalized reusable knowledge,
- execution instructions,
- evaluation policy.

## Invariants

- Provenance is preserved.
- Interpretation is explicit.
- Creation does not erase source observations.
- Plain and Observation-derived Experiences have `decision_review_promotion is None`.
- A promoted Experience contains one optional `DecisionReviewPromotion`; it remains Experience,
  not generalized Knowledge.

## Typical transitions

`Experience` → `Knowledge`

The application layer coordinates this separate explicit transformation. Experience creation does
not create Knowledge automatically.

Knowledge creation and reads consume Experience through the narrow application-facing
`ExperienceReader` implemented by `ExperienceService.get_by_id()`. For promoted Experiences this
reuses the existing Review graph, selector-index, and copied-source-text validation before the
Experience can support returned or newly created Knowledge. It does not add recursive Observation
validation to ordinary Experience reads.

---

# Knowledge

## Responsibility

Knowledge is reusable, generalized understanding derived from experience.

## Owns

- normalized insight,
- reusable statement,
- provenance to source experiences,
- identity.

## Must not own

- executable workflow steps,
- runtime execution state,
- evaluation outcome.

## Invariants

- Knowledge must be sufficiently generalized to be reusable.
- At least one Experience ID is required by `KnowledgeService.add()`.
- Every supplied or returned Experience relation is validated through the narrow
  application-facing `ExperienceReader` implemented by `ExperienceService.get_by_id()`.
- Provenance remains transitively available through `Knowledge.experience_ids`; Review provenance
  is not copied into Knowledge.
- Domain and relation validation precede persistence.
- Under supported repository operations, one persisted Knowledge UUID binds to one complete
  modeled Knowledge value.

Complete persisted equality is exact and order-sensitive:

```text
id
timestamp
statement
rationale
confidence
experience_ids in order
tags in order
```

This is not semantic equivalence or content deduplication. The same content under a new UUID is a
distinct Knowledge value.

## Typical transitions

`Knowledge` → `Playbook`

## Explicit capture and navigation

Knowledge creation remains available through:

```text
neural knowledge add
neural knowledge from-experience EXPERIENCE_UUID
```

Both commands store caller-supplied statement, rationale, confidence, Experience IDs, and tags.
They do not infer or automatically promote Knowledge. `neural experience knowledge
EXPERIENCE_UUID` is read-only navigation through `KnowledgeService.list_for_experience()` and does
not create Knowledge.

## Validated Experience boundary

`KnowledgeService` depends on `KnowledgeRepository` and the `ExperienceReader.get_by_id()`
protocol, not on `ExperienceRepository`. The container injects `ExperienceService`, whose
`get_by_id()` remains the canonical validation owner for promoted Experience ancestry.
The dependency is acyclic: ExperienceService has no KnowledgeService dependency.

Creation behavior is exact:

- `add()` rejects empty evidence before any Experience read, validates IDs in caller order,
  preserves order and duplicates, and saves only after all reads succeed;
- `add_from_experience()` validates its one source through the same reader and performs no save
  when that source is missing or corrupt.

Read behavior is exact:

- `list_knowledge()` validates every Experience relation of every record in repository and
  relation order and fails closed without partial results;
- `get_by_id()` performs no Experience read when Knowledge is absent and validates every relation
  when it is present;
- `list_for_experience()` validates the requested Experience first, preserves repository-order
  membership filtering, validates every relation of every matching Knowledge record, and does not
  validate unrelated Knowledge records.

Missing relations continue to raise `ExperienceNotFoundError`. Existing canonical
`DecisionReviewError` and `DecisionReviewPromotionError` instances propagate unchanged for missing
or malformed Review ancestry, invalid promotion selectors/indexes, or copied text that no longer
matches the Review. The guarantee is limited to validation already owned by
`ExperienceService.get_by_id()`; it does not recursively validate every possible Observation or
DecisionAction relation.

## Create-once persistence integrity

`KnowledgeRepository.save()` defines this supported-write contract:

```text
absent UUID path
→ create one persisted Knowledge payload

same ID + identical complete validated payload
→ successful no-op replay without rewriting existing bytes

same ID + different complete payload
→ KnowledgePersistenceConflictError without modifying existing bytes
```

`JsonKnowledgeRepository` serializes and validates the candidate, writes and flushes a
same-directory temporary file, and uses a non-replacing local filesystem publication operation.
If the final UUID path already exists, the adapter validates the stored payload before deciding
whether the operation is an identical replay or a conflict.

Stored-data failures remain distinct:

- `KnowledgePersistenceConflictError` means one UUID was reused for a different complete payload;
- `KnowledgeStoredDataError` means existing persisted data is malformed or invalid;
- `KnowledgeIdentityMismatchError` means the filename or requested UUID differs from embedded
  `Knowledge.id`.

Existing corrupt data fails visibly and is not repaired, replaced, skipped, or silently
substituted. `get_by_id()` and `load_all()` verify the requested or filename UUID against embedded
`Knowledge.id`; a missing `get_by_id()` still returns `None`.

The guarantee is create-once under supported repository operations. Direct filesystem mutation
remains out-of-band corruption. There is no tamper-proof storage, cryptographic immutability,
filesystem tamper evidence, content hash, Knowledge version or revision lifecycle, historical
reconstruction, or payload snapshot.

## Compatibility and learning boundary

The hardening adds no Knowledge JSON field, Review provenance copy, authority marker, repository
method, command, option, migration, backfill, or automatic creation. Valid old JSON remains
readable, existing IDs and relations remain unchanged, and the current valid payload already
stored for an ID is authoritative going forward. This does not retroactively prove that it was
never overwritten before the hardening.

Knowledge may still reference one or more Experiences, mix ordinary and promoted sources,
combine different Reviews, and retain duplicate Experience IDs. Ordinary service/CLI creation
still generates a new UUID and is not semantic or content-idempotent; only an identical
repository replay of the same complete ID-bearing value is a no-op.

Durable provenance is:

```text
Knowledge.experience_ids
→ Experience.decision_review_promotion
→ DecisionReview
```

Storing Knowledge proves explicit durable capture only. It does not by itself prove later use or
improvement. Durable Playbook-scoped use and Run feedback exist through:

```text
PlaybookEvaluation.run_id
→ PlaybookRun(revision_id?, playbook_id)
→ Playbook.knowledge_ids
→ Knowledge.id
```

This is feedback on the Playbook and its declared Knowledge set. It does not prove one Knowledge
item caused an outcome, attribute contributions within a multi-Knowledge Playbook, or demonstrate
causal or comparative improvement. Durable retrieval history, recommendation events, and
per-Knowledge contribution provenance are not recorded. Optional revision-specific Run provenance
is recorded only when the Run caller supplies an exact `revision_id`; downstream exact Run
relations preserve it transitively without attributing effects to one Knowledge item.

Read validation performs one validated Experience read per stored relation, including duplicates.
The resulting linear read amplification is an intentional fail-closed trade-off; this milestone
adds no cache, batch reader, or deduplication.

The contract also adds no Knowledge update, edit, delete, supersession, revision/version
lifecycle, content-addressed ID, actor/change audit, automatic repair, retrieval history,
recommendation event, per-Knowledge causal attribution, or automatic learning.

---

# Playbook

## Responsibility

A Playbook defines an executable or operationalized procedure derived from knowledge.

## Owns

- executable intent,
- ordered guidance or steps,
- identity,
- revision-related semantics through dedicated services.

## Must not own

- execution state,
- evaluation outcome,
- repository traversal logic,
- infrastructure-specific behavior.

## Invariants

- A playbook is distinct from a run.
- `knowledge_ids` contains the exact Knowledge UUIDs selected by the caller.
- `PlaybookService.add()` requires at least one Knowledge ID and validates every referenced
  Knowledge item before persistence.
- Revision navigation is owned by `PlaybookRevisionService`.
- Persistence concerns remain outside the domain object.

Knowledge selection is explicit. It is not durable retrieval history, a recommendation event,
execution, evaluation, or proof that any individual Knowledge item caused an outcome.

The Playbook retains exact Knowledge UUIDs rather than Knowledge payload snapshots. Supported
create-once Knowledge repository writes give each referenced UUID stable payload meaning going
forward. This does not add a Knowledge snapshot, version relation, content hash, historical
reconstruction, or protection from direct filesystem mutation.

## Typical transitions

`Playbook` → `PlaybookRun`

---

# PlaybookRun

## Responsibility

A PlaybookRun is the caller's explicit record that one existing Playbook was manually or
externally applied to a concrete situation. NeuralEngine does not execute Playbook steps.

## Owns

- exact base Playbook reference,
- optional exact PlaybookRevision execution-provenance reference,
- execution state,
- runtime inputs and outputs where modeled,
- identity.

## Must not own

- reusable playbook definition,
- evaluation policy,
- proposal approval logic.

## Invariants

- A run references exactly one playbook identity.
- `playbook_id` is the exact persisted relation to that Playbook.
- A Run references zero or one PlaybookRevision through `revision_id`; one revision may be
  referenced by zero or many Runs.
- Under supported repository writes, one Run UUID binds to one complete validated modeled
  `PlaybookRun` payload. Complete equality covers `id`, `timestamp`, `playbook_id`, `revision_id`,
  `situation`, ordered `actions_taken`, `outcome`, `success`, ordered `evidence`, `notes`, and
  ordered `tags`.
- An absent UUID is published once without replacement. An identical complete same-ID replay is a
  successful no-op that preserves bytes, inode, size, mtime, and ctime. Any different complete
  same-ID payload conflicts without overwrite.
- Repository replay is distinct from ordinary `PlaybookRunService.add()` and `neural run add`.
  Those public creation paths continue to generate a fresh Run UUID and timestamp; they do not
  expose semantic or content-level replay across newly generated UUIDs.
- Present repository data is validated as `PlaybookRun`. Malformed JSON or model data, non-UUID
  filename stems, and filename/request-to-payload UUID mismatches fail visibly and are not
  repaired, overwritten, or skipped. Missing `get_by_id()` retains `None`, and valid existing JSON
  remains readable without migration.
- The Run caller is the authority for `revision_id`. A supplied UUID declares that exact immutable
  revision content was used.
- Under supported create-once Revision repository operations, that UUID retains stable complete
  Revision payload meaning going forward. Run does not snapshot the Revision payload.
- `revision_id=None` makes no revision-specific execution claim. It covers base Playbook
  execution, legacy records, or unknown revision provenance.
- Write validation requires actions first, then the base Playbook, then a supplied revision, then
  same-Playbook revision ownership. Only a fully valid Run is saved; no failure path writes.
- Linked Run reads validate that the revision exists and belongs to the Run's Playbook. Missing or
  cross-Playbook revision provenance fails closed; legacy Runs without the relation remain valid.
- Revision provenance is never inferred from active-revision state, activation history,
  repository order, timestamps, `PlaybookRevisionApplication`, or application-intent records.
- A declared revision need not be active or applied.
- No retroactive guarantee is made for Revision payload history recorded before the create-once
  hardening.
- Runtime state must not mutate the playbook definition.
- Evaluation is modeled separately.

## Navigation and CLI

`PlaybookRunService.list_for_revision(revision_id)` validates the requested revision, filters
explicit matches in repository order, and validates every returned Run.

Implemented CLI surfaces are:

```text
neural run add --revision-id REVISION_UUID ...
neural run list
neural run show RUN_UUID
neural revision runs REVISION_UUID
```

Run list and show output render the revision ID or `-` when absent.

## Explicit non-behavior

The relation does not implement automatic active-revision selection,
Run-to-PlaybookRevisionApplication binding, Playbook materialization, revision content execution,
an execution engine, service/CLI Run idempotency, semantic replay, content deduplication across
fresh UUIDs, mixed or partial revision execution, multiple revisions per Run, automatic
activation/application, per-Knowledge contribution attribution, causal improvement, automatic
learning, or Consigliere integration.

The persistence contract adds no update, delete, replace, versioning, migration, repair, backup,
transaction, generalized crash-recovery, tamper-proofing, cryptographic integrity, or protection
from direct filesystem mutation. No other record automatically creates a Run. Saving one
explicitly supplied Run creates no automatic additional Run, Evaluation, DecisionAction, Outcome,
Review, Experience, Knowledge, or evolution record.

## Typical transitions

`PlaybookRun` → `PlaybookEvaluation`

---

# PlaybookEvaluation

## Responsibility

A PlaybookEvaluation records the assessment of a completed or assessable playbook run.

## Owns

- run reference,
- evaluation result,
- evidence or rationale where modeled,
- identity.

## Must not own

- playbook execution,
- revision persistence,
- evolution proposal application.

## Invariants

- Evaluation targets a specific run.
- `run_id` is the exact persisted relation to that Run.
- Evaluation semantics are explicit.
- Evaluation does not silently mutate a playbook.

Through `PlaybookEvaluation.run_id → PlaybookRun(revision_id?, playbook_id) →
Playbook.knowledge_ids`, an Evaluation provides durable feedback at Playbook and declared
Knowledge-set scope and preserves explicit optional revision provenance transitively. The
Evaluation schema does not store a revision ID directly. It does not attribute an outcome to one
Knowledge item or prove causal or comparative improvement. Under supported create-once Revision
writes, the transitive Revision UUID retains stable payload meaning going forward; Evaluation
does not snapshot that payload or prove pre-hardening history.

## Typical transitions

`PlaybookEvaluation` → `EvolutionProposal`

---

# EvolutionProposal

## Responsibility

An EvolutionProposal expresses a controlled suggestion for changing a playbook based on evaluation evidence.

## Owns

- exact target `playbook_id`,
- exact source `evaluation_ids`,
- proposed change,
- rationale,
- lifecycle state where modeled,
- identity.

## Must not own

- direct mutation of the playbook,
- revision persistence implementation,
- approval side effects outside application services.

## Invariants

- Proposal provenance is preserved.
- At least one Evaluation ID is required.
- `EvolutionProposalService` verifies that every referenced Evaluation exists and that its Run
  belongs to the target Playbook through the validated Run reader.
- Exact `evaluation_ids → PlaybookEvaluation.run_id → PlaybookRun.revision_id?` relations preserve
  optional revision provenance transitively; EvolutionProposal does not store a revision ID
  directly. Under supported create-once Revision writes, a present transitive UUID retains stable
  payload meaning going forward; the Proposal stores no Revision payload snapshot and proves no
  pre-hardening history.
- Proposal and applied revision are distinct concepts.
- Public behavior changes require architectural review.

## Typical transitions

`EvolutionProposal` → `PlaybookRevision`

---

# PlaybookRevision

## Responsibility

A PlaybookRevision is an immutable candidate snapshot of explicitly supplied revised Playbook
content. It is linked to one existing Playbook and one accepted EvolutionProposal.

## Owns

- playbook reference,
- revised content and metadata,
- source proposal reference,
- identity.

## Must not own

- repository navigation,
- unrelated playbook service responsibilities,
- infrastructure-specific persistence behavior.
- activation state,
- application state.

## Lifecycle boundary

Creating a revision does not mutate the Playbook, apply the proposal, activate the revision, or
perform automatic evolution. Activation and application are represented by separate immutable
records.

A frozen top-level model expresses immutable domain intent but does not deeply freeze nested list
fields. Under supported repository writes, one Revision UUID binds to one complete validated
modeled payload. Complete equality includes every modeled scalar and ordered collection. An
identical same-ID replay preserves existing bytes; any different same-ID payload conflicts without
overwrite. The same content under a new UUID remains a distinct valid Revision.

Valid old JSON remains readable without migration. The guarantee is prospective: pre-hardening
payload history cannot be proven retroactively, and direct filesystem mutation remains
out-of-band corruption. Revision is not tamper-proof, cryptographically immutable, versioned, or
snapshotted into a Run. No content hash, historical reconstruction, repair, edit, update, delete,
correction, or supersession lifecycle is added.

A PlaybookRun may independently carry zero or one caller-supplied `revision_id`. A supplied
relation declares that exact immutable revision content was used; omission makes no
revision-specific claim. Revision selection, activation, or application intent never supplies or
proves this Run relation.

Any Knowledge provenance retained by the parent Playbook or revised content remains UUID-based.
Supported create-once Knowledge repository writes give those exact IDs stable payload meaning
going forward; PlaybookRevision does not embed or snapshot Knowledge, add Knowledge versioning, or
provide cryptographic or filesystem tamper evidence.

## Confirmed application rule

`PlaybookRevisionService.list_for_playbook(UUID)` owns revision navigation for a playbook.
`PlaybookRunService.list_for_revision(UUID)` separately owns reverse navigation from one revision
to Runs that explicitly declare it.

The repository port remains persistence-focused and should not gain a broad `find_by_playbook_id` method solely to move application navigation into persistence.

`PlaybookRevisionService.add()` remains fresh-ID and non-idempotent. It exposes no replay or
replacement use case.

## Invariants

- Revision identity is explicit.
- Parent playbook identity is explicit.
- Provenance to proposal is preserved.
- Revision creation does not change proposal status.
- Revision creation does not apply proposal changes.

---

# PlaybookRevisionActivation

## Responsibility

A PlaybookRevisionActivation is a separate immutable lifecycle and audit record for an explicit
manual or external-system decision about one PlaybookRevision.

Supported decisions are:

- `active`,
- `superseded`,
- `rejected`.

Activation does not imply application. It does not materialize revision content into a Playbook,
mutate a Playbook or PlaybookRevision, change EvolutionProposal status, apply a proposal, or
perform automatic evolution.

Activation also does not imply execution. PlaybookRun revision provenance is supplied explicitly
by the Run caller and is never selected from current or historical activation state. A revision
does not need to be active for a caller to declare truthfully that its content was used.

The activation record's exact `revision_id` retains stable Revision payload meaning going forward
under supported create-once repository writes. The record does not snapshot Revision content,
mutate it, or prove pre-hardening payload history.

## Application ownership

`PlaybookRevisionActivationService` owns read-only lifecycle navigation by Playbook,
PlaybookRevision, and EvolutionProposal. It also owns canonical active-revision derivation through:

```python
PlaybookRevisionActivationService.get_active_revision_for_playbook(playbook_id)
```

Activation records are replayed in repository order only inside this service. Consumers must
delegate active-revision resolution rather than duplicate lifecycle replay.

Each relation-list method verifies its source entity, loads all activation records through
`PlaybookRevisionActivationRepository.load_all()`, filters in the application layer, and preserves
repository order. No relation-specific repository query methods are added.

## Current CLI

Read-only lifecycle inspection exists through:

```text
neural playbook revision-history PLAYBOOK_UUID
neural playbook active-revision PLAYBOOK_UUID
neural revision activation-history REVISION_UUID
neural revision runs REVISION_UUID
neural proposal activation-history PROPOSAL_UUID
```

`neural revision runs` is execution-provenance navigation through `PlaybookRunService`; unlike the
other commands in this list, it does not inspect lifecycle records.

Explicit lifecycle decisions can be recorded through:

```text
neural revision activate ...
neural revision supersede ...
neural revision reject ...
```

These write only PlaybookRevisionActivation records.

---

# PlaybookRevisionApplication

## Responsibility

A PlaybookRevisionApplication is an immutable application-intent and audit record. The current
foundation records that an active revision reached an explicit application boundary; it does not
materialize or copy revision content into a Playbook.

Current fields are:

```text
id
applied_at
playbook_id
revision_id
proposal_id
reason
applied_by
notes
tags
source_activation_id
idempotency_key
content_changed
```

`content_changed` defaults to `False`.

## Current foundation

The implemented vertical-slice foundation includes:

- the `PlaybookRevisionApplication` domain model,
- `PlaybookRevisionApplicationRepository`,
- `JsonPlaybookRevisionApplicationRepository`,
- `NeuralPaths.PLAYBOOK_REVISION_APPLICATIONS`,
- container repository and service wiring,
- `PlaybookRevisionApplicationService.add(...)`,
- read-only `list_for_playbook(...)`, `list_for_revision(...)`, and
  `list_for_proposal(...)` navigation.

## Invariants and non-behavior

Creating an application record does not mutate Playbook, PlaybookRevision, EvolutionProposal, or
PlaybookRevisionActivation records. It does not change proposal status, apply a proposal, or
perform automatic evolution. It is not Playbook execution and does not establish or bind
PlaybookRun provenance; `content_changed=False` cannot establish revision-specific execution
provenance.

Conversely, an explicit `PlaybookRun.revision_id` does not require or imply an application record.
Run provenance is never inferred from application intent, and a revision need not be represented
by `PlaybookRevisionApplication` for the Run caller to declare that its content was used.

The application's exact `revision_id` retains stable Revision payload meaning going forward under
supported create-once repository writes. The application record does not snapshot Revision
content, mutate it, or prove pre-hardening payload history.

There is currently:

- no CLI apply command,
- no CLI application-history commands,
- no Playbook content mutation,
- no PlaybookRevision materialization,
- no proposal application,
- no application-specific repository query method.

---

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

---

# DecisionReview

## Responsibility

A DecisionReview is an immutable, append-only authorized interpretation record over one Decision,
one DecisionAcceptance, and an explicit ordered set of DecisionOutcome records. It owns assessment,
findings, candidate lessons, review evidence, and reviewer confidence. It does not own factual
execution results, rewrite outcomes, execute evidence, mutate lifecycle state, create learning
records, or call Consigliere.

## Implemented fields and vocabularies

- `id`
- `recorded_at`
- `decision_id`
- `acceptance_id`
- ordered unique `outcome_ids`
- `reviewed_by`
- `reviewed_at`
- `assessment`
- `summary`
- ordered `findings`
- ordered `candidate_lessons`
- embedded `evidence_references`
- `confidence`
- `idempotency_key`
- normalized `tags`

Assessment is exactly `sound`, `flawed`, `mixed`, or `inconclusive`. Confidence is exactly `low`,
`medium`, or `high`. These are independent of `DecisionOutcomeResult`, whose values remain
`succeeded`, `failed`, `partial`, and `unknown`: a successful outcome can support a flawed review,
and a failed outcome can support a sound review.

## Validation and provenance

- `outcome_ids` is ordered, unique, and non-empty; every outcome must exist and belong to the same
  Decision and acceptance.
- Action IDs are not persisted on a review. Provenance is transitive through
  `DecisionReview → DecisionOutcome[] → DecisionAction[]`.
- `reviewed_by` is trimmed, non-blank, and at most 255 characters; `summary` is trimmed, non-blank,
  and at most 1000 characters. The idempotency key is trimmed and non-blank.
- Findings are required, ordered, trimmed, non-blank, case-insensitively unique, and limited to 100
  entries of at most 1000 characters each.
- Candidate lessons use the same ordering, normalization, uniqueness, count, and length bounds, but
  may be empty. They are not Experience or Knowledge until a separate authorized use case succeeds.
- Tags are trimmed and case-insensitively deduplicated while first-seen order is preserved.
- `recorded_at` and `reviewed_at` must be timezone-aware and are normalized to UTC. Locally,
  `reviewed_at` cannot be later than `recorded_at`; the service also requires it not to precede the
  latest `validated_at` among the explicitly selected outcomes.
- The candidate's local validation occurs before repository reads. Decision, acceptance, outcome,
  cross-record, and time validation all fail closed before a write.

Repository enumeration order never defines review scope or chronology. The caller supplies the
ordered outcome scope, and history is sorted deterministically by `(reviewed_at, review.id)`.

## History, corrections, and idempotency

Multiple reviews are allowed for a Decision, an outcome, or the same ordered outcome set when they
use different idempotency keys. Reassessment and correction append another review. This foundation
has no mutation, replacement, supersession, deletion, or persisted `current` behavior.

Idempotency is scoped by `(decision_id, "decision_review", idempotency_key)`:

- zero matches creates the validated candidate;
- exactly one semantically equivalent match returns the existing review;
- exactly one different match raises `DecisionReviewIdempotencyConflictError` without a write;
- more than one match raises `DecisionReviewIdempotencyAmbiguityError` with the Decision ID, key,
  and match count, without selecting or comparing an arbitrary duplicate and without a write.

Ambiguity is independent of repository enumeration order and applies whether duplicates are
semantically equivalent or different. For the exactly-one-match comparison, semantic payload
excludes generated `id`, generated `recorded_at`, and each evidence reference's `captured_at`; it
includes all caller-supplied fields and preserves the order sensitivity of `outcome_ids`, findings,
candidate lessons, evidence references, and tags.

## Persistence, service, and CLI

`DecisionReviewRepository` exposes exactly `save()`, `load_all()`, and `get_by_id()`.
`JsonDecisionReviewRepository` stores one deterministic, sorted-key JSON file per review under
`NeuralPaths.DECISION_REVIEWS`; `load_all()` sorts filenames and reconstructs records through domain
validation. Brain initialization creates the directory. `Container.decision_review_repository()`
and `Container.decision_review_service()` wire the JSON review repository together with Decision,
acceptance, and outcome repositories.

`DecisionReviewService` implements `add()`, `list_for_decision()`, and `show()`. Its controlled
errors cover missing Decision, acceptance, outcome, or review; acceptance/Decision mismatch;
outcome/Decision or outcome/acceptance mismatch; review before the latest outcome; idempotency
conflict; and duplicate-key ambiguity. Read operations validate persisted relations before
returning records.

The CLI group is `neural decision review` with exact commands `add DECISION_UUID`,
`history DECISION_UUID`, and `show REVIEW_UUID`. Add requires `--acceptance-id`, repeatable
`--outcome-id`, `--reviewed-by`, `--reviewed-at`, `--assessment`, `--summary`, repeatable
`--finding`, `--confidence`, and `--idempotency-key`. Optional repeatable inputs are
`--candidate-lesson`, `--evidence` JSON, and `--tag`. Success prints the stored ID and every field.
History renders `ID`, `Reviewed`, `Reviewed by`, `Assessment`, `Confidence`, `Outcome IDs`, and
`Summary`; its controlled empty message is `No review history found for Decision: ...`. Show
renders every field. Evidence locators are retained but not opened.

## Lifecycle and learning boundary

DecisionReview is orthogonal interpretive history. Saving one never creates Experience. The
separate `ExperienceService.add_from_decision_review()` use case may explicitly copy selected
findings or candidate lessons into one Experience without mutating the Review.
DecisionReview does not affect `DecisionLifecycleService`.
The lifecycle remains exactly `proposed`, `accepted`, `in_progress`, `succeeded`, `failed`,
`partial`, and `outcome_unknown`; no `reviewed` state exists. A review never automatically creates
Observation, Knowledge, Playbook, PlaybookEvaluation, EvolutionProposal, revision records, or
Consigliere work. Promotion remains explicit and a promoted Experience is not Knowledge.

---

# DecisionReview-to-Experience Promotion

## Responsibility and chain

The implemented promotion foundation converts selected immutable DecisionReview interpretation
into one existing `Experience` record only through the explicitly authorized
`ExperienceService.add_from_decision_review(...)` use case:

```text
DecisionReview
→ explicitly promoted Experience
→ separately and explicitly created Knowledge
```

A finding or candidate lesson is not Experience before promotion succeeds. A promoted Experience
is still not Knowledge. Reviewer and promoter are separate authorities and may be different people;
this foundation introduces no RBAC or approval system.

## Durable schema

`Experience` now has one optional field:

```text
decision_review_promotion: DecisionReviewPromotion | None
```

`DecisionReviewPromotion` contains exactly:

```text
decision_review_id
source_statements
promoted_by
promotion_reason
idempotency_key
```

Each ordered `DecisionReviewPromotionSourceStatement` contains exactly:

```text
kind
index
text
```

The source-kind vocabulary is exactly `finding | candidate_lesson`. Durable indexes are zero-based
and non-negative. Source statements are ordered and non-empty, and each `(kind, index)` pair is
unique. Promotion and source-statement values are immutable.

`promoted_by` and `idempotency_key` are trimmed, non-blank, and at most 255 characters;
`promotion_reason` is trimmed, non-blank, and at most 1000 characters. Copied statement text is
trimmed, non-blank, and at most 1000 characters. The service stores the normalized exact immutable
Review item at the selected index; callers and the CLI never supply independent source text.

Plain direct and Observation-derived Experiences retain `decision_review_promotion is None`. A
promotion copies no Decision, DecisionAcceptance, DecisionAction, DecisionOutcome, reviewer,
assessment, confidence, or evidence fields into Experience. Their provenance remains transitive
through the referenced Review.

## Cardinality and corrections

- One promoted Experience references exactly one DecisionReview.
- One promoted Experience selects one or more ordered statements from that Review.
- One DecisionReview may produce multiple Experiences.
- One source statement may be promoted repeatedly under different idempotency keys.
- One promoted Experience cannot combine multiple DecisionReviews.

Corrections append another Experience under a different key. There is no replacement,
supersession, deletion, status, ranking, scoring, or current/best promotion behavior.

## Explicit application and read integrity

`ExperienceService.add_from_decision_review(...)` performs this sequence:

1. validate the non-empty, unique, non-negative caller selectors and normalize bounded promotion
   authority metadata;
2. call the existing validated `DecisionReviewService.show(review_id)` boundary;
3. validate each ordered finding or candidate-lesson index and copy exact Review text;
4. validate optional Observation references through the existing behavior;
5. construct one promoted Experience;
6. scan `ExperienceRepository.load_all()` for the scoped idempotency key;
7. save exactly one Experience only after every validation and idempotency check.

Validation failure, conflict, or ambiguity performs no write. The service creates no second link
record and performs no transaction emulation.

Equivalent replay validates the existing promoted Experience before returning it. `get_by_id()`,
the complete Experience list, and the Observation-linked Experience list also revalidate promoted
records. Validation calls the referenced Review's existing `show()` boundary, which revalidates its
persisted Decision, acceptance, outcome, and time relations, then checks selector bounds and exact
copied text. Missing or malformed provenance fails closed without repair or skipping. Plain
Experience reads are unaffected; Observation-linked listing validates only returned linked records.

## Idempotency

Promotion idempotency is application-layer policy scoped by:

```text
(decision_review_id, "review_experience_promotion", idempotency_key)
```

| Matches | Implemented behavior |
| ---: | --- |
| 0 | Save and return one promoted Experience. |
| 1 equivalent | Return the existing Experience with its original ID and timestamp; no write. |
| 1 conflicting | Raise `DecisionReviewPromotionIdempotencyConflictError`; no write. |
| More than 1 | Raise `DecisionReviewPromotionIdempotencyAmbiguityError`; do not select or compare an arbitrary duplicate; no write. |

Ambiguity is independent of repository enumeration order. Semantic equivalence excludes only
generated `Experience.id` and `Experience.timestamp`. It includes every caller-supplied Experience
field, optional Observation IDs, tags, and every ordered promotion field, including copied text,
promoter, reason, and key.

## Persistence compatibility

`ExperienceRepository` remains limited to `save()`, `load_all()`, and `get_by_id()`; scanning and
relation policy remain in the application layer. Existing `JsonExperienceRepository` already
round-trips plain and promoted records through domain validation under `NeuralPaths.EXPERIENCES`.
Old JSON without `decision_review_promotion` remains valid and loads with `None`.

No migration, inferred provenance, second write, separate aggregate, repository, adapter, path, or
Brain collection was introduced. The production adapter required no rewrite.

## CLI and boundaries

The implemented command is `neural experience from-review REVIEW_UUID`. It requires repeatable
ordered `--source KIND:ORDINAL`, `--promoted-by`, `--promotion-reason`, `--idempotency-key`,
`--title`, `--context`, `--action`, `--outcome`, and `--result`. Optional repeatable inputs are
`--observation-id` and `--tag`.

For example, `--source finding:1 --source candidate_lesson:2` uses one-based user ordinals and is
converted deterministically to durable indexes `0` and `1`. Invalid syntax, kind, non-positive
ordinal, Review, source index, Observation, conflict, ambiguity, or persisted integrity renders a
controlled error. Success and equivalent replay render the stored Experience identity and complete
promotion provenance, including user ordinal, stored index, copied text, actor, reason, and key.

Ordinary `neural experience add`, `from-observation`, `list`, `show`, `knowledge`, and
`neural observation experiences` retain their existing inputs and behavior. Ordinary creation does
not require promotion data or an idempotency key.

Promotion changes no canonical Decision lifecycle state and adds no `reviewed`, `promoted`, or
`learned` state. It creates no Knowledge, Playbook, PlaybookEvaluation, EvolutionProposal,
revision, evidence execution, automatic learning, or Consigliere work. `DecisionReview.assessment`,
`DecisionOutcome.result`, and `Experience.result` remain distinct meanings. A later explicit
Knowledge generalization uses the existing generic Knowledge commands and validated Experience
reader boundary; `neural experience knowledge` remains read-only navigation. Durable
Playbook-scoped Knowledge use and Run feedback already exist. Knowledge-specific causal
attribution, durable retrieval or recommendation events, and demonstrated improvement remain
unsupported. Optional revision-specific Run provenance exists only as an explicit caller-supplied
Run relation and remains transitive through exact downstream Run IDs.

---

# Application Services

## Responsibility

Application services coordinate use cases across domain objects and ports.

They own orchestration, not persistence implementation or user-interface rendering.

## Required properties

Every application service should:

- expose one coherent responsibility,
- depend on ports rather than concrete adapters,
- preserve domain validation order,
- coordinate provenance explicitly,
- remain testable without CLI, database, filesystem, or network,
- avoid constructing dependencies internally,
- return domain/application results rather than rendered text.

## Service boundary rules

A service may:

- load entities through repository ports,
- invoke domain behavior,
- coordinate multiple domain objects,
- persist results through ports,
- raise explicit application errors,
- compose relationship navigation.

A service must not:

- instantiate repositories,
- import CLI modules,
- render Rich tables,
- parse command-line strings,
- depend on concrete SQL/filesystem adapters,
- silently change public behavior,
- absorb unrelated use cases.

## Public method design

Prefer explicit methods named after use cases.

Good:

```python
revision_service.list_for_playbook(playbook_id)
```

Avoid generic, ambiguous methods:

```python
service.process(data)
service.handle(value)
```

## Service growth rule

When a service gains unrelated responsibilities, split by use case or domain ownership.

Do not split merely to reduce line count. Split when reasons to change diverge.

## Revision lifecycle ownership

`PlaybookRevisionActivationService` owns active-revision derivation through
`get_active_revision_for_playbook(playbook_id)`.

`PlaybookRevisionApplicationService.add(...)` validates the Playbook, revision, accepted proposal,
relation consistency, optional source activation, and current active revision before saving one
application audit record. It delegates active-revision resolution to the activation service.

Its relation-list methods verify the source entity, load all application records, filter in the
application layer, preserve repository order, and perform no mutation.

## PlaybookRevision persistence boundary

`PlaybookRevisionService.add()` retains normal fresh-ID, non-idempotent creation. It validates the
Playbook, accepted proposal, required ordered content, and Knowledge relations, constructs one new
Revision, and delegates persistence. It does not compare stored payloads or implement filesystem
publication.

The `PlaybookRevisionRepository` port owns create-once persistence. An absent UUID is created
without replacement, an identical complete same-ID replay succeeds without rewriting bytes, and a
different same-ID payload conflicts without overwrite. Stored-data and identity-mismatch failures
propagate through application services. Existing affected CLI handlers render the base repository
error as controlled exit-code-1 output; no command, option, or normal success output changed.

No Revision update, replace, edit, delete, repair, replay, version, or supersession service exists.
Activation and application remain separate immutable records and do not mutate Revision.
`PlaybookRunService` remains the owner of optional caller-supplied Revision execution provenance;
it does not consult activation or application state and adds no automatic selection or
Run-to-application binding.

## PlaybookRun persistence boundary

`PlaybookRunService.add()` retains ordinary fresh-identity creation. After validating actions, the
base Playbook, and any explicitly supplied same-Playbook Revision, it constructs a `PlaybookRun`
whose UUID and timestamp use the model defaults and delegates one save. `neural run add` exposes
that service behavior. Neither surface accepts a caller-supplied Run UUID or performs semantic
replay or content deduplication.

The `PlaybookRunRepository` port separately owns exact create-once persistence. It creates an
absent UUID without replacement, accepts an identical complete same-ID modeled replay without
rewriting the file, and rejects a different same-ID payload without overwrite. Stored-data and
identity-mismatch failures are visible; the repository does not repair or skip invalid records.
This source checkpoint adds no dedicated PlaybookRun repository-error mapping to the CLI.

No Run update, replace, delete, migration, repair, versioning, content-level idempotency, or replay
service exists. No other record automatically creates a Run. Repository exact replay creates no
additional Run, Evaluation, DecisionAction, Outcome, Review, Experience, Knowledge, or evolution
record. Optional `revision_id` semantics are unchanged: the caller supplies it explicitly,
omission makes no revision claim, and neither activation, application, timestamps, tags, nor
repository order may infer it.

## Development evidence orchestration ownership

`DevelopmentEvidenceService` coordinates one specialized local prompt/review/commit bundle. It
depends on `DevelopmentEvidenceSource` and the existing Decision, acceptance, action, outcome,
review, and Experience services. It does not depend on the local adapter directly and does not
persist its frozen `DevelopmentEvidenceCandidate`.

`preview()` reads and correlates source facts, classifies validation-tree strength, creates bounded
`EvidenceReference` values, validates the complete caller-supplied semantic payload locally, and
returns a side-effect-free candidate. Source facts and review outcome remain evidence claims;
caller interpretation and `DecisionOutcome.result` remain explicit caller semantics.

`apply()` first requires explicit authority confirmation, then calls `preview()` again and compares
fresh source facts with the candidate. Stale evidence fails before the first durable service call.
Only then does it delegate in dependency order:

```text
DecisionService
→ DecisionAcceptanceService
→ DecisionActionService
→ DecisionOutcomeService
→ DecisionReviewService
→ optional ExperienceService.add_from_decision_review()
```

The replay identity is `NeuralEngine:<full commit SHA>`, and the service derives the per-record
idempotency key. Exact replay resumes through existing service idempotency; changed evidence or
semantics conflicts. The sequence is resumable but non-transactional and provides no rollback.
It never creates Observation, Knowledge, Playbook-family, persisted evidence, or persisted
candidate records.

## Decision service ownership

`DecisionService.add()` creates an immutable candidate, validates referenced Observations and an
optional same-project superseded Decision, then performs idempotency detection through repository
`load_all()` and application-layer filtering. Its scope is
`(project_key, "decision", idempotency_key)`; no repository query method exists.

An equivalent replay returns the existing Decision. Reusing the same key with a different semantic
payload fails visibly without writing. Generated Decision identity and timestamps, including
embedded `EvidenceReference.captured_at`, are excluded from semantic comparison.

`list_decisions()` preserves repository order and may filter by a non-blank project key in the
application layer. `show()` owns the explicit not-found behavior. No lifecycle transition,
automatic learning, or downstream record creation is part of this service.

## Decision acceptance service ownership

`DecisionAcceptanceService.accept()` validates Decision existence, constructs an immutable
candidate, and uses `DecisionAcceptanceRepository.load_all()` for idempotency and first-acceptance
eligibility. The scope is `(decision_id, "decision_acceptance", idempotency_key)`. Equivalent
semantic replay returns the existing record; conflicting reuse of the key and a distinct second
acceptance both fail visibly without writing.

`list_for_decision()` verifies the Decision, filters acceptance records in the application layer,
and preserves repository order. `show()` owns explicit acceptance not-found behavior. Acceptance
does not mutate Decision or create actions, outcomes, reviews, execution, or learning.

## Decision action ownership

`DecisionActionService.add()` validates the Decision, matching acceptance, and optional
PlaybookRun before creating an immutable action. It uses
`(decision_id, "decision_action", idempotency_key)` for application-layer idempotency, permits
multiple distinct actions, and mutates no related record. PlaybookRun and Playbook expose no
`project_key`, so the service can validate only run existence without a schema change.

`list_for_decision()` validates the Decision, filters `load_all()` in repository order, and
`show()` owns explicit action-not-found behavior. The service creates no Outcome, Review, or
learning record.

## Playbook-scoped Knowledge use and feedback ownership

`KnowledgeService` still owns evidence validation and creation. It validates Experience evidence,
constructs the complete Knowledge value, and delegates persistence through `KnowledgeRepository`;
it does not compare stored payloads or implement filesystem publication.

The repository port owns create-once persistence semantics, and `JsonKnowledgeRepository`
enforces them. An absent UUID is created once, an identical complete same-ID replay succeeds
without rewrite, and a different same-ID payload conflicts without writing. Stored-data and
identity mismatch failures propagate through the service. Knowledge-related CLI handlers only
render `KnowledgeRepositoryError` as controlled exit-code-1 output; no command, option, or success
behavior changed.

`PlaybookService.add()` requires at least one exact Knowledge UUID and validates every supplied
Knowledge relation before saving the caller-defined Playbook.

`PlaybookRunService.add()` validates and records the caller's declaration that the exact Playbook
was manually or externally applied and may accept one explicit `revision_id`. Its write order is:

1. require actions;
2. require the base Playbook;
3. require a supplied revision to exist;
4. require that revision to belong to the same Playbook;
5. construct and save the Run.

No failure path writes. Omission performs no revision lookup and makes no revision-specific claim.
`get_by_id()`, the complete and Playbook-scoped lists, and `list_for_revision()` validate linked
revision existence and same-Playbook ownership. Corrupt linked provenance fails closed; legacy
Runs remain valid. Revision navigation validates its source revision, filters explicit matches in
repository order, and validates every result.

The caller is the sole authority for the optional factual relation. The service never consults or
infers from active revision, activation history, timestamps, repository order,
`PlaybookRevisionApplication`, or application-intent records. A revision need not be active or
applied. `PlaybookEvaluationService.add()` validates and evaluates one exact Run.

`EvolutionProposalService.add()` persists the target `playbook_id` and exact `evaluation_ids`.
Before saving, it loads every Evaluation and its Run and rejects any Run whose `playbook_id` does
not equal the target Playbook. This preserves:

```text
PlaybookEvaluation.run_id
→ PlaybookRun(revision_id?, playbook_id)
→ Playbook.knowledge_ids
→ Knowledge.id
```

`DecisionActionService.add()` validates an optional exact PlaybookRun relation.
`DecisionOutcomeService.add()` validates exact DecisionAction IDs, enabling the optional path:

```text
DecisionOutcome.action_ids
→ DecisionAction.playbook_run_id?
→ PlaybookRun(revision_id?, playbook_id)
→ Playbook.knowledge_ids
```

`PlaybookEvaluationService`, `EvolutionProposalService`, and `DecisionActionService` consume the
narrow validated `PlaybookRunReader.get_by_id()` boundary. Their schemas do not store a revision
ID directly; existing exact Run relations preserve optional revision provenance transitively.
No service attributes an outcome to one Knowledge item, persists retrieval or recommendation
events, infers provenance, or performs automatic learning or evolution.

## Decision outcome and lifecycle ownership

`DecisionOutcomeService.add()` validates the Decision, matching acceptance, one or more unique
actions, each action's Decision and acceptance relations, and validation time against the earliest
linked action start before constructing or saving an immutable outcome. It uses
`(decision_id, "decision_outcome", idempotency_key)` for application-layer idempotency. Zero
matches creates normally; exactly one equivalent match returns the existing outcome; exactly one
different match conflicts. More than one persisted scoped match raises
`DecisionOutcomeIdempotencyAmbiguityError`, regardless of payload equivalence or repository order,
without selecting a duplicate or writing. Another key may append another outcome for the same
Decision.

`list_for_decision()` validates the Decision and returns all matching outcomes in repository order.
`show()` owns explicit outcome-not-found behavior. `summary_for_decision()` validates persisted
outcome relations and returns an immutable, non-persisted `DecisionOutcomeSummary` with outcome
count, deterministic latest result/time, distinct linked-action count, counts by result, and
success/failure presence. Latest selection uses `(validated_at, outcome.id)` rather than repository
order.

`DecisionLifecycleService` is the only canonical projection owner. It validates persisted
Decision/acceptance/action/outcome relations and derives exactly `proposed`, `accepted`,
`in_progress`, `succeeded`, `failed`, `partial`, or `outcome_unknown`. When outcomes exist, the
latest is selected by `(validated_at, outcome.id)`. It writes no status and exposes no generic
`completed`, `resolved`, or reviewed state. Outcome creation and projection create no Review or
learning record.

## Decision review ownership

`DecisionReviewService.add()` first constructs the immutable candidate, then validates Decision,
matching acceptance, every explicit ordered outcome relation, and that `reviewed_at` is not earlier
than the latest referenced outcome validation. It writes only after all validation. The scope is
`(decision_id, "decision_review", idempotency_key)`: zero matches creates, exactly one equivalent
match replays, and exactly one different match raises `DecisionReviewIdempotencyConflictError`.
More than one match raises `DecisionReviewIdempotencyAmbiguityError` with identifying details,
independent of repository order and duplicate payload equivalence, without arbitrary selection,
semantic comparison against a selected duplicate, or a write.

Semantic comparison for the exactly-one-match case excludes generated review ID and recording
time plus evidence capture times. It includes ordered outcome IDs, findings, candidate lessons,
evidence, tags, and every other caller-supplied semantic field, so ordered collections remain order
sensitive. `list_for_decision()` validates the Decision and every persisted review relation, then
sorts by `(reviewed_at, review.id)`. `show()` validates persisted relations and owns explicit
review-not-found behavior.

Multiple reviews may cover one Decision, one outcome, or the same ordered outcome set under
different keys. Corrections append; the service has no replacement, supersession, deletion, or
`current` behavior. It creates no Experience, Knowledge, Playbook, proposal, or Consigliere work
and does not participate in `DecisionLifecycleService`.

The DecisionOutcome and DecisionReview duplicate-key rules are the same reusable fail-closed
application-service invariant: more than one persisted match for a scoped key is corruption or
ambiguity to surface, never an ordering problem to resolve by choosing the first record. Their
scopes and controlled ambiguity error types remain separate.

## DecisionReview-to-Experience promotion ownership

`ExperienceService.add_from_decision_review(...)` is the one implemented explicit promotion use
case. It validates selectors and bounded promoter/reason/key metadata before relation reads, calls
the existing validated `DecisionReviewService.show(review_id)` boundary, validates ordered finding
and candidate-lesson indexes, copies exact Review text, validates optional Observation IDs,
constructs one Experience, then loads Experiences for application-layer idempotency. Only a fully
validated zero-match candidate is saved.

The scope is `(decision_review_id, "review_experience_promotion", idempotency_key)`. Exactly one
equivalent match returns the original Experience identity and timestamp without writing; exactly
one different match raises `DecisionReviewPromotionIdempotencyConflictError`; more than one match
raises `DecisionReviewPromotionIdempotencyAmbiguityError` without repository-order selection or
arbitrary semantic comparison. Semantic equivalence excludes only generated Experience ID and
timestamp and includes every caller-supplied Experience and ordered promotion field.

Equivalent replay validates the existing provenance. `get_by_id()`, `list_experiences()`, and
`list_for_observation()` also fail closed for promoted records when the Review graph is invalid, an
index is out of range, or copied text differs. Plain Experience reads remain unaffected. Direct and
Observation-derived `add` paths keep their existing inputs and do not acquire idempotency or
promotion requirements.

One Review may produce multiple Experiences under different keys, and the same statement may be
promoted repeatedly. Each Experience references only one Review. Corrections append; no promotion
replacement, ranking, deletion, lifecycle state, Knowledge creation, or Consigliere behavior is
owned here.

## Knowledge-to-Experience integrity ownership

`KnowledgeService` keeps its existing public methods:

```text
add()
add_from_experience()
list_knowledge()
list_for_experience()
get_by_id()
```

It depends on `KnowledgeRepository` plus a narrow application-facing `ExperienceReader` protocol
that exposes only `get_by_id()`. `ExperienceService` implements that reader, and its
`get_by_id()` remains the single owner of persisted DecisionReview-promotion provenance
validation. KnowledgeService does not depend on `ExperienceRepository`, inspect promotion fields,
load DecisionReview directly, or translate canonical DecisionReview and promotion errors.

`add()` rejects an empty Experience ID list before any relation read. It validates supplied IDs in
caller order through the reader, preserves order and duplicates, constructs Knowledge only after
all reads succeed, and then saves once. `add_from_experience()` validates its one source through
the same reader and performs no save for a missing or corrupt source.

`list_knowledge()` validates every relation of every loaded record in repository and relation
order, then returns the complete list; it does not skip, repair, filter, or partially return
invalid records. `get_by_id()` performs no Experience read for an absent Knowledge item and
validates every relation of a present item. `list_for_experience()` validates the requested
Experience first, filters in repository order, validates every relation of every matching record,
and deliberately does not validate unrelated Knowledge records.

Missing Experience relations retain `ExperienceNotFoundError`. Existing `DecisionReviewError` and
`DecisionReviewPromotionError` instances propagate unchanged. The validation guarantee is exactly
the existing `ExperienceService.get_by_id()` contract, including Review graph, selector, and
copied-text integrity; it does not recursively revalidate every Observation or DecisionAction
relation. One validated Experience read occurs per stored relation, including duplicates. This
linear fail-closed cost is accepted; no caching, batching, or deduplication is implemented.

---

# Application Errors

## Purpose

Application errors communicate expected use-case failures across layer boundaries.

## Rules

- Use explicit error types.
- Include stable contextual identifiers.
- Preserve the original cause when wrapping infrastructure errors.
- Keep rendering outside the error type.
- Avoid leaking adapter-specific exception classes into CLI.

Good:

```python
raise PlaybookNotFoundError(playbook_id)
```

Avoid:

```python
raise Exception("something failed")
```

## Mapping

- Domain violations remain domain errors.
- Missing application resources use application errors.
- Infrastructure failures are translated at adapter/application boundaries.
- CLI maps application errors to user-facing messages and exit codes.

## Neural home selection errors

`NeuralHomeError` is the bounded resolver and availability error for `NEURAL_HOME`, default-root,
and Brain preflight failures. Its stable reasons are:

```text
invalid_configuration
home_unavailable
home_not_directory
home_inaccessible
brain_uninitialized
brain_unavailable
```

The CLI renders these expected failures as human-readable exit-code-1 messages without a
traceback. Invalid or unavailable overrides identify the configured or resolved selection and
state that no fallback was used. Rendering may expose those exact diagnostic paths, but not the
full environment, unrelated variables, record contents, credentials, mount catalogs, or home
directory listings. No general JSON error envelope is introduced.

`neural status` uses the same reason boundary but remains read-only and reports the unavailable
selection as status fields. Normal override commands fail during root/Brain preflight before the
container or service is invoked.

## Development evidence errors

The local source adapter distinguishes invalid, missing, insufficient, and unsupported evidence.
The application orchestrator distinguishes correlation mismatch, missing apply authority, stale
source facts, and conflicting durable replay. Existing Decision-family idempotency conflicts are
translated to the development-evidence conflict category without being hidden.

Both `neural development-evidence preview` and `neural development-evidence apply` render these
expected failures as controlled exit-code-1 messages without tracebacks. Rejection happens before
writes for invalid topology, mismatch, absent authority, or stale evidence. A conflict after an
earlier successful service call remains a visible non-transactional partial apply.

## Knowledge-to-Experience integrity errors

KnowledgeService retains `ExperienceNotFoundError` for missing Experience relations. It propagates
existing `DecisionReviewError` and `DecisionReviewPromotionError` instances unchanged when
`ExperienceService.get_by_id()` finds corrupt promoted ancestry. It does not wrap them or create a
parallel Knowledge-specific taxonomy.

The CLI renders controlled nonzero failures without tracebacks for:

```text
neural knowledge add
neural knowledge from-experience
neural knowledge list
neural knowledge show
neural experience knowledge
```

## Knowledge persistence integrity errors

The repository port exposes `KnowledgeRepositoryError` with three distinct failures:

- `KnowledgePersistenceConflictError` for a same-ID different-payload collision;
- `KnowledgeStoredDataError` for malformed or invalid stored Knowledge;
- `KnowledgeIdentityMismatchError` when the requested or filename UUID differs from embedded
  `Knowledge.id`.

These errors preserve visible create-once failures across the application boundary. Knowledge
services do not repair, overwrite, skip, or silently substitute persisted data. Existing
Knowledge-related CLI handlers render the repository error message and exit with code 1 without a
traceback; no commands or options were added.

## PlaybookRevision persistence integrity errors

The repository port exposes `PlaybookRevisionRepositoryError` with three distinct failures:

- `PlaybookRevisionPersistenceConflictError` for a same-ID different-payload collision;
- `PlaybookRevisionStoredDataError` for malformed or invalid stored Revision data or a non-UUID
  filename stem;
- `PlaybookRevisionIdentityMismatchError` when the requested or filename UUID differs from the
  embedded `PlaybookRevision.id`.

These errors fail visibly without overwrite, repair, skipping, or substitution. Existing affected
Revision, Run, Evaluation, Proposal, activation, Knowledge-navigation, and DecisionAction CLI
paths render the repository error message and exit with code 1 without a traceback. No command or
option was added, and normal success output is unchanged.

## PlaybookRun persistence integrity errors

The repository port exposes `PlaybookRunRepositoryError` with three distinct failures:

- `PlaybookRunPersistenceConflictError` for a same-ID different-payload collision;
- `PlaybookRunStoredDataError` for malformed or invalid stored Run data or a non-UUID filename
  stem;
- `PlaybookRunIdentityMismatchError` when the requested or filename UUID differs from the embedded
  `PlaybookRun.id`.

These failures preserve the existing file and do not repair, overwrite, skip, or substitute
stored data. They are repository contract errors, not a new application idempotency taxonomy.
The committed checkpoint adds no dedicated CLI mapping for this error family.

---

# Ports

## Responsibility

Ports define the contracts required by the application layer from external systems.

## Port design rules

A port must:

- describe application needs, not adapter capabilities,
- use domain/application types,
- avoid database-specific concepts,
- remain minimal,
- have behaviorally meaningful method names,
- be mockable or replaceable in tests.

A port must not expose:

- SQL,
- ORM sessions,
- filesystem paths unless the application concept requires them,
- HTTP response objects,
- CLI rendering concerns,
- concrete adapter classes.

## Change policy

Changing a port is architectural work.

A port change requires:

- Codex GPT-5.5 medium,
- review of all implementations,
- review of service call sites,
- updated contract tests,
- full validation.

## Development evidence source boundary

`DevelopmentEvidenceSource` is a narrow read port, not a repository. Its single `read()` operation
accepts one repository root, one repository-relative prompt, one repository-relative review, and
one exact full commit SHA, then returns bounded `DevelopmentEvidenceSnapshot` facts.

The port does not search, watch, persist, approve, authenticate, execute validation, or expose a
generic file/Git client. Application correlation and authority remain outside the port.

## Narrow application reader boundary

`ExperienceReader` is defined beside `KnowledgeService` because it describes one application
service's validated read need rather than a persistence contract. It exposes only:

```text
get_by_id(experience_id)
```

`ExperienceService` satisfies the protocol structurally. The protocol prevents KnowledgeService
from depending on the broader raw `ExperienceRepository` surface or duplicating promoted
Experience validation. No repository port changed for this boundary.

## Validated PlaybookRun reader boundary

`PlaybookRunReader` is defined beside `PlaybookRunService` and exposes only:

```text
get_by_id(run_id)
```

`PlaybookRunService` satisfies it structurally and remains the canonical owner of persisted
Run-to-Revision integrity validation. PlaybookEvaluation, EvolutionProposal, and DecisionAction
services use this boundary instead of a raw `PlaybookRunRepository`, so revision-linked corruption
fails closed without expanding the persistence port.

---

# Repository Ports

## Responsibility

Repository ports define persistence operations needed by application services.

## Allowed operations

Typical operations include:

- add/save,
- get by identity,
- list,
- delete when domain policy allows it,
- narrowly justified persistence queries.

## Forbidden expansion

Do not add repository methods merely because a relationship exists.

First ask whether the application service can compose the navigation from existing persistence operations.

Development-evidence dogfooding adds no evidence or candidate repository port. Durable apply
continues through the existing Decision-family and Experience repository contracts; the
non-persisted candidate and source snapshot have no save, load, query, lifecycle, or approval
surface.

Confirmed rule:

`PlaybookRevisionService.list_for_playbook(UUID)` owns playbook revision navigation.

`PlaybookRevisionRepository` remains limited to `save()`, `load_all()`, and `get_by_id()`.
Its `save()` contract is create-once: create an absent Revision UUID without replacement, accept
an identical complete same-ID replay as a byte-preserving no-op, and reject a different same-ID
payload as `PlaybookRevisionPersistenceConflictError` without writing.
`PlaybookRevisionRepositoryError` is the base persistence failure category;
`PlaybookRevisionStoredDataError` identifies malformed or invalid stored data and non-UUID
filename stems, while `PlaybookRevisionIdentityMismatchError` identifies filename/request versus
embedded UUID disagreement. A missing `get_by_id()` returns `None`. Relation filtering and normal
fresh-ID creation remain application-service responsibilities.

`PlaybookRevisionApplicationRepository` remains limited to `save()`, `load_all()`, and
`get_by_id()`. Navigation by Playbook, PlaybookRevision, or EvolutionProposal is composed by
`PlaybookRevisionApplicationService`; no relation-specific query methods are part of the port.

`DecisionRepository` is likewise limited to `save()`, `load_all()`, and `get_by_id()`.
Project filtering and idempotency detection belong to `DecisionService`; no project or idempotency
query method is part of the port.

`DecisionAcceptanceRepository` is also limited to `save()`, `load_all()`, and `get_by_id()`.
Decision relation filtering, eligibility, and idempotency belong to
`DecisionAcceptanceService`; no relation, project, or idempotency query method is part of the port.

`DecisionActionRepository` is limited to `save()`, `load_all()`, and `get_by_id()`.
Relation validation, Decision filtering, idempotency, and lifecycle projection belong to
application services; no relation, idempotency, or lifecycle query method is part of the port.

`DecisionOutcomeRepository` is limited to `save()`, `load_all()`, and `get_by_id()`.
Decision filtering, acceptance/action relation validation, multiple-outcome history, idempotency,
summary derivation, and lifecycle projection belong to application services; no relation,
idempotency, summary, latest-outcome, or lifecycle query method is part of the port.

`DecisionReviewRepository` is likewise limited to `save()`, `load_all()`, and `get_by_id()`.
Decision filtering, cross-record validation, history ordering, and scoped idempotency—including
fail-closed duplicate-match ambiguity—belong to `DecisionReviewService`; no relation,
idempotency, chronology, or lifecycle query method is part of the port.

`ExperienceRepository` remains limited to `save()`, `load_all()`, and `get_by_id()` for both plain
and promoted Experiences. Review validation, copied-text integrity, Observation validation, and
`(decision_review_id, "review_experience_promotion", idempotency_key)` scanning belong to
`ExperienceService`; no promotion, relation, or idempotency query belongs to the port.

`KnowledgeRepository` also remains limited to `save()`, `load_all()`, and `get_by_id()`.
Its `save()` contract is create-once: create an absent Knowledge UUID, accept an identical
complete same-ID replay as a no-op, and reject a different same-ID payload as
`KnowledgePersistenceConflictError` without writing. Persistence conflict, invalid stored data,
and filename/request-to-payload identity mismatch are distinct repository failures.
Knowledge membership filtering and complete relation validation remain in `KnowledgeService`.
KnowledgeService does not use `ExperienceRepository` directly; its separate application-facing
`ExperienceReader` exposes only validated `get_by_id()` behavior implemented by
`ExperienceService`. No Knowledge/Experience relation query or promotion-integrity method is added
to either repository port.

`PlaybookRunRepository` remains limited to `save()`, `load_all()`, and `get_by_id()`.
Its `save()` contract is create-once: create an absent Run UUID without replacement, accept an
identical complete same-ID replay as a metadata-preserving no-op, and reject a different same-ID
payload as `PlaybookRunPersistenceConflictError` without writing.
`PlaybookRunRepositoryError` is the base persistence failure category;
`PlaybookRunStoredDataError` identifies malformed or invalid stored data and non-UUID filename
stems, while `PlaybookRunIdentityMismatchError` identifies filename/request versus embedded UUID
disagreement. A missing `get_by_id()` returns `None`.

Optional revision validation, complete and scoped relation integrity, ordinary fresh-ID creation,
and revision-to-Runs filtering belong to `PlaybookRunService`. The separate application-facing
`PlaybookRunReader` exposes its validated `get_by_id()` behavior to downstream services. No
revision-specific repository query method, update/delete surface, or content-level idempotency
operation is added.

## Repository return types

Prefer:

- domain entities,
- value objects,
- explicit optional results,
- application-facing collections.

Avoid:

- ORM models,
- database rows,
- SQL tuples,
- adapter-specific pagination objects.

## Not-found behavior

Choose one consistent contract:

- return `None`, or
- raise an explicit port/application error.

Do not mix behavior across implementations.

---

# Infrastructure Adapters

## Responsibility

Adapters implement ports using concrete external mechanisms.

Examples:

- filesystem persistence,
- SQL persistence,
- JSON serialization,
- clock providers,
- UUID providers.

## Adapter rules

Adapters may:

- translate between persistence and domain representations,
- handle external resource lifecycle,
- convert external failures into stable adapter/application errors,
- enforce storage-level constraints that mirror domain requirements.

Adapters must not:

- decide business policy,
- change validation order,
- infer domain transitions,
- render CLI output,
- orchestrate use cases,
- silently repair invalid domain state.

## Mapping rule

Mapping code should be explicit and testable.

Persistence models must not leak into application services.

## Local development evidence adapter

`LocalDevelopmentEvidenceSource` implements `DevelopmentEvidenceSource` for one NeuralEngine Git
worktree. It validates the repository root and repository-relative paths, reads each selected
Markdown file once, hashes the exact bytes, conservatively parses required sections, resolves one
exact lowercase full commit, rejects merge commits, and reads the parent, subject, tree, changed
paths, and patch.

The adapter returns normalized source facts and stable source errors. It does not correlate domain
meaning, classify authority, create candidates, persist records, execute validation commands,
search for artifacts, integrate with GitHub or CI, or support background/multi-repository
ingestion.

---

# Repository Adapters

## Responsibility

Repository adapters implement repository ports.

## Implementation rules

- Preserve domain identity exactly.
- Preserve provenance fields.
- Make serialization round-trippable.
- Keep ordering deterministic when public behavior depends on ordering.
- Handle missing records according to the port contract.
- Do not broaden the port from inside the adapter.
- Do not add business filtering without an application requirement.

## Testing requirements

Repository adapters require tests for:

- save and load,
- missing identity,
- list behavior,
- ordering where relevant,
- serialization round trip,
- invalid/corrupted persisted data,
- provenance preservation.

Development-evidence dogfooding adds no repository adapter, JSON path, Brain directory, persisted
evidence, or persisted candidate. Its optional durable writes use the existing Decision-family and
Experience adapters through their application services. Full prompts, reviews, diffs, and
unrestricted validation output are not copied into repository records.

## Default Neural home paths

All 15 JSON repository adapters accept either an explicit `directory=...` or the immutable
`NeuralPaths` selected for their dependency graph. With neither supplied, the adapter resolves the
current process environment at construction time. The no-argument default therefore follows the
sole public `NEURAL_HOME` selector without freezing an environment-derived path at module import.

The private `RepositoryPath` helper owns only this duplicated adapter path policy. Before default
I/O it revalidates the configured root and Brain. Before a write it also checks write access.
Missing individual store directories below an available Brain retain their established
empty/`None` read behavior and may be created exactly where expected for a write. Under an
override, creation is non-recursive: an adapter cannot reconstruct a missing selected root or
Brain.

Explicit `directory=...` injection remains supported without a selected-root guard. It is mutually
exclusive with `paths=...` and preserves existing test and alternate-infrastructure composition.
Path selection changes no repository port, serialization, ordering, relation validation,
create-once integrity, or missing-record contract.

## Revision application adapter

`JsonPlaybookRevisionApplicationRepository` implements
`PlaybookRevisionApplicationRepository` and stores application audit records under
`NeuralPaths.PLAYBOOK_REVISION_APPLICATIONS`. It supplies only the port's basic save, load-all, and
identity lookup operations; relation filtering remains in the application layer.

## PlaybookRevision adapter create-once integrity

`JsonPlaybookRevisionRepository` still stores one JSON file per Revision under
`NeuralPaths.PLAYBOOK_REVISIONS`, with no schema, path, or repository-method change. It serializes
and validates the complete candidate, writes and fsyncs a same-directory temporary file, and uses
a non-replacing local filesystem publication operation so a supported save cannot replace an
existing UUID path.

An identical complete same-ID replay compares as the validated model and succeeds without
rewriting existing bytes. Any different modeled field raises
`PlaybookRevisionPersistenceConflictError` without write. Malformed or invalid stored data raises
`PlaybookRevisionStoredDataError`; requested or filename UUID disagreement with embedded
`PlaybookRevision.id` raises `PlaybookRevisionIdentityMismatchError`. `load_all()` validates UUID
filename syntax and embedded identity. Integrity failures are not repaired, overwritten, skipped,
or substituted, while a missing `get_by_id()` returns `None`.

Valid old JSON remains readable without migration or backfill. Direct filesystem mutation remains
out-of-band corruption. The adapter adds no deep in-memory collection immutability, tamper-proof
or cryptographic storage, hashes, content-addressed IDs, versions, snapshots, historical
reconstruction, repair, or backup/restore workflow.

## Decision adapter

`JsonDecisionRepository` implements `DecisionRepository` and stores one JSON file per Decision
under `NeuralPaths.DECISIONS`. UUIDs, timestamps, optional values, and embedded
`EvidenceReference` values round-trip through domain validation. `load_all()` sorts file names for
deterministic order, and malformed data surfaces validation errors. The adapter performs no
project filtering, idempotency query, migration, or ingestion.

## Decision acceptance adapter

`JsonDecisionAcceptanceRepository` implements `DecisionAcceptanceRepository` and stores one JSON
file per acceptance under `NeuralPaths.DECISION_ACCEPTANCES`; Brain initialization creates the
directory. UUIDs, timestamps, embedded evidence, and tags round-trip through domain validation.
`load_all()` sorts file names for deterministic order, and malformed data surfaces validation
errors. The adapter performs no relation filtering, eligibility decision, migration, or ingestion.

## Decision action adapter

`JsonDecisionActionRepository` implements `DecisionActionRepository` and stores one JSON file per
action under `NeuralPaths.DECISION_ACTIONS`; Brain initialization creates the directory. Complete
DecisionAction records round-trip through domain validation. `load_all()` sorts file names for
deterministic order, and malformed data surfaces validation errors. The adapter performs no
relation filtering, lifecycle projection, migration, ingestion, or command execution.

## Decision outcome adapter

`JsonDecisionOutcomeRepository` implements `DecisionOutcomeRepository` and stores one JSON file
per outcome under `NeuralPaths.DECISION_OUTCOMES`; Brain initialization creates the directory.
Complete DecisionOutcome records, including immutable scalar metrics, round-trip through domain
validation. JSON object keys and metric keys are serialized deterministically, `load_all()` sorts
file names, and malformed data surfaces validation errors. The adapter performs no relation
validation or filtering, latest-outcome selection, summary or lifecycle projection, idempotency
decision, migration, ingestion, review, or learning.

## Decision review adapter

`JsonDecisionReviewRepository` implements `DecisionReviewRepository` and stores one JSON file per
review under `NeuralPaths.DECISION_REVIEWS`; Brain initialization creates the directory. Complete
DecisionReview records round-trip through domain validation. JSON object keys are serialized with
`indent=2` and `sort_keys=True`, `load_all()` sorts filenames, and malformed data surfaces
validation errors. The adapter performs no Decision filtering, relation validation, chronology,
idempotency selection, lifecycle projection, evidence ingestion, learning, or Consigliere work.

## Experience adapter and promotion compatibility

`JsonExperienceRepository` continues to implement the unchanged `ExperienceRepository` under
`NeuralPaths.EXPERIENCES`, storing one JSON file per Experience and sorting filenames for
deterministic `load_all()`. Domain validation round-trips both ordinary records and the optional
embedded `DecisionReviewPromotion`. Old JSON without that field loads with `None` and remains plain.

No migration or production adapter rewrite was required. The adapter performs no Review lookup,
source copying, integrity repair, idempotency decision, promotion policy, second write, or inferred
provenance. No promotion adapter, repository, path, or Brain directory exists.

## Knowledge adapter create-once integrity

`JsonKnowledgeRepository` still stores one JSON file per Knowledge under
`NeuralPaths.KNOWLEDGE`, with no schema, path, or repository-method change. Before publication it
serializes and validates the complete candidate and writes, flushes, and fsyncs a same-directory
temporary file. It then uses a non-replacing local filesystem publication operation, so a final
UUID path cannot be replaced by a supported save.

An absent path is created once. If the path exists, exact complete modeled equality produces a
successful no-op without rewriting existing bytes; any different modeled field raises
`KnowledgePersistenceConflictError` without a write. Malformed or invalid existing data raises
`KnowledgeStoredDataError`, and filename/request UUID disagreement with embedded `Knowledge.id`
raises `KnowledgeIdentityMismatchError`. Save collisions, `get_by_id()`, and `load_all()` fail
visibly for those integrity problems instead of repairing, replacing, skipping, or substituting
data. Missing `get_by_id()` retains `None`.

Valid old JSON remains readable without migration or backfill, and the already stored valid
payload is grandfathered as authoritative for its UUID going forward. Direct filesystem mutation
is out-of-band corruption; the adapter adds no tamper-proofing, cryptographic immutability,
content hashes, Knowledge versions, snapshots, or historical reconstruction.

Knowledge-to-Experience relation integrity remains separate application composition through
`ExperienceReader` and `ExperienceService.get_by_id()`. No Knowledge or Experience JSON field,
relation index, or repair-on-read behavior was added.

## PlaybookRun adapter create-once integrity

`JsonPlaybookRunRepository` still stores one JSON file per Run under
`NeuralPaths.PLAYBOOK_RUNS`, with no schema, path, or repository-method change. It serializes and
validates the complete candidate, writes it to a repository-owned same-directory temporary file,
flushes and `fsync`s that file, then uses non-replacing publication. The adapter removes its own
temporary file after creation, replay, or failure.

An absent UUID path is created once. On collision, the adapter loads and validates the existing
complete model. Exact same-ID modeled equality succeeds without rewriting the target and preserves
bytes, inode, size, mtime, and ctime. Any different modeled field raises
`PlaybookRunPersistenceConflictError` without overwrite. Malformed or invalid stored data raises
`PlaybookRunStoredDataError`; requested or filename UUID disagreement with embedded
`PlaybookRun.id` raises `PlaybookRunIdentityMismatchError`.

`get_by_id()` returns `None` only for an absent file; present data is validated and identity
checked. Sorted `load_all()` validates every filename stem as a UUID and every file as a complete
identity-matching Run. Invalid records are not skipped. Valid existing JSON remains readable
without migration. Old JSON without `revision_id` loads with `None` and makes no
revision-specific claim.

The adapter adds no update/delete/replace operation, migration, repair, transaction, generalized
crash-recovery guarantee, tamper resistance, or protection from direct filesystem mutation.
Revision inference and same-Playbook ownership remain in `PlaybookRunService`.

---

# Dependency Injection and Container

## Responsibility

The container is the composition root.

It constructs concrete adapters and injects them into application services.

## Rules

The container may:

- instantiate repositories,
- instantiate infrastructure providers,
- instantiate application services,
- define lifecycle and sharing policy,
- expose configured services to CLI.

The container must not:

- contain business logic,
- perform use-case orchestration,
- parse CLI arguments,
- hide mutable global state,
- create cyclic dependencies.

## Constructor injection

Prefer constructor injection.

Good:

```python
service = PlaybookRevisionService(repository=revision_repository)
```

Avoid service locator access inside services:

```python
repository = container.get("revision_repository")
```

## Change policy

Any container or registration change is architectural work owned by Codex.

## Neural home propagation

Each container service graph resolves one immutable `NeuralPaths` value and passes that same value
to every default JSON repository in the graph. Nested container composition is scoped with the
already resolved value, so one graph cannot mix default and override roots or independently
resolved paths. `Brain` and CLI preflight consume the same path type.

The container does not cache an environment-derived path globally. Independent top-level
resolution may observe a later process-environment change, while a graph already under
construction remains internally consistent. Explicit repository `directory=...` injection
continues to be available outside default container composition.

The current revision application foundation is wired through
`Container.playbook_revision_application_repository()` and
`Container.playbook_revision_application_service()`. The service receives its repositories and a
`PlaybookRevisionActivationService`, preserving canonical ownership of active-revision resolution.

The Decision foundation is wired through `Container.decision_repository()` and
`Container.decision_service()`. The container supplies `JsonDecisionRepository` and
`JsonObservationRepository` to `DecisionService`; Decision CLI handlers resolve the service and do
not construct repositories.

The acceptance foundation is wired through `Container.decision_acceptance_repository()` and
`Container.decision_acceptance_service()`. The container supplies
`JsonDecisionAcceptanceRepository` and `JsonDecisionRepository` to
`DecisionAcceptanceService`; acceptance CLI handlers construct no repositories.

The action foundation is wired through `Container.decision_action_repository()` and
`Container.decision_action_service()`. The action service receives JSON action, Decision,
and acceptance repositories plus `PlaybookRunService` as the validated `PlaybookRunReader`.

`Container.playbook_run_service()` injects `JsonPlaybookRunRepository`,
`JsonPlaybookRepository`, and `JsonPlaybookRevisionRepository`. It deliberately receives no
activation service or revision-application repository: Run revision provenance is explicit caller
input, not lifecycle-derived state.

`Container.playbook_evaluation_service()` and `Container.evolution_proposal_service()` also
receive a constructed `PlaybookRunService` rather than a raw Run repository. Revision-linked
corruption therefore fails closed for Evaluation, Proposal, and DecisionAction Run reads while the
dependency graph remains acyclic.

The outcome foundation is wired through `Container.decision_outcome_repository()` and
`Container.decision_outcome_service()`. The outcome service receives JSON outcome, Decision,
acceptance, and action repositories. `Container.decision_lifecycle_service()` receives those same
four repository categories so it can validate relations and derive the canonical state. Decision
action, outcome, summary, and state CLI handlers resolve services and construct no repositories.

The review foundation is wired through `Container.decision_review_repository()` and
`Container.decision_review_service()`. The service receives `JsonDecisionReviewRepository`,
`JsonDecisionRepository`, `JsonDecisionAcceptanceRepository`, and
`JsonDecisionOutcomeRepository`. Brain initialization creates `NeuralPaths.DECISION_REVIEWS`.
Decision review CLI handlers resolve the service and construct no repositories.

`Container.experience_service()` supplies `JsonExperienceRepository`,
`JsonObservationRepository`, and the existing validated `DecisionReviewService` boundary to
`ExperienceService`. The container adds no promotion policy, link repository, path, or lifecycle
behavior; `neural experience from-review` resolves this service like the ordinary Experience
commands.

`Container.knowledge_service()` supplies `JsonKnowledgeRepository` and the constructed
`ExperienceService` as the narrow `ExperienceReader`. It does not inject a raw
`JsonExperienceRepository` into KnowledgeService. This keeps promoted-Experience validation in
one owner and preserves an acyclic graph:

```text
KnowledgeService
→ ExperienceReader
→ ExperienceService
→ ExperienceRepository + ObservationRepository + DecisionReviewService
```

ExperienceService has no KnowledgeService dependency, and the container adds no Knowledge
validation or learning policy.

---

# Dependency Lifecycle

## Default policy

Prefer explicit, simple lifetimes.

- Stateless services may be reused.
- Repositories may be reused when their adapter is safe to share.
- Per-operation resources must be scoped explicitly.
- Global mutable singletons are forbidden.

## Resource ownership

The component that opens an external resource must have a defined closing strategy.

Examples:

- database connection/session,
- file handle,
- transaction,
- network client.

Resource cleanup must not depend on process termination.

---

# Cookbook: Add an Application Service

1. Identify the exact use case.
2. Confirm no existing service already owns it.
3. Identify required domain entities and value objects.
4. Identify required ports.
5. Define explicit application errors.
6. Implement constructor-injected dependencies.
7. Implement one coherent public method.
8. Add service-level tests using fakes.
9. Wire the service in the container.
10. Add CLI integration only if requested.
11. Run full validation.
12. Produce the review artifact.

---

# Cookbook: Add a Repository

1. Confirm the domain concept requires persistence.
2. Confirm a repository is the correct abstraction.
3. Define the minimal repository port.
4. Use domain/application types in the contract.
5. Implement the adapter.
6. Add mapping and round-trip tests.
7. Add missing-record behavior tests.
8. Register the adapter in the container.
9. Inject the repository into the owning service.
10. Run full validation.
11. Produce the review artifact.

---

# Cookbook: Add an Adapter

1. Start from an existing port.
2. Do not design from the external library API.
3. Map external types to domain/application types.
4. Translate external failures.
5. Define resource lifecycle.
6. Add adapter contract tests.
7. Register the adapter in the container.
8. Verify no concrete adapter leaks inward.
9. Run full validation.
10. Produce the review artifact.

---

# Cookbook: Wire the Container

1. Identify new concrete dependencies.
2. Confirm service constructors remain explicit.
3. Instantiate adapters before services.
4. Inject ports through constructor arguments.
5. Avoid service-locator access.
6. Keep lifecycle policy explicit.
7. Add or update container tests.
8. Verify CLI resolves the service, not the adapter.
9. Run full validation.
10. Produce the review artifact.

---

# Anti-pattern: Fat Service

## Symptom

One application service coordinates unrelated use cases and depends on many unrelated ports.

## Risk

- high coupling,
- difficult testing,
- unclear ownership,
- unrelated changes collide.

## Correction

Split by use-case responsibility or domain ownership.

Do not split solely by file length.

---

# Anti-pattern: God Repository

## Symptom

A repository exposes relationship navigation, filtering, reporting, validation, and business operations.

## Risk

- persistence controls application behavior,
- services become thin wrappers,
- adapters become difficult to replace,
- domain decisions leak outward.

## Correction

Keep persistence methods minimal. Move orchestration and navigation into application services.

---

# Anti-pattern: Service Locator

## Symptom

Application code fetches dependencies from a global container at runtime.

## Risk

- hidden dependencies,
- brittle tests,
- runtime failures,
- cyclic coupling.

## Correction

Use constructor injection and keep the container at the composition root.

---

# Anti-pattern: Business Logic in Adapter

## Symptom

An infrastructure adapter decides validation, eligibility, transition, or policy.

## Risk

- behavior changes when adapters change,
- domain rules become untestable in isolation,
- persistence becomes the source of truth.

## Correction

Move policy into domain or application services. Keep the adapter focused on translation and external interaction.

---

# Application Service Checklist

- Is the use case explicit?
- Does one service clearly own it?
- Are dependencies constructor-injected?
- Are dependencies ports rather than adapters?
- Is business logic outside CLI and infrastructure?
- Are errors explicit?
- Is validation order preserved?
- Is provenance preserved?
- Can the service be tested without external systems?
- Are tests written with fakes?
- Is container wiring updated?
- Is Codex assigned when architecture changes?

---

# Repository Checklist

- Does the domain concept require persistence?
- Is the port minimal?
- Are method names persistence-focused?
- Are domain/application types used?
- Is relationship navigation better owned by a service?
- Is missing-record behavior consistent?
- Are adapters covered by round-trip tests?
- Is ordering deterministic where observable?
- Is provenance preserved?
- Are all implementations updated after a port change?

---

# Adapter Checklist

- Does the adapter implement an existing port?
- Are external types translated?
- Are external failures mapped?
- Is resource lifecycle explicit?
- Is business policy absent?
- Is validation order unchanged?
- Are adapter contract tests present?
- Does no adapter type leak inward?
- Is container registration explicit?

---

# Container Checklist

- Is the container only composing dependencies?
- Are constructors explicit?
- Are adapters instantiated before services?
- Are lifetimes clear?
- Is mutable global state absent?
- Are cyclic dependencies absent?
- Does CLI resolve services rather than repositories?
- Are container tests updated?

---

# ADR-0005: Constructor injection

Status: Accepted

## Decision

Application services receive dependencies through constructors.

The dependency container remains the composition root.

## Consequences

- Dependencies are visible.
- Services are testable with fakes.
- Service-locator access inside application code is prohibited.

---

# ADR-0006: Minimal application-driven ports

Status: Accepted

## Decision

Ports describe the minimum contracts required by application use cases.

They do not mirror every capability of an external library or persistence technology.

## Consequences

- Adapters remain replaceable.
- Port changes require architectural review.
- External types do not leak into application code.

---

# ADR-0007: Adapters contain no business policy

Status: Accepted

## Decision

Infrastructure adapters translate and interact with external systems but do not own business rules or use-case orchestration.

## Consequences

- Business behavior remains stable across adapter changes.
- Domain and service tests can run without infrastructure.
- Adapter tests focus on contracts and translation.

---

# Development Workflow

## Before work

1. Read `AGENTS.md`.
2. Read `.agent-work/project-state.md` when present.
3. Run `./scripts/validate.sh`.
4. Inspect affected code and tests.
5. Define the smallest complete scope.
6. Create a task prompt under `.agent-work/prompts/`.

## During work

- Implement a coherent vertical slice.
- Follow current patterns.
- Add tests with implementation.
- Preserve public behavior unless explicitly changing it.
- Preserve persisted schemas unless explicitly changing them.
- Avoid unrelated cleanup.

## After work

1. Run `./scripts/validate.sh`.
2. Create a review file under `.agent-work/reviews/`.
3. Include validation output, diff stat, diff check, git status, and full diff.
4. Stop without committing or pushing.

## Development evidence dogfooding

NeuralEngine development is intended to become a dogfooding source through:

```text
prompt
→ agent execution
→ review finding
→ decision/correction
→ implementation
→ validation
→ commit
→ push
→ post-work lesson
```

Source commit `25599655d0b1483eb37f88d379f6ca99afaf828d` implements the first deliberately
bounded local path through this wider workflow:

```text
one NeuralEngine worktree
+ one distinct repository-relative prompt
+ one distinct repository-relative review
+ one exact lowercase full non-merge commit SHA
→ validated non-persisted candidate preview
→ separate authority-confirmed apply
→ existing Decision-family records
→ optional explicit Review-to-Experience promotion
```

Preview is side-effect free and is the default. Apply requires `--confirm-authority`, rebuilds the
preview from fresh local file and Git facts, and rejects stale evidence before any durable call.
The candidate is frozen, replaceable, non-persisted, and neither truth nor authority.

This is explicit local ingestion, not automatic capture. It does not watch the worktree, run in the
background, integrate with GitHub or CI, authenticate actors, create an Observation or Knowledge,
evolve a Playbook, or learn autonomously.

## Handbook synchronization

```text
major NeuralEngine milestone
→ commit/push NeuralEngine
→ sync NeuralEngine-Handbook
→ generate SKILL.md
→ copy generated SKILL.md back to NeuralEngine
→ commit/push skill sync
```

Each repository change is separate and reviewable. Generated outputs are rebuilt from Handbook
sources and are never edited manually. Publishing the generated skill back to NeuralEngine is a
later separate repository task; a Handbook synchronization task must not perform that publication
unless it is explicitly included in scope.

---

# Validation Policy

Preferred command:

```bash
./scripts/validate.sh
```

Required checks:

```bash
ruff format --check .
ruff check .
mypy src tests
pytest
```

Never claim success unless all required checks pass.

When validation fails:

- show the failing command,
- include relevant output,
- identify whether the failure is pre-existing,
- do not bypass or suppress the failure.

---

# Agent Assignment Policy

## Codex GPT-5.5 medium

Use for:

- new features,
- domain models,
- vertical slices,
- ports and adapters,
- repositories and services,
- dependency injection,
- CLI additions,
- persisted schema changes,
- public behavior changes,
- validation-order changes,
- provenance decisions,
- architectural documentation.

## DeepSeek

Use only for small controlled post-review fixes, normally one to three files:

- one concrete bug,
- targeted regression tests,
- Ruff or MyPy corrections,
- small message, type, validation, or CLI-option fixes,
- minor refactors without behavior change.

Every DeepSeek prompt must begin with reading `AGENTS.md`.

Required scope guard:

> Do not add features. Do not broaden scope. Do not change architecture, persisted schemas, public behavior, validation order, or provenance rules. Modify only the files required for the specified fix.

---

# Pattern: New Feature

1. Identify the owning domain concept.
2. Decide whether the change requires a new entity or extends an existing one.
3. Define or update ports.
4. Implement adapters.
5. Implement the application service.
6. Wire dependencies in the container.
7. Add CLI only when required.
8. Add unit, service, adapter, and CLI tests as applicable.
9. Run full validation.
10. Produce the review artifact.

---

# Pattern: Controlled Bug Fix

1. Reproduce the problem.
2. Add a regression test when practical.
3. Fix the root cause.
4. Run targeted tests.
5. Run full validation.
6. Produce the review artifact.
7. Stop without committing or pushing.

---

# Definition of Done

A task is complete only when:

- requested behavior is implemented,
- scope has not expanded,
- architectural boundaries are preserved,
- tests cover the change,
- all required validation passes,
- prompt and review artifacts exist,
- review includes complete evidence,
- no commit or push was performed.

---

# Review Checklist

- Is the requested scope complete?
- Were unrelated changes avoided?
- Are layer responsibilities preserved?
- Is business logic in the correct layer?
- Are repository interfaces persistence-focused?
- Are tests sufficient?
- Did validation pass?
- Does the review include diff stat, diff check, git status, and full diff?
- Were persisted schemas or public behavior changed?
- Was any commit or push performed?

---

# Domain Change Checklist

- Which entity or value object owns the new responsibility?
- Does the change preserve the canonical domain chain?
- Is provenance preserved?
- Is validation placed before persistence?
- Does the change require a new port?
- Does it require an adapter?
- Does it require application orchestration?
- Does container wiring change?
- Does public behavior change?
- Does persisted schema change?
- Are unit and service tests sufficient?
- Is Codex assigned?

---

# New CLI Command Checklist

- Does an application service already expose the required use case?
- Is business logic absent from the command handler?
- Is dependency resolution delegated to the container?
- Are UUID inputs validated consistently?
- Are errors mapped to useful user-facing messages?
- Are CLI tests included?
- Is public output intentionally specified?
- Is the task assigned to Codex?

---

# ADR-0001: Service-owned relationship navigation

Status: Accepted

## Decision

Relationship navigation that can be composed from persistence operations belongs in application services rather than repository interfaces.

## Context

Playbook revision navigation previously risked expanding repository responsibilities and coupling unrelated services.

## Consequences

- Repository ports remain persistence-focused.
- Application services own use-case navigation.
- Service tests describe the relationship behavior.

---

# ADR-0002: Canonical domain chain

Status: Accepted

## Decision

The canonical NeuralEngine chain is:

`Observation`
→ `Experience`
→ `Knowledge`
→ `Playbook`
→ `PlaybookRun`
→ `PlaybookEvaluation`
→ `EvolutionProposal`
→ `PlaybookRevision`
→ `PlaybookRevisionActivation`
→ `PlaybookRevisionApplication`

## Consequences

- New features must identify their position in the chain.
- Transitions are application use cases.
- Provenance must not be lost between stages.
- A later-stage object must not silently absorb the responsibility of an earlier-stage object.
- Revision, activation, and application remain separate explicit records.
- Activation does not imply application, and application intent does not imply materialization.

---

# ADR-0003: Agent assignment policy

Status: Accepted

## Decision

Codex GPT-5.5 medium owns architectural and feature work.

DeepSeek is restricted to small, controlled, post-review fixes, normally one to three files.

## Consequences

- New features are never delegated to DeepSeek.
- Repository, service, container, CLI, schema, public behavior, validation-order, and provenance changes belong to Codex.
- DeepSeek prompts require an explicit scope guard.

---

# ADR-0004: Mandatory prompt and review artifacts

Status: Accepted

## Decision

Every agent task must have:

- a prompt in `.agent-work/prompts/`,
- a review in `.agent-work/reviews/`.

The review must contain validation output, diff stat, diff check, git status, and full diff.

## Consequences

- Agent work is inspectable before commit.
- Success claims require evidence.
- Agents do not commit or push.

---

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
- At the earlier `1b45beb` Experience-integrity checkpoint, no Knowledge schema, authority,
  idempotency, repository, adapter, or command changed. Duplicate Experience IDs remain supported,
  and read validation performs one validated read per relation.
- Source commit `0ffdda6bfdbadd5952c1066fddd303185939d643` hardens the unchanged Knowledge
  schema and repository surface with create-once supported-write integrity: identical complete
  same-ID replay is a no-op, different payload conflicts, malformed data and identity mismatch
  fail visibly, and no migration or repair occurs. This is not Knowledge versioning, snapshotting,
  hashing, historical reconstruction, or filesystem tamper protection.
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
