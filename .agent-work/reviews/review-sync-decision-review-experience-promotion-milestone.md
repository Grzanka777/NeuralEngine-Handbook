# Review: DecisionReview-to-Experience promotion Handbook synchronization

## Outcome

completed

The Handbook now documents the complete DecisionReview-to-Experience promotion milestone implemented by NeuralEngine commit `12097feb0159cc8e8831000ab04c290b56ecfc8e`. Authoritative sources, builder registration, focused builder tests, and all generated outputs are synchronized as one vertical slice.

## Starting checkpoints and repository state

### NeuralEngine-Handbook

Command: `git branch --show-current`
Exit status: `0`

~~~~text
main
~~~~

Command: `git rev-parse HEAD`
Exit status: `0`

~~~~text
2f46b441a9a8c53973f53f005378daf5d290914d
~~~~

Command: `git rev-parse origin/main`
Exit status: `0`

~~~~text
2f46b441a9a8c53973f53f005378daf5d290914d
~~~~

Command: `git log -1 --format='%s'`
Exit status: `0`

~~~~text
docs: sync decision review milestone
~~~~

Command: `git status --short --untracked-files=all`
Exit status: `0`

~~~~text
?? .agent-work/prompts/codex-implement-decision-foundation.md
?? .agent-work/prompts/codex-sync-decision-acceptance-foundation-milestone.md
?? .agent-work/prompts/codex-sync-decision-action-lifecycle-foundation-milestone.md
?? .agent-work/prompts/codex-sync-decision-foundation-milestone.md
?? .agent-work/prompts/codex-sync-decision-learning-design-milestone.md
?? .agent-work/prompts/codex-sync-decision-outcome-handbook.md
?? .agent-work/prompts/codex-sync-decision-review-experience-promotion-handbook.md
?? .agent-work/prompts/codex-sync-decision-review-handbook.md
?? .agent-work/prompts/codex-sync-neuralengine-application-foundation-milestone.md
?? .agent-work/reviews/review-sync-decision-acceptance-foundation-milestone.md
?? .agent-work/reviews/review-sync-decision-action-lifecycle-foundation-milestone.md
?? .agent-work/reviews/review-sync-decision-foundation-milestone.md
?? .agent-work/reviews/review-sync-decision-learning-design-milestone.md
?? .agent-work/reviews/review-sync-neuralengine-application-foundation-milestone.md
?? .directory
~~~~

The tracked Handbook worktree was clean. Every listed untracked path existed before this task and was preserved.

### NeuralEngine

Command: `git -C ../NeuralEngine branch --show-current`
Exit status: `0`

~~~~text
main
~~~~

Command: `git -C ../NeuralEngine rev-parse HEAD`
Exit status: `0`

~~~~text
12097feb0159cc8e8831000ab04c290b56ecfc8e
~~~~

Command: `git -C ../NeuralEngine rev-parse origin/main`
Exit status: `0`

~~~~text
12097feb0159cc8e8831000ab04c290b56ecfc8e
~~~~

Command: `git -C ../NeuralEngine log -1 --format='%s'`
Exit status: `0`

~~~~text
feat: add decision review experience promotion
~~~~

Command: `git -C ../NeuralEngine status --short --untracked-files=all`
Exit status: `0`

~~~~text

~~~~

The authoritative repository was at the required checkpoint and clean.

## Baseline validation

Command: `env PYTHONPATH=src uv run --no-project --with pytest --with typer --with pyyaml pytest`
Exit status: `0`

~~~~text
============================= test session starts ==============================
platform linux -- Python 3.12.8, pytest-9.1.1, pluggy-1.6.0
rootdir: /run/media/grzanka/Big_Shit/projekty/NeuralEngine-Handbook
configfile: pyproject.toml
testpaths: tests
collected 8 items

tests/test_builder.py ........                                           [100%]

============================== 8 passed in 5.15s ===============================
~~~~

Command: `ruff check .`
Exit status: `0`

~~~~text
All checks passed!
~~~~

Command: `uv run --no-project --with mypy --with typer --with pyyaml python -m mypy src`
Exit status: `0`

~~~~text
Success: no issues found in 3 source files
~~~~

## Source-of-truth inspection

The implementation was inspected at the exact authoritative commit, including:

- `src/neural_engine/domain/experience.py` and `src/neural_engine/domain/decision_review.py`;
- `src/neural_engine/application/experience_service.py` and `src/neural_engine/application/decision_review_service.py`;
- Experience and Observation repository ports and JSON adapters;
- dependency injection and the Experience CLI;
- promotion unit, boundary, persistence, container, and CLI tests;
- repository README, vision/context/about documents, project state, conventions, and relevant commit history from the prior Handbook checkpoint through `12097feb`.

The inspected milestone adds one explicit promotion use case. It does not add automatic promotion, Knowledge creation, a new lifecycle state, a new repository/path/Brain collection, or a separate link aggregate.

## Changed-file inventory

### Authoritative Handbook sources

- `handbook/application/services.md`
- `handbook/architecture/architecture.md`
- `handbook/architecture/decision-learning.md`
- `handbook/container/dependency-injection.md`
- `handbook/decisions/ADR-0008-decision-learning-boundary.md`
- `handbook/domain/decision-review.md`
- `handbook/domain/decision-review-experience-promotion.md` — task-created canonical source
- `handbook/domain/domain-chain.md`
- `handbook/domain/experience.md`
- `handbook/infrastructure/repositories.md`
- `handbook/ports/repository-ports.md`

### Builder and tests

- `src/neuralengine_handbook/builder.py`
- `tests/test_builder.py`

### Generated outputs rebuilt by the builder

- `outputs/claude-skill/SKILL.md`
- `outputs/generated/AGENTS.generated.md`
- `outputs/generated/APPLICATION_ARCHITECTURE.md`
- `outputs/generated/DECISION_ENGINE.md`
- `outputs/generated/HANDBOOK.md`

The following generated outputs were also rebuilt and verified but remained byte-identical, so Git reports no content change:

- `outputs/generated/codex-task-template.md`
- `outputs/generated/deepseek-task-template.md`
- `outputs/generated/review-template.md`

### Review artifact

- `.agent-work/reviews/review-sync-decision-review-experience-promotion-milestone.md`

### Pre-existing unrelated untracked files, excluded from the task commit

- `.agent-work/prompts/codex-implement-decision-foundation.md`
- `.agent-work/prompts/codex-sync-decision-acceptance-foundation-milestone.md`
- `.agent-work/prompts/codex-sync-decision-action-lifecycle-foundation-milestone.md`
- `.agent-work/prompts/codex-sync-decision-foundation-milestone.md`
- `.agent-work/prompts/codex-sync-decision-learning-design-milestone.md`
- `.agent-work/prompts/codex-sync-decision-outcome-handbook.md`
- `.agent-work/prompts/codex-sync-decision-review-experience-promotion-handbook.md`
- `.agent-work/prompts/codex-sync-decision-review-handbook.md`
- `.agent-work/prompts/codex-sync-neuralengine-application-foundation-milestone.md`
- `.agent-work/reviews/review-sync-decision-acceptance-foundation-milestone.md`
- `.agent-work/reviews/review-sync-decision-action-lifecycle-foundation-milestone.md`
- `.agent-work/reviews/review-sync-decision-foundation-milestone.md`
- `.agent-work/reviews/review-sync-decision-learning-design-milestone.md`
- `.agent-work/reviews/review-sync-neuralengine-application-foundation-milestone.md`
- `.directory`

### Intended commit scope

The intended commit contains the 11 authoritative source files, 2 builder/test files, 5 changed generated outputs, and this review artifact: 19 files total. None of the pre-existing untracked paths above belongs to that scope.

## Stale or conflicting statements corrected

The synchronization corrected all affected claims that Review and Experience creation are necessarily separate or that no implemented Review-to-Experience boundary exists. It now distinguishes:

- ordinary Experience creation, which remains unchanged and has no review provenance;
- explicit `ExperienceService.add_from_decision_review(...)`, which creates exactly one promoted Experience;
- Review completion, which remains non-automatic and does not itself create Experience;
- Experience-to-Knowledge promotion, which remains a separate future explicit decision/use case.

Command used for the final targeted stale-text scan:

`rg -n "separate explicit Experience creation from DecisionReview|review only; Experience creation remains separate|DecisionReview.*does not create Experience|no implemented.*Review.*Experience|DecisionReview.*terminal.*Experience" handbook src tests outputs || true`

Exit status: `0`

~~~~text
tests/test_builder.py:220:    assert "separate explicit Experience creation from DecisionReview" not in handbook
~~~~

The only result is a negative regression assertion proving that the obsolete phrase is absent from the generated Handbook.

## Acceptance criteria

- [x] Exact promotion provenance schema, field limits, selector kinds, ordering, uniqueness, and nested immutability are documented.
- [x] Plain Experience remains compatible with `decision_review_promotion is None`.
- [x] The single explicit application use case and its exact validation/read/idempotency/write sequence are documented.
- [x] Duplicate-idempotency ambiguity is checked before selection integrity, semantic comparison, or replay.
- [x] Replay, conflict, ambiguity, source-index, and source-text failure behavior is documented.
- [x] Read-side promotion integrity is documented for replay, `get_by_id`, `list_experiences`, and scoped `list_for_observation`.
- [x] Repository compatibility, old JSON loading, and round-trip behavior are documented without inventing new persistence infrastructure.
- [x] Container dependency and exact `neural experience from-review` selector convention are documented.
- [x] Decision lifecycle remains unchanged and reviewer/promoter authority is kept separate.
- [x] Automatic promotion, Experience-to-Knowledge implementation, Consigliere, justfile, and unrelated work remain explicit non-goals.
- [x] The new source is registered deterministically in the `domain_files` list immediately after `handbook/domain/decision-review.md`.
- [x] Builder tests verify source inclusion, generated section order (DecisionReview before DecisionReview-to-Experience Promotion), generated contracts, and removal of the stale statement.
- [x] Every generated artifact was rebuilt twice through the documented builder with identical checksums.
- [x] Complete raw validation evidence and full diffs are recorded below.

## Exact documented contract

### Domain

`Experience` has optional `decision_review_promotion: DecisionReviewPromotion | None = None`. A plain Experience uses `None`; no upstream Decision, Acceptance, Outcome, Action, reviewer, assessment, confidence, or evidence fields are copied.

`DecisionReviewPromotion` is a frozen nested value object with exactly:

- `decision_review_id`;
- ordered non-empty `source_statements`;
- trimmed non-blank `promoted_by`, maximum 255 characters;
- trimmed non-blank `promotion_reason`, maximum 1000 characters;
- trimmed non-blank `idempotency_key`, maximum 255 characters.

Each frozen `DecisionReviewPromotionSourceStatement` has exactly `kind`, zero-based `index >= 0`, and exact copied `text` with a 1000-character maximum. Kinds are exactly `finding` and `candidate_lesson`. The ordered selector sequence must be non-empty and unique by `(kind, index)`. Experience itself is not made globally frozen; the nested provenance is frozen.

One promotion creates one Experience from one DecisionReview. Promotion replacement, supersession, deletion, multi-Review aggregation, ranking, and scoring are not implemented. Corrections require a new Experience and a new idempotency key.

### Application and validation order

`ExperienceService` receives a `DecisionReviewReader` port exposing `show(review_id)`. `add_from_decision_review(...)`:

1. validates the non-empty, unique source-selector sequence;
2. normalizes and validates promoter, reason, and idempotency key before reading the Review;
3. calls the existing validated `DecisionReviewService.show(review_id)` boundary;
4. resolves indexes against ordered findings/candidate lessons and copies exact source text;
5. validates optional Observation identifiers;
6. constructs the candidate Experience with frozen promotion provenance;
7. loads all Experiences and scans the scoped idempotency key;
8. fails on more than one scoped match before selection integrity, semantic comparison, or replay;
9. for one match, validates stored promotion integrity, then returns an equivalent record or raises conflict;
10. for no match, performs exactly one Experience save.

Read paths validate linked promotion integrity through the Review boundary: the selected index must exist and stored text must exactly match current Review text. This applies to replay, `get_by_id`, all promoted records returned by `list_experiences`, and only promoted records returned by `list_for_observation`. Plain Experiences are unaffected.

### Idempotency

Scope is exactly:

`(decision_review_id, "review_experience_promotion", idempotency_key)`.

The semantic payload excludes only Experience `id` and timestamp. It includes all remaining Experience fields and the complete promotion provenance:

| Scoped matches | Result |
|---|---|
| 0 | Save one new Experience. |
| 1, stored provenance valid, semantic payload equal | Return the existing Experience without a second write. |
| 1, stored provenance valid, semantic payload different | Raise `DecisionReviewPromotionIdempotencyConflictError`. |
| More than 1 | Raise `DecisionReviewPromotionIdempotencyAmbiguityError` before integrity/comparison/replay. |
| 1 with invalid selector index | Raise `DecisionReviewPromotionSourceIndexError`. |
| 1 with source text drift | Raise `DecisionReviewPromotionSourceTextMismatchError`. |

An empty selector sequence raises `DecisionReviewPromotionSourcesRequiredError`. Ordinary `add` and `add_from_observation` do not acquire promotion idempotency.

### Compatibility and persistence

The existing Experience repository contract remains unchanged: `save`, `load_all`, and `get_by_id`. Existing JSON without `decision_review_promotion` remains valid and loads with `None`; promoted provenance round-trips through the existing JSON adapter. There is no migration, inferred provenance, second record, transaction emulation, new repository, adapter, path, or Brain collection.

### CLI and container

The container injects the JSON Experience repository, JSON Observation repository, and the existing validated DecisionReview service into ExperienceService.

The command is exactly `neural experience from-review REVIEW_UUID`. It requires repeatable `--source KIND:ORDINAL` plus `--promoted-by`, `--promotion-reason`, `--idempotency-key`, `--title`, `--context`, `--action`, `--outcome`, and `--result`. Optional repeatable `--observation-id` and `--tag` are supported. CLI ordinals are one-based and are converted to zero-based durable indexes. Supported kinds are exactly `finding` and `candidate_lesson`. Controlled domain failures are rendered as actionable CLI errors; success prints the Experience ID, full Experience/provenance, and each source as `kind:ordinal (stored index index) text`.

### Lifecycle and authority

The Decision lifecycle remains `proposed`, `accepted`, `in_progress`, `succeeded`, `failed`, `partial`, and `outcome_unknown`. No `reviewed`, `promoted`, or `learned` state is added. Review completion does not automatically promote. Reviewer and promoter are separate authorities and may be different people; no RBAC or approval workflow is invented. A promoted Experience is not Knowledge. Experience-to-Knowledge remains a separate explicit future decision/use case.

## Generated-output proof

No generated output was edited manually. All output changes came from the registered source page and the repository builder. The new page is registered at the end of the local `domain_files` list, immediately after `decision-review.md`; focused tests assert this order and the required generated contracts.

### Build 1

Command: `uv run --no-project --with-editable . handbook build`
Exit status: `0`

~~~~text
/run/media/grzanka/Big_Shit/projekty/NeuralEngine-Handbook/outputs/claude-skill/SKILL.md
/run/media/grzanka/Big_Shit/projekty/NeuralEngine-Handbook/outputs/generated/AGENTS.generated.md
/run/media/grzanka/Big_Shit/projekty/NeuralEngine-Handbook/outputs/generated/codex-task-template.md
/run/media/grzanka/Big_Shit/projekty/NeuralEngine-Handbook/outputs/generated/deepseek-task-template.md
/run/media/grzanka/Big_Shit/projekty/NeuralEngine-Handbook/outputs/generated/review-template.md
/run/media/grzanka/Big_Shit/projekty/NeuralEngine-Handbook/outputs/generated/HANDBOOK.md
/run/media/grzanka/Big_Shit/projekty/NeuralEngine-Handbook/outputs/generated/DECISION_ENGINE.md
/run/media/grzanka/Big_Shit/projekty/NeuralEngine-Handbook/outputs/generated/APPLICATION_ARCHITECTURE.md
~~~~

Command: `sha256sum outputs/claude-skill/SKILL.md outputs/generated/AGENTS.generated.md outputs/generated/codex-task-template.md outputs/generated/deepseek-task-template.md outputs/generated/review-template.md outputs/generated/HANDBOOK.md outputs/generated/DECISION_ENGINE.md outputs/generated/APPLICATION_ARCHITECTURE.md`
Exit status: `0`

~~~~text
f19bf5cbd174f9ed870dee77191a61ae0984c39881f7b365f36d4357cb770e82  outputs/claude-skill/SKILL.md
cf28bec83c4b3779691a171d443c6e0aa6f8b1c862522f0201f897b4058faf5e  outputs/generated/AGENTS.generated.md
cb8717f6d11ef37f22301cddd3adcc6018244ae6ae0716153e9d163f7356788e  outputs/generated/codex-task-template.md
dd0b789499891f724d96711dcabe968e9c22c0961c1b6aa0cbb106c8153133c9  outputs/generated/deepseek-task-template.md
dfe91096687c6a46d611bf788274b9f04bb46af4ec2d6da0e53563d7a9551fe9  outputs/generated/review-template.md
8b00ea9829a21091ddd43e029f3201dac73851c9010e57b43a18f90b80cbb05a  outputs/generated/HANDBOOK.md
65e78c098fb221cb16fe347e1909069d10039b6085c75eeadee0e40e91936eac  outputs/generated/DECISION_ENGINE.md
b66d7c828efbddc2c5cf808322a854d270c52557be9e9198337c06d6c3967c16  outputs/generated/APPLICATION_ARCHITECTURE.md
~~~~

### Build 2

Command: `uv run --no-project --with-editable . handbook build`
Exit status: `0`

