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
