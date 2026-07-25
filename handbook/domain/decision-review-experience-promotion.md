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
reader boundary; `neural experience knowledge` remains read-only navigation. Durable Knowledge use
and feedback remain separate future work.