~~~~text
/run/media/grzanka/Big_Shit/projekty/NeuralEngine-Handbook/outputs/claude-skill/SKILL.md
/run/media/grzanka/Big_Shit/projekty/NeuralEngine-Handbook/outputs/generated/AGENTS.generated.md
/run/media/grzanka/Big_Shit/projekty/NeuralEngine-Handbook/outputs/generated/codex-task-template.md
/run/media/grzanka/Big_Shit/projekty/NeuralEngine-Handbook/outputs/generated/deepseek-task-template.md
/run/media/grzanka/Big_Shit/projekty/NeuralEngine-Handbook/outputs/generated/review-template.md
/run/media/grzanka/Big_Shit/projekty/NeuralEngine-Handbook/outputs/generated/HANDBOOK.md
/run/media/grzanka/Big_Shit/projekty/NeuralEngine-Handbook/outputs/generated/DECISION_ENGINE.md
/run/media/grzanka/Big_Shit/projekty/NeuralEngine-Handbook/outputs/generated/APPLICATION_ARCHITECTURE.md
~~~~

Command: `sha256sum outputs/claude-skill/SKILL.md outputs/generated/AGENTS.generated.md outputs/generated/codex-task-template.md outputs/generated/deepseek-task-template.md outputs/generated/review-template.md outputs/generated/HANDBOOK.md outputs/generated/DECISION_ENGINE.md outputs/generated/APPLICATION_ARCHITECTURE.md`
Exit status: `0`

~~~~text
f19bf5cbd174f9ed870dee77191a61ae0984c39881f7b365f36d4357cb770e82  outputs/claude-skill/SKILL.md
cf28bec83c4b3779691a171d443c6e0aa6f8b1c862522f0201f897b4058faf5e  outputs/generated/AGENTS.generated.md
cb8717f6d11ef37f22301cddd3adcc6018244ae6ae0716153e9d163f7356788e  outputs/generated/codex-task-template.md
dd0b789499891f724d96711dcabe968e9c22c0961c1b6aa0cbb106c8153133c9  outputs/generated/deepseek-task-template.md
dfe91096687c6a46d611bf788274b9f04bb46af4ec2d6da0e53563d7a9551fe9  outputs/generated/review-template.md
8b00ea9829a21091ddd43e029f3201dac73851c9010e57b43a18f90b80cbb05a  outputs/generated/HANDBOOK.md
65e78c098fb221cb16fe347e1909069d10039b6085c75eeadee0e40e91936eac  outputs/generated/DECISION_ENGINE.md
b66d7c828efbddc2c5cf808322a854d270c52557be9e9198337c06d6c3967c16  outputs/generated/APPLICATION_ARCHITECTURE.md
~~~~

The two complete checksum sets are byte-for-byte identical (`match: true`). There was no content drift after the second build.

## Final validation

Command: `env PYTHONPATH=src uv run --no-project --with pytest --with typer --with pyyaml pytest`
Exit status: `0`

~~~~text
============================= test session starts ==============================
platform linux -- Python 3.12.8, pytest-9.1.1, pluggy-1.6.0
rootdir: /run/media/grzanka/Big_Shit/projekty/NeuralEngine-Handbook
configfile: pyproject.toml
testpaths: tests
collected 8 items

tests/test_builder.py ........                                           [100%]

============================== 8 passed in 2.48s ===============================
~~~~

Command: `ruff check .`
Exit status: `0`

~~~~text
All checks passed!
~~~~

Command: `uv run --no-project --with mypy --with typer --with pyyaml python -m mypy src`
Exit status: `0`

~~~~text
Success: no issues found in 3 source files
~~~~

### Intermediate failures and corrections

Two in-scope validation attempts failed before the successful final run:

1. A focused builder test initially expected the substring `fail closed without`, while the authoritative source wording was `fails closed without`. The assertion was corrected to match the actual generated contract, then the full suite passed.
2. One subsequent pytest invocation exited `2` before collection because the sandbox could not read `/home/grzanka/.cache/uv/sdists-v6/.git` (`Read-only file system (os error 30)`). The identical repository-defined command was rerun with approved access to the existing uv cache and passed all 8 tests.

No failure was hidden and neither required a source-of-truth deviation.

### Whitespace and tracked-diff checks

Command: `git diff --check`
Exit status: `0`

~~~~text

~~~~

Command: `git diff --cached --exit-code`
Exit status: `0`

~~~~text

~~~~

The empty cached diff proves that nothing is staged.

## Complete tracked diff stat

Command: `git diff --stat`
Exit status: `0`

~~~~text
 handbook/application/services.md                   |  27 ++
 handbook/architecture/architecture.md              |  18 +-
 handbook/architecture/decision-learning.md         | 161 +++++++-
 handbook/container/dependency-injection.md         |   6 +
 .../ADR-0008-decision-learning-boundary.md         |  20 +-
 handbook/domain/decision-review.md                 |  12 +-
 handbook/domain/domain-chain.md                    |  17 +-
 handbook/domain/experience.md                      |  10 +-
 handbook/infrastructure/repositories.md            |  11 +
 handbook/ports/repository-ports.md                 |   5 +
 outputs/claude-skill/SKILL.md                      | 196 ++++++++--
 outputs/generated/AGENTS.generated.md              |  18 +-
 outputs/generated/APPLICATION_ARCHITECTURE.md      |  49 +++
 outputs/generated/DECISION_ENGINE.md               | 181 ++++++++-
 outputs/generated/HANDBOOK.md                      | 434 +++++++++++++++++++--
 src/neuralengine_handbook/builder.py               |   1 +
 tests/test_builder.py                              |  41 +-
 17 files changed, 1077 insertions(+), 130 deletions(-)
~~~~

Task-created untracked files supplement the tracked stat:

- `handbook/domain/decision-review-experience-promotion.md`: 144 inserted lines;
- `.agent-work/reviews/review-sync-decision-review-experience-promotion-milestone.md`: 2983 inserted lines.

The review artifact itself is new and contains this evidence. Its creation diff is not recursively embedded into itself; the artifact's complete current content is this file. This is the only logical self-reference exception. It is explicitly included in the task inventory, consolidated stat, and final status.

Consolidated task diff stat: 19 files changed, 4204 insertions(+), 130 deletions(-).

## Complete final status and scope evidence

Command: `git status --short --untracked-files=all`
Exit status: `0`

~~~~text
 M handbook/application/services.md
 M handbook/architecture/architecture.md
 M handbook/architecture/decision-learning.md
 M handbook/container/dependency-injection.md
 M handbook/decisions/ADR-0008-decision-learning-boundary.md
 M handbook/domain/decision-review.md
 M handbook/domain/domain-chain.md
 M handbook/domain/experience.md
 M handbook/infrastructure/repositories.md
 M handbook/ports/repository-ports.md
 M outputs/claude-skill/SKILL.md
 M outputs/generated/AGENTS.generated.md
 M outputs/generated/APPLICATION_ARCHITECTURE.md
 M outputs/generated/DECISION_ENGINE.md
 M outputs/generated/HANDBOOK.md
 M src/neuralengine_handbook/builder.py
 M tests/test_builder.py
?? .agent-work/prompts/codex-implement-decision-foundation.md
?? .agent-work/prompts/codex-sync-decision-acceptance-foundation-milestone.md
?? .agent-work/prompts/codex-sync-decision-action-lifecycle-foundation-milestone.md
?? .agent-work/prompts/codex-sync-decision-foundation-milestone.md
?? .agent-work/prompts/codex-sync-decision-learning-design-milestone.md
?? .agent-work/prompts/codex-sync-decision-outcome-handbook.md
?? .agent-work/prompts/codex-sync-decision-review-experience-promotion-handbook.md
?? .agent-work/prompts/codex-sync-decision-review-handbook.md
?? .agent-work/prompts/codex-sync-neuralengine-application-foundation-milestone.md
?? .agent-work/reviews/review-sync-decision-acceptance-foundation-milestone.md
?? .agent-work/reviews/review-sync-decision-action-lifecycle-foundation-milestone.md
?? .agent-work/reviews/review-sync-decision-foundation-milestone.md
?? .agent-work/reviews/review-sync-decision-learning-design-milestone.md
?? .agent-work/reviews/review-sync-decision-review-experience-promotion-milestone.md
?? .agent-work/reviews/review-sync-neuralengine-application-foundation-milestone.md
?? .directory
?? handbook/domain/decision-review-experience-promotion.md
~~~~

Task-created paths are:

- `handbook/domain/decision-review-experience-promotion.md`;
- `.agent-work/reviews/review-sync-decision-review-experience-promotion-milestone.md`.

All other untracked paths in the status are the preserved pre-existing artifacts listed above.

### NeuralEngine checkpoint proof after Handbook work

Command: `git -C ../NeuralEngine status --short --untracked-files=all`
Exit status: `0`

~~~~text

~~~~

Command: `git -C ../NeuralEngine rev-parse HEAD`
Exit status: `0`

~~~~text
12097feb0159cc8e8831000ab04c290b56ecfc8e
~~~~

Command: `git -C ../NeuralEngine rev-parse origin/main`
Exit status: `0`

~~~~text
12097feb0159cc8e8831000ab04c290b56ecfc8e
~~~~

Command: `git -C ../NeuralEngine log -1 --format='%s'`
Exit status: `0`

~~~~text
feat: add decision review experience promotion
~~~~

NeuralEngine remained clean and exactly at the authoritative local/remote checkpoint.

## Complete tracked diff

Command: `git diff --no-ext-diff --binary`
Exit status: `0`

~~~~text
diff --git a/handbook/application/services.md b/handbook/application/services.md
index 4d745d7..bbb8a7b 100644
--- a/handbook/application/services.md
+++ b/handbook/application/services.md
@@ -166,3 +166,30 @@ The DecisionOutcome and DecisionReview duplicate-key rules are the same reusable
 application-service invariant: more than one persisted match for a scoped key is corruption or
 ambiguity to surface, never an ordering problem to resolve by choosing the first record. Their
 scopes and controlled ambiguity error types remain separate.
+
+## DecisionReview-to-Experience promotion ownership
+
+`ExperienceService.add_from_decision_review(...)` is the one implemented explicit promotion use
+case. It validates selectors and bounded promoter/reason/key metadata before relation reads, calls
+the existing validated `DecisionReviewService.show(review_id)` boundary, validates ordered finding
+and candidate-lesson indexes, copies exact Review text, validates optional Observation IDs,
+constructs one Experience, then loads Experiences for application-layer idempotency. Only a fully
+validated zero-match candidate is saved.
+
+The scope is `(decision_review_id, "review_experience_promotion", idempotency_key)`. Exactly one
+equivalent match returns the original Experience identity and timestamp without writing; exactly
+one different match raises `DecisionReviewPromotionIdempotencyConflictError`; more than one match
+raises `DecisionReviewPromotionIdempotencyAmbiguityError` without repository-order selection or
+arbitrary semantic comparison. Semantic equivalence excludes only generated Experience ID and
+timestamp and includes every caller-supplied Experience and ordered promotion field.
+
+Equivalent replay validates the existing provenance. `get_by_id()`, `list_experiences()`, and
+`list_for_observation()` also fail closed for promoted records when the Review graph is invalid, an
+index is out of range, or copied text differs. Plain Experience reads remain unaffected. Direct and
+Observation-derived `add` paths keep their existing inputs and do not acquire idempotency or
+promotion requirements.
+
+One Review may produce multiple Experiences under different keys, and the same statement may be
+promoted repeatedly. Each Experience references only one Review. Corrections append; no promotion
+replacement, ranking, deletion, lifecycle state, Knowledge creation, or Consigliere behavior is
+owned here.
diff --git a/handbook/architecture/architecture.md b/handbook/architecture/architecture.md
index 754e247..ddea3ae 100644
--- a/handbook/architecture/architecture.md
+++ b/handbook/architecture/architecture.md
@@ -68,7 +68,7 @@ a milestone snapshot, not a timeless guarantee.

 ## Decision Learning boundary

-Source commit `910f481e27302daa6d3f15bde30d678ffc9e5d2f` implements separate immutable
+Source commit `12097feb0159cc8e8831000ab04c290b56ecfc8e` implements separate immutable
 `Decision`, `DecisionAcceptance`, `DecisionAction`, `DecisionOutcome`, and `DecisionReview`
 records, persistence-focused ports and JSON adapters, application services, container wiring,
 thin proposal/acceptance/action/outcome/review CLI commands, and the canonical
@@ -82,10 +82,18 @@ the latest outcome using `(validated_at, outcome.id)` rather than repository ord
 `DecisionReview` targets an explicit ordered non-empty set of outcomes for one Decision and
 acceptance. Multiple reviews form immutable history ordered by `(reviewed_at, review.id)`.

+The same checkpoint implements explicit Review-to-Experience promotion. One Experience may embed
+optional immutable `DecisionReviewPromotion` provenance containing ordered copied Review
+statements. `ExperienceService` uses the validated Review service boundary and existing Experience
+repository; no promotion aggregate, repository, adapter, path, Brain collection, or automatic
+learning exists. Old and ordinary Experiences remain compatible.
+
 The canonical lifecycle states remain exactly `proposed`, `accepted`, `in_progress`, `succeeded`,
 `failed`, `partial`, and `outcome_unknown`. Review is orthogonal append-only history; there is no
-`reviewed` state. Outcome or review creation does not create learning. There is no execution
-engine, lifecycle reversal, ingestion, automatic learning or evolution, generic event replay, or
+`reviewed`, `promoted`, or `learned` state. Outcome or review creation does not create learning;
+only the explicit promotion use case creates an Experience, which remains distinct from Knowledge.
+There is no execution engine, lifecycle reversal, ingestion, automatic learning or evolution,
+generic event replay, or
 Consigliere integration. The authoritative implemented contract and future boundary are defined
-in `handbook/architecture/decision-learning.md`; the recommended next controlled slice is
-separate explicit Experience creation from review findings or candidate lessons.
+in `handbook/architecture/decision-learning.md`; the next controlled downstream step remains a
+separate explicit Experience-to-Knowledge decision or use case.
diff --git a/handbook/architecture/decision-learning.md b/handbook/architecture/decision-learning.md
index 6fe5ad5..c3bf084 100644
--- a/handbook/architecture/decision-learning.md
+++ b/handbook/architecture/decision-learning.md
@@ -2,12 +2,13 @@

 ## Status and purpose

-NeuralEngine source commit `910f481e27302daa6d3f15bde30d678ffc9e5d2f` implements the Decision,
+NeuralEngine source commit `12097feb0159cc8e8831000ab04c290b56ecfc8e` implements the Decision,
 DecisionAcceptance, DecisionAction, DecisionOutcome, and DecisionReview foundations plus the
 canonical `DecisionLifecycleService` projection. They record an immutable proposed choice,
 explicit authorization, work performed under that authorization, factual results, and authorized
-interpretation. Each foundation persists immutable records, exposes application use cases, is
-wired through the container, and provides a thin CLI.
+interpretation, plus explicit promotion of selected Review statements into an existing Experience.
+Each foundation persists its durable records, exposes application use cases, is wired through the
+container, and provides a thin CLI.

 The wider Decision Learning lifecycle remains accepted future architecture. Decision tracking
 complements the existing Observation-to-Playbook chain; it does not replace it.
@@ -23,6 +24,8 @@ DecisionAcceptance
 DecisionAction
 DecisionOutcome
 DecisionReview
+DecisionReviewPromotion
+DecisionReviewPromotionSourceStatement
 DecisionRepository
 DecisionAcceptanceRepository
 DecisionActionRepository
@@ -39,6 +42,7 @@ DecisionActionService
 DecisionOutcomeService
 DecisionOutcomeSummary
 DecisionReviewService
+ExperienceService.add_from_decision_review
 DecisionLifecycleService
 container wiring
 neural decision add/list/show
@@ -54,6 +58,7 @@ neural decision outcome-summary
 neural decision review add
 neural decision review history
 neural decision review show
+neural experience from-review
 neural decision state
 ```

@@ -62,6 +67,8 @@ proposal for possible future work. Creating a DecisionAction records work perfor
 acceptance. Creating a DecisionOutcome records factual results and validation evidence for one or
 more linked actions. Creating a DecisionReview records authorized interpretation over an explicit
 ordered outcome set. None of these operations automatically creates learning.
+Only the separate authorized Review-to-Experience promotion use case creates one Experience from
+selected copied Review interpretation; that Experience remains distinct from Knowledge.

 ## Decision model

@@ -292,6 +299,37 @@ is transitive through `DecisionReview → DecisionOutcome[] → DecisionAction[]
 may cover one Decision, outcome, or ordered outcome set under different keys. Corrections append;
 there is no replacement, supersession, deletion, or persisted `current` behavior.

+## DecisionReview-to-Experience promotion foundation
+
+At source commit `12097fe`, `Experience` has optional immutable
+`decision_review_promotion: DecisionReviewPromotion | None`. Plain direct and
+Observation-derived Experiences retain `None`. Promotion contains exactly one Review ID, ordered
+non-empty immutable source statements, promoter, reason, and idempotency key. Each statement stores
+exactly `kind`, zero-based non-negative `index`, and exact copied `text`; kind is exactly `finding`
+or `candidate_lesson`, and `(kind, index)` pairs are unique.
+
+Promoter and key are bounded to 255 characters; reason and copied text are bounded to 1000. All are
+trimmed and non-blank. Reviewer and promoter are separate explicit authorities. Promotion copies no
+Decision, acceptance, action, outcome, reviewer, assessment, confidence, or evidence fields into
+Experience. One Experience references one Review and one or more selected statements; one Review
+and one source statement may produce multiple Experiences under different keys. Corrections append.
+
+The implemented chain is:
+
+```text
+Observation
+→ Decision
+→ DecisionAcceptance
+→ DecisionAction
+→ DecisionOutcome
+→ DecisionReview
+→ explicitly promoted Experience
+→ separately and explicitly created Knowledge
+```
+
+Review save does not promote. Promotion does not create Knowledge or change Decision lifecycle.
+`DecisionReview.assessment`, `DecisionOutcome.result`, and `Experience.result` remain distinct.
+
 ## Persistence

 The persistence-focused `DecisionRepository` port implements only:
