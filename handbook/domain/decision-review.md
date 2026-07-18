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
