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