@@ -368,6 +406,20 @@ It has no relation, idempotency, chronology, or lifecycle query methods.
 filenames and every record round-trips through domain validation. Filtering, relation validation,
 history ordering, ambiguity detection, and semantic comparison remain in the application service.

+The existing `ExperienceRepository` also remains limited to:
+
+```text
+save()
+load_all()
+get_by_id()
+```
+
+`JsonExperienceRepository` continues to store one JSON file per Experience under
+`NeuralPaths.EXPERIENCES` and round-trips the optional embedded promotion through domain
+validation. Old JSON without the field loads with `None`. No migration, new path, Brain directory,
+link record, promotion repository, second write, or production adapter rewrite was introduced.
+Idempotency and Review integrity remain application policy.
+
 ## Application service

 `DecisionService` implements:
@@ -632,6 +684,40 @@ for a scoped idempotency key must be surfaced, never resolved through `next()`,
 selection, repository order, or comparison with an arbitrarily chosen record. Their scopes and
 ambiguity error types remain separate.

+### ExperienceService Review promotion
+
+`ExperienceService.add_from_decision_review(...)` validates selectors and bounded authority
+metadata before calling `DecisionReviewService.show()`. It then copies caller-ordered exact Review
+items, validates optional Observations, constructs one promoted Experience, loads all Experiences,
+and applies this scope:
+
+```text
+(decision_review_id, "review_experience_promotion", idempotency_key)
+```
+
+```text
+zero matches
+→ save and return one promoted Experience
+
+exactly one equivalent match
+→ validate its provenance and return original ID/timestamp, no write
+
+exactly one different match
+→ `DecisionReviewPromotionIdempotencyConflictError`, no write
+
+more than one match
+→ `DecisionReviewPromotionIdempotencyAmbiguityError`, no selection or comparison, no write
+```
+
+Equivalence excludes only generated `Experience.id` and `Experience.timestamp`; every ordinary
+Experience field, optional Observation ID, tag, and ordered promotion value remains semantic.
+Ambiguity is repository-order independent.
+
+Replay, `get_by_id()`, complete list, and Observation-linked list revalidate the referenced Review
+graph, selector bounds, and exact copied text. Missing or malformed provenance fails closed without
+repair or skipping; plain records bypass promotion validation. The use case owns no Knowledge,
+Playbook, evolution, lifecycle, evidence, or Consigliere behavior.
+
 ### Canonical DecisionLifecycleService

 `DecisionLifecycleService` is the only canonical owner of the current lifecycle projection. It
@@ -692,6 +778,8 @@ JsonDecisionOutcomeRepository
 DecisionOutcomeService
 JsonDecisionReviewRepository
 DecisionReviewService
+JsonExperienceRepository
+ExperienceService
 DecisionLifecycleService
 ```

@@ -707,10 +795,13 @@ receives `JsonDecisionOutcomeRepository` plus Decision, acceptance, and action r
 outcome repositories. `Container.decision_review_repository()` and
 `Container.decision_review_service()` expose the review composition. CLI handlers resolve services
 from the container and construct no repositories.
+`Container.experience_service()` injects `JsonExperienceRepository`,
+`JsonObservationRepository`, and that validated `DecisionReviewService` boundary into
+`ExperienceService`; the container owns no promotion policy.

 ## Implemented CLI

-These commands exist at commit `910f481e`:
+These commands exist at commit `12097fe`:

 ```text
 neural decision add
@@ -728,6 +819,13 @@ neural decision outcome-summary DECISION_UUID
 neural decision review add DECISION_UUID
 neural decision review history DECISION_UUID
 neural decision review show REVIEW_UUID
+neural experience add
+neural experience from-observation OBSERVATION_UUID
+neural experience from-review REVIEW_UUID
+neural experience list
+neural experience show EXPERIENCE_UUID
+neural experience knowledge EXPERIENCE_UUID
+neural observation experiences OBSERVATION_UUID
 neural decision state DECISION_UUID
 ```

@@ -936,6 +1034,37 @@ and every review field.
 existing Decision with no reviews renders `No review history found for Decision: ...`.
 `neural decision review show REVIEW_UUID` renders every field after persisted relation validation.

+### Review-to-Experience promotion command
+
+`neural experience from-review REVIEW_UUID` requires repeatable ordered `--source`, plus:
+
+```text
+--promoted-by
+--promotion-reason
+--idempotency-key
+--title
+--context
+--action
+--outcome
+--result
+```
+
+Optional repeatable inputs are `--observation-id` and `--tag`. Selectors use exact syntax such as
+`--source finding:1 --source candidate_lesson:2`. CLI ordinals are positive and one-based; they
+become durable zero-based indexes `0` and `1` without caller-supplied text. Invalid selector syntax,
+kind, ordinal, Review, source index, Observation, conflict, ambiguity, or read integrity renders a
+controlled error.
+
+Success and equivalent replay print the stored Experience ID and complete auditable Experience
+details. Promotion source rendering shows kind, user ordinal, stored index, and copied text, plus
+promoter, reason, and key. Reviewer and promoter remain separate authorities.
+
+Ordinary Experience commands keep their existing contracts. Direct `add` requires title, context,
+action, outcome, and result; `from-observation` derives context from the required Observation and
+requires title, action, outcome, and result. Observation IDs and tags remain optional where already
+supported. List, show, Experience-to-Knowledge navigation, and Observation-to-Experience navigation
+remain read-only. Ordinary Experience creation requires no promotion metadata or idempotency key.
+
 `neural decision state DECISION_UUID` renders exactly one of:

 ```text
@@ -966,10 +1095,12 @@ Decision
 - `DecisionOutcome` is the implemented factual result and validation evidence record.
 - `DecisionReview` is the implemented authorized interpretation over explicit ordered outcomes.

-All five records exist. Records remain immutable semantic records rather than fields on a mutable
+All five decision records and the explicit Review-to-Experience promotion use case exist. Records
+remain immutable semantic records rather than fields on a mutable
 Decision or a duplicate generic event stream. A proposed option is not an acceptance, acceptance
 is not execution, an outcome is not a review or Experience, and review findings or candidate
-lessons are not automatically Experience, Knowledge, or a Playbook change.
+lessons are not Experience until promotion succeeds and are never automatically Knowledge or a
+Playbook change.

 The currently derivable projection is only:

@@ -1012,13 +1143,14 @@ Observation
 → DecisionAction
 → DecisionOutcome
 → DecisionReview
-→ explicitly created Experience
-→ explicitly created Knowledge
+→ explicitly promoted Experience
+→ separately and explicitly created Knowledge
 ```

 DecisionAction may optionally reference an existing PlaybookRun, with existence-only validation
 because PlaybookRun and Playbook expose no project key. `DecisionOutcome` remains distinct from
-Experience, and Decision review must never mutate a Playbook. Any connection from an action to
+Experience. The promotion use case copies selected Review text into optional immutable Experience
+provenance and never mutates a Playbook. Any connection from an action to
 PlaybookEvaluation, EvolutionProposal, or the revision lifecycle requires a separate reviewed use
 case.

@@ -1038,7 +1170,7 @@ prompt
 → post-work lesson
 ```

-Commit `910f481e` does not capture or ingest those events automatically. Automatic candidates and
+Commit `12097fe` does not capture or ingest those events automatically. Automatic candidates and
 manual confirmation remain future concepts; no automatic persistence, ingestion, or learning
 exists.

@@ -1047,7 +1179,7 @@ no recommendation can directly mutate NeuralEngine or authorize a durable record

 ## Current non-behavior

-Commit `910f481e` does not implement:
+Commit `12097fe` does not implement:

 ```text
 execution engine
@@ -1064,6 +1196,7 @@ git ingestion
 automatic Observation creation
 automatic Experience creation
 automatic Knowledge creation
+Experience-to-Knowledge promotion
 automatic Playbook creation or mutation
 automatic evolution
 Consigliere integration
@@ -1072,18 +1205,18 @@ Consigliere integration
 It also does not execute commands referenced by evidence, open locators, automatically accept
 Decisions, materialize Playbook revisions, or infer outcomes from `completed_at`. Explicit user
 requests are required to create Decision, DecisionAcceptance, DecisionAction, DecisionOutcome, or
-DecisionReview records.
+DecisionReview records and to promote Review statements into Experience.

 ## Recommended next milestone

 The recommended next controlled slice is:

 ```text
-separate explicit Experience creation from DecisionReview findings or candidate lessons
+separate explicit Experience-to-Knowledge decision or use case
 ```

 It must preserve explicit authority and remain separate from automatic Knowledge, Playbook,
-PlaybookEvaluation, EvolutionProposal, or Consigliere creation.
+PlaybookEvaluation, EvolutionProposal, lifecycle, or Consigliere behavior.

 ## Handbook synchronization policy

diff --git a/handbook/container/dependency-injection.md b/handbook/container/dependency-injection.md
index 06318ec..0562c3d 100644
--- a/handbook/container/dependency-injection.md
+++ b/handbook/container/dependency-injection.md
@@ -74,3 +74,9 @@ The review foundation is wired through `Container.decision_review_repository()`
 `JsonDecisionRepository`, `JsonDecisionAcceptanceRepository`, and
 `JsonDecisionOutcomeRepository`. Brain initialization creates `NeuralPaths.DECISION_REVIEWS`.
 Decision review CLI handlers resolve the service and construct no repositories.
+
+`Container.experience_service()` supplies `JsonExperienceRepository`,
+`JsonObservationRepository`, and the existing validated `DecisionReviewService` boundary to
+`ExperienceService`. The container adds no promotion policy, link repository, path, or lifecycle
+behavior; `neural experience from-review` resolves this service like the ordinary Experience
+commands.
diff --git a/handbook/decisions/ADR-0008-decision-learning-boundary.md b/handbook/decisions/ADR-0008-decision-learning-boundary.md
index d4415bb..27c744c 100644
--- a/handbook/decisions/ADR-0008-decision-learning-boundary.md
+++ b/handbook/decisions/ADR-0008-decision-learning-boundary.md
@@ -11,6 +11,11 @@ authorized interpretation over an explicit ordered outcome set. Lifecycle state
 acceptance, actions, and the latest factual outcome, not stored as mutable status or duplicated in
 a generic event stream. Review is orthogonal append-only history.

+Selected Review interpretation becomes Experience only through an explicit authorized use case.
+Promotion provenance is embedded immutably in the existing Experience rather than represented by
+a link aggregate, second write, new repository, or new lifecycle state. Experience-to-Knowledge
+remains a separate explicit decision.
+
 Decision tracking complements the existing Observation-to-Playbook chain. Evidence uses bounded
 embedded references, durable writes require explicit authority, and Consigliere remains a future
 advisory layer rather than authoritative storage.
@@ -23,9 +28,12 @@ advisory layer rather than authoritative storage.
   idempotency checks; repository ports remain persistence-focused.
 - No automatic ingestion, persistence, learning, Playbook evolution, or Consigliere integration is
   implied.
-- Source commit `910f481e27302daa6d3f15bde30d678ffc9e5d2f` implements Decision proposal,
+- Source commit `12097feb0159cc8e8831000ab04c290b56ecfc8e` implements Decision proposal,
   acceptance, action, outcome, and review recording; outcome history/summary; review history; their
   CLI; and the canonical `DecisionLifecycleService`.
+- The same checkpoint implements explicit ordered DecisionReview statement promotion into one
+  existing Experience with embedded immutable provenance, fail-closed read integrity, and scoped
+  application-layer idempotency. It does not implement automatic learning.
 - The canonical states are exactly proposed, accepted, in-progress, succeeded, failed, partial,
   and outcome-unknown. Latest outcome selection uses validation time and outcome UUID, not
   repository order. No generic completed, resolved, or reviewed state exists.
@@ -39,6 +47,10 @@ advisory layer rather than authoritative storage.
 - Outcome and review idempotency both fail closed when more than one persisted record matches a
   scoped key: their distinct ambiguity errors replace arbitrary first-match selection and no write
   occurs regardless of repository order or payload equivalence.
-- The recommended next controlled slice is separate explicit Experience creation from review
-  findings or candidate lessons; downstream Experience, Knowledge, or Playbook creation remains
-  explicit.
+- A Review may produce multiple Experiences under distinct keys, but one promoted Experience
+  references exactly one Review. Corrections append and ordinary Experience remains compatible.
+- Automatic promotion and a separate promotion/link aggregate were rejected because authority and
+  provenance belong in one explicit Experience write. Repository-order duplicate selection was
+  rejected in favor of a dedicated fail-closed ambiguity error.
+- The next controlled downstream step remains a separate explicit Experience-to-Knowledge decision
+  or use case; Knowledge, Playbook, and evolution creation remain explicit.
diff --git a/handbook/domain/decision-review.md b/handbook/domain/decision-review.md
index ee93c48..a06fe86 100644
--- a/handbook/domain/decision-review.md
+++ b/handbook/domain/decision-review.md
@@ -42,7 +42,7 @@ and a failed outcome can support a sound review.
 - Findings are required, ordered, trimmed, non-blank, case-insensitively unique, and limited to 100
   entries of at most 1000 characters each.
 - Candidate lessons use the same ordering, normalization, uniqueness, count, and length bounds, but
-  may be empty. They carry no authority to create or promote Experience or Knowledge.
+  may be empty. They are not Experience or Knowledge until a separate authorized use case succeeds.
 - Tags are trimmed and case-insensitively deduplicated while first-seen order is preserved.
 - `recorded_at` and `reviewed_at` must be timezone-aware and are normalized to UTC. Locally,
   `reviewed_at` cannot be later than `recorded_at`; the service also requires it not to precede the
@@ -99,9 +99,11 @@ renders every field. Evidence locators are retained but not opened.

 ## Lifecycle and learning boundary

-DecisionReview is orthogonal interpretive history. It does not affect `DecisionLifecycleService`.
+DecisionReview is orthogonal interpretive history. Saving one never creates Experience. The
+separate `ExperienceService.add_from_decision_review()` use case may explicitly copy selected
+findings or candidate lessons into one Experience without mutating the Review.
+DecisionReview does not affect `DecisionLifecycleService`.
 The lifecycle remains exactly `proposed`, `accepted`, `in_progress`, `succeeded`, `failed`,
 `partial`, and `outcome_unknown`; no `reviewed` state exists. A review never automatically creates
-Observation, Experience, Knowledge, Playbook, PlaybookEvaluation, EvolutionProposal, revision
-records, or Consigliere work. The next controlled slice is separate explicit Experience creation
-from review findings or candidate lessons.
+Observation, Knowledge, Playbook, PlaybookEvaluation, EvolutionProposal, revision records, or
+Consigliere work. Promotion remains explicit and a promoted Experience is not Knowledge.
diff --git a/handbook/domain/domain-chain.md b/handbook/domain/domain-chain.md
index 6f447a0..d9e2a38 100644
--- a/handbook/domain/domain-chain.md
+++ b/handbook/domain/domain-chain.md
@@ -50,15 +50,16 @@ Observation
 → DecisionAction
 → DecisionOutcome
 → DecisionReview
-→ explicitly created Experience
-→ explicitly created Knowledge
+→ explicitly promoted Experience
+→ separately and explicitly created Knowledge
 ```

 This is a complementary provenance path, not a replacement for the canonical domain chain.
 DecisionOutcome is factual; DecisionReview is authorized interpretation; Experience captures
-separately created operational learning; Knowledge is generalized; Playbook remains a separately
-created repeatable procedure. A Decision may have multiple immutable outcomes and multiple reviews,
-including reviews over the same ordered outcome set when their idempotency keys differ. Review
-action provenance is transitive through its explicit outcomes; it does not persist action IDs.
-These records and their embedded EvidenceReference values exist at source commit `910f481e`; no
-Review-driven lifecycle transition or later learning record in this path is automatic.
+explicitly promoted operational learning; Knowledge is separately generalized; Playbook remains a
+separately created repeatable procedure. A Decision may have multiple immutable outcomes and
+reviews, and one Review may explicitly produce multiple Experiences under different promotion
+keys. A promoted Experience selects ordered Review statements and cannot combine Reviews. Review
+action provenance remains transitive through explicit outcomes; promoted Experience provenance
+remains transitive through its one Review. These records exist at source commit `12097fe`; no
+Review save, promotion, lifecycle transition, or later Knowledge record in this path is automatic.
diff --git a/handbook/domain/experience.md b/handbook/domain/experience.md
index 2bad1e4..ca71e73 100644
--- a/handbook/domain/experience.md
+++ b/handbook/domain/experience.md
@@ -2,13 +2,15 @@

 ## Responsibility

-An Experience represents interpreted learning derived from one or more observations.
+An Experience represents explicitly recorded operational learning. It may be created directly,
+derived from one Observation, or explicitly promoted from selected DecisionReview statements.

 ## Owns

 - interpreted outcome,
 - contextual meaning,
 - provenance back to observations,
+- optional immutable DecisionReview promotion provenance,
 - identity.

 ## Must not own
@@ -22,9 +24,13 @@ An Experience represents interpreted learning derived from one or more observati
 - Provenance is preserved.
 - Interpretation is explicit.
 - Creation does not erase source observations.
+- Plain and Observation-derived Experiences have `decision_review_promotion is None`.
+- A promoted Experience contains one optional `DecisionReviewPromotion`; it remains Experience,
+  not generalized Knowledge.

 ## Typical transitions

 `Experience` → `Knowledge`

