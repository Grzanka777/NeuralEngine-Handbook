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

## Compatibility and learning boundary

The hardening adds no Knowledge field, Review provenance copy, authority marker, idempotency
behavior, repository method, adapter format, command, or automatic creation. Knowledge may still
reference one or more Experiences, mix ordinary and promoted sources, combine different Reviews,
and retain duplicate Experience IDs. Knowledge creation itself remains non-idempotent.

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
→ PlaybookRun.playbook_id
→ Playbook.knowledge_ids
→ Knowledge.id
```

This is feedback on the Playbook and its declared Knowledge set. It does not prove one Knowledge
item caused an outcome, attribute contributions within a multi-Knowledge Playbook, or demonstrate
causal or comparative improvement. Durable retrieval history, recommendation events, and
revision-specific Run provenance are not recorded.

Read validation performs one validated Experience read per stored relation, including duplicates.
The resulting linear read amplification is an intentional fail-closed trade-off; this milestone
adds no cache, batch reader, or deduplication.