-The application layer coordinates this transformation.
+The application layer coordinates this separate explicit transformation. Experience creation does
+not create Knowledge automatically.
diff --git a/handbook/infrastructure/repositories.md b/handbook/infrastructure/repositories.md
index c6c2e92..fdbd73d 100644
--- a/handbook/infrastructure/repositories.md
+++ b/handbook/infrastructure/repositories.md
@@ -75,3 +75,14 @@ DecisionReview records round-trip through domain validation. JSON object keys ar
 `indent=2` and `sort_keys=True`, `load_all()` sorts filenames, and malformed data surfaces
 validation errors. The adapter performs no Decision filtering, relation validation, chronology,
 idempotency selection, lifecycle projection, evidence ingestion, learning, or Consigliere work.
+
+## Experience adapter and promotion compatibility
+
+`JsonExperienceRepository` continues to implement the unchanged `ExperienceRepository` under
+`NeuralPaths.EXPERIENCES`, storing one JSON file per Experience and sorting filenames for
+deterministic `load_all()`. Domain validation round-trips both ordinary records and the optional
+embedded `DecisionReviewPromotion`. Old JSON without that field loads with `None` and remains plain.
+
+No migration or production adapter rewrite was required. The adapter performs no Review lookup,
+source copying, integrity repair, idempotency decision, promotion policy, second write, or inferred
+provenance. No promotion adapter, repository, path, or Brain directory exists.
diff --git a/handbook/ports/repository-ports.md b/handbook/ports/repository-ports.md
index 18a492f..df5f2cd 100644
--- a/handbook/ports/repository-ports.md
+++ b/handbook/ports/repository-ports.md
@@ -50,6 +50,11 @@ Decision filtering, cross-record validation, history ordering, and scoped idempo
 fail-closed duplicate-match ambiguity—belong to `DecisionReviewService`; no relation,
 idempotency, chronology, or lifecycle query method is part of the port.

+`ExperienceRepository` remains limited to `save()`, `load_all()`, and `get_by_id()` for both plain
+and promoted Experiences. Review validation, copied-text integrity, Observation validation, and
+`(decision_review_id, "review_experience_promotion", idempotency_key)` scanning belong to
+`ExperienceService`; no promotion, relation, or idempotency query belongs to the port.
+
 ## Repository return types

 Prefer:
diff --git a/outputs/claude-skill/SKILL.md b/outputs/claude-skill/SKILL.md
index 2821d0f..be653e3 100644
--- a/outputs/claude-skill/SKILL.md
+++ b/outputs/claude-skill/SKILL.md
@@ -118,7 +118,7 @@ a milestone snapshot, not a timeless guarantee.

 ## Decision Learning boundary

-Source commit `910f481e27302daa6d3f15bde30d678ffc9e5d2f` implements separate immutable
+Source commit `12097feb0159cc8e8831000ab04c290b56ecfc8e` implements separate immutable
 `Decision`, `DecisionAcceptance`, `DecisionAction`, `DecisionOutcome`, and `DecisionReview`
 records, persistence-focused ports and JSON adapters, application services, container wiring,
 thin proposal/acceptance/action/outcome/review CLI commands, and the canonical
@@ -132,13 +132,21 @@ the latest outcome using `(validated_at, outcome.id)` rather than repository ord
 `DecisionReview` targets an explicit ordered non-empty set of outcomes for one Decision and
 acceptance. Multiple reviews form immutable history ordered by `(reviewed_at, review.id)`.

+The same checkpoint implements explicit Review-to-Experience promotion. One Experience may embed
+optional immutable `DecisionReviewPromotion` provenance containing ordered copied Review
+statements. `ExperienceService` uses the validated Review service boundary and existing Experience
+repository; no promotion aggregate, repository, adapter, path, Brain collection, or automatic
+learning exists. Old and ordinary Experiences remain compatible.
+
 The canonical lifecycle states remain exactly `proposed`, `accepted`, `in_progress`, `succeeded`,
 `failed`, `partial`, and `outcome_unknown`. Review is orthogonal append-only history; there is no
-`reviewed` state. Outcome or review creation does not create learning. There is no execution
-engine, lifecycle reversal, ingestion, automatic learning or evolution, generic event replay, or
+`reviewed`, `promoted`, or `learned` state. Outcome or review creation does not create learning;
+only the explicit promotion use case creates an Experience, which remains distinct from Knowledge.
+There is no execution engine, lifecycle reversal, ingestion, automatic learning or evolution,
+generic event replay, or
 Consigliere integration. The authoritative implemented contract and future boundary are defined
-in `handbook/architecture/decision-learning.md`; the recommended next controlled slice is
-separate explicit Experience creation from review findings or candidate lessons.
+in `handbook/architecture/decision-learning.md`; the next controlled downstream step remains a
+separate explicit Experience-to-Knowledge decision or use case.

 ## Decision Learning architecture

@@ -146,12 +154,13 @@ separate explicit Experience creation from review findings or candidate lessons.

 ## Status and purpose

-NeuralEngine source commit `910f481e27302daa6d3f15bde30d678ffc9e5d2f` implements the Decision,
+NeuralEngine source commit `12097feb0159cc8e8831000ab04c290b56ecfc8e` implements the Decision,
 DecisionAcceptance, DecisionAction, DecisionOutcome, and DecisionReview foundations plus the
 canonical `DecisionLifecycleService` projection. They record an immutable proposed choice,
 explicit authorization, work performed under that authorization, factual results, and authorized
-interpretation. Each foundation persists immutable records, exposes application use cases, is
-wired through the container, and provides a thin CLI.
+interpretation, plus explicit promotion of selected Review statements into an existing Experience.
+Each foundation persists its durable records, exposes application use cases, is wired through the
+container, and provides a thin CLI.

 The wider Decision Learning lifecycle remains accepted future architecture. Decision tracking
 complements the existing Observation-to-Playbook chain; it does not replace it.
@@ -167,6 +176,8 @@ DecisionAcceptance
 DecisionAction
 DecisionOutcome
 DecisionReview
+DecisionReviewPromotion
+DecisionReviewPromotionSourceStatement
 DecisionRepository
 DecisionAcceptanceRepository
 DecisionActionRepository
@@ -183,6 +194,7 @@ DecisionActionService
 DecisionOutcomeService
 DecisionOutcomeSummary
 DecisionReviewService
+ExperienceService.add_from_decision_review
 DecisionLifecycleService
 container wiring
 neural decision add/list/show
@@ -198,6 +210,7 @@ neural decision outcome-summary
 neural decision review add
 neural decision review history
 neural decision review show
+neural experience from-review
 neural decision state
 ```

@@ -206,6 +219,8 @@ proposal for possible future work. Creating a DecisionAction records work perfor
 acceptance. Creating a DecisionOutcome records factual results and validation evidence for one or
 more linked actions. Creating a DecisionReview records authorized interpretation over an explicit
 ordered outcome set. None of these operations automatically creates learning.
+Only the separate authorized Review-to-Experience promotion use case creates one Experience from
+selected copied Review interpretation; that Experience remains distinct from Knowledge.

 ## Decision model

@@ -436,6 +451,37 @@ is transitive through `DecisionReview → DecisionOutcome[] → DecisionAction[]
 may cover one Decision, outcome, or ordered outcome set under different keys. Corrections append;
 there is no replacement, supersession, deletion, or persisted `current` behavior.

+## DecisionReview-to-Experience promotion foundation
+
+At source commit `12097fe`, `Experience` has optional immutable
+`decision_review_promotion: DecisionReviewPromotion | None`. Plain direct and
+Observation-derived Experiences retain `None`. Promotion contains exactly one Review ID, ordered
+non-empty immutable source statements, promoter, reason, and idempotency key. Each statement stores
+exactly `kind`, zero-based non-negative `index`, and exact copied `text`; kind is exactly `finding`
+or `candidate_lesson`, and `(kind, index)` pairs are unique.
+
+Promoter and key are bounded to 255 characters; reason and copied text are bounded to 1000. All are
+trimmed and non-blank. Reviewer and promoter are separate explicit authorities. Promotion copies no
+Decision, acceptance, action, outcome, reviewer, assessment, confidence, or evidence fields into
+Experience. One Experience references one Review and one or more selected statements; one Review
+and one source statement may produce multiple Experiences under different keys. Corrections append.
+
+The implemented chain is:
+
+```text
+Observation
+→ Decision
+→ DecisionAcceptance
+→ DecisionAction
+→ DecisionOutcome
+→ DecisionReview
+→ explicitly promoted Experience
+→ separately and explicitly created Knowledge
+```
+
+Review save does not promote. Promotion does not create Knowledge or change Decision lifecycle.
+`DecisionReview.assessment`, `DecisionOutcome.result`, and `Experience.result` remain distinct.
+
 ## Persistence

 The persistence-focused `DecisionRepository` port implements only:
@@ -512,6 +558,20 @@ It has no relation, idempotency, chronology, or lifecycle query methods.
 filenames and every record round-trips through domain validation. Filtering, relation validation,
 history ordering, ambiguity detection, and semantic comparison remain in the application service.

+The existing `ExperienceRepository` also remains limited to:
+
+```text
+save()
+load_all()
+get_by_id()
+```
+
+`JsonExperienceRepository` continues to store one JSON file per Experience under
+`NeuralPaths.EXPERIENCES` and round-trips the optional embedded promotion through domain
+validation. Old JSON without the field loads with `None`. No migration, new path, Brain directory,
+link record, promotion repository, second write, or production adapter rewrite was introduced.
+Idempotency and Review integrity remain application policy.
+
 ## Application service

 `DecisionService` implements:
@@ -776,6 +836,40 @@ for a scoped idempotency key must be surfaced, never resolved through `next()`,
 selection, repository order, or comparison with an arbitrarily chosen record. Their scopes and
 ambiguity error types remain separate.

+### ExperienceService Review promotion
+
+`ExperienceService.add_from_decision_review(...)` validates selectors and bounded authority
+metadata before calling `DecisionReviewService.show()`. It then copies caller-ordered exact Review
+items, validates optional Observations, constructs one promoted Experience, loads all Experiences,
+and applies this scope:
+
+```text
+(decision_review_id, "review_experience_promotion", idempotency_key)
+```
+
+```text
+zero matches
+→ save and return one promoted Experience
+
+exactly one equivalent match
+→ validate its provenance and return original ID/timestamp, no write
+
+exactly one different match
+→ `DecisionReviewPromotionIdempotencyConflictError`, no write
+
+more than one match
+→ `DecisionReviewPromotionIdempotencyAmbiguityError`, no selection or comparison, no write
+```
+
+Equivalence excludes only generated `Experience.id` and `Experience.timestamp`; every ordinary
+Experience field, optional Observation ID, tag, and ordered promotion value remains semantic.
+Ambiguity is repository-order independent.
+
+Replay, `get_by_id()`, complete list, and Observation-linked list revalidate the referenced Review
+graph, selector bounds, and exact copied text. Missing or malformed provenance fails closed without
+repair or skipping; plain records bypass promotion validation. The use case owns no Knowledge,
+Playbook, evolution, lifecycle, evidence, or Consigliere behavior.
+
 ### Canonical DecisionLifecycleService

 `DecisionLifecycleService` is the only canonical owner of the current lifecycle projection. It
@@ -836,6 +930,8 @@ JsonDecisionOutcomeRepository
 DecisionOutcomeService
 JsonDecisionReviewRepository
 DecisionReviewService
+JsonExperienceRepository
+ExperienceService
 DecisionLifecycleService
 ```

@@ -851,10 +947,13 @@ receives `JsonDecisionOutcomeRepository` plus Decision, acceptance, and action r
 outcome repositories. `Container.decision_review_repository()` and
 `Container.decision_review_service()` expose the review composition. CLI handlers resolve services
 from the container and construct no repositories.
+`Container.experience_service()` injects `JsonExperienceRepository`,
+`JsonObservationRepository`, and that validated `DecisionReviewService` boundary into
+`ExperienceService`; the container owns no promotion policy.

 ## Implemented CLI

-These commands exist at commit `910f481e`:
+These commands exist at commit `12097fe`:

 ```text
 neural decision add
@@ -872,6 +971,13 @@ neural decision outcome-summary DECISION_UUID
 neural decision review add DECISION_UUID
 neural decision review history DECISION_UUID
 neural decision review show REVIEW_UUID
+neural experience add
+neural experience from-observation OBSERVATION_UUID
+neural experience from-review REVIEW_UUID
+neural experience list
+neural experience show EXPERIENCE_UUID
+neural experience knowledge EXPERIENCE_UUID
+neural observation experiences OBSERVATION_UUID
 neural decision state DECISION_UUID
 ```

@@ -1080,6 +1186,37 @@ and every review field.
 existing Decision with no reviews renders `No review history found for Decision: ...`.
 `neural decision review show REVIEW_UUID` renders every field after persisted relation validation.

+### Review-to-Experience promotion command
+
+`neural experience from-review REVIEW_UUID` requires repeatable ordered `--source`, plus:
+
+```text
+--promoted-by
+--promotion-reason
+--idempotency-key
+--title
+--context
+--action
+--outcome
+--result
+```
+
+Optional repeatable inputs are `--observation-id` and `--tag`. Selectors use exact syntax such as
+`--source finding:1 --source candidate_lesson:2`. CLI ordinals are positive and one-based; they
+become durable zero-based indexes `0` and `1` without caller-supplied text. Invalid selector syntax,
+kind, ordinal, Review, source index, Observation, conflict, ambiguity, or read integrity renders a
+controlled error.
+
+Success and equivalent replay print the stored Experience ID and complete auditable Experience
+details. Promotion source rendering shows kind, user ordinal, stored index, and copied text, plus
+promoter, reason, and key. Reviewer and promoter remain separate authorities.
+
+Ordinary Experience commands keep their existing contracts. Direct `add` requires title, context,
+action, outcome, and result; `from-observation` derives context from the required Observation and
+requires title, action, outcome, and result. Observation IDs and tags remain optional where already
+supported. List, show, Experience-to-Knowledge navigation, and Observation-to-Experience navigation
+remain read-only. Ordinary Experience creation requires no promotion metadata or idempotency key.
+
 `neural decision state DECISION_UUID` renders exactly one of:

 ```text
@@ -1110,10 +1247,12 @@ Decision
 - `DecisionOutcome` is the implemented factual result and validation evidence record.
 - `DecisionReview` is the implemented authorized interpretation over explicit ordered outcomes.

-All five records exist. Records remain immutable semantic records rather than fields on a mutable
+All five decision records and the explicit Review-to-Experience promotion use case exist. Records
+remain immutable semantic records rather than fields on a mutable
 Decision or a duplicate generic event stream. A proposed option is not an acceptance, acceptance
 is not execution, an outcome is not a review or Experience, and review findings or candidate
-lessons are not automatically Experience, Knowledge, or a Playbook change.
+lessons are not Experience until promotion succeeds and are never automatically Knowledge or a
+Playbook change.

 The currently derivable projection is only:

@@ -1156,13 +1295,14 @@ Observation
 → DecisionAction
 → DecisionOutcome
 → DecisionReview
-→ explicitly created Experience
-→ explicitly created Knowledge
+→ explicitly promoted Experience
+→ separately and explicitly created Knowledge
 ```

 DecisionAction may optionally reference an existing PlaybookRun, with existence-only validation
 because PlaybookRun and Playbook expose no project key. `DecisionOutcome` remains distinct from
-Experience, and Decision review must never mutate a Playbook. Any connection from an action to
+Experience. The promotion use case copies selected Review text into optional immutable Experience
+provenance and never mutates a Playbook. Any connection from an action to
 PlaybookEvaluation, EvolutionProposal, or the revision lifecycle requires a separate reviewed use
 case.

@@ -1182,7 +1322,7 @@ prompt
 → post-work lesson
 ```

-Commit `910f481e` does not capture or ingest those events automatically. Automatic candidates and
+Commit `12097fe` does not capture or ingest those events automatically. Automatic candidates and
 manual confirmation remain future concepts; no automatic persistence, ingestion, or learning
 exists.

@@ -1191,7 +1331,7 @@ no recommendation can directly mutate NeuralEngine or authorize a durable record

 ## Current non-behavior

-Commit `910f481e` does not implement:
+Commit `12097fe` does not implement:

 ```text
 execution engine
@@ -1208,6 +1348,7 @@ git ingestion
 automatic Observation creation
 automatic Experience creation
 automatic Knowledge creation
+Experience-to-Knowledge promotion
 automatic Playbook creation or mutation
 automatic evolution
 Consigliere integration
@@ -1216,18 +1357,18 @@ Consigliere integration
 It also does not execute commands referenced by evidence, open locators, automatically accept
 Decisions, materialize Playbook revisions, or infer outcomes from `completed_at`. Explicit user
 requests are required to create Decision, DecisionAcceptance, DecisionAction, DecisionOutcome, or
-DecisionReview records.
+DecisionReview records and to promote Review statements into Experience.

 ## Recommended next milestone

 The recommended next controlled slice is:

 ```text
-separate explicit Experience creation from DecisionReview findings or candidate lessons
+separate explicit Experience-to-Knowledge decision or use case
 ```

 It must preserve explicit authority and remain separate from automatic Knowledge, Playbook,
-PlaybookEvaluation, EvolutionProposal, or Consigliere creation.
+PlaybookEvaluation, EvolutionProposal, lifecycle, or Consigliere behavior.

 ## Handbook synchronization policy

@@ -1288,18 +1429,19 @@ Observation
 → DecisionAction
 → DecisionOutcome
 → DecisionReview
-→ explicitly created Experience
-→ explicitly created Knowledge
+→ explicitly promoted Experience
+→ separately and explicitly created Knowledge
 ```

 This is a complementary provenance path, not a replacement for the canonical domain chain.
 DecisionOutcome is factual; DecisionReview is authorized interpretation; Experience captures
-separately created operational learning; Knowledge is generalized; Playbook remains a separately
-created repeatable procedure. A Decision may have multiple immutable outcomes and multiple reviews,
-including reviews over the same ordered outcome set when their idempotency keys differ. Review
-action provenance is transitive through its explicit outcomes; it does not persist action IDs.
-These records and their embedded EvidenceReference values exist at source commit `910f481e`; no
-Review-driven lifecycle transition or later learning record in this path is automatic.
+explicitly promoted operational learning; Knowledge is separately generalized; Playbook remains a
+separately created repeatable procedure. A Decision may have multiple immutable outcomes and
+reviews, and one Review may explicitly produce multiple Experiences under different promotion
+keys. A promoted Experience selects ordered Review statements and cannot combine Reviews. Review
+action provenance remains transitive through explicit outcomes; promoted Experience provenance
+remains transitive through its one Review. These records exist at source commit `12097fe`; no
+Review save, promotion, lifecycle transition, or later Knowledge record in this path is automatic.

 ## Workflow

diff --git a/outputs/generated/AGENTS.generated.md b/outputs/generated/AGENTS.generated.md
index 31bc748..db1a914 100644
--- a/outputs/generated/AGENTS.generated.md
+++ b/outputs/generated/AGENTS.generated.md
@@ -137,7 +137,7 @@ a milestone snapshot, not a timeless guarantee.

 ## Decision Learning boundary

-Source commit `910f481e27302daa6d3f15bde30d678ffc9e5d2f` implements separate immutable
+Source commit `12097feb0159cc8e8831000ab04c290b56ecfc8e` implements separate immutable
 `Decision`, `DecisionAcceptance`, `DecisionAction`, `DecisionOutcome`, and `DecisionReview`
 records, persistence-focused ports and JSON adapters, application services, container wiring,
 thin proposal/acceptance/action/outcome/review CLI commands, and the canonical
@@ -151,13 +151,21 @@ the latest outcome using `(validated_at, outcome.id)` rather than repository ord
 `DecisionReview` targets an explicit ordered non-empty set of outcomes for one Decision and
 acceptance. Multiple reviews form immutable history ordered by `(reviewed_at, review.id)`.

+The same checkpoint implements explicit Review-to-Experience promotion. One Experience may embed
+optional immutable `DecisionReviewPromotion` provenance containing ordered copied Review
+statements. `ExperienceService` uses the validated Review service boundary and existing Experience
+repository; no promotion aggregate, repository, adapter, path, Brain collection, or automatic
+learning exists. Old and ordinary Experiences remain compatible.
+
 The canonical lifecycle states remain exactly `proposed`, `accepted`, `in_progress`, `succeeded`,
 `failed`, `partial`, and `outcome_unknown`. Review is orthogonal append-only history; there is no
-`reviewed` state. Outcome or review creation does not create learning. There is no execution
-engine, lifecycle reversal, ingestion, automatic learning or evolution, generic event replay, or
+`reviewed`, `promoted`, or `learned` state. Outcome or review creation does not create learning;
+only the explicit promotion use case creates an Experience, which remains distinct from Knowledge.
+There is no execution engine, lifecycle reversal, ingestion, automatic learning or evolution,
+generic event replay, or
 Consigliere integration. The authoritative implemented contract and future boundary are defined
-in `handbook/architecture/decision-learning.md`; the recommended next controlled slice is
-separate explicit Experience creation from review findings or candidate lessons.
+in `handbook/architecture/decision-learning.md`; the next controlled downstream step remains a
+separate explicit Experience-to-Knowledge decision or use case.

 ## Agent policy

diff --git a/outputs/generated/APPLICATION_ARCHITECTURE.md b/outputs/generated/APPLICATION_ARCHITECTURE.md
index 195c578..9d9ddd5 100644
--- a/outputs/generated/APPLICATION_ARCHITECTURE.md
+++ b/outputs/generated/APPLICATION_ARCHITECTURE.md
@@ -169,6 +169,33 @@ application-service invariant: more than one persisted match for a scoped key is
 ambiguity to surface, never an ordering problem to resolve by choosing the first record. Their
 scopes and controlled ambiguity error types remain separate.

+## DecisionReview-to-Experience promotion ownership
+
+`ExperienceService.add_from_decision_review(...)` is the one implemented explicit promotion use
+case. It validates selectors and bounded promoter/reason/key metadata before relation reads, calls
+the existing validated `DecisionReviewService.show(review_id)` boundary, validates ordered finding
+and candidate-lesson indexes, copies exact Review text, validates optional Observation IDs,
+constructs one Experience, then loads Experiences for application-layer idempotency. Only a fully
+validated zero-match candidate is saved.
+
+The scope is `(decision_review_id, "review_experience_promotion", idempotency_key)`. Exactly one
+equivalent match returns the original Experience identity and timestamp without writing; exactly
+one different match raises `DecisionReviewPromotionIdempotencyConflictError`; more than one match
+raises `DecisionReviewPromotionIdempotencyAmbiguityError` without repository-order selection or
+arbitrary semantic comparison. Semantic equivalence excludes only generated Experience ID and
+timestamp and includes every caller-supplied Experience and ordered promotion field.
+
+Equivalent replay validates the existing provenance. `get_by_id()`, `list_experiences()`, and
+`list_for_observation()` also fail closed for promoted records when the Review graph is invalid, an
+index is out of range, or copied text differs. Plain Experience reads remain unaffected. Direct and
+Observation-derived `add` paths keep their existing inputs and do not acquire idempotency or
+promotion requirements.
+
+One Review may produce multiple Experiences under different keys, and the same statement may be
+promoted repeatedly. Each Experience references only one Review. Corrections append; no promotion
+replacement, ranking, deletion, lifecycle state, Knowledge creation, or Consigliere behavior is
+owned here.
+
 ---

 # Application Errors
@@ -298,6 +325,11 @@ Decision filtering, cross-record validation, history ordering, and scoped idempo
 fail-closed duplicate-match ambiguity—belong to `DecisionReviewService`; no relation,
 idempotency, chronology, or lifecycle query method is part of the port.

+`ExperienceRepository` remains limited to `save()`, `load_all()`, and `get_by_id()` for both plain
+and promoted Experiences. Review validation, copied-text integrity, Observation validation, and
+`(decision_review_id, "review_experience_promotion", idempotency_key)` scanning belong to
+`ExperienceService`; no promotion, relation, or idempotency query belongs to the port.
+
 ## Repository return types

 Prefer:
@@ -443,6 +475,17 @@ DecisionReview records round-trip through domain validation. JSON object keys ar
 validation errors. The adapter performs no Decision filtering, relation validation, chronology,
 idempotency selection, lifecycle projection, evidence ingestion, learning, or Consigliere work.

+## Experience adapter and promotion compatibility
+
+`JsonExperienceRepository` continues to implement the unchanged `ExperienceRepository` under
+`NeuralPaths.EXPERIENCES`, storing one JSON file per Experience and sorting filenames for
+deterministic `load_all()`. Domain validation round-trips both ordinary records and the optional
+embedded `DecisionReviewPromotion`. Old JSON without that field loads with `None` and remains plain.
+
+No migration or production adapter rewrite was required. The adapter performs no Review lookup,
+source copying, integrity repair, idempotency decision, promotion policy, second write, or inferred
+provenance. No promotion adapter, repository, path, or Brain directory exists.
+
 ---

 # Dependency Injection and Container
@@ -522,6 +565,12 @@ The review foundation is wired through `Container.decision_review_repository()`
 `JsonDecisionOutcomeRepository`. Brain initialization creates `NeuralPaths.DECISION_REVIEWS`.
 Decision review CLI handlers resolve the service and construct no repositories.

+`Container.experience_service()` supplies `JsonExperienceRepository`,
+`JsonObservationRepository`, and the existing validated `DecisionReviewService` boundary to
+`ExperienceService`. The container adds no promotion policy, link repository, path, or lifecycle
+behavior; `neural experience from-review` resolves this service like the ordinary Experience
+commands.
+
 ---

 # Dependency Lifecycle
diff --git a/outputs/generated/DECISION_ENGINE.md b/outputs/generated/DECISION_ENGINE.md
index fecf8bd..9ace2d5 100644
--- a/outputs/generated/DECISION_ENGINE.md
+++ b/outputs/generated/DECISION_ENGINE.md
@@ -104,12 +104,13 @@ New behavior

 ## Status and purpose

-NeuralEngine source commit `910f481e27302daa6d3f15bde30d678ffc9e5d2f` implements the Decision,
+NeuralEngine source commit `12097feb0159cc8e8831000ab04c290b56ecfc8e` implements the Decision,
 DecisionAcceptance, DecisionAction, DecisionOutcome, and DecisionReview foundations plus the
 canonical `DecisionLifecycleService` projection. They record an immutable proposed choice,
 explicit authorization, work performed under that authorization, factual results, and authorized
-interpretation. Each foundation persists immutable records, exposes application use cases, is
-wired through the container, and provides a thin CLI.
+interpretation, plus explicit promotion of selected Review statements into an existing Experience.
+Each foundation persists its durable records, exposes application use cases, is wired through the
+container, and provides a thin CLI.

 The wider Decision Learning lifecycle remains accepted future architecture. Decision tracking
 complements the existing Observation-to-Playbook chain; it does not replace it.
@@ -125,6 +126,8 @@ DecisionAcceptance
 DecisionAction
 DecisionOutcome
 DecisionReview
+DecisionReviewPromotion
+DecisionReviewPromotionSourceStatement
 DecisionRepository
 DecisionAcceptanceRepository
 DecisionActionRepository
@@ -141,6 +144,7 @@ DecisionActionService
 DecisionOutcomeService
 DecisionOutcomeSummary
 DecisionReviewService
+ExperienceService.add_from_decision_review
 DecisionLifecycleService
 container wiring
 neural decision add/list/show
@@ -156,6 +160,7 @@ neural decision outcome-summary
 neural decision review add
 neural decision review history
 neural decision review show
+neural experience from-review
 neural decision state
 ```

@@ -164,6 +169,8 @@ proposal for possible future work. Creating a DecisionAction records work perfor
 acceptance. Creating a DecisionOutcome records factual results and validation evidence for one or
 more linked actions. Creating a DecisionReview records authorized interpretation over an explicit
 ordered outcome set. None of these operations automatically creates learning.
+Only the separate authorized Review-to-Experience promotion use case creates one Experience from
+selected copied Review interpretation; that Experience remains distinct from Knowledge.

 ## Decision model

@@ -394,6 +401,37 @@ is transitive through `DecisionReview → DecisionOutcome[] → DecisionAction[]
 may cover one Decision, outcome, or ordered outcome set under different keys. Corrections append;
 there is no replacement, supersession, deletion, or persisted `current` behavior.

+## DecisionReview-to-Experience promotion foundation
+
+At source commit `12097fe`, `Experience` has optional immutable
+`decision_review_promotion: DecisionReviewPromotion | None`. Plain direct and
+Observation-derived Experiences retain `None`. Promotion contains exactly one Review ID, ordered
+non-empty immutable source statements, promoter, reason, and idempotency key. Each statement stores
+exactly `kind`, zero-based non-negative `index`, and exact copied `text`; kind is exactly `finding`
+or `candidate_lesson`, and `(kind, index)` pairs are unique.
+
+Promoter and key are bounded to 255 characters; reason and copied text are bounded to 1000. All are
+trimmed and non-blank. Reviewer and promoter are separate explicit authorities. Promotion copies no
+Decision, acceptance, action, outcome, reviewer, assessment, confidence, or evidence fields into
+Experience. One Experience references one Review and one or more selected statements; one Review
+and one source statement may produce multiple Experiences under different keys. Corrections append.
+
+The implemented chain is:
+
+```text
+Observation
+→ Decision
+→ DecisionAcceptance
+→ DecisionAction
+→ DecisionOutcome
+→ DecisionReview
+→ explicitly promoted Experience
+→ separately and explicitly created Knowledge
+```
+
+Review save does not promote. Promotion does not create Knowledge or change Decision lifecycle.
+`DecisionReview.assessment`, `DecisionOutcome.result`, and `Experience.result` remain distinct.
+
 ## Persistence

 The persistence-focused `DecisionRepository` port implements only:
@@ -470,6 +508,20 @@ It has no relation, idempotency, chronology, or lifecycle query methods.
 filenames and every record round-trips through domain validation. Filtering, relation validation,
 history ordering, ambiguity detection, and semantic comparison remain in the application service.

+The existing `ExperienceRepository` also remains limited to:
+
+```text
+save()
+load_all()
+get_by_id()
+```
+
+`JsonExperienceRepository` continues to store one JSON file per Experience under
+`NeuralPaths.EXPERIENCES` and round-trips the optional embedded promotion through domain
+validation. Old JSON without the field loads with `None`. No migration, new path, Brain directory,
+link record, promotion repository, second write, or production adapter rewrite was introduced.
+Idempotency and Review integrity remain application policy.
+
 ## Application service

 `DecisionService` implements:
@@ -734,6 +786,40 @@ for a scoped idempotency key must be surfaced, never resolved through `next()`,
 selection, repository order, or comparison with an arbitrarily chosen record. Their scopes and
 ambiguity error types remain separate.

+### ExperienceService Review promotion
+
+`ExperienceService.add_from_decision_review(...)` validates selectors and bounded authority
+metadata before calling `DecisionReviewService.show()`. It then copies caller-ordered exact Review
+items, validates optional Observations, constructs one promoted Experience, loads all Experiences,
+and applies this scope:
+
+```text
+(decision_review_id, "review_experience_promotion", idempotency_key)
+```
+
+```text
+zero matches
+→ save and return one promoted Experience
+
+exactly one equivalent match
+→ validate its provenance and return original ID/timestamp, no write
+
+exactly one different match
+→ `DecisionReviewPromotionIdempotencyConflictError`, no write
+
+more than one match
+→ `DecisionReviewPromotionIdempotencyAmbiguityError`, no selection or comparison, no write
+```
+
+Equivalence excludes only generated `Experience.id` and `Experience.timestamp`; every ordinary
+Experience field, optional Observation ID, tag, and ordered promotion value remains semantic.
+Ambiguity is repository-order independent.
+
+Replay, `get_by_id()`, complete list, and Observation-linked list revalidate the referenced Review
+graph, selector bounds, and exact copied text. Missing or malformed provenance fails closed without
+repair or skipping; plain records bypass promotion validation. The use case owns no Knowledge,
+Playbook, evolution, lifecycle, evidence, or Consigliere behavior.
+
 ### Canonical DecisionLifecycleService

 `DecisionLifecycleService` is the only canonical owner of the current lifecycle projection. It
@@ -794,6 +880,8 @@ JsonDecisionOutcomeRepository
 DecisionOutcomeService
 JsonDecisionReviewRepository
 DecisionReviewService
+JsonExperienceRepository
+ExperienceService
 DecisionLifecycleService
 ```

@@ -809,10 +897,13 @@ receives `JsonDecisionOutcomeRepository` plus Decision, acceptance, and action r
 outcome repositories. `Container.decision_review_repository()` and
 `Container.decision_review_service()` expose the review composition. CLI handlers resolve services
 from the container and construct no repositories.
+`Container.experience_service()` injects `JsonExperienceRepository`,
+`JsonObservationRepository`, and that validated `DecisionReviewService` boundary into
+`ExperienceService`; the container owns no promotion policy.

 ## Implemented CLI

-These commands exist at commit `910f481e`:
+These commands exist at commit `12097fe`:

 ```text
 neural decision add
@@ -830,6 +921,13 @@ neural decision outcome-summary DECISION_UUID
 neural decision review add DECISION_UUID
 neural decision review history DECISION_UUID
 neural decision review show REVIEW_UUID
+neural experience add
+neural experience from-observation OBSERVATION_UUID
+neural experience from-review REVIEW_UUID
+neural experience list
+neural experience show EXPERIENCE_UUID
+neural experience knowledge EXPERIENCE_UUID
+neural observation experiences OBSERVATION_UUID
 neural decision state DECISION_UUID
 ```

@@ -1038,6 +1136,37 @@ and every review field.
 existing Decision with no reviews renders `No review history found for Decision: ...`.
 `neural decision review show REVIEW_UUID` renders every field after persisted relation validation.

+### Review-to-Experience promotion command
+
+`neural experience from-review REVIEW_UUID` requires repeatable ordered `--source`, plus:
+
+```text
+--promoted-by
+--promotion-reason
+--idempotency-key
+--title
+--context
+--action
+--outcome
+--result
+```
+
+Optional repeatable inputs are `--observation-id` and `--tag`. Selectors use exact syntax such as
+`--source finding:1 --source candidate_lesson:2`. CLI ordinals are positive and one-based; they
+become durable zero-based indexes `0` and `1` without caller-supplied text. Invalid selector syntax,
+kind, ordinal, Review, source index, Observation, conflict, ambiguity, or read integrity renders a
+controlled error.
+
+Success and equivalent replay print the stored Experience ID and complete auditable Experience
+details. Promotion source rendering shows kind, user ordinal, stored index, and copied text, plus
+promoter, reason, and key. Reviewer and promoter remain separate authorities.
+
+Ordinary Experience commands keep their existing contracts. Direct `add` requires title, context,
+action, outcome, and result; `from-observation` derives context from the required Observation and
+requires title, action, outcome, and result. Observation IDs and tags remain optional where already
+supported. List, show, Experience-to-Knowledge navigation, and Observation-to-Experience navigation
+remain read-only. Ordinary Experience creation requires no promotion metadata or idempotency key.
+
 `neural decision state DECISION_UUID` renders exactly one of:

 ```text
@@ -1068,10 +1197,12 @@ Decision
 - `DecisionOutcome` is the implemented factual result and validation evidence record.
 - `DecisionReview` is the implemented authorized interpretation over explicit ordered outcomes.

-All five records exist. Records remain immutable semantic records rather than fields on a mutable
+All five decision records and the explicit Review-to-Experience promotion use case exist. Records
+remain immutable semantic records rather than fields on a mutable
 Decision or a duplicate generic event stream. A proposed option is not an acceptance, acceptance
 is not execution, an outcome is not a review or Experience, and review findings or candidate
-lessons are not automatically Experience, Knowledge, or a Playbook change.
+lessons are not Experience until promotion succeeds and are never automatically Knowledge or a
+Playbook change.

 The currently derivable projection is only:

@@ -1114,13 +1245,14 @@ Observation
 → DecisionAction
 → DecisionOutcome
 → DecisionReview
-→ explicitly created Experience
-→ explicitly created Knowledge
+→ explicitly promoted Experience
+→ separately and explicitly created Knowledge
 ```

 DecisionAction may optionally reference an existing PlaybookRun, with existence-only validation
 because PlaybookRun and Playbook expose no project key. `DecisionOutcome` remains distinct from
-Experience, and Decision review must never mutate a Playbook. Any connection from an action to
+Experience. The promotion use case copies selected Review text into optional immutable Experience
+provenance and never mutates a Playbook. Any connection from an action to
 PlaybookEvaluation, EvolutionProposal, or the revision lifecycle requires a separate reviewed use
 case.

@@ -1140,7 +1272,7 @@ prompt
 → post-work lesson
 ```

-Commit `910f481e` does not capture or ingest those events automatically. Automatic candidates and
+Commit `12097fe` does not capture or ingest those events automatically. Automatic candidates and
 manual confirmation remain future concepts; no automatic persistence, ingestion, or learning
 exists.

@@ -1149,7 +1281,7 @@ no recommendation can directly mutate NeuralEngine or authorize a durable record

 ## Current non-behavior

-Commit `910f481e` does not implement:
+Commit `12097fe` does not implement:

 ```text
 execution engine
@@ -1166,6 +1298,7 @@ git ingestion
 automatic Observation creation
 automatic Experience creation
 automatic Knowledge creation
+Experience-to-Knowledge promotion
 automatic Playbook creation or mutation
 automatic evolution
 Consigliere integration
@@ -1174,18 +1307,18 @@ Consigliere integration
 It also does not execute commands referenced by evidence, open locators, automatically accept
 Decisions, materialize Playbook revisions, or infer outcomes from `completed_at`. Explicit user
 requests are required to create Decision, DecisionAcceptance, DecisionAction, DecisionOutcome, or
-DecisionReview records.
+DecisionReview records and to promote Review statements into Experience.

 ## Recommended next milestone

 The recommended next controlled slice is:

 ```text
-separate explicit Experience creation from DecisionReview findings or candidate lessons
+separate explicit Experience-to-Knowledge decision or use case
 ```

 It must preserve explicit authority and remain separate from automatic Knowledge, Playbook,
-PlaybookEvaluation, EvolutionProposal, or Consigliere creation.
+PlaybookEvaluation, EvolutionProposal, lifecycle, or Consigliere behavior.

 ## Handbook synchronization policy

@@ -1313,6 +1446,11 @@ authorized interpretation over an explicit ordered outcome set. Lifecycle state
 acceptance, actions, and the latest factual outcome, not stored as mutable status or duplicated in
 a generic event stream. Review is orthogonal append-only history.

+Selected Review interpretation becomes Experience only through an explicit authorized use case.
+Promotion provenance is embedded immutably in the existing Experience rather than represented by
+a link aggregate, second write, new repository, or new lifecycle state. Experience-to-Knowledge
+remains a separate explicit decision.
+
 Decision tracking complements the existing Observation-to-Playbook chain. Evidence uses bounded
 embedded references, durable writes require explicit authority, and Consigliere remains a future
 advisory layer rather than authoritative storage.
@@ -1325,9 +1463,12 @@ advisory layer rather than authoritative storage.
   idempotency checks; repository ports remain persistence-focused.
 - No automatic ingestion, persistence, learning, Playbook evolution, or Consigliere integration is
   implied.
-- Source commit `910f481e27302daa6d3f15bde30d678ffc9e5d2f` implements Decision proposal,
+- Source commit `12097feb0159cc8e8831000ab04c290b56ecfc8e` implements Decision proposal,
   acceptance, action, outcome, and review recording; outcome history/summary; review history; their
   CLI; and the canonical `DecisionLifecycleService`.
+- The same checkpoint implements explicit ordered DecisionReview statement promotion into one
+  existing Experience with embedded immutable provenance, fail-closed read integrity, and scoped
+  application-layer idempotency. It does not implement automatic learning.
 - The canonical states are exactly proposed, accepted, in-progress, succeeded, failed, partial,
   and outcome-unknown. Latest outcome selection uses validation time and outcome UUID, not
   repository order. No generic completed, resolved, or reviewed state exists.
@@ -1341,6 +1482,10 @@ advisory layer rather than authoritative storage.
 - Outcome and review idempotency both fail closed when more than one persisted record matches a
   scoped key: their distinct ambiguity errors replace arbitrary first-match selection and no write
   occurs regardless of repository order or payload equivalence.
-- The recommended next controlled slice is separate explicit Experience creation from review
-  findings or candidate lessons; downstream Experience, Knowledge, or Playbook creation remains
-  explicit.
+- A Review may produce multiple Experiences under distinct keys, but one promoted Experience
+  references exactly one Review. Corrections append and ordinary Experience remains compatible.
+- Automatic promotion and a separate promotion/link aggregate were rejected because authority and
+  provenance belong in one explicit Experience write. Repository-order duplicate selection was
+  rejected in favor of a dedicated fail-closed ambiguity error.
+- The next controlled downstream step remains a separate explicit Experience-to-Knowledge decision
+  or use case; Knowledge, Playbook, and evolution creation remain explicit.
diff --git a/outputs/generated/HANDBOOK.md b/outputs/generated/HANDBOOK.md
index 4bcad1e..afee8a9 100644
--- a/outputs/generated/HANDBOOK.md
+++ b/outputs/generated/HANDBOOK.md
@@ -103,7 +103,7 @@ a milestone snapshot, not a timeless guarantee.

 ## Decision Learning boundary

-Source commit `910f481e27302daa6d3f15bde30d678ffc9e5d2f` implements separate immutable
+Source commit `12097feb0159cc8e8831000ab04c290b56ecfc8e` implements separate immutable
 `Decision`, `DecisionAcceptance`, `DecisionAction`, `DecisionOutcome`, and `DecisionReview`
 records, persistence-focused ports and JSON adapters, application services, container wiring,
 thin proposal/acceptance/action/outcome/review CLI commands, and the canonical
@@ -117,13 +117,21 @@ the latest outcome using `(validated_at, outcome.id)` rather than repository ord
 `DecisionReview` targets an explicit ordered non-empty set of outcomes for one Decision and
 acceptance. Multiple reviews form immutable history ordered by `(reviewed_at, review.id)`.

+The same checkpoint implements explicit Review-to-Experience promotion. One Experience may embed
+optional immutable `DecisionReviewPromotion` provenance containing ordered copied Review
+statements. `ExperienceService` uses the validated Review service boundary and existing Experience
+repository; no promotion aggregate, repository, adapter, path, Brain collection, or automatic
+learning exists. Old and ordinary Experiences remain compatible.
+
 The canonical lifecycle states remain exactly `proposed`, `accepted`, `in_progress`, `succeeded`,
 `failed`, `partial`, and `outcome_unknown`. Review is orthogonal append-only history; there is no
-`reviewed` state. Outcome or review creation does not create learning. There is no execution
-engine, lifecycle reversal, ingestion, automatic learning or evolution, generic event replay, or
+`reviewed`, `promoted`, or `learned` state. Outcome or review creation does not create learning;
+only the explicit promotion use case creates an Experience, which remains distinct from Knowledge.
+There is no execution engine, lifecycle reversal, ingestion, automatic learning or evolution,
+generic event replay, or
 Consigliere integration. The authoritative implemented contract and future boundary are defined
-in `handbook/architecture/decision-learning.md`; the recommended next controlled slice is
-separate explicit Experience creation from review findings or candidate lessons.
+in `handbook/architecture/decision-learning.md`; the next controlled downstream step remains a
+separate explicit Experience-to-Knowledge decision or use case.

 ---

@@ -131,12 +139,13 @@ separate explicit Experience creation from review findings or candidate lessons.

 ## Status and purpose

-NeuralEngine source commit `910f481e27302daa6d3f15bde30d678ffc9e5d2f` implements the Decision,
+NeuralEngine source commit `12097feb0159cc8e8831000ab04c290b56ecfc8e` implements the Decision,
 DecisionAcceptance, DecisionAction, DecisionOutcome, and DecisionReview foundations plus the
 canonical `DecisionLifecycleService` projection. They record an immutable proposed choice,
 explicit authorization, work performed under that authorization, factual results, and authorized
-interpretation. Each foundation persists immutable records, exposes application use cases, is
-wired through the container, and provides a thin CLI.
+interpretation, plus explicit promotion of selected Review statements into an existing Experience.
+Each foundation persists its durable records, exposes application use cases, is wired through the
+container, and provides a thin CLI.

 The wider Decision Learning lifecycle remains accepted future architecture. Decision tracking
 complements the existing Observation-to-Playbook chain; it does not replace it.
@@ -152,6 +161,8 @@ DecisionAcceptance
 DecisionAction
 DecisionOutcome
 DecisionReview
+DecisionReviewPromotion
+DecisionReviewPromotionSourceStatement
 DecisionRepository
 DecisionAcceptanceRepository
 DecisionActionRepository
@@ -168,6 +179,7 @@ DecisionActionService
 DecisionOutcomeService
 DecisionOutcomeSummary
 DecisionReviewService
+ExperienceService.add_from_decision_review
 DecisionLifecycleService
 container wiring
 neural decision add/list/show
@@ -183,6 +195,7 @@ neural decision outcome-summary
 neural decision review add
 neural decision review history
 neural decision review show
+neural experience from-review
 neural decision state
 ```

@@ -191,6 +204,8 @@ proposal for possible future work. Creating a DecisionAction records work perfor
 acceptance. Creating a DecisionOutcome records factual results and validation evidence for one or
 more linked actions. Creating a DecisionReview records authorized interpretation over an explicit
 ordered outcome set. None of these operations automatically creates learning.
+Only the separate authorized Review-to-Experience promotion use case creates one Experience from
+selected copied Review interpretation; that Experience remains distinct from Knowledge.

 ## Decision model

@@ -421,6 +436,37 @@ is transitive through `DecisionReview → DecisionOutcome[] → DecisionAction[]
 may cover one Decision, outcome, or ordered outcome set under different keys. Corrections append;
 there is no replacement, supersession, deletion, or persisted `current` behavior.

+## DecisionReview-to-Experience promotion foundation
+
+At source commit `12097fe`, `Experience` has optional immutable
+`decision_review_promotion: DecisionReviewPromotion | None`. Plain direct and
+Observation-derived Experiences retain `None`. Promotion contains exactly one Review ID, ordered
+non-empty immutable source statements, promoter, reason, and idempotency key. Each statement stores
+exactly `kind`, zero-based non-negative `index`, and exact copied `text`; kind is exactly `finding`
+or `candidate_lesson`, and `(kind, index)` pairs are unique.
+
+Promoter and key are bounded to 255 characters; reason and copied text are bounded to 1000. All are
+trimmed and non-blank. Reviewer and promoter are separate explicit authorities. Promotion copies no
+Decision, acceptance, action, outcome, reviewer, assessment, confidence, or evidence fields into
+Experience. One Experience references one Review and one or more selected statements; one Review
+and one source statement may produce multiple Experiences under different keys. Corrections append.
+
+The implemented chain is:
+
+```text
+Observation
+→ Decision
+→ DecisionAcceptance
+→ DecisionAction
+→ DecisionOutcome
+→ DecisionReview
+→ explicitly promoted Experience
+→ separately and explicitly created Knowledge
+```
+
+Review save does not promote. Promotion does not create Knowledge or change Decision lifecycle.
+`DecisionReview.assessment`, `DecisionOutcome.result`, and `Experience.result` remain distinct.
+
 ## Persistence

 The persistence-focused `DecisionRepository` port implements only:
@@ -497,6 +543,20 @@ It has no relation, idempotency, chronology, or lifecycle query methods.
 filenames and every record round-trips through domain validation. Filtering, relation validation,
 history ordering, ambiguity detection, and semantic comparison remain in the application service.

+The existing `ExperienceRepository` also remains limited to:
+
+```text
+save()
+load_all()
+get_by_id()
+```
+
+`JsonExperienceRepository` continues to store one JSON file per Experience under
+`NeuralPaths.EXPERIENCES` and round-trips the optional embedded promotion through domain
+validation. Old JSON without the field loads with `None`. No migration, new path, Brain directory,
+link record, promotion repository, second write, or production adapter rewrite was introduced.
+Idempotency and Review integrity remain application policy.
+
 ## Application service

 `DecisionService` implements:
@@ -761,6 +821,40 @@ for a scoped idempotency key must be surfaced, never resolved through `next()`,
 selection, repository order, or comparison with an arbitrarily chosen record. Their scopes and
 ambiguity error types remain separate.

+### ExperienceService Review promotion
+
+`ExperienceService.add_from_decision_review(...)` validates selectors and bounded authority
+metadata before calling `DecisionReviewService.show()`. It then copies caller-ordered exact Review
+items, validates optional Observations, constructs one promoted Experience, loads all Experiences,
+and applies this scope:
+
+```text
+(decision_review_id, "review_experience_promotion", idempotency_key)
+```
+
+```text
+zero matches
+→ save and return one promoted Experience
+
+exactly one equivalent match
+→ validate its provenance and return original ID/timestamp, no write
+
+exactly one different match
+→ `DecisionReviewPromotionIdempotencyConflictError`, no write
+
+more than one match
+→ `DecisionReviewPromotionIdempotencyAmbiguityError`, no selection or comparison, no write
+```
+
+Equivalence excludes only generated `Experience.id` and `Experience.timestamp`; every ordinary
+Experience field, optional Observation ID, tag, and ordered promotion value remains semantic.
+Ambiguity is repository-order independent.
+
+Replay, `get_by_id()`, complete list, and Observation-linked list revalidate the referenced Review
+graph, selector bounds, and exact copied text. Missing or malformed provenance fails closed without
+repair or skipping; plain records bypass promotion validation. The use case owns no Knowledge,
+Playbook, evolution, lifecycle, evidence, or Consigliere behavior.
+
 ### Canonical DecisionLifecycleService

 `DecisionLifecycleService` is the only canonical owner of the current lifecycle projection. It
@@ -821,6 +915,8 @@ JsonDecisionOutcomeRepository
 DecisionOutcomeService
 JsonDecisionReviewRepository
 DecisionReviewService
+JsonExperienceRepository
+ExperienceService
 DecisionLifecycleService
 ```

@@ -836,10 +932,13 @@ receives `JsonDecisionOutcomeRepository` plus Decision, acceptance, and action r
 outcome repositories. `Container.decision_review_repository()` and
 `Container.decision_review_service()` expose the review composition. CLI handlers resolve services
 from the container and construct no repositories.
+`Container.experience_service()` injects `JsonExperienceRepository`,
+`JsonObservationRepository`, and that validated `DecisionReviewService` boundary into
+`ExperienceService`; the container owns no promotion policy.

 ## Implemented CLI

-These commands exist at commit `910f481e`:
+These commands exist at commit `12097fe`:

 ```text
 neural decision add
@@ -857,6 +956,13 @@ neural decision outcome-summary DECISION_UUID
 neural decision review add DECISION_UUID
 neural decision review history DECISION_UUID
 neural decision review show REVIEW_UUID
+neural experience add
+neural experience from-observation OBSERVATION_UUID
+neural experience from-review REVIEW_UUID
+neural experience list
+neural experience show EXPERIENCE_UUID
+neural experience knowledge EXPERIENCE_UUID
+neural observation experiences OBSERVATION_UUID
 neural decision state DECISION_UUID
 ```

@@ -1065,6 +1171,37 @@ and every review field.
 existing Decision with no reviews renders `No review history found for Decision: ...`.
 `neural decision review show REVIEW_UUID` renders every field after persisted relation validation.

+### Review-to-Experience promotion command
+
+`neural experience from-review REVIEW_UUID` requires repeatable ordered `--source`, plus:
+
+```text
+--promoted-by
+--promotion-reason
+--idempotency-key
+--title
+--context
+--action
+--outcome
+--result
+```
+
+Optional repeatable inputs are `--observation-id` and `--tag`. Selectors use exact syntax such as
+`--source finding:1 --source candidate_lesson:2`. CLI ordinals are positive and one-based; they
+become durable zero-based indexes `0` and `1` without caller-supplied text. Invalid selector syntax,
+kind, ordinal, Review, source index, Observation, conflict, ambiguity, or read integrity renders a
+controlled error.
+
+Success and equivalent replay print the stored Experience ID and complete auditable Experience
+details. Promotion source rendering shows kind, user ordinal, stored index, and copied text, plus
+promoter, reason, and key. Reviewer and promoter remain separate authorities.
+
+Ordinary Experience commands keep their existing contracts. Direct `add` requires title, context,
+action, outcome, and result; `from-observation` derives context from the required Observation and
+requires title, action, outcome, and result. Observation IDs and tags remain optional where already
+supported. List, show, Experience-to-Knowledge navigation, and Observation-to-Experience navigation
+remain read-only. Ordinary Experience creation requires no promotion metadata or idempotency key.
+
 `neural decision state DECISION_UUID` renders exactly one of:

 ```text
@@ -1095,10 +1232,12 @@ Decision
 - `DecisionOutcome` is the implemented factual result and validation evidence record.
 - `DecisionReview` is the implemented authorized interpretation over explicit ordered outcomes.

-All five records exist. Records remain immutable semantic records rather than fields on a mutable
+All five decision records and the explicit Review-to-Experience promotion use case exist. Records
+remain immutable semantic records rather than fields on a mutable
 Decision or a duplicate generic event stream. A proposed option is not an acceptance, acceptance
 is not execution, an outcome is not a review or Experience, and review findings or candidate
-lessons are not automatically Experience, Knowledge, or a Playbook change.
+lessons are not Experience until promotion succeeds and are never automatically Knowledge or a
+Playbook change.

 The currently derivable projection is only:

@@ -1141,13 +1280,14 @@ Observation
 → DecisionAction
 → DecisionOutcome
 → DecisionReview
-→ explicitly created Experience
-→ explicitly created Knowledge
+→ explicitly promoted Experience
+→ separately and explicitly created Knowledge
 ```

 DecisionAction may optionally reference an existing PlaybookRun, with existence-only validation
 because PlaybookRun and Playbook expose no project key. `DecisionOutcome` remains distinct from
-Experience, and Decision review must never mutate a Playbook. Any connection from an action to
+Experience. The promotion use case copies selected Review text into optional immutable Experience
+provenance and never mutates a Playbook. Any connection from an action to
 PlaybookEvaluation, EvolutionProposal, or the revision lifecycle requires a separate reviewed use
 case.

@@ -1167,7 +1307,7 @@ prompt
 → post-work lesson
 ```

-Commit `910f481e` does not capture or ingest those events automatically. Automatic candidates and
+Commit `12097fe` does not capture or ingest those events automatically. Automatic candidates and
 manual confirmation remain future concepts; no automatic persistence, ingestion, or learning
 exists.

@@ -1176,7 +1316,7 @@ no recommendation can directly mutate NeuralEngine or authorize a durable record

 ## Current non-behavior

-Commit `910f481e` does not implement:
+Commit `12097fe` does not implement:

 ```text
 execution engine
@@ -1193,6 +1333,7 @@ git ingestion
 automatic Observation creation
 automatic Experience creation
 automatic Knowledge creation
+Experience-to-Knowledge promotion
 automatic Playbook creation or mutation
 automatic evolution
 Consigliere integration
@@ -1201,18 +1342,18 @@ Consigliere integration
 It also does not execute commands referenced by evidence, open locators, automatically accept
 Decisions, materialize Playbook revisions, or infer outcomes from `completed_at`. Explicit user
 requests are required to create Decision, DecisionAcceptance, DecisionAction, DecisionOutcome, or
-DecisionReview records.
+DecisionReview records and to promote Review statements into Experience.

 ## Recommended next milestone

 The recommended next controlled slice is:

 ```text
-separate explicit Experience creation from DecisionReview findings or candidate lessons
+separate explicit Experience-to-Knowledge decision or use case
 ```

 It must preserve explicit authority and remain separate from automatic Knowledge, Playbook,
-PlaybookEvaluation, EvolutionProposal, or Consigliere creation.
+PlaybookEvaluation, EvolutionProposal, lifecycle, or Consigliere behavior.

 ## Handbook synchronization policy

@@ -1290,18 +1431,19 @@ Observation
 → DecisionAction
 → DecisionOutcome
 → DecisionReview
-→ explicitly created Experience
-→ explicitly created Knowledge
+→ explicitly promoted Experience
+→ separately and explicitly created Knowledge
 ```

 This is a complementary provenance path, not a replacement for the canonical domain chain.
 DecisionOutcome is factual; DecisionReview is authorized interpretation; Experience captures
-separately created operational learning; Knowledge is generalized; Playbook remains a separately
-created repeatable procedure. A Decision may have multiple immutable outcomes and multiple reviews,
-including reviews over the same ordered outcome set when their idempotency keys differ. Review
-action provenance is transitive through its explicit outcomes; it does not persist action IDs.
-These records and their embedded EvidenceReference values exist at source commit `910f481e`; no
-Review-driven lifecycle transition or later learning record in this path is automatic.
+explicitly promoted operational learning; Knowledge is separately generalized; Playbook remains a
+separately created repeatable procedure. A Decision may have multiple immutable outcomes and
+reviews, and one Review may explicitly produce multiple Experiences under different promotion
+keys. A promoted Experience selects ordered Review statements and cannot combine Reviews. Review
+action provenance remains transitive through explicit outcomes; promoted Experience provenance
+remains transitive through its one Review. These records exist at source commit `12097fe`; no
+Review save, promotion, lifecycle transition, or later Knowledge record in this path is automatic.

 ---

@@ -1349,13 +1491,15 @@ The transition must be performed by an application use case, not a repository ad

 ## Responsibility

-An Experience represents interpreted learning derived from one or more observations.
+An Experience represents explicitly recorded operational learning. It may be created directly,
+derived from one Observation, or explicitly promoted from selected DecisionReview statements.

 ## Owns

 - interpreted outcome,
 - contextual meaning,
 - provenance back to observations,
+- optional immutable DecisionReview promotion provenance,
 - identity.

 ## Must not own
@@ -1369,12 +1513,16 @@ An Experience represents interpreted learning derived from one or more observati
 - Provenance is preserved.
 - Interpretation is explicit.
 - Creation does not erase source observations.
+- Plain and Observation-derived Experiences have `decision_review_promotion is None`.
+- A promoted Experience contains one optional `DecisionReviewPromotion`; it remains Experience,
+  not generalized Knowledge.

 ## Typical transitions

 `Experience` → `Knowledge`

-The application layer coordinates this transformation.
+The application layer coordinates this separate explicit transformation. Experience creation does
+not create Knowledge automatically.

 ---

@@ -1806,7 +1954,7 @@ and a failed outcome can support a sound review.
 - Findings are required, ordered, trimmed, non-blank, case-insensitively unique, and limited to 100
   entries of at most 1000 characters each.
 - Candidate lessons use the same ordering, normalization, uniqueness, count, and length bounds, but
-  may be empty. They carry no authority to create or promote Experience or Knowledge.
+  may be empty. They are not Experience or Knowledge until a separate authorized use case succeeds.
 - Tags are trimmed and case-insensitively deduplicated while first-seen order is preserved.
 - `recorded_at` and `reviewed_at` must be timezone-aware and are normalized to UTC. Locally,
   `reviewed_at` cannot be later than `recorded_at`; the service also requires it not to precede the
@@ -1863,12 +2011,161 @@ renders every field. Evidence locators are retained but not opened.

 ## Lifecycle and learning boundary

-DecisionReview is orthogonal interpretive history. It does not affect `DecisionLifecycleService`.
+DecisionReview is orthogonal interpretive history. Saving one never creates Experience. The
+separate `ExperienceService.add_from_decision_review()` use case may explicitly copy selected
+findings or candidate lessons into one Experience without mutating the Review.
+DecisionReview does not affect `DecisionLifecycleService`.
 The lifecycle remains exactly `proposed`, `accepted`, `in_progress`, `succeeded`, `failed`,
 `partial`, and `outcome_unknown`; no `reviewed` state exists. A review never automatically creates
-Observation, Experience, Knowledge, Playbook, PlaybookEvaluation, EvolutionProposal, revision
-records, or Consigliere work. The next controlled slice is separate explicit Experience creation
-from review findings or candidate lessons.
+Observation, Knowledge, Playbook, PlaybookEvaluation, EvolutionProposal, revision records, or
+Consigliere work. Promotion remains explicit and a promoted Experience is not Knowledge.
+
+---
+
+# DecisionReview-to-Experience Promotion
+
+## Responsibility and chain
+
+The implemented promotion foundation converts selected immutable DecisionReview interpretation
+into one existing `Experience` record only through the explicitly authorized
+`ExperienceService.add_from_decision_review(...)` use case:
+
+```text
+DecisionReview
+→ explicitly promoted Experience
+→ separately and explicitly created Knowledge
+```
+
+A finding or candidate lesson is not Experience before promotion succeeds. A promoted Experience
+is still not Knowledge. Reviewer and promoter are separate authorities and may be different people;
+this foundation introduces no RBAC or approval system.
+
+## Durable schema
+
+`Experience` now has one optional field:
+
+```text
+decision_review_promotion: DecisionReviewPromotion | None
+```
+
+`DecisionReviewPromotion` contains exactly:
+
+```text
+decision_review_id
+source_statements
+promoted_by
+promotion_reason
+idempotency_key
+```
+
+Each ordered `DecisionReviewPromotionSourceStatement` contains exactly:
+
+```text
+kind
+index
+text
+```
+
+The source-kind vocabulary is exactly `finding | candidate_lesson`. Durable indexes are zero-based
+and non-negative. Source statements are ordered and non-empty, and each `(kind, index)` pair is
+unique. Promotion and source-statement values are immutable.
+
+`promoted_by` and `idempotency_key` are trimmed, non-blank, and at most 255 characters;
+`promotion_reason` is trimmed, non-blank, and at most 1000 characters. Copied statement text is
+trimmed, non-blank, and at most 1000 characters. The service stores the normalized exact immutable
+Review item at the selected index; callers and the CLI never supply independent source text.
+
+Plain direct and Observation-derived Experiences retain `decision_review_promotion is None`. A
+promotion copies no Decision, DecisionAcceptance, DecisionAction, DecisionOutcome, reviewer,
+assessment, confidence, or evidence fields into Experience. Their provenance remains transitive
+through the referenced Review.
+
+## Cardinality and corrections
+
+- One promoted Experience references exactly one DecisionReview.
+- One promoted Experience selects one or more ordered statements from that Review.
+- One DecisionReview may produce multiple Experiences.
+- One source statement may be promoted repeatedly under different idempotency keys.
+- One promoted Experience cannot combine multiple DecisionReviews.
+
+Corrections append another Experience under a different key. There is no replacement,
+supersession, deletion, status, ranking, scoring, or current/best promotion behavior.
+
+## Explicit application and read integrity
+
+`ExperienceService.add_from_decision_review(...)` performs this sequence:
+
+1. validate the non-empty, unique, non-negative caller selectors and normalize bounded promotion
+   authority metadata;
+2. call the existing validated `DecisionReviewService.show(review_id)` boundary;
+3. validate each ordered finding or candidate-lesson index and copy exact Review text;
+4. validate optional Observation references through the existing behavior;
+5. construct one promoted Experience;
+6. scan `ExperienceRepository.load_all()` for the scoped idempotency key;
+7. save exactly one Experience only after every validation and idempotency check.
+
+Validation failure, conflict, or ambiguity performs no write. The service creates no second link
+record and performs no transaction emulation.
+
+Equivalent replay validates the existing promoted Experience before returning it. `get_by_id()`,
+the complete Experience list, and the Observation-linked Experience list also revalidate promoted
+records. Validation calls the referenced Review's existing `show()` boundary, which revalidates its
+persisted Decision, acceptance, outcome, and time relations, then checks selector bounds and exact
+copied text. Missing or malformed provenance fails closed without repair or skipping. Plain
+Experience reads are unaffected; Observation-linked listing validates only returned linked records.
+
+## Idempotency
+
+Promotion idempotency is application-layer policy scoped by:
+
+```text
+(decision_review_id, "review_experience_promotion", idempotency_key)
+```
+
+| Matches | Implemented behavior |
+| ---: | --- |
+| 0 | Save and return one promoted Experience. |
+| 1 equivalent | Return the existing Experience with its original ID and timestamp; no write. |
+| 1 conflicting | Raise `DecisionReviewPromotionIdempotencyConflictError`; no write. |
+| More than 1 | Raise `DecisionReviewPromotionIdempotencyAmbiguityError`; do not select or compare an arbitrary duplicate; no write. |
+
+Ambiguity is independent of repository enumeration order. Semantic equivalence excludes only
+generated `Experience.id` and `Experience.timestamp`. It includes every caller-supplied Experience
+field, optional Observation IDs, tags, and every ordered promotion field, including copied text,
+promoter, reason, and key.
+
+## Persistence compatibility
+
+`ExperienceRepository` remains limited to `save()`, `load_all()`, and `get_by_id()`; scanning and
+relation policy remain in the application layer. Existing `JsonExperienceRepository` already
+round-trips plain and promoted records through domain validation under `NeuralPaths.EXPERIENCES`.
+Old JSON without `decision_review_promotion` remains valid and loads with `None`.
+
+No migration, inferred provenance, second write, separate aggregate, repository, adapter, path, or
+Brain collection was introduced. The production adapter required no rewrite.
+
+## CLI and boundaries
+
+The implemented command is `neural experience from-review REVIEW_UUID`. It requires repeatable
+ordered `--source KIND:ORDINAL`, `--promoted-by`, `--promotion-reason`, `--idempotency-key`,
+`--title`, `--context`, `--action`, `--outcome`, and `--result`. Optional repeatable inputs are
+`--observation-id` and `--tag`.
+
+For example, `--source finding:1 --source candidate_lesson:2` uses one-based user ordinals and is
+converted deterministically to durable indexes `0` and `1`. Invalid syntax, kind, non-positive
+ordinal, Review, source index, Observation, conflict, ambiguity, or persisted integrity renders a
+controlled error. Success and equivalent replay render the stored Experience identity and complete
+promotion provenance, including user ordinal, stored index, copied text, actor, reason, and key.
+
+Ordinary `neural experience add`, `from-observation`, `list`, `show`, `knowledge`, and
+`neural observation experiences` retain their existing inputs and behavior. Ordinary creation does
+not require promotion data or an idempotency key.
+
+Promotion changes no canonical Decision lifecycle state and adds no `reviewed`, `promoted`, or
+`learned` state. It creates no Knowledge, Playbook, PlaybookEvaluation, EvolutionProposal,
+revision, evidence execution, automatic learning, or Consigliere work. `DecisionReview.assessment`,
+`DecisionOutcome.result`, and `Experience.result` remain distinct meanings. The next controlled
+downstream step remains a separate explicit Experience-to-Knowledge decision or use case.

 ---

@@ -2041,6 +2338,33 @@ application-service invariant: more than one persisted match for a scoped key is
 ambiguity to surface, never an ordering problem to resolve by choosing the first record. Their
 scopes and controlled ambiguity error types remain separate.

+## DecisionReview-to-Experience promotion ownership
+
+`ExperienceService.add_from_decision_review(...)` is the one implemented explicit promotion use
+case. It validates selectors and bounded promoter/reason/key metadata before relation reads, calls
+the existing validated `DecisionReviewService.show(review_id)` boundary, validates ordered finding
+and candidate-lesson indexes, copies exact Review text, validates optional Observation IDs,
+constructs one Experience, then loads Experiences for application-layer idempotency. Only a fully
+validated zero-match candidate is saved.
+
+The scope is `(decision_review_id, "review_experience_promotion", idempotency_key)`. Exactly one
+equivalent match returns the original Experience identity and timestamp without writing; exactly
+one different match raises `DecisionReviewPromotionIdempotencyConflictError`; more than one match
+raises `DecisionReviewPromotionIdempotencyAmbiguityError` without repository-order selection or
+arbitrary semantic comparison. Semantic equivalence excludes only generated Experience ID and
+timestamp and includes every caller-supplied Experience and ordered promotion field.
+
+Equivalent replay validates the existing provenance. `get_by_id()`, `list_experiences()`, and
+`list_for_observation()` also fail closed for promoted records when the Review graph is invalid, an
+index is out of range, or copied text differs. Plain Experience reads remain unaffected. Direct and
+Observation-derived `add` paths keep their existing inputs and do not acquire idempotency or
+promotion requirements.
+
+One Review may produce multiple Experiences under different keys, and the same statement may be
+promoted repeatedly. Each Experience references only one Review. Corrections append; no promotion
+replacement, ranking, deletion, lifecycle state, Knowledge creation, or Consigliere behavior is
+owned here.
+
 ---

 # Application Errors
@@ -2170,6 +2494,11 @@ Decision filtering, cross-record validation, history ordering, and scoped idempo
 fail-closed duplicate-match ambiguity—belong to `DecisionReviewService`; no relation,
 idempotency, chronology, or lifecycle query method is part of the port.

+`ExperienceRepository` remains limited to `save()`, `load_all()`, and `get_by_id()` for both plain
+and promoted Experiences. Review validation, copied-text integrity, Observation validation, and
+`(decision_review_id, "review_experience_promotion", idempotency_key)` scanning belong to
+`ExperienceService`; no promotion, relation, or idempotency query belongs to the port.
+
 ## Repository return types

 Prefer:
@@ -2315,6 +2644,17 @@ DecisionReview records round-trip through domain validation. JSON object keys ar
 validation errors. The adapter performs no Decision filtering, relation validation, chronology,
 idempotency selection, lifecycle projection, evidence ingestion, learning, or Consigliere work.

+## Experience adapter and promotion compatibility
+
+`JsonExperienceRepository` continues to implement the unchanged `ExperienceRepository` under
+`NeuralPaths.EXPERIENCES`, storing one JSON file per Experience and sorting filenames for
+deterministic `load_all()`. Domain validation round-trips both ordinary records and the optional
+embedded `DecisionReviewPromotion`. Old JSON without that field loads with `None` and remains plain.
+
+No migration or production adapter rewrite was required. The adapter performs no Review lookup,
+source copying, integrity repair, idempotency decision, promotion policy, second write, or inferred
+provenance. No promotion adapter, repository, path, or Brain directory exists.
+
 ---

 # Dependency Injection and Container
@@ -2394,6 +2734,12 @@ The review foundation is wired through `Container.decision_review_repository()`
 `JsonDecisionOutcomeRepository`. Brain initialization creates `NeuralPaths.DECISION_REVIEWS`.
 Decision review CLI handlers resolve the service and construct no repositories.

+`Container.experience_service()` supplies `JsonExperienceRepository`,
+`JsonObservationRepository`, and the existing validated `DecisionReviewService` boundary to
+`ExperienceService`. The container adds no promotion policy, link repository, path, or lifecycle
+behavior; `neural experience from-review` resolves this service like the ordinary Experience
+commands.
+
 ---

 # Dependency Lifecycle
@@ -2990,6 +3336,11 @@ authorized interpretation over an explicit ordered outcome set. Lifecycle state
 acceptance, actions, and the latest factual outcome, not stored as mutable status or duplicated in
 a generic event stream. Review is orthogonal append-only history.

+Selected Review interpretation becomes Experience only through an explicit authorized use case.
+Promotion provenance is embedded immutably in the existing Experience rather than represented by
+a link aggregate, second write, new repository, or new lifecycle state. Experience-to-Knowledge
+remains a separate explicit decision.
+
 Decision tracking complements the existing Observation-to-Playbook chain. Evidence uses bounded
 embedded references, durable writes require explicit authority, and Consigliere remains a future
 advisory layer rather than authoritative storage.
@@ -3002,9 +3353,12 @@ advisory layer rather than authoritative storage.
   idempotency checks; repository ports remain persistence-focused.
 - No automatic ingestion, persistence, learning, Playbook evolution, or Consigliere integration is
   implied.
-- Source commit `910f481e27302daa6d3f15bde30d678ffc9e5d2f` implements Decision proposal,
+- Source commit `12097feb0159cc8e8831000ab04c290b56ecfc8e` implements Decision proposal,
   acceptance, action, outcome, and review recording; outcome history/summary; review history; their
   CLI; and the canonical `DecisionLifecycleService`.
+- The same checkpoint implements explicit ordered DecisionReview statement promotion into one
+  existing Experience with embedded immutable provenance, fail-closed read integrity, and scoped
+  application-layer idempotency. It does not implement automatic learning.
 - The canonical states are exactly proposed, accepted, in-progress, succeeded, failed, partial,
   and outcome-unknown. Latest outcome selection uses validation time and outcome UUID, not
   repository order. No generic completed, resolved, or reviewed state exists.
@@ -3018,6 +3372,10 @@ advisory layer rather than authoritative storage.
 - Outcome and review idempotency both fail closed when more than one persisted record matches a
   scoped key: their distinct ambiguity errors replace arbitrary first-match selection and no write
   occurs regardless of repository order or payload equivalence.
-- The recommended next controlled slice is separate explicit Experience creation from review
-  findings or candidate lessons; downstream Experience, Knowledge, or Playbook creation remains
-  explicit.
+- A Review may produce multiple Experiences under distinct keys, but one promoted Experience
+  references exactly one Review. Corrections append and ordinary Experience remains compatible.
+- Automatic promotion and a separate promotion/link aggregate were rejected because authority and
+  provenance belong in one explicit Experience write. Repository-order duplicate selection was
+  rejected in favor of a dedicated fail-closed ambiguity error.
+- The next controlled downstream step remains a separate explicit Experience-to-Knowledge decision
+  or use case; Knowledge, Playbook, and evolution creation remain explicit.
diff --git a/src/neuralengine_handbook/builder.py b/src/neuralengine_handbook/builder.py
index 5cae603..f1b392a 100644
--- a/src/neuralengine_handbook/builder.py
+++ b/src/neuralengine_handbook/builder.py
@@ -101,6 +101,7 @@ def build(root: Path) -> list[Path]:
         paths.handbook / "domain/playbook-revision-application.md",
         paths.handbook / "domain/decision-outcome.md",
         paths.handbook / "domain/decision-review.md",
+        paths.handbook / "domain/decision-review-experience-promotion.md",
     ]

     application_files = [
diff --git a/tests/test_builder.py b/tests/test_builder.py
index 4475a04..bea4ea4 100644
--- a/tests/test_builder.py
+++ b/tests/test_builder.py
@@ -39,7 +39,7 @@ def test_generated_skill_contains_neuralengine_rules(tmp_path: Path) -> None:
     assert "Application CLI commands do not" in skill
     assert "Playbook content mutation" in skill
     assert "# Decision Learning Architecture" in skill
-    assert "These commands exist at commit `910f481e`" in skill
+    assert "These commands exist at commit `12097fe`" in skill
     assert "neural decision add" in skill
     assert "neural decision list" in skill
     assert "neural decision show DECISION_UUID" in skill
@@ -55,6 +55,7 @@ def test_generated_skill_contains_neuralengine_rules(tmp_path: Path) -> None:
     assert "neural decision review add DECISION_UUID" in skill
     assert "neural decision review history DECISION_UUID" in skill
     assert "neural decision review show REVIEW_UUID" in skill
+    assert "neural experience from-review REVIEW_UUID" in skill
     assert "neural decision state DECISION_UUID" in skill
     assert "DecisionOutcome foundation" in skill
     assert "DecisionReview` remains future-only" not in skill
@@ -65,6 +66,17 @@ def test_generated_skill_contains_neuralengine_rules(tmp_path: Path) -> None:
     assert "`high`" in skill
     assert "DecisionReviewIdempotencyAmbiguityError" in skill
     assert "DecisionOutcomeIdempotencyAmbiguityError" in skill
+    assert "DecisionReviewPromotionSourceStatement" in skill
+    assert "kind is exactly `finding`" in skill
+    assert "`candidate_lesson`" in skill
+    assert '(decision_review_id, "review_experience_promotion", idempotency_key)' in skill
+    assert "DecisionReviewPromotionIdempotencyConflictError" in skill
+    assert "DecisionReviewPromotionIdempotencyAmbiguityError" in skill
+    assert "CLI ordinals are positive and one-based" in skill
+    assert "durable zero-based indexes" in skill
+    assert "Old JSON without the field loads with `None`" in skill
+    assert "fails closed without" in skill
+    assert "separate explicit Experience-to-Knowledge" in skill
     assert "No Consigliere integration exists" in skill
     assert "no automatic persistence, ingestion, or learning" in skill
     assert "same key + equivalent semantic payload" in skill
@@ -97,6 +109,7 @@ def test_handbook_contains_all_domain_entities(tmp_path: Path) -> None:
     ]
     for entity in entities:
         assert f"# {entity}" in handbook
+    assert "# DecisionReview-to-Experience Promotion" in handbook


 def test_handbook_preserves_revision_application_boundaries(tmp_path: Path) -> None:
@@ -125,14 +138,14 @@ def test_decision_engine_contains_agent_and_repository_rules(tmp_path: Path) ->
     assert "ADR-0008" in decision_engine


-def test_handbook_contains_decision_review_lifecycle_and_learning_boundaries(
+def test_handbook_contains_decision_review_experience_promotion_boundaries(
     tmp_path: Path,
 ) -> None:
     work_root = _copy_repo(tmp_path)
     build(work_root)

     handbook = (work_root / "outputs/generated/HANDBOOK.md").read_text(encoding="utf-8")
-    assert "NeuralEngine source commit `910f481e27302daa6d3f15bde30d678ffc9e5d2f`" in handbook
+    assert "NeuralEngine source commit `12097feb0159cc8e8831000ab04c290b56ecfc8e`" in handbook
     assert "neural decision add" in handbook
     assert "neural decision list" in handbook
     assert "neural decision show DECISION_UUID" in handbook
@@ -148,6 +161,7 @@ def test_handbook_contains_decision_review_lifecycle_and_learning_boundaries(
     assert "neural decision review add DECISION_UUID" in handbook
     assert "neural decision review history DECISION_UUID" in handbook
     assert "neural decision review show REVIEW_UUID" in handbook
+    assert "neural experience from-review REVIEW_UUID" in handbook
     assert "neural decision state DECISION_UUID" in handbook
     assert "DecisionAcceptance" in handbook
     assert "DecisionAcceptance foundation" in handbook
@@ -190,7 +204,20 @@ def test_handbook_contains_decision_review_lifecycle_and_learning_boundaries(
     assert "Action IDs are not persisted" in handbook
     assert "(reviewed_at, review.id)" in handbook
     assert "no `reviewed` state" in handbook
-    assert "explicit Experience creation" in handbook
+    assert "explicitly promoted Experience" in handbook
+    assert "decision_review_promotion: DecisionReviewPromotion | None" in handbook
+    assert "DecisionReviewPromotionSourceStatement" in handbook
+    assert "finding | candidate_lesson" in handbook
+    assert "CLI ordinals are positive and one-based" in handbook
+    assert "durable zero-based indexes" in handbook
+    assert '(decision_review_id, "review_experience_promotion", idempotency_key)' in handbook
+    assert "DecisionReviewPromotionIdempotencyConflictError" in handbook
+    assert "DecisionReviewPromotionIdempotencyAmbiguityError" in handbook
+    assert "Old JSON without `decision_review_promotion` remains valid" in handbook
+    assert "Missing or malformed provenance fails closed" in handbook
+    assert "a promoted Experience is not Knowledge" in handbook
+    assert "separate explicit Experience-to-Knowledge" in handbook
+    assert "separate explicit Experience creation from DecisionReview" not in handbook
     assert "No Consigliere integration exists" in handbook
     assert "no automatic persistence, ingestion, or learning" in handbook
     assert "ADR-0008" in handbook
@@ -217,6 +244,12 @@ def test_application_architecture_contains_core_boundaries(tmp_path: Path) -> No
     assert "Container.decision_review_service()" in application
     assert "DecisionReviewIdempotencyAmbiguityError" in application
     assert "DecisionOutcomeIdempotencyAmbiguityError" in application
+    assert "ExperienceService.add_from_decision_review(...)" in application
+    assert "DecisionReviewPromotionIdempotencyConflictError" in application
+    assert "DecisionReviewPromotionIdempotencyAmbiguityError" in application
+    assert "ExperienceRepository` remains limited" in application
+    assert "Old JSON without that field loads with `None`" in application
+    assert "Container.experience_service()" in application


 def test_application_architecture_includes_accepted_adrs(tmp_path: Path) -> None:
~~~~

## Complete creation diff: canonical promotion source

Command: `git diff --no-index -- /dev/null handbook/domain/decision-review-experience-promotion.md`
Exit status: `1` (expected because a new file differs from `/dev/null`)

~~~~text
diff --git a/handbook/domain/decision-review-experience-promotion.md b/handbook/domain/decision-review-experience-promotion.md
new file mode 100644
index 0000000..f24e95c
--- /dev/null
+++ b/handbook/domain/decision-review-experience-promotion.md
@@ -0,0 +1,144 @@
+# DecisionReview-to-Experience Promotion
+
+## Responsibility and chain
+
+The implemented promotion foundation converts selected immutable DecisionReview interpretation
+into one existing `Experience` record only through the explicitly authorized
+`ExperienceService.add_from_decision_review(...)` use case:
+
+```text
+DecisionReview
+→ explicitly promoted Experience
+→ separately and explicitly created Knowledge
+```
+
+A finding or candidate lesson is not Experience before promotion succeeds. A promoted Experience
+is still not Knowledge. Reviewer and promoter are separate authorities and may be different people;
+this foundation introduces no RBAC or approval system.
+
+## Durable schema
+
+`Experience` now has one optional field:
+
+```text
+decision_review_promotion: DecisionReviewPromotion | None
+```
+
+`DecisionReviewPromotion` contains exactly:
+
+```text
+decision_review_id
+source_statements
+promoted_by
+promotion_reason
+idempotency_key
+```
+
+Each ordered `DecisionReviewPromotionSourceStatement` contains exactly:
+
+```text
+kind
+index
+text
+```
+
+The source-kind vocabulary is exactly `finding | candidate_lesson`. Durable indexes are zero-based
+and non-negative. Source statements are ordered and non-empty, and each `(kind, index)` pair is
+unique. Promotion and source-statement values are immutable.
+
+`promoted_by` and `idempotency_key` are trimmed, non-blank, and at most 255 characters;
+`promotion_reason` is trimmed, non-blank, and at most 1000 characters. Copied statement text is
+trimmed, non-blank, and at most 1000 characters. The service stores the normalized exact immutable
+Review item at the selected index; callers and the CLI never supply independent source text.
+
+Plain direct and Observation-derived Experiences retain `decision_review_promotion is None`. A
+promotion copies no Decision, DecisionAcceptance, DecisionAction, DecisionOutcome, reviewer,
+assessment, confidence, or evidence fields into Experience. Their provenance remains transitive
+through the referenced Review.
+
+## Cardinality and corrections
+
+- One promoted Experience references exactly one DecisionReview.
+- One promoted Experience selects one or more ordered statements from that Review.
+- One DecisionReview may produce multiple Experiences.
+- One source statement may be promoted repeatedly under different idempotency keys.
+- One promoted Experience cannot combine multiple DecisionReviews.
+
+Corrections append another Experience under a different key. There is no replacement,
+supersession, deletion, status, ranking, scoring, or current/best promotion behavior.
+
+## Explicit application and read integrity
+
+`ExperienceService.add_from_decision_review(...)` performs this sequence:
+
+1. validate the non-empty, unique, non-negative caller selectors and normalize bounded promotion
+   authority metadata;
+2. call the existing validated `DecisionReviewService.show(review_id)` boundary;
+3. validate each ordered finding or candidate-lesson index and copy exact Review text;
+4. validate optional Observation references through the existing behavior;
+5. construct one promoted Experience;
+6. scan `ExperienceRepository.load_all()` for the scoped idempotency key;
+7. save exactly one Experience only after every validation and idempotency check.
+
+Validation failure, conflict, or ambiguity performs no write. The service creates no second link
+record and performs no transaction emulation.
+
+Equivalent replay validates the existing promoted Experience before returning it. `get_by_id()`,
+the complete Experience list, and the Observation-linked Experience list also revalidate promoted
+records. Validation calls the referenced Review's existing `show()` boundary, which revalidates its
+persisted Decision, acceptance, outcome, and time relations, then checks selector bounds and exact
+copied text. Missing or malformed provenance fails closed without repair or skipping. Plain
+Experience reads are unaffected; Observation-linked listing validates only returned linked records.
+
+## Idempotency
+
+Promotion idempotency is application-layer policy scoped by:
+
+```text
+(decision_review_id, "review_experience_promotion", idempotency_key)
+```
+
+| Matches | Implemented behavior |
+| ---: | --- |
+| 0 | Save and return one promoted Experience. |
+| 1 equivalent | Return the existing Experience with its original ID and timestamp; no write. |
+| 1 conflicting | Raise `DecisionReviewPromotionIdempotencyConflictError`; no write. |
+| More than 1 | Raise `DecisionReviewPromotionIdempotencyAmbiguityError`; do not select or compare an arbitrary duplicate; no write. |
+
+Ambiguity is independent of repository enumeration order. Semantic equivalence excludes only
+generated `Experience.id` and `Experience.timestamp`. It includes every caller-supplied Experience
+field, optional Observation IDs, tags, and every ordered promotion field, including copied text,
+promoter, reason, and key.
+
+## Persistence compatibility
+
+`ExperienceRepository` remains limited to `save()`, `load_all()`, and `get_by_id()`; scanning and
+relation policy remain in the application layer. Existing `JsonExperienceRepository` already
+round-trips plain and promoted records through domain validation under `NeuralPaths.EXPERIENCES`.
+Old JSON without `decision_review_promotion` remains valid and loads with `None`.
+
+No migration, inferred provenance, second write, separate aggregate, repository, adapter, path, or
+Brain collection was introduced. The production adapter required no rewrite.
+
+## CLI and boundaries
+
+The implemented command is `neural experience from-review REVIEW_UUID`. It requires repeatable
+ordered `--source KIND:ORDINAL`, `--promoted-by`, `--promotion-reason`, `--idempotency-key`,
+`--title`, `--context`, `--action`, `--outcome`, and `--result`. Optional repeatable inputs are
+`--observation-id` and `--tag`.
+
+For example, `--source finding:1 --source candidate_lesson:2` uses one-based user ordinals and is
+converted deterministically to durable indexes `0` and `1`. Invalid syntax, kind, non-positive
+ordinal, Review, source index, Observation, conflict, ambiguity, or persisted integrity renders a
+controlled error. Success and equivalent replay render the stored Experience identity and complete
+promotion provenance, including user ordinal, stored index, copied text, actor, reason, and key.
+
+Ordinary `neural experience add`, `from-observation`, `list`, `show`, `knowledge`, and
+`neural observation experiences` retain their existing inputs and behavior. Ordinary creation does
+not require promotion data or an idempotency key.
+
+Promotion changes no canonical Decision lifecycle state and adds no `reviewed`, `promoted`, or
+`learned` state. It creates no Knowledge, Playbook, PlaybookEvaluation, EvolutionProposal,
+revision, evidence execution, automatic learning, or Consigliere work. `DecisionReview.assessment`,
+`DecisionOutcome.result`, and `Experience.result` remain distinct meanings. The next controlled
+downstream step remains a separate explicit Experience-to-Knowledge decision or use case.
~~~~

## Review artifact trailing-whitespace check

Command: `rg -n '[[:blank:]]+$' .agent-work/reviews/review-sync-decision-review-experience-promotion-milestone.md`
Exit status: `1` (expected: no matches)

~~~~text

~~~~

Correction confirmation: the complete review artifact contains no trailing spaces or tabs. Embedded diff blank lines were normalized only to remove trailing blank characters; no evidence, heading, validation output, diff content, or conclusion was removed.

## Risks, deviations, assumptions, and blockers

none

The canonical filename required by the task was suitable and was used without deviation. The authoritative milestone's documented 852-test NeuralEngine count was treated as source inspection evidence, not rerun in the immutable source repository; Handbook validation is complete.

## Prohibition confirmations

- NeuralEngine was not modified.
- `outputs/claude-skill/SKILL.md` was not copied into NeuralEngine.
- Generated outputs were changed only by the documented builder.
- Decision lifecycle, Knowledge/Playbook/EvolutionProposal, Consigliere, and justfile work were not added.
- Nothing was staged, committed, or pushed.
