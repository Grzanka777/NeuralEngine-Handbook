# Review: DecisionReview Handbook synchronization

## Outcome

completed

## Starting checkpoints

### NeuralEngine — authoritative source

- Branch: `main`
- HEAD: `910f481e27302daa6d3f15bde30d678ffc9e5d2f`
- origin/main: `910f481e27302daa6d3f15bde30d678ffc9e5d2f`
- Subject: `fix: reject ambiguous outcome idempotency keys`
- Initial worktree: clean (the complete initial `git status --short --untracked-files=all` output was empty).
- Expected authoritative test state recorded by the task: 797 passing tests.
- This task used the implementation, tests, documentation, and commit range through the exact checkpoint as source of truth; it did not modify or run write operations in NeuralEngine.

### NeuralEngine-Handbook — target

- Branch: `main`
- Starting HEAD: `98c0e526d3e30ab068bfc359544155067eab7b0e`
- Starting origin/main: `98c0e526d3e30ab068bfc359544155067eab7b0e`
- Subject: `docs: sync decision outcome milestone`
- Starting tracked worktree: clean.
- Complete initial status (all entries were pre-existing untracked workflow or desktop artifacts):

~~~~text
?? .agent-work/prompts/codex-implement-decision-foundation.md
?? .agent-work/prompts/codex-sync-decision-acceptance-foundation-milestone.md
?? .agent-work/prompts/codex-sync-decision-action-lifecycle-foundation-milestone.md
?? .agent-work/prompts/codex-sync-decision-foundation-milestone.md
?? .agent-work/prompts/codex-sync-decision-learning-design-milestone.md
?? .agent-work/prompts/codex-sync-decision-outcome-handbook.md
?? .agent-work/prompts/codex-sync-decision-review-handbook.md
?? .agent-work/prompts/codex-sync-neuralengine-application-foundation-milestone.md
?? .agent-work/reviews/review-sync-decision-acceptance-foundation-milestone.md
?? .agent-work/reviews/review-sync-decision-action-lifecycle-foundation-milestone.md
?? .agent-work/reviews/review-sync-decision-foundation-milestone.md
?? .agent-work/reviews/review-sync-decision-learning-design-milestone.md
?? .agent-work/reviews/review-sync-neuralengine-application-foundation-milestone.md
?? .directory
~~~~

The pre-existing untracked entries above are not task changes. The prompt
`.agent-work/prompts/codex-sync-decision-review-handbook.md` supplied this task but also existed
before execution.

## Changed-file inventory

### Authoritative Handbook sources

- `handbook/application/services.md`
- `handbook/architecture/architecture.md`
- `handbook/architecture/decision-learning.md`
- `handbook/container/dependency-injection.md`
- `handbook/decisions/ADR-0008-decision-learning-boundary.md`
- `handbook/domain/decision-outcome.md`
- `handbook/domain/domain-chain.md`
- `handbook/domain/decision-review.md` (new)
- `handbook/infrastructure/repositories.md`
- `handbook/ports/repository-ports.md`

### Builder and tests

- `src/neuralengine_handbook/builder.py`
- `tests/test_builder.py`

### Generated outputs changed by the builder

- `outputs/claude-skill/SKILL.md`
- `outputs/generated/AGENTS.generated.md`
- `outputs/generated/APPLICATION_ARCHITECTURE.md`
- `outputs/generated/DECISION_ENGINE.md`
- `outputs/generated/HANDBOOK.md`

### Generated outputs rebuilt but content-unchanged

- `outputs/generated/codex-task-template.md`
- `outputs/generated/deepseek-task-template.md`
- `outputs/generated/review-template.md`

### Review artifact

- `.agent-work/reviews/review-sync-decision-review-milestone.md` (new, this file)

### Files intended for the eventual task commit

All files in the four task categories above: the ten authoritative sources, builder, tests, five
content-changed generated outputs, and this review artifact. The three rebuilt task templates have
no diff and therefore do not enter a commit.

### Pre-existing untracked entries excluded from the eventual task commit

- `.directory`
- every other pre-existing untracked file under `.agent-work/`, listed verbatim in the starting
  status above.

## Synchronization summary

The Handbook now records DecisionReview as the implemented immutable, append-only authorized
interpretation layer over one Decision, one acceptance, and caller-ordered explicit outcomes. It
documents all durable fields, exact assessment and confidence vocabularies, text and collection
bounds, UTC normalization, local and cross-record time constraints, transitive action provenance,
cardinality, corrections, deterministic history, persistence port, JSON adapter, Brain path,
container construction, service methods and controlled failures, and the exact add/history/show
CLI.

DecisionOutcome remains the factual layer. Both DecisionOutcome and DecisionReview now document the
same reusable fail-closed duplicate-key invariant with separate scopes and errors: zero matches
creates, exactly one match replays or conflicts by semantic payload, and more than one persisted
scoped match raises ambiguity without arbitrary selection, semantic comparison against a selected
duplicate, or a write, regardless of repository enumeration order or duplicate payload equivalence.

Lifecycle remains exactly `proposed`, `accepted`, `in_progress`, `succeeded`, `failed`,
`partial`, and `outcome_unknown`. Review is orthogonal history and creates no lifecycle state or
automatic learning. The recommended next controlled slice follows NeuralEngine source wording:
separate explicit Experience creation from review findings or candidate lessons.

## Stale or conflicting statements corrected

- DecisionReview described as future-only, absent, or the next foundation.
- The durable chain stopping at Outcome or labeling Review as future.
- Current-state text pinned to `5befd7c` instead of the authoritative `910f481e...` checkpoint.
- Missing DecisionReview domain fields, validation, provenance, cardinality, service, storage,
  wiring, CLI, and lifecycle boundaries.
- Outcome idempotency text that covered only equivalent replay and single-record conflict.
- Missing fail-closed behavior for multiple persisted Outcome or Review scoped-key matches.
- Any implication that repository order may choose an idempotent replay or review chronology.
- Next-milestone wording that still proposed DecisionReview rather than explicit Experience
  creation from review findings or candidate lessons.
- Generated artifacts containing the same stale statements.

During complete diff inspection, one concrete authoring error was found before final validation:
the Outcome ambiguity row had initially landed in the Action idempotency table. It was moved to the
Outcome table, then every generated artifact was rebuilt twice again.

## Acceptance criteria

- [x] Both starting checkpoints, hashes, subjects, and statuses verified and recorded.
- [x] NeuralEngine remained unchanged.
- [x] Handbook source matches the committed DecisionReview implementation at `910f481e...`.
- [x] Responsibility, fields, vocabularies, validation, provenance, cardinality, ordering,
  idempotency, persistence, wiring, CLI, and lifecycle boundary documented.
- [x] Fail-closed duplicate idempotency documented for DecisionReview and DecisionOutcome.
- [x] No authoritative source or generated statement describes DecisionReview as future-only.
- [x] No review-driven lifecycle state or automatic learning was introduced.
- [x] New DecisionReview domain source registered after DecisionOutcome in deterministic order.
- [x] Focused builder tests protect the source and critical semantic boundaries.
- [x] All eight generated artifacts rebuilt through the documented command; none hand-edited.
- [x] Two consecutive final builds have identical checksums and no second-build drift.
- [x] Pytest, Ruff, MyPy, and whitespace validation pass.
- [x] Complete tracked and new-domain diffs inspected; no unrelated task changes found.
- [x] Full raw evidence and relevant diffs are included below.
- [x] Nothing was staged, committed, or pushed.

## Generated-output inventory

~~~~text
outputs/claude-skill/SKILL.md
outputs/generated/AGENTS.generated.md
outputs/generated/codex-task-template.md
outputs/generated/deepseek-task-template.md
outputs/generated/review-template.md
outputs/generated/HANDBOOK.md
outputs/generated/DECISION_ENGINE.md
outputs/generated/APPLICATION_ARCHITECTURE.md
~~~~

Generated outputs were not manually edited. They were written only by
`uv run --no-project --with-editable . handbook build`. The generated
`outputs/claude-skill/SKILL.md` was not copied into NeuralEngine.

## Two-build deterministic rebuild evidence

### Final build 1

Command: `uv run --no-project --with-editable . handbook build`
Exit status: 0

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
Exit status: 0

~~~~text
85391d7dc40374d8940ddf7b98f9c9b618ce0b5316a9554688b481de08f5c2f1  outputs/claude-skill/SKILL.md
b6bc0e481545b15fc36d1f11d4279b4276242706c779d5aa2af7b67863cdea26  outputs/generated/AGENTS.generated.md
cb8717f6d11ef37f22301cddd3adcc6018244ae6ae0716153e9d163f7356788e  outputs/generated/codex-task-template.md
dd0b789499891f724d96711dcabe968e9c22c0961c1b6aa0cbb106c8153133c9  outputs/generated/deepseek-task-template.md
dfe91096687c6a46d611bf788274b9f04bb46af4ec2d6da0e53563d7a9551fe9  outputs/generated/review-template.md
e66ff472258d47d03982ef59dd25b395f77dae1139ef8f37bef312fb35ac25f2  outputs/generated/HANDBOOK.md
d0d6cde7483e04e4fb309373d323709b96bfc95edb944ceff764fcee887b4ba8  outputs/generated/DECISION_ENGINE.md
6991499680f089bf62560ec1aaaf5e1fc01d206f816e771e0fa76abd1a55662b  outputs/generated/APPLICATION_ARCHITECTURE.md
~~~~

### Final build 2

Command: `uv run --no-project --with-editable . handbook build`
Exit status: 0

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
Exit status: 0

~~~~text
85391d7dc40374d8940ddf7b98f9c9b618ce0b5316a9554688b481de08f5c2f1  outputs/claude-skill/SKILL.md
b6bc0e481545b15fc36d1f11d4279b4276242706c779d5aa2af7b67863cdea26  outputs/generated/AGENTS.generated.md
cb8717f6d11ef37f22301cddd3adcc6018244ae6ae0716153e9d163f7356788e  outputs/generated/codex-task-template.md
dd0b789499891f724d96711dcabe968e9c22c0961c1b6aa0cbb106c8153133c9  outputs/generated/deepseek-task-template.md
dfe91096687c6a46d611bf788274b9f04bb46af4ec2d6da0e53563d7a9551fe9  outputs/generated/review-template.md
e66ff472258d47d03982ef59dd25b395f77dae1139ef8f37bef312fb35ac25f2  outputs/generated/HANDBOOK.md
d0d6cde7483e04e4fb309373d323709b96bfc95edb944ceff764fcee887b4ba8  outputs/generated/DECISION_ENGINE.md
6991499680f089bf62560ec1aaaf5e1fc01d206f816e771e0fa76abd1a55662b  outputs/generated/APPLICATION_ARCHITECTURE.md
~~~~

Exact checksum comparison: `MATCH`.

## Final validation: complete raw output

### Pytest

Command: `env PYTHONPATH=src uv run --no-project --with pytest --with typer --with pyyaml pytest`
Exit status: 0

~~~~text
============================= test session starts ==============================
platform linux -- Python 3.12.8, pytest-9.1.1, pluggy-1.6.0
rootdir: /run/media/grzanka/Big_Shit/projekty/NeuralEngine-Handbook
configfile: pyproject.toml
testpaths: tests
collected 8 items

tests/test_builder.py ........                                           [100%]

============================== 8 passed in 2.35s ===============================
~~~~

### Ruff

Command: `ruff check .`
Exit status: 0

~~~~text
All checks passed!
~~~~

### MyPy

Command: `uv run --no-project --with mypy --with typer --with pyyaml python -m mypy src`
Exit status: 0

~~~~text
Success: no issues found in 3 source files
~~~~

### git diff --check

Command: `git diff --check`
Exit status: 0

~~~~text
~~~~

### NeuralEngine unchanged proof

Command: `git -C ../NeuralEngine status --short --untracked-files=all`
Exit status: 0

~~~~text
~~~~

Command: `git -C ../NeuralEngine rev-parse HEAD`
Exit status: 0

~~~~text
910f481e27302daa6d3f15bde30d678ffc9e5d2f
~~~~

Command: `git -C ../NeuralEngine rev-parse origin/main`
Exit status: 0

~~~~text
910f481e27302daa6d3f15bde30d678ffc9e5d2f
~~~~

Command: `git -C ../NeuralEngine log -1 --format='%s'`
Exit status: 0

~~~~text
fix: reject ambiguous outcome idempotency keys
~~~~

## Complete diff stat

### Tracked files

Command: `git diff --stat`
Exit status: 0

~~~~text
 handbook/application/services.md                   |  37 +-
 handbook/architecture/architecture.md              |  28 +-
 handbook/architecture/decision-learning.md         | 209 +++++++--
 handbook/container/dependency-injection.md         |   6 +
 .../ADR-0008-decision-learning-boundary.md         |  25 +-
 handbook/domain/decision-outcome.md                |  15 +-
 handbook/domain/domain-chain.md                    |  24 +-
 handbook/infrastructure/repositories.md            |   9 +
 handbook/ports/repository-ports.md                 |   5 +
 outputs/claude-skill/SKILL.md                      | 259 +++++++++---
 outputs/generated/AGENTS.generated.md              |  28 +-
 outputs/generated/APPLICATION_ARCHITECTURE.md      |  57 ++-
 outputs/generated/DECISION_ENGINE.md               | 234 +++++++++--
 outputs/generated/HANDBOOK.md                      | 466 ++++++++++++++++++---
 src/neuralengine_handbook/builder.py               |   1 +
 tests/test_builder.py                              |  45 +-
 16 files changed, 1219 insertions(+), 229 deletions(-)
~~~~

### New task source

~~~~text
 handbook/domain/decision-review.md | 107 ++++++++++++++++++++++++++++++++++++++
 .agent-work/reviews/review-sync-decision-review-milestone.md | 3071 ++++++++++
 2 files changed, 3178 insertions(+)
~~~~

The review artifact itself is new and contains this evidence. Its creation diff is not recursively
embedded into itself; the artifact's complete current content is this file. This is the only
logical self-reference exception. It remains explicitly included in the task inventory and final
status.

## Final git status --short --untracked-files=all

Command: `git status --short --untracked-files=all`
Exit status: 0

~~~~text
 M handbook/application/services.md
 M handbook/architecture/architecture.md
 M handbook/architecture/decision-learning.md
 M handbook/container/dependency-injection.md
 M handbook/decisions/ADR-0008-decision-learning-boundary.md
 M handbook/domain/decision-outcome.md
 M handbook/domain/domain-chain.md
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
?? .agent-work/prompts/codex-sync-decision-review-handbook.md
?? .agent-work/prompts/codex-sync-neuralengine-application-foundation-milestone.md
?? .agent-work/reviews/review-sync-decision-acceptance-foundation-milestone.md
?? .agent-work/reviews/review-sync-decision-action-lifecycle-foundation-milestone.md
?? .agent-work/reviews/review-sync-decision-foundation-milestone.md
?? .agent-work/reviews/review-sync-decision-learning-design-milestone.md
?? .agent-work/reviews/review-sync-decision-review-milestone.md
?? .agent-work/reviews/review-sync-neuralengine-application-foundation-milestone.md
?? .directory
?? handbook/domain/decision-review.md
~~~~

## Full tracked diff

Command: `git diff --no-ext-diff --binary`
Exit status: 0

~~~~diff
diff --git a/handbook/application/services.md b/handbook/application/services.md
index 08b4014..4d745d7 100644
--- a/handbook/application/services.md
+++ b/handbook/application/services.md
@@ -118,9 +118,12 @@ learning record.
 `DecisionOutcomeService.add()` validates the Decision, matching acceptance, one or more unique
 actions, each action's Decision and acceptance relations, and validation time against the earliest
 linked action start before constructing or saving an immutable outcome. It uses
-`(decision_id, "decision_outcome", idempotency_key)` for application-layer idempotency. Equivalent
-replay returns the existing outcome; conflicting reuse fails without a write; another key may
-append another outcome for the same Decision.
+`(decision_id, "decision_outcome", idempotency_key)` for application-layer idempotency. Zero
+matches creates normally; exactly one equivalent match returns the existing outcome; exactly one
+different match conflicts. More than one persisted scoped match raises
+`DecisionOutcomeIdempotencyAmbiguityError`, regardless of payload equivalence or repository order,
+without selecting a duplicate or writing. Another key may append another outcome for the same
+Decision.

 `list_for_decision()` validates the Decision and returns all matching outcomes in repository order.
 `show()` owns explicit outcome-not-found behavior. `summary_for_decision()` validates persisted
@@ -135,3 +138,31 @@ Decision/acceptance/action/outcome relations and derives exactly `proposed`, `ac
 latest is selected by `(validated_at, outcome.id)`. It writes no status and exposes no generic
 `completed`, `resolved`, or reviewed state. Outcome creation and projection create no Review or
 learning record.
+
+## Decision review ownership
+
+`DecisionReviewService.add()` first constructs the immutable candidate, then validates Decision,
+matching acceptance, every explicit ordered outcome relation, and that `reviewed_at` is not earlier
+than the latest referenced outcome validation. It writes only after all validation. The scope is
+`(decision_id, "decision_review", idempotency_key)`: zero matches creates, exactly one equivalent
+match replays, and exactly one different match raises `DecisionReviewIdempotencyConflictError`.
+More than one match raises `DecisionReviewIdempotencyAmbiguityError` with identifying details,
+independent of repository order and duplicate payload equivalence, without arbitrary selection,
+semantic comparison against a selected duplicate, or a write.
+
+Semantic comparison for the exactly-one-match case excludes generated review ID and recording
+time plus evidence capture times. It includes ordered outcome IDs, findings, candidate lessons,
+evidence, tags, and every other caller-supplied semantic field, so ordered collections remain order
+sensitive. `list_for_decision()` validates the Decision and every persisted review relation, then
+sorts by `(reviewed_at, review.id)`. `show()` validates persisted relations and owns explicit
+review-not-found behavior.
+
+Multiple reviews may cover one Decision, one outcome, or the same ordered outcome set under
+different keys. Corrections append; the service has no replacement, supersession, deletion, or
+`current` behavior. It creates no Experience, Knowledge, Playbook, proposal, or Consigliere work
+and does not participate in `DecisionLifecycleService`.
+
+The DecisionOutcome and DecisionReview duplicate-key rules are the same reusable fail-closed
+application-service invariant: more than one persisted match for a scoped key is corruption or
+ambiguity to surface, never an ordering problem to resolve by choosing the first record. Their
+scopes and controlled ambiguity error types remain separate.
diff --git a/handbook/architecture/architecture.md b/handbook/architecture/architecture.md
index 6896cb9..754e247 100644
--- a/handbook/architecture/architecture.md
+++ b/handbook/architecture/architecture.md
@@ -68,20 +68,24 @@ a milestone snapshot, not a timeless guarantee.

 ## Decision Learning boundary

-Source commit `5befd7c` implements separate immutable `Decision`, `DecisionAcceptance`,
-`DecisionAction`, and `DecisionOutcome` records, persistence-focused ports and JSON adapters,
-application services, container wiring, thin proposal/acceptance/action/outcome CLI commands, and
-the canonical `DecisionLifecycleService`. An action records work performed; only a linked outcome
-records factual results and validation evidence.
+Source commit `910f481e27302daa6d3f15bde30d678ffc9e5d2f` implements separate immutable
+`Decision`, `DecisionAcceptance`, `DecisionAction`, `DecisionOutcome`, and `DecisionReview`
+records, persistence-focused ports and JSON adapters, application services, container wiring,
+thin proposal/acceptance/action/outcome/review CLI commands, and the canonical
+`DecisionLifecycleService`. An action records work performed; only a linked outcome records
+factual results and validation evidence; a review records authorized interpretation.

 `DecisionOutcome` links one Decision, its acceptance, and one or more ordered unique actions. Its
 result is exactly `succeeded`, `failed`, `partial`, or `unknown`; scalar metrics are immutable.
 Multiple outcomes form history, and the non-persisted `DecisionOutcomeSummary` derives counts and
 the latest outcome using `(validated_at, outcome.id)` rather than repository order.
-
-The canonical lifecycle states are exactly `proposed`, `accepted`, `in_progress`, `succeeded`,
-`failed`, `partial`, and `outcome_unknown`. `DecisionReview` and a reviewed state remain
-future-only. Outcome creation does not create learning. There is no execution engine, lifecycle
-reversal, ingestion, automatic learning or evolution, generic event replay, or Consigliere
-integration. The authoritative implemented contract and future boundary are defined in
-`handbook/architecture/decision-learning.md`; the next milestone is the DecisionReview foundation.
+`DecisionReview` targets an explicit ordered non-empty set of outcomes for one Decision and
+acceptance. Multiple reviews form immutable history ordered by `(reviewed_at, review.id)`.
+
+The canonical lifecycle states remain exactly `proposed`, `accepted`, `in_progress`, `succeeded`,
+`failed`, `partial`, and `outcome_unknown`. Review is orthogonal append-only history; there is no
+`reviewed` state. Outcome or review creation does not create learning. There is no execution
+engine, lifecycle reversal, ingestion, automatic learning or evolution, generic event replay, or
+Consigliere integration. The authoritative implemented contract and future boundary are defined
+in `handbook/architecture/decision-learning.md`; the recommended next controlled slice is
+separate explicit Experience creation from review findings or candidate lessons.
diff --git a/handbook/architecture/decision-learning.md b/handbook/architecture/decision-learning.md
index c8d3c26..6fe5ad5 100644
--- a/handbook/architecture/decision-learning.md
+++ b/handbook/architecture/decision-learning.md
@@ -2,11 +2,12 @@

 ## Status and purpose

-NeuralEngine source commit `5befd7c` implements the Decision, DecisionAcceptance,
-DecisionAction, and DecisionOutcome foundations plus the canonical `DecisionLifecycleService`
-projection. They record an immutable proposed choice, explicit authorization, work performed under
-that authorization, and factual results. Each foundation persists immutable records, exposes
-application use cases, is wired through the container, and provides a thin CLI.
+NeuralEngine source commit `910f481e27302daa6d3f15bde30d678ffc9e5d2f` implements the Decision,
+DecisionAcceptance, DecisionAction, DecisionOutcome, and DecisionReview foundations plus the
+canonical `DecisionLifecycleService` projection. They record an immutable proposed choice,
+explicit authorization, work performed under that authorization, factual results, and authorized
+interpretation. Each foundation persists immutable records, exposes application use cases, is
+wired through the container, and provides a thin CLI.

 The wider Decision Learning lifecycle remains accepted future architecture. Decision tracking
 complements the existing Observation-to-Playbook chain; it does not replace it.
@@ -21,19 +22,23 @@ EvidenceReference
 DecisionAcceptance
 DecisionAction
 DecisionOutcome
+DecisionReview
 DecisionRepository
 DecisionAcceptanceRepository
 DecisionActionRepository
 DecisionOutcomeRepository
+DecisionReviewRepository
 JsonDecisionRepository
 JsonDecisionAcceptanceRepository
 JsonDecisionActionRepository
 JsonDecisionOutcomeRepository
+JsonDecisionReviewRepository
 DecisionService
 DecisionAcceptanceService
 DecisionActionService
 DecisionOutcomeService
 DecisionOutcomeSummary
+DecisionReviewService
 DecisionLifecycleService
 container wiring
 neural decision add/list/show
@@ -46,14 +51,17 @@ neural decision outcome add
 neural decision outcome-history
 neural decision outcome-show
 neural decision outcome-summary
+neural decision review add
+neural decision review history
+neural decision review show
 neural decision state
 ```

 Creating a Decision records a proposal. Creating a DecisionAcceptance explicitly authorizes that
 proposal for possible future work. Creating a DecisionAction records work performed under that
 acceptance. Creating a DecisionOutcome records factual results and validation evidence for one or
-more linked actions. None of these operations performs review or learning. `DecisionReview`
-remains future-only.
+more linked actions. Creating a DecisionReview records authorized interpretation over an explicit
+ordered outcome set. None of these operations automatically creates learning.

 ## Decision model

@@ -96,7 +104,7 @@ not rewrite the earlier record.
 ## EvidenceReference

 `EvidenceReference` is an implemented immutable value embedded in a Decision,
-DecisionAcceptance, DecisionAction, or DecisionOutcome:
+DecisionAcceptance, DecisionAction, DecisionOutcome, or DecisionReview:

 ```text
 kind
@@ -244,6 +252,46 @@ One Decision may have multiple outcomes. Each outcome appends factual history an
 more actions; no outcome replaces or mutates an earlier record. An outcome does not mean review,
 Experience, Knowledge, Playbook change, or automatic learning occurred.

+## DecisionReview foundation
+
+`DecisionReview` is an immutable, append-only authorized interpretation record with these exact
+implemented fields:
+
+```text
+id
+recorded_at
+decision_id
+acceptance_id
+outcome_ids
+reviewed_by
+reviewed_at
+assessment
+summary
+findings
+candidate_lessons
+evidence_references
+confidence
+idempotency_key
+tags
+```
+
+Assessment is exactly `sound`, `flawed`, `mixed`, or `inconclusive`; confidence is exactly `low`,
+`medium`, or `high`. Assessment is not the outcome result vocabulary: successful factual outcomes
+may support a flawed review, and failed outcomes may support a sound review.
+
+`outcome_ids` is ordered, unique, and non-empty. Findings are required ordered text; findings and
+candidate lessons each allow at most 100 case-insensitively unique entries of at most 1000
+characters. Candidate lessons may be empty and have no promotion authority. Reviewer is bounded to
+255 characters and summary to 1000; required text is trimmed and non-blank. Tags preserve
+first-seen order while removing case-insensitive duplicates. UTC-aware timestamps are normalized
+to UTC, and `reviewed_at` cannot be later than `recorded_at`.
+
+Every outcome must exist and belong to the same Decision and acceptance. Review time cannot
+precede the latest `validated_at` among selected outcomes. Action IDs are not persisted: provenance
+is transitive through `DecisionReview → DecisionOutcome[] → DecisionAction[]`. Multiple reviews
+may cover one Decision, outcome, or ordered outcome set under different keys. Corrections append;
+there is no replacement, supersession, deletion, or persisted `current` behavior.
+
 ## Persistence

 The persistence-focused `DecisionRepository` port implements only:
@@ -306,6 +354,20 @@ and immutable scalar metrics round-trip through domain validation; malformed dat
 The adapter performs no relation filtering, lifecycle projection, review, learning, migration, or
 ingestion.

+The persistence-focused `DecisionReviewRepository` implements only:
+
+```text
+save()
+load_all()
+get_by_id()
+```
+
+It has no relation, idempotency, chronology, or lifecycle query methods.
+`JsonDecisionReviewRepository` stores one deterministic sorted-key JSON file per review under
+`NeuralPaths.DECISION_REVIEWS`, and Brain initialization creates that directory. `load_all()` sorts
+filenames and every record round-trips through domain validation. Filtering, relation validation,
+history ordering, ambiguity detection, and semantic comparison remain in the application service.
+
 ## Application service

 `DecisionService` implements:
@@ -489,6 +551,9 @@ same scoped key + equivalent semantic payload
 same scoped key + different semantic payload
 → visible conflict, no write

+more than one persisted scoped match
+→ `DecisionOutcomeIdempotencyAmbiguityError`, no arbitrary selection, no write
+
 different key
 → another outcome may be recorded
 ```
@@ -508,6 +573,65 @@ validates every persisted outcome-to-acceptance/action relation. Latest selectio
 by `(validated_at, outcome.id)` and never depends on repository order. The summary is derived on
 demand and is neither persisted nor cached.

+More than one matching persisted outcome always raises ambiguity before selecting or semantically
+comparing a record. This is independent of repository enumeration order and applies to equivalent
+and different duplicate payloads. Zero matches follows normal creation; exactly one match retains
+the equivalent-replay or conflict behavior. This hardening changes no outcome fields, vocabulary,
+relations, ordering, summary, CLI, stored schema, or lifecycle behavior.
+
+### DecisionReviewService
+
+`DecisionReviewService` implements:
+
+```text
+add()
+list_for_decision()
+show()
+```
+
+`add()` constructs the candidate first, so local domain validation precedes repository reads. It
+then requires the Decision, validates the acceptance belongs to it, loads every caller-ordered
+outcome by ID, validates Decision and acceptance ownership, and requires `reviewed_at` to be at or
+after the latest selected outcome validation. Missing or mismatched relations and invalid time all
+fail before persistence.
+
+Review idempotency is scoped by:
+
+```text
+(decision_id, "decision_review", idempotency_key)
+```
+
+```text
+zero scoped matches
+→ save the validated candidate
+
+exactly one equivalent match
+→ validate persisted relations and return existing DecisionReview
+
+exactly one different match
+→ `DecisionReviewIdempotencyConflictError`, no write
+
+more than one persisted scoped match
+→ `DecisionReviewIdempotencyAmbiguityError`, no arbitrary selection or comparison, no write
+```
+
+The ambiguity error carries Decision ID, idempotency key, and match count. Ambiguity is independent
+of repository order and applies to semantically equivalent or different duplicates. For exactly
+one match, semantic equivalence excludes generated review ID and recording time and embedded
+evidence capture times; it includes every caller-supplied semantic field. Ordered outcome IDs,
+findings, candidate lessons, evidence, and tags therefore remain order sensitive.
+
+`list_for_decision()` requires the Decision, validates every persisted relation, and sorts by
+`(reviewed_at, review.id)`. `show()` loads by ID and validates its relations. Controlled errors
+cover missing Decision, acceptance, outcome, or review; acceptance/Decision mismatch;
+outcome/Decision or outcome/acceptance mismatch; review before outcome; idempotency conflict; and
+duplicate-key ambiguity. No failing path writes.
+
+DecisionReview and DecisionOutcome share the reusable fail-closed invariant that multiple matches
+for a scoped idempotency key must be surfaced, never resolved through `next()`, first-match
+selection, repository order, or comparison with an arbitrarily chosen record. Their scopes and
+ambiguity error types remain separate.
+
 ### Canonical DecisionLifecycleService

 `DecisionLifecycleService` is the only canonical owner of the current lifecycle projection. It
@@ -566,6 +690,8 @@ JsonPlaybookRunRepository
 DecisionActionService
 JsonDecisionOutcomeRepository
 DecisionOutcomeService
+JsonDecisionReviewRepository
+DecisionReviewService
 DecisionLifecycleService
 ```

@@ -577,11 +703,14 @@ repositories or own validation, relation checks, persistence, eligibility, or id
 `JsonDecisionAcceptanceRepository`, and `JsonPlaybookRunRepository`. `DecisionOutcomeService`
 receives `JsonDecisionOutcomeRepository` plus Decision, acceptance, and action repositories.
 `DecisionLifecycleService` receives the Decision, acceptance, action, and outcome repositories.
-CLI handlers resolve services from the container and construct no repositories.
+`DecisionReviewService` receives `JsonDecisionReviewRepository` plus Decision, acceptance, and
+outcome repositories. `Container.decision_review_repository()` and
+`Container.decision_review_service()` expose the review composition. CLI handlers resolve services
+from the container and construct no repositories.

 ## Implemented CLI

-These commands exist at commit `5befd7c`:
+These commands exist at commit `910f481e`:

 ```text
 neural decision add
@@ -596,6 +725,9 @@ neural decision outcome add DECISION_UUID
 neural decision outcome-history DECISION_UUID
 neural decision outcome-show OUTCOME_UUID
 neural decision outcome-summary DECISION_UUID
+neural decision review add DECISION_UUID
+neural decision review history DECISION_UUID
+neural decision review show REVIEW_UUID
 neural decision state DECISION_UUID
 ```

@@ -776,6 +908,34 @@ every stored field, including evidence, metrics, idempotency key, and tags.
 result/time, distinct linked-action count, counts by result, and success/failure presence. It does
 not persist the summary.

+### Decision review commands
+
+`neural decision review add DECISION_UUID` requires:
+
+```text
+--acceptance-id
+--outcome-id (one or more, repeatable and ordered)
+--reviewed-by
+--reviewed-at
+--assessment
+--summary
+--finding (one or more, repeatable and ordered)
+--confidence
+--idempotency-key
+```
+
+Optional repeatable inputs are `--candidate-lesson`, `--evidence` JSON, and `--tag`. Assessment
+accepts `sound`, `flawed`, `mixed`, or `inconclusive`; confidence accepts `low`, `medium`, or
+`high`. The CLI parses ISO-8601 review time and embedded evidence but never opens evidence
+locators. Validation errors render their first message; `ValueError` and controlled
+`DecisionReviewError` failures render visibly and exit nonzero. Success prints the stored review ID
+and every review field.
+
+`neural decision review history DECISION_UUID` renders deterministic service history with columns
+`ID`, `Reviewed`, `Reviewed by`, `Assessment`, `Confidence`, `Outcome IDs`, and `Summary`. An
+existing Decision with no reviews renders `No review history found for Decision: ...`.
+`neural decision review show REVIEW_UUID` renders every field after persisted relation validation.
+
 `neural decision state DECISION_UUID` renders exactly one of:

 ```text
@@ -804,12 +964,12 @@ Decision
 - `DecisionAcceptance` is the implemented explicit authorization for possible future execution.
 - `DecisionAction` is the implemented record of work performed under an accepted Decision.
 - `DecisionOutcome` is the implemented factual result and validation evidence record.
-- `DecisionReview` would assess outcomes and hold candidate lessons.
+- `DecisionReview` is the implemented authorized interpretation over explicit ordered outcomes.

-The first four records exist; DecisionReview does not. Records remain immutable semantic records
-rather than fields on a mutable Decision or a duplicate generic event stream. A proposed option is
-not an acceptance, acceptance is not execution, an outcome is not a review or Experience, and
-candidate lessons are not automatically Knowledge or a Playbook change.
+All five records exist. Records remain immutable semantic records rather than fields on a mutable
+Decision or a duplicate generic event stream. A proposed option is not an acceptance, acceptance
+is not execution, an outcome is not a review or Experience, and review findings or candidate
+lessons are not automatically Experience, Knowledge, or a Playbook change.

 The currently derivable projection is only:

@@ -851,7 +1011,7 @@ Observation
 → DecisionAcceptance
 → DecisionAction
 → DecisionOutcome
-→ future DecisionReview
+→ DecisionReview
 → explicitly created Experience
 → explicitly created Knowledge
 ```
@@ -878,7 +1038,7 @@ prompt
 → post-work lesson
 ```

-Commit `5befd7c` does not capture or ingest those events automatically. Automatic candidates and
+Commit `910f481e` does not capture or ingest those events automatically. Automatic candidates and
 manual confirmation remain future concepts; no automatic persistence, ingestion, or learning
 exists.

@@ -887,10 +1047,9 @@ no recommendation can directly mutate NeuralEngine or authorize a durable record

 ## Current non-behavior

-Commit `5befd7c` does not implement:
+Commit `910f481e` does not implement:

 ```text
-DecisionReview
 execution engine
 command/shell execution
 rejection
@@ -912,19 +1071,19 @@ Consigliere integration

 It also does not execute commands referenced by evidence, open locators, automatically accept
 Decisions, materialize Playbook revisions, or infer outcomes from `completed_at`. Explicit user
-requests are required to create Decision, DecisionAcceptance, DecisionAction, or DecisionOutcome
-records.
+requests are required to create Decision, DecisionAcceptance, DecisionAction, DecisionOutcome, or
+DecisionReview records.

 ## Recommended next milestone

-The one recommended next controlled slice is:
+The recommended next controlled slice is:

 ```text
-DecisionReview foundation
+separate explicit Experience creation from DecisionReview findings or candidate lessons
 ```

-It must remain separate from automatic Experience, Knowledge, Playbook, PlaybookEvaluation, or
-EvolutionProposal creation.
+It must preserve explicit authority and remain separate from automatic Knowledge, Playbook,
+PlaybookEvaluation, EvolutionProposal, or Consigliere creation.

 ## Handbook synchronization policy

diff --git a/handbook/container/dependency-injection.md b/handbook/container/dependency-injection.md
index bdb35fd..06318ec 100644
--- a/handbook/container/dependency-injection.md
+++ b/handbook/container/dependency-injection.md
@@ -68,3 +68,9 @@ The outcome foundation is wired through `Container.decision_outcome_repository()
 acceptance, and action repositories. `Container.decision_lifecycle_service()` receives those same
 four repository categories so it can validate relations and derive the canonical state. Decision
 action, outcome, summary, and state CLI handlers resolve services and construct no repositories.
+
+The review foundation is wired through `Container.decision_review_repository()` and
+`Container.decision_review_service()`. The service receives `JsonDecisionReviewRepository`,
+`JsonDecisionRepository`, `JsonDecisionAcceptanceRepository`, and
+`JsonDecisionOutcomeRepository`. Brain initialization creates `NeuralPaths.DECISION_REVIEWS`.
+Decision review CLI handlers resolve the service and construct no repositories.
diff --git a/handbook/decisions/ADR-0008-decision-learning-boundary.md b/handbook/decisions/ADR-0008-decision-learning-boundary.md
index 02861d2..d4415bb 100644
--- a/handbook/decisions/ADR-0008-decision-learning-boundary.md
+++ b/handbook/decisions/ADR-0008-decision-learning-boundary.md
@@ -5,10 +5,11 @@ Status: Accepted
 ## Decision

 Development decision tracking uses implemented separate immutable `Decision`,
-`DecisionAcceptance`, `DecisionAction`, and `DecisionOutcome` records with embedded immutable
-`EvidenceReference` values. `DecisionReview` remains a separate future-only record. Lifecycle
-state is derived from semantic records, not stored as mutable status or duplicated in a generic
-event stream.
+`DecisionAcceptance`, `DecisionAction`, `DecisionOutcome`, and `DecisionReview` records with
+embedded immutable `EvidenceReference` values. Outcome owns factual results; Review owns
+authorized interpretation over an explicit ordered outcome set. Lifecycle state is derived from
+acceptance, actions, and the latest factual outcome, not stored as mutable status or duplicated in
+a generic event stream. Review is orthogonal append-only history.

 Decision tracking complements the existing Observation-to-Playbook chain. Evidence uses bounded
 embedded references, durable writes require explicit authority, and Consigliere remains a future
@@ -22,8 +23,9 @@ advisory layer rather than authoritative storage.
   idempotency checks; repository ports remain persistence-focused.
 - No automatic ingestion, persistence, learning, Playbook evolution, or Consigliere integration is
   implied.
-- Source commit `5befd7c` implements Decision proposal, acceptance, action and outcome recording,
-  outcome history/summary, their CLI, and the canonical `DecisionLifecycleService`.
+- Source commit `910f481e27302daa6d3f15bde30d678ffc9e5d2f` implements Decision proposal,
+  acceptance, action, outcome, and review recording; outcome history/summary; review history; their
+  CLI; and the canonical `DecisionLifecycleService`.
 - The canonical states are exactly proposed, accepted, in-progress, succeeded, failed, partial,
   and outcome-unknown. Latest outcome selection uses validation time and outcome UUID, not
   repository order. No generic completed, resolved, or reviewed state exists.
@@ -31,5 +33,12 @@ advisory layer rather than authoritative storage.
   creates no later lifecycle or learning record.
 - Multiple immutable outcomes may be appended for one Decision. Outcome creation is factual only
   and creates no review or learning record.
-- The one recommended next milestone is `DecisionReview foundation`, kept separate from automatic
-  learning and downstream Experience, Knowledge, or Playbook creation.
+- Multiple immutable reviews may cover one Decision, outcome, or ordered outcome set. Corrections
+  append, action provenance remains transitive through outcomes, and no `current`, replacement,
+  supersession, deletion, lifecycle transition, or automatic learning behavior exists.
+- Outcome and review idempotency both fail closed when more than one persisted record matches a
+  scoped key: their distinct ambiguity errors replace arbitrary first-match selection and no write
+  occurs regardless of repository order or payload equivalence.
+- The recommended next controlled slice is separate explicit Experience creation from review
+  findings or candidate lessons; downstream Experience, Knowledge, or Playbook creation remains
+  explicit.
diff --git a/handbook/domain/decision-outcome.md b/handbook/domain/decision-outcome.md
index e360021..c702db1 100644
--- a/handbook/domain/decision-outcome.md
+++ b/handbook/domain/decision-outcome.md
@@ -42,8 +42,12 @@ bounded to 1000 characters, and nested values are rejected. JSON serialization s

 Idempotency is scoped by `(decision_id, "decision_outcome", idempotency_key)`. Equivalent replay
 returns the existing outcome. Reusing the same scoped key with a different semantic payload fails
-without a write. Generated outcome ID, recording time, and evidence capture times are excluded
-from semantic equivalence; a different key may append another outcome for the same Decision.
+without a write. If more than one persisted outcome matches the scoped key,
+`DecisionOutcomeIdempotencyAmbiguityError` is raised whether their payloads are equivalent or
+different. The service never chooses an arbitrary duplicate, the result is independent of
+repository enumeration order, and no write occurs. Generated outcome ID, recording time, and
+evidence capture times are excluded from the exactly-one-match semantic comparison; a different
+key may append another outcome for the same Decision.

 `DecisionOutcomeSummary` is an immutable, non-persisted read model derived on demand. It reports
 outcome count, latest result and validation time, distinct linked-action count, counts for every
@@ -57,6 +61,7 @@ order.
 `outcome_unknown`. Earlier outcomes remain available as history. No `completed` or `resolved`
 lifecycle state exists.

-DecisionReview is not implemented. Recording an outcome does not review a Decision and does not
-create Observation, Experience, Knowledge, Playbook, PlaybookEvaluation, EvolutionProposal, or
-automatic learning. The next milestone is the separate DecisionReview foundation.
+Recording an outcome does not review a Decision and does not create Observation, Experience,
+Knowledge, Playbook, PlaybookEvaluation, EvolutionProposal, or automatic learning. The separately
+implemented DecisionReview foundation interprets explicit outcomes without rewriting them or
+changing lifecycle state.
diff --git a/handbook/domain/domain-chain.md b/handbook/domain/domain-chain.md
index 9736490..6f447a0 100644
--- a/handbook/domain/domain-chain.md
+++ b/handbook/domain/domain-chain.md
@@ -39,9 +39,9 @@ Confirmed example:

 ## Complementary Decision Learning chain

-The implemented Decision, DecisionAcceptance, DecisionAction, and DecisionOutcome foundations
-record a bounded proposed choice, explicit authorization, work performed, and factual results
-after Observation context:
+The implemented Decision, DecisionAcceptance, DecisionAction, DecisionOutcome, and DecisionReview
+foundations record a bounded proposed choice, explicit authorization, work performed, factual
+results, and authorized interpretation after Observation context:

 ```text
 Observation
@@ -49,14 +49,16 @@ Observation
 → DecisionAcceptance
 → DecisionAction
 → DecisionOutcome
-→ future DecisionReview
-→ Experience
-→ Knowledge
+→ DecisionReview
+→ explicitly created Experience
+→ explicitly created Knowledge
 ```

 This is a complementary provenance path, not a replacement for the canonical domain chain.
-DecisionOutcome is factual; Experience is interpreted; Knowledge is generalized; Playbook remains
-a separately created repeatable procedure. DecisionOutcome may have multiple immutable records per
-Decision and does not automatically create a Review or learning artifact. Decision,
-DecisionAcceptance, DecisionAction, DecisionOutcome, and their embedded EvidenceReference values
-exist at source commit `5befd7c`; no Review or later transition in this path is automatic.
+DecisionOutcome is factual; DecisionReview is authorized interpretation; Experience captures
+separately created operational learning; Knowledge is generalized; Playbook remains a separately
+created repeatable procedure. A Decision may have multiple immutable outcomes and multiple reviews,
+including reviews over the same ordered outcome set when their idempotency keys differ. Review
+action provenance is transitive through its explicit outcomes; it does not persist action IDs.
+These records and their embedded EvidenceReference values exist at source commit `910f481e`; no
+Review-driven lifecycle transition or later learning record in this path is automatic.
diff --git a/handbook/infrastructure/repositories.md b/handbook/infrastructure/repositories.md
index 77e9f87..c6c2e92 100644
--- a/handbook/infrastructure/repositories.md
+++ b/handbook/infrastructure/repositories.md
@@ -66,3 +66,12 @@ validation. JSON object keys and metric keys are serialized deterministically, `
 file names, and malformed data surfaces validation errors. The adapter performs no relation
 validation or filtering, latest-outcome selection, summary or lifecycle projection, idempotency
 decision, migration, ingestion, review, or learning.
+
+## Decision review adapter
+
+`JsonDecisionReviewRepository` implements `DecisionReviewRepository` and stores one JSON file per
+review under `NeuralPaths.DECISION_REVIEWS`; Brain initialization creates the directory. Complete
+DecisionReview records round-trip through domain validation. JSON object keys are serialized with
+`indent=2` and `sort_keys=True`, `load_all()` sorts filenames, and malformed data surfaces
+validation errors. The adapter performs no Decision filtering, relation validation, chronology,
+idempotency selection, lifecycle projection, evidence ingestion, learning, or Consigliere work.
diff --git a/handbook/ports/repository-ports.md b/handbook/ports/repository-ports.md
index 69edd5d..18a492f 100644
--- a/handbook/ports/repository-ports.md
+++ b/handbook/ports/repository-ports.md
@@ -45,6 +45,11 @@ Decision filtering, acceptance/action relation validation, multiple-outcome hist
 summary derivation, and lifecycle projection belong to application services; no relation,
 idempotency, summary, latest-outcome, or lifecycle query method is part of the port.

+`DecisionReviewRepository` is likewise limited to `save()`, `load_all()`, and `get_by_id()`.
+Decision filtering, cross-record validation, history ordering, and scoped idempotency—including
+fail-closed duplicate-match ambiguity—belong to `DecisionReviewService`; no relation,
+idempotency, chronology, or lifecycle query method is part of the port.
+
 ## Repository return types

 Prefer:
diff --git a/outputs/claude-skill/SKILL.md b/outputs/claude-skill/SKILL.md
index 94e0a1b..2821d0f 100644
--- a/outputs/claude-skill/SKILL.md
+++ b/outputs/claude-skill/SKILL.md
@@ -118,23 +118,27 @@ a milestone snapshot, not a timeless guarantee.

 ## Decision Learning boundary

-Source commit `5befd7c` implements separate immutable `Decision`, `DecisionAcceptance`,
-`DecisionAction`, and `DecisionOutcome` records, persistence-focused ports and JSON adapters,
-application services, container wiring, thin proposal/acceptance/action/outcome CLI commands, and
-the canonical `DecisionLifecycleService`. An action records work performed; only a linked outcome
-records factual results and validation evidence.
+Source commit `910f481e27302daa6d3f15bde30d678ffc9e5d2f` implements separate immutable
+`Decision`, `DecisionAcceptance`, `DecisionAction`, `DecisionOutcome`, and `DecisionReview`
+records, persistence-focused ports and JSON adapters, application services, container wiring,
+thin proposal/acceptance/action/outcome/review CLI commands, and the canonical
+`DecisionLifecycleService`. An action records work performed; only a linked outcome records
+factual results and validation evidence; a review records authorized interpretation.

 `DecisionOutcome` links one Decision, its acceptance, and one or more ordered unique actions. Its
 result is exactly `succeeded`, `failed`, `partial`, or `unknown`; scalar metrics are immutable.
 Multiple outcomes form history, and the non-persisted `DecisionOutcomeSummary` derives counts and
 the latest outcome using `(validated_at, outcome.id)` rather than repository order.
+`DecisionReview` targets an explicit ordered non-empty set of outcomes for one Decision and
+acceptance. Multiple reviews form immutable history ordered by `(reviewed_at, review.id)`.

-The canonical lifecycle states are exactly `proposed`, `accepted`, `in_progress`, `succeeded`,
-`failed`, `partial`, and `outcome_unknown`. `DecisionReview` and a reviewed state remain
-future-only. Outcome creation does not create learning. There is no execution engine, lifecycle
-reversal, ingestion, automatic learning or evolution, generic event replay, or Consigliere
-integration. The authoritative implemented contract and future boundary are defined in
-`handbook/architecture/decision-learning.md`; the next milestone is the DecisionReview foundation.
+The canonical lifecycle states remain exactly `proposed`, `accepted`, `in_progress`, `succeeded`,
+`failed`, `partial`, and `outcome_unknown`. Review is orthogonal append-only history; there is no
+`reviewed` state. Outcome or review creation does not create learning. There is no execution
+engine, lifecycle reversal, ingestion, automatic learning or evolution, generic event replay, or
+Consigliere integration. The authoritative implemented contract and future boundary are defined
+in `handbook/architecture/decision-learning.md`; the recommended next controlled slice is
+separate explicit Experience creation from review findings or candidate lessons.

 ## Decision Learning architecture

@@ -142,11 +146,12 @@ integration. The authoritative implemented contract and future boundary are defi

 ## Status and purpose

-NeuralEngine source commit `5befd7c` implements the Decision, DecisionAcceptance,
-DecisionAction, and DecisionOutcome foundations plus the canonical `DecisionLifecycleService`
-projection. They record an immutable proposed choice, explicit authorization, work performed under
-that authorization, and factual results. Each foundation persists immutable records, exposes
-application use cases, is wired through the container, and provides a thin CLI.
+NeuralEngine source commit `910f481e27302daa6d3f15bde30d678ffc9e5d2f` implements the Decision,
+DecisionAcceptance, DecisionAction, DecisionOutcome, and DecisionReview foundations plus the
+canonical `DecisionLifecycleService` projection. They record an immutable proposed choice,
+explicit authorization, work performed under that authorization, factual results, and authorized
+interpretation. Each foundation persists immutable records, exposes application use cases, is
+wired through the container, and provides a thin CLI.

 The wider Decision Learning lifecycle remains accepted future architecture. Decision tracking
 complements the existing Observation-to-Playbook chain; it does not replace it.
@@ -161,19 +166,23 @@ EvidenceReference
 DecisionAcceptance
 DecisionAction
 DecisionOutcome
+DecisionReview
 DecisionRepository
 DecisionAcceptanceRepository
 DecisionActionRepository
 DecisionOutcomeRepository
+DecisionReviewRepository
 JsonDecisionRepository
 JsonDecisionAcceptanceRepository
 JsonDecisionActionRepository
 JsonDecisionOutcomeRepository
+JsonDecisionReviewRepository
 DecisionService
 DecisionAcceptanceService
 DecisionActionService
 DecisionOutcomeService
 DecisionOutcomeSummary
+DecisionReviewService
 DecisionLifecycleService
 container wiring
 neural decision add/list/show
@@ -186,14 +195,17 @@ neural decision outcome add
 neural decision outcome-history
 neural decision outcome-show
 neural decision outcome-summary
+neural decision review add
+neural decision review history
+neural decision review show
 neural decision state
 ```

 Creating a Decision records a proposal. Creating a DecisionAcceptance explicitly authorizes that
 proposal for possible future work. Creating a DecisionAction records work performed under that
 acceptance. Creating a DecisionOutcome records factual results and validation evidence for one or
-more linked actions. None of these operations performs review or learning. `DecisionReview`
-remains future-only.
+more linked actions. Creating a DecisionReview records authorized interpretation over an explicit
+ordered outcome set. None of these operations automatically creates learning.

 ## Decision model

@@ -236,7 +248,7 @@ not rewrite the earlier record.
 ## EvidenceReference

 `EvidenceReference` is an implemented immutable value embedded in a Decision,
-DecisionAcceptance, DecisionAction, or DecisionOutcome:
+DecisionAcceptance, DecisionAction, DecisionOutcome, or DecisionReview:

 ```text
 kind
@@ -384,6 +396,46 @@ One Decision may have multiple outcomes. Each outcome appends factual history an
 more actions; no outcome replaces or mutates an earlier record. An outcome does not mean review,
 Experience, Knowledge, Playbook change, or automatic learning occurred.

+## DecisionReview foundation
+
+`DecisionReview` is an immutable, append-only authorized interpretation record with these exact
+implemented fields:
+
+```text
+id
+recorded_at
+decision_id
+acceptance_id
+outcome_ids
+reviewed_by
+reviewed_at
+assessment
+summary
+findings
+candidate_lessons
+evidence_references
+confidence
+idempotency_key
+tags
+```
+
+Assessment is exactly `sound`, `flawed`, `mixed`, or `inconclusive`; confidence is exactly `low`,
+`medium`, or `high`. Assessment is not the outcome result vocabulary: successful factual outcomes
+may support a flawed review, and failed outcomes may support a sound review.
+
+`outcome_ids` is ordered, unique, and non-empty. Findings are required ordered text; findings and
+candidate lessons each allow at most 100 case-insensitively unique entries of at most 1000
+characters. Candidate lessons may be empty and have no promotion authority. Reviewer is bounded to
+255 characters and summary to 1000; required text is trimmed and non-blank. Tags preserve
+first-seen order while removing case-insensitive duplicates. UTC-aware timestamps are normalized
+to UTC, and `reviewed_at` cannot be later than `recorded_at`.
+
+Every outcome must exist and belong to the same Decision and acceptance. Review time cannot
+precede the latest `validated_at` among selected outcomes. Action IDs are not persisted: provenance
+is transitive through `DecisionReview → DecisionOutcome[] → DecisionAction[]`. Multiple reviews
+may cover one Decision, outcome, or ordered outcome set under different keys. Corrections append;
+there is no replacement, supersession, deletion, or persisted `current` behavior.
+
 ## Persistence

 The persistence-focused `DecisionRepository` port implements only:
@@ -446,6 +498,20 @@ and immutable scalar metrics round-trip through domain validation; malformed dat
 The adapter performs no relation filtering, lifecycle projection, review, learning, migration, or
 ingestion.

+The persistence-focused `DecisionReviewRepository` implements only:
+
+```text
+save()
+load_all()
+get_by_id()
+```
+
+It has no relation, idempotency, chronology, or lifecycle query methods.
+`JsonDecisionReviewRepository` stores one deterministic sorted-key JSON file per review under
+`NeuralPaths.DECISION_REVIEWS`, and Brain initialization creates that directory. `load_all()` sorts
+filenames and every record round-trips through domain validation. Filtering, relation validation,
+history ordering, ambiguity detection, and semantic comparison remain in the application service.
+
 ## Application service

 `DecisionService` implements:
@@ -629,6 +695,9 @@ same scoped key + equivalent semantic payload
 same scoped key + different semantic payload
 → visible conflict, no write

+more than one persisted scoped match
+→ `DecisionOutcomeIdempotencyAmbiguityError`, no arbitrary selection, no write
+
 different key
 → another outcome may be recorded
 ```
@@ -648,6 +717,65 @@ validates every persisted outcome-to-acceptance/action relation. Latest selectio
 by `(validated_at, outcome.id)` and never depends on repository order. The summary is derived on
 demand and is neither persisted nor cached.

+More than one matching persisted outcome always raises ambiguity before selecting or semantically
+comparing a record. This is independent of repository enumeration order and applies to equivalent
+and different duplicate payloads. Zero matches follows normal creation; exactly one match retains
+the equivalent-replay or conflict behavior. This hardening changes no outcome fields, vocabulary,
+relations, ordering, summary, CLI, stored schema, or lifecycle behavior.
+
+### DecisionReviewService
+
+`DecisionReviewService` implements:
+
+```text
+add()
+list_for_decision()
+show()
+```
+
+`add()` constructs the candidate first, so local domain validation precedes repository reads. It
+then requires the Decision, validates the acceptance belongs to it, loads every caller-ordered
+outcome by ID, validates Decision and acceptance ownership, and requires `reviewed_at` to be at or
+after the latest selected outcome validation. Missing or mismatched relations and invalid time all
+fail before persistence.
+
+Review idempotency is scoped by:
+
+```text
+(decision_id, "decision_review", idempotency_key)
+```
+
+```text
+zero scoped matches
+→ save the validated candidate
+
+exactly one equivalent match
+→ validate persisted relations and return existing DecisionReview
+
+exactly one different match
+→ `DecisionReviewIdempotencyConflictError`, no write
+
+more than one persisted scoped match
+→ `DecisionReviewIdempotencyAmbiguityError`, no arbitrary selection or comparison, no write
+```
+
+The ambiguity error carries Decision ID, idempotency key, and match count. Ambiguity is independent
+of repository order and applies to semantically equivalent or different duplicates. For exactly
+one match, semantic equivalence excludes generated review ID and recording time and embedded
+evidence capture times; it includes every caller-supplied semantic field. Ordered outcome IDs,
+findings, candidate lessons, evidence, and tags therefore remain order sensitive.
+
+`list_for_decision()` requires the Decision, validates every persisted relation, and sorts by
+`(reviewed_at, review.id)`. `show()` loads by ID and validates its relations. Controlled errors
+cover missing Decision, acceptance, outcome, or review; acceptance/Decision mismatch;
+outcome/Decision or outcome/acceptance mismatch; review before outcome; idempotency conflict; and
+duplicate-key ambiguity. No failing path writes.
+
+DecisionReview and DecisionOutcome share the reusable fail-closed invariant that multiple matches
+for a scoped idempotency key must be surfaced, never resolved through `next()`, first-match
+selection, repository order, or comparison with an arbitrarily chosen record. Their scopes and
+ambiguity error types remain separate.
+
 ### Canonical DecisionLifecycleService

 `DecisionLifecycleService` is the only canonical owner of the current lifecycle projection. It
@@ -706,6 +834,8 @@ JsonPlaybookRunRepository
 DecisionActionService
 JsonDecisionOutcomeRepository
 DecisionOutcomeService
+JsonDecisionReviewRepository
+DecisionReviewService
 DecisionLifecycleService
 ```

@@ -717,11 +847,14 @@ repositories or own validation, relation checks, persistence, eligibility, or id
 `JsonDecisionAcceptanceRepository`, and `JsonPlaybookRunRepository`. `DecisionOutcomeService`
 receives `JsonDecisionOutcomeRepository` plus Decision, acceptance, and action repositories.
 `DecisionLifecycleService` receives the Decision, acceptance, action, and outcome repositories.
-CLI handlers resolve services from the container and construct no repositories.
+`DecisionReviewService` receives `JsonDecisionReviewRepository` plus Decision, acceptance, and
+outcome repositories. `Container.decision_review_repository()` and
+`Container.decision_review_service()` expose the review composition. CLI handlers resolve services
+from the container and construct no repositories.

 ## Implemented CLI

-These commands exist at commit `5befd7c`:
+These commands exist at commit `910f481e`:

 ```text
 neural decision add
@@ -736,6 +869,9 @@ neural decision outcome add DECISION_UUID
 neural decision outcome-history DECISION_UUID
 neural decision outcome-show OUTCOME_UUID
 neural decision outcome-summary DECISION_UUID
+neural decision review add DECISION_UUID
+neural decision review history DECISION_UUID
+neural decision review show REVIEW_UUID
 neural decision state DECISION_UUID
 ```

@@ -916,6 +1052,34 @@ every stored field, including evidence, metrics, idempotency key, and tags.
 result/time, distinct linked-action count, counts by result, and success/failure presence. It does
 not persist the summary.

+### Decision review commands
+
+`neural decision review add DECISION_UUID` requires:
+
+```text
+--acceptance-id
+--outcome-id (one or more, repeatable and ordered)
+--reviewed-by
+--reviewed-at
+--assessment
+--summary
+--finding (one or more, repeatable and ordered)
+--confidence
+--idempotency-key
+```
+
+Optional repeatable inputs are `--candidate-lesson`, `--evidence` JSON, and `--tag`. Assessment
+accepts `sound`, `flawed`, `mixed`, or `inconclusive`; confidence accepts `low`, `medium`, or
+`high`. The CLI parses ISO-8601 review time and embedded evidence but never opens evidence
+locators. Validation errors render their first message; `ValueError` and controlled
+`DecisionReviewError` failures render visibly and exit nonzero. Success prints the stored review ID
+and every review field.
+
+`neural decision review history DECISION_UUID` renders deterministic service history with columns
+`ID`, `Reviewed`, `Reviewed by`, `Assessment`, `Confidence`, `Outcome IDs`, and `Summary`. An
+existing Decision with no reviews renders `No review history found for Decision: ...`.
+`neural decision review show REVIEW_UUID` renders every field after persisted relation validation.
+
 `neural decision state DECISION_UUID` renders exactly one of:

 ```text
@@ -944,12 +1108,12 @@ Decision
 - `DecisionAcceptance` is the implemented explicit authorization for possible future execution.
 - `DecisionAction` is the implemented record of work performed under an accepted Decision.
 - `DecisionOutcome` is the implemented factual result and validation evidence record.
-- `DecisionReview` would assess outcomes and hold candidate lessons.
+- `DecisionReview` is the implemented authorized interpretation over explicit ordered outcomes.

-The first four records exist; DecisionReview does not. Records remain immutable semantic records
-rather than fields on a mutable Decision or a duplicate generic event stream. A proposed option is
-not an acceptance, acceptance is not execution, an outcome is not a review or Experience, and
-candidate lessons are not automatically Knowledge or a Playbook change.
+All five records exist. Records remain immutable semantic records rather than fields on a mutable
+Decision or a duplicate generic event stream. A proposed option is not an acceptance, acceptance
+is not execution, an outcome is not a review or Experience, and review findings or candidate
+lessons are not automatically Experience, Knowledge, or a Playbook change.

 The currently derivable projection is only:

@@ -991,7 +1155,7 @@ Observation
 → DecisionAcceptance
 → DecisionAction
 → DecisionOutcome
-→ future DecisionReview
+→ DecisionReview
 → explicitly created Experience
 → explicitly created Knowledge
 ```
@@ -1018,7 +1182,7 @@ prompt
 → post-work lesson
 ```

-Commit `5befd7c` does not capture or ingest those events automatically. Automatic candidates and
+Commit `910f481e` does not capture or ingest those events automatically. Automatic candidates and
 manual confirmation remain future concepts; no automatic persistence, ingestion, or learning
 exists.

@@ -1027,10 +1191,9 @@ no recommendation can directly mutate NeuralEngine or authorize a durable record

 ## Current non-behavior

-Commit `5befd7c` does not implement:
+Commit `910f481e` does not implement:

 ```text
-DecisionReview
 execution engine
 command/shell execution
 rejection
@@ -1052,19 +1215,19 @@ Consigliere integration

 It also does not execute commands referenced by evidence, open locators, automatically accept
 Decisions, materialize Playbook revisions, or infer outcomes from `completed_at`. Explicit user
-requests are required to create Decision, DecisionAcceptance, DecisionAction, or DecisionOutcome
-records.
+requests are required to create Decision, DecisionAcceptance, DecisionAction, DecisionOutcome, or
+DecisionReview records.

 ## Recommended next milestone

-The one recommended next controlled slice is:
+The recommended next controlled slice is:

 ```text
-DecisionReview foundation
+separate explicit Experience creation from DecisionReview findings or candidate lessons
 ```

-It must remain separate from automatic Experience, Knowledge, Playbook, PlaybookEvaluation, or
-EvolutionProposal creation.
+It must preserve explicit authority and remain separate from automatic Knowledge, Playbook,
+PlaybookEvaluation, EvolutionProposal, or Consigliere creation.

 ## Handbook synchronization policy

@@ -1114,9 +1277,9 @@ Confirmed example:

 ## Complementary Decision Learning chain

-The implemented Decision, DecisionAcceptance, DecisionAction, and DecisionOutcome foundations
-record a bounded proposed choice, explicit authorization, work performed, and factual results
-after Observation context:
+The implemented Decision, DecisionAcceptance, DecisionAction, DecisionOutcome, and DecisionReview
+foundations record a bounded proposed choice, explicit authorization, work performed, factual
+results, and authorized interpretation after Observation context:

 ```text
 Observation
@@ -1124,17 +1287,19 @@ Observation
 → DecisionAcceptance
 → DecisionAction
 → DecisionOutcome
-→ future DecisionReview
-→ Experience
-→ Knowledge
+→ DecisionReview
+→ explicitly created Experience
+→ explicitly created Knowledge
 ```

 This is a complementary provenance path, not a replacement for the canonical domain chain.
-DecisionOutcome is factual; Experience is interpreted; Knowledge is generalized; Playbook remains
-a separately created repeatable procedure. DecisionOutcome may have multiple immutable records per
-Decision and does not automatically create a Review or learning artifact. Decision,
-DecisionAcceptance, DecisionAction, DecisionOutcome, and their embedded EvidenceReference values
-exist at source commit `5befd7c`; no Review or later transition in this path is automatic.
+DecisionOutcome is factual; DecisionReview is authorized interpretation; Experience captures
+separately created operational learning; Knowledge is generalized; Playbook remains a separately
+created repeatable procedure. A Decision may have multiple immutable outcomes and multiple reviews,
+including reviews over the same ordered outcome set when their idempotency keys differ. Review
+action provenance is transitive through its explicit outcomes; it does not persist action IDs.
+These records and their embedded EvidenceReference values exist at source commit `910f481e`; no
+Review-driven lifecycle transition or later learning record in this path is automatic.

 ## Workflow

diff --git a/outputs/generated/AGENTS.generated.md b/outputs/generated/AGENTS.generated.md
index e287853..31bc748 100644
--- a/outputs/generated/AGENTS.generated.md
+++ b/outputs/generated/AGENTS.generated.md
@@ -137,23 +137,27 @@ a milestone snapshot, not a timeless guarantee.

 ## Decision Learning boundary

-Source commit `5befd7c` implements separate immutable `Decision`, `DecisionAcceptance`,
-`DecisionAction`, and `DecisionOutcome` records, persistence-focused ports and JSON adapters,
-application services, container wiring, thin proposal/acceptance/action/outcome CLI commands, and
-the canonical `DecisionLifecycleService`. An action records work performed; only a linked outcome
-records factual results and validation evidence.
+Source commit `910f481e27302daa6d3f15bde30d678ffc9e5d2f` implements separate immutable
+`Decision`, `DecisionAcceptance`, `DecisionAction`, `DecisionOutcome`, and `DecisionReview`
+records, persistence-focused ports and JSON adapters, application services, container wiring,
+thin proposal/acceptance/action/outcome/review CLI commands, and the canonical
+`DecisionLifecycleService`. An action records work performed; only a linked outcome records
+factual results and validation evidence; a review records authorized interpretation.

 `DecisionOutcome` links one Decision, its acceptance, and one or more ordered unique actions. Its
 result is exactly `succeeded`, `failed`, `partial`, or `unknown`; scalar metrics are immutable.
 Multiple outcomes form history, and the non-persisted `DecisionOutcomeSummary` derives counts and
 the latest outcome using `(validated_at, outcome.id)` rather than repository order.
-
-The canonical lifecycle states are exactly `proposed`, `accepted`, `in_progress`, `succeeded`,
-`failed`, `partial`, and `outcome_unknown`. `DecisionReview` and a reviewed state remain
-future-only. Outcome creation does not create learning. There is no execution engine, lifecycle
-reversal, ingestion, automatic learning or evolution, generic event replay, or Consigliere
-integration. The authoritative implemented contract and future boundary are defined in
-`handbook/architecture/decision-learning.md`; the next milestone is the DecisionReview foundation.
+`DecisionReview` targets an explicit ordered non-empty set of outcomes for one Decision and
+acceptance. Multiple reviews form immutable history ordered by `(reviewed_at, review.id)`.
+
+The canonical lifecycle states remain exactly `proposed`, `accepted`, `in_progress`, `succeeded`,
+`failed`, `partial`, and `outcome_unknown`. Review is orthogonal append-only history; there is no
+`reviewed` state. Outcome or review creation does not create learning. There is no execution
+engine, lifecycle reversal, ingestion, automatic learning or evolution, generic event replay, or
+Consigliere integration. The authoritative implemented contract and future boundary are defined
+in `handbook/architecture/decision-learning.md`; the recommended next controlled slice is
+separate explicit Experience creation from review findings or candidate lessons.

 ## Agent policy

diff --git a/outputs/generated/APPLICATION_ARCHITECTURE.md b/outputs/generated/APPLICATION_ARCHITECTURE.md
index 5d90c05..195c578 100644
--- a/outputs/generated/APPLICATION_ARCHITECTURE.md
+++ b/outputs/generated/APPLICATION_ARCHITECTURE.md
@@ -120,9 +120,12 @@ learning record.
 `DecisionOutcomeService.add()` validates the Decision, matching acceptance, one or more unique
 actions, each action's Decision and acceptance relations, and validation time against the earliest
 linked action start before constructing or saving an immutable outcome. It uses
-`(decision_id, "decision_outcome", idempotency_key)` for application-layer idempotency. Equivalent
-replay returns the existing outcome; conflicting reuse fails without a write; another key may
-append another outcome for the same Decision.
+`(decision_id, "decision_outcome", idempotency_key)` for application-layer idempotency. Zero
+matches creates normally; exactly one equivalent match returns the existing outcome; exactly one
+different match conflicts. More than one persisted scoped match raises
+`DecisionOutcomeIdempotencyAmbiguityError`, regardless of payload equivalence or repository order,
+without selecting a duplicate or writing. Another key may append another outcome for the same
+Decision.

 `list_for_decision()` validates the Decision and returns all matching outcomes in repository order.
 `show()` owns explicit outcome-not-found behavior. `summary_for_decision()` validates persisted
@@ -138,6 +141,34 @@ latest is selected by `(validated_at, outcome.id)`. It writes no status and expo
 `completed`, `resolved`, or reviewed state. Outcome creation and projection create no Review or
 learning record.

+## Decision review ownership
+
+`DecisionReviewService.add()` first constructs the immutable candidate, then validates Decision,
+matching acceptance, every explicit ordered outcome relation, and that `reviewed_at` is not earlier
+than the latest referenced outcome validation. It writes only after all validation. The scope is
+`(decision_id, "decision_review", idempotency_key)`: zero matches creates, exactly one equivalent
+match replays, and exactly one different match raises `DecisionReviewIdempotencyConflictError`.
+More than one match raises `DecisionReviewIdempotencyAmbiguityError` with identifying details,
+independent of repository order and duplicate payload equivalence, without arbitrary selection,
+semantic comparison against a selected duplicate, or a write.
+
+Semantic comparison for the exactly-one-match case excludes generated review ID and recording
+time plus evidence capture times. It includes ordered outcome IDs, findings, candidate lessons,
+evidence, tags, and every other caller-supplied semantic field, so ordered collections remain order
+sensitive. `list_for_decision()` validates the Decision and every persisted review relation, then
+sorts by `(reviewed_at, review.id)`. `show()` validates persisted relations and owns explicit
+review-not-found behavior.
+
+Multiple reviews may cover one Decision, one outcome, or the same ordered outcome set under
+different keys. Corrections append; the service has no replacement, supersession, deletion, or
+`current` behavior. It creates no Experience, Knowledge, Playbook, proposal, or Consigliere work
+and does not participate in `DecisionLifecycleService`.
+
+The DecisionOutcome and DecisionReview duplicate-key rules are the same reusable fail-closed
+application-service invariant: more than one persisted match for a scoped key is corruption or
+ambiguity to surface, never an ordering problem to resolve by choosing the first record. Their
+scopes and controlled ambiguity error types remain separate.
+
 ---

 # Application Errors
@@ -262,6 +293,11 @@ Decision filtering, acceptance/action relation validation, multiple-outcome hist
 summary derivation, and lifecycle projection belong to application services; no relation,
 idempotency, summary, latest-outcome, or lifecycle query method is part of the port.

+`DecisionReviewRepository` is likewise limited to `save()`, `load_all()`, and `get_by_id()`.
+Decision filtering, cross-record validation, history ordering, and scoped idempotency—including
+fail-closed duplicate-match ambiguity—belong to `DecisionReviewService`; no relation,
+idempotency, chronology, or lifecycle query method is part of the port.
+
 ## Repository return types

 Prefer:
@@ -398,6 +434,15 @@ file names, and malformed data surfaces validation errors. The adapter performs
 validation or filtering, latest-outcome selection, summary or lifecycle projection, idempotency
 decision, migration, ingestion, review, or learning.

+## Decision review adapter
+
+`JsonDecisionReviewRepository` implements `DecisionReviewRepository` and stores one JSON file per
+review under `NeuralPaths.DECISION_REVIEWS`; Brain initialization creates the directory. Complete
+DecisionReview records round-trip through domain validation. JSON object keys are serialized with
+`indent=2` and `sort_keys=True`, `load_all()` sorts filenames, and malformed data surfaces
+validation errors. The adapter performs no Decision filtering, relation validation, chronology,
+idempotency selection, lifecycle projection, evidence ingestion, learning, or Consigliere work.
+
 ---

 # Dependency Injection and Container
@@ -471,6 +516,12 @@ acceptance, and action repositories. `Container.decision_lifecycle_service()` re
 four repository categories so it can validate relations and derive the canonical state. Decision
 action, outcome, summary, and state CLI handlers resolve services and construct no repositories.

+The review foundation is wired through `Container.decision_review_repository()` and
+`Container.decision_review_service()`. The service receives `JsonDecisionReviewRepository`,
+`JsonDecisionRepository`, `JsonDecisionAcceptanceRepository`, and
+`JsonDecisionOutcomeRepository`. Brain initialization creates `NeuralPaths.DECISION_REVIEWS`.
+Decision review CLI handlers resolve the service and construct no repositories.
+
 ---

 # Dependency Lifecycle
diff --git a/outputs/generated/DECISION_ENGINE.md b/outputs/generated/DECISION_ENGINE.md
index 40ea38e..fecf8bd 100644
--- a/outputs/generated/DECISION_ENGINE.md
+++ b/outputs/generated/DECISION_ENGINE.md
@@ -104,11 +104,12 @@ New behavior

 ## Status and purpose

-NeuralEngine source commit `5befd7c` implements the Decision, DecisionAcceptance,
-DecisionAction, and DecisionOutcome foundations plus the canonical `DecisionLifecycleService`
-projection. They record an immutable proposed choice, explicit authorization, work performed under
-that authorization, and factual results. Each foundation persists immutable records, exposes
-application use cases, is wired through the container, and provides a thin CLI.
+NeuralEngine source commit `910f481e27302daa6d3f15bde30d678ffc9e5d2f` implements the Decision,
+DecisionAcceptance, DecisionAction, DecisionOutcome, and DecisionReview foundations plus the
+canonical `DecisionLifecycleService` projection. They record an immutable proposed choice,
+explicit authorization, work performed under that authorization, factual results, and authorized
+interpretation. Each foundation persists immutable records, exposes application use cases, is
+wired through the container, and provides a thin CLI.

 The wider Decision Learning lifecycle remains accepted future architecture. Decision tracking
 complements the existing Observation-to-Playbook chain; it does not replace it.
@@ -123,19 +124,23 @@ EvidenceReference
 DecisionAcceptance
 DecisionAction
 DecisionOutcome
+DecisionReview
 DecisionRepository
 DecisionAcceptanceRepository
 DecisionActionRepository
 DecisionOutcomeRepository
+DecisionReviewRepository
 JsonDecisionRepository
 JsonDecisionAcceptanceRepository
 JsonDecisionActionRepository
 JsonDecisionOutcomeRepository
+JsonDecisionReviewRepository
 DecisionService
 DecisionAcceptanceService
 DecisionActionService
 DecisionOutcomeService
 DecisionOutcomeSummary
+DecisionReviewService
 DecisionLifecycleService
 container wiring
 neural decision add/list/show
@@ -148,14 +153,17 @@ neural decision outcome add
 neural decision outcome-history
 neural decision outcome-show
 neural decision outcome-summary
+neural decision review add
+neural decision review history
+neural decision review show
 neural decision state
 ```

 Creating a Decision records a proposal. Creating a DecisionAcceptance explicitly authorizes that
 proposal for possible future work. Creating a DecisionAction records work performed under that
 acceptance. Creating a DecisionOutcome records factual results and validation evidence for one or
-more linked actions. None of these operations performs review or learning. `DecisionReview`
-remains future-only.
+more linked actions. Creating a DecisionReview records authorized interpretation over an explicit
+ordered outcome set. None of these operations automatically creates learning.

 ## Decision model

@@ -198,7 +206,7 @@ not rewrite the earlier record.
 ## EvidenceReference

 `EvidenceReference` is an implemented immutable value embedded in a Decision,
-DecisionAcceptance, DecisionAction, or DecisionOutcome:
+DecisionAcceptance, DecisionAction, DecisionOutcome, or DecisionReview:

 ```text
 kind
@@ -346,6 +354,46 @@ One Decision may have multiple outcomes. Each outcome appends factual history an
 more actions; no outcome replaces or mutates an earlier record. An outcome does not mean review,
 Experience, Knowledge, Playbook change, or automatic learning occurred.

+## DecisionReview foundation
+
+`DecisionReview` is an immutable, append-only authorized interpretation record with these exact
+implemented fields:
+
+```text
+id
+recorded_at
+decision_id
+acceptance_id
+outcome_ids
+reviewed_by
+reviewed_at
+assessment
+summary
+findings
+candidate_lessons
+evidence_references
+confidence
+idempotency_key
+tags
+```
+
+Assessment is exactly `sound`, `flawed`, `mixed`, or `inconclusive`; confidence is exactly `low`,
+`medium`, or `high`. Assessment is not the outcome result vocabulary: successful factual outcomes
+may support a flawed review, and failed outcomes may support a sound review.
+
+`outcome_ids` is ordered, unique, and non-empty. Findings are required ordered text; findings and
+candidate lessons each allow at most 100 case-insensitively unique entries of at most 1000
+characters. Candidate lessons may be empty and have no promotion authority. Reviewer is bounded to
+255 characters and summary to 1000; required text is trimmed and non-blank. Tags preserve
+first-seen order while removing case-insensitive duplicates. UTC-aware timestamps are normalized
+to UTC, and `reviewed_at` cannot be later than `recorded_at`.
+
+Every outcome must exist and belong to the same Decision and acceptance. Review time cannot
+precede the latest `validated_at` among selected outcomes. Action IDs are not persisted: provenance
+is transitive through `DecisionReview → DecisionOutcome[] → DecisionAction[]`. Multiple reviews
+may cover one Decision, outcome, or ordered outcome set under different keys. Corrections append;
+there is no replacement, supersession, deletion, or persisted `current` behavior.
+
 ## Persistence

 The persistence-focused `DecisionRepository` port implements only:
@@ -408,6 +456,20 @@ and immutable scalar metrics round-trip through domain validation; malformed dat
 The adapter performs no relation filtering, lifecycle projection, review, learning, migration, or
 ingestion.

+The persistence-focused `DecisionReviewRepository` implements only:
+
+```text
+save()
+load_all()
+get_by_id()
+```
+
+It has no relation, idempotency, chronology, or lifecycle query methods.
+`JsonDecisionReviewRepository` stores one deterministic sorted-key JSON file per review under
+`NeuralPaths.DECISION_REVIEWS`, and Brain initialization creates that directory. `load_all()` sorts
+filenames and every record round-trips through domain validation. Filtering, relation validation,
+history ordering, ambiguity detection, and semantic comparison remain in the application service.
+
 ## Application service

 `DecisionService` implements:
@@ -591,6 +653,9 @@ same scoped key + equivalent semantic payload
 same scoped key + different semantic payload
 → visible conflict, no write

+more than one persisted scoped match
+→ `DecisionOutcomeIdempotencyAmbiguityError`, no arbitrary selection, no write
+
 different key
 → another outcome may be recorded
 ```
@@ -610,6 +675,65 @@ validates every persisted outcome-to-acceptance/action relation. Latest selectio
 by `(validated_at, outcome.id)` and never depends on repository order. The summary is derived on
 demand and is neither persisted nor cached.

+More than one matching persisted outcome always raises ambiguity before selecting or semantically
+comparing a record. This is independent of repository enumeration order and applies to equivalent
+and different duplicate payloads. Zero matches follows normal creation; exactly one match retains
+the equivalent-replay or conflict behavior. This hardening changes no outcome fields, vocabulary,
+relations, ordering, summary, CLI, stored schema, or lifecycle behavior.
+
+### DecisionReviewService
+
+`DecisionReviewService` implements:
+
+```text
+add()
+list_for_decision()
+show()
+```
+
+`add()` constructs the candidate first, so local domain validation precedes repository reads. It
+then requires the Decision, validates the acceptance belongs to it, loads every caller-ordered
+outcome by ID, validates Decision and acceptance ownership, and requires `reviewed_at` to be at or
+after the latest selected outcome validation. Missing or mismatched relations and invalid time all
+fail before persistence.
+
+Review idempotency is scoped by:
+
+```text
+(decision_id, "decision_review", idempotency_key)
+```
+
+```text
+zero scoped matches
+→ save the validated candidate
+
+exactly one equivalent match
+→ validate persisted relations and return existing DecisionReview
+
+exactly one different match
+→ `DecisionReviewIdempotencyConflictError`, no write
+
+more than one persisted scoped match
+→ `DecisionReviewIdempotencyAmbiguityError`, no arbitrary selection or comparison, no write
+```
+
+The ambiguity error carries Decision ID, idempotency key, and match count. Ambiguity is independent
+of repository order and applies to semantically equivalent or different duplicates. For exactly
+one match, semantic equivalence excludes generated review ID and recording time and embedded
+evidence capture times; it includes every caller-supplied semantic field. Ordered outcome IDs,
+findings, candidate lessons, evidence, and tags therefore remain order sensitive.
+
+`list_for_decision()` requires the Decision, validates every persisted relation, and sorts by
+`(reviewed_at, review.id)`. `show()` loads by ID and validates its relations. Controlled errors
+cover missing Decision, acceptance, outcome, or review; acceptance/Decision mismatch;
+outcome/Decision or outcome/acceptance mismatch; review before outcome; idempotency conflict; and
+duplicate-key ambiguity. No failing path writes.
+
+DecisionReview and DecisionOutcome share the reusable fail-closed invariant that multiple matches
+for a scoped idempotency key must be surfaced, never resolved through `next()`, first-match
+selection, repository order, or comparison with an arbitrarily chosen record. Their scopes and
+ambiguity error types remain separate.
+
 ### Canonical DecisionLifecycleService

 `DecisionLifecycleService` is the only canonical owner of the current lifecycle projection. It
@@ -668,6 +792,8 @@ JsonPlaybookRunRepository
 DecisionActionService
 JsonDecisionOutcomeRepository
 DecisionOutcomeService
+JsonDecisionReviewRepository
+DecisionReviewService
 DecisionLifecycleService
 ```

@@ -679,11 +805,14 @@ repositories or own validation, relation checks, persistence, eligibility, or id
 `JsonDecisionAcceptanceRepository`, and `JsonPlaybookRunRepository`. `DecisionOutcomeService`
 receives `JsonDecisionOutcomeRepository` plus Decision, acceptance, and action repositories.
 `DecisionLifecycleService` receives the Decision, acceptance, action, and outcome repositories.
-CLI handlers resolve services from the container and construct no repositories.
+`DecisionReviewService` receives `JsonDecisionReviewRepository` plus Decision, acceptance, and
+outcome repositories. `Container.decision_review_repository()` and
+`Container.decision_review_service()` expose the review composition. CLI handlers resolve services
+from the container and construct no repositories.

 ## Implemented CLI

-These commands exist at commit `5befd7c`:
+These commands exist at commit `910f481e`:

 ```text
 neural decision add
@@ -698,6 +827,9 @@ neural decision outcome add DECISION_UUID
 neural decision outcome-history DECISION_UUID
 neural decision outcome-show OUTCOME_UUID
 neural decision outcome-summary DECISION_UUID
+neural decision review add DECISION_UUID
+neural decision review history DECISION_UUID
+neural decision review show REVIEW_UUID
 neural decision state DECISION_UUID
 ```

@@ -878,6 +1010,34 @@ every stored field, including evidence, metrics, idempotency key, and tags.
 result/time, distinct linked-action count, counts by result, and success/failure presence. It does
 not persist the summary.

+### Decision review commands
+
+`neural decision review add DECISION_UUID` requires:
+
+```text
+--acceptance-id
+--outcome-id (one or more, repeatable and ordered)
+--reviewed-by
+--reviewed-at
+--assessment
+--summary
+--finding (one or more, repeatable and ordered)
+--confidence
+--idempotency-key
+```
+
+Optional repeatable inputs are `--candidate-lesson`, `--evidence` JSON, and `--tag`. Assessment
+accepts `sound`, `flawed`, `mixed`, or `inconclusive`; confidence accepts `low`, `medium`, or
+`high`. The CLI parses ISO-8601 review time and embedded evidence but never opens evidence
+locators. Validation errors render their first message; `ValueError` and controlled
+`DecisionReviewError` failures render visibly and exit nonzero. Success prints the stored review ID
+and every review field.
+
+`neural decision review history DECISION_UUID` renders deterministic service history with columns
+`ID`, `Reviewed`, `Reviewed by`, `Assessment`, `Confidence`, `Outcome IDs`, and `Summary`. An
+existing Decision with no reviews renders `No review history found for Decision: ...`.
+`neural decision review show REVIEW_UUID` renders every field after persisted relation validation.
+
 `neural decision state DECISION_UUID` renders exactly one of:

 ```text
@@ -906,12 +1066,12 @@ Decision
 - `DecisionAcceptance` is the implemented explicit authorization for possible future execution.
 - `DecisionAction` is the implemented record of work performed under an accepted Decision.
 - `DecisionOutcome` is the implemented factual result and validation evidence record.
-- `DecisionReview` would assess outcomes and hold candidate lessons.
+- `DecisionReview` is the implemented authorized interpretation over explicit ordered outcomes.

-The first four records exist; DecisionReview does not. Records remain immutable semantic records
-rather than fields on a mutable Decision or a duplicate generic event stream. A proposed option is
-not an acceptance, acceptance is not execution, an outcome is not a review or Experience, and
-candidate lessons are not automatically Knowledge or a Playbook change.
+All five records exist. Records remain immutable semantic records rather than fields on a mutable
+Decision or a duplicate generic event stream. A proposed option is not an acceptance, acceptance
+is not execution, an outcome is not a review or Experience, and review findings or candidate
+lessons are not automatically Experience, Knowledge, or a Playbook change.

 The currently derivable projection is only:

@@ -953,7 +1113,7 @@ Observation
 → DecisionAcceptance
 → DecisionAction
 → DecisionOutcome
-→ future DecisionReview
+→ DecisionReview
 → explicitly created Experience
 → explicitly created Knowledge
 ```
@@ -980,7 +1140,7 @@ prompt
 → post-work lesson
 ```

-Commit `5befd7c` does not capture or ingest those events automatically. Automatic candidates and
+Commit `910f481e` does not capture or ingest those events automatically. Automatic candidates and
 manual confirmation remain future concepts; no automatic persistence, ingestion, or learning
 exists.

@@ -989,10 +1149,9 @@ no recommendation can directly mutate NeuralEngine or authorize a durable record

 ## Current non-behavior

-Commit `5befd7c` does not implement:
+Commit `910f481e` does not implement:

 ```text
-DecisionReview
 execution engine
 command/shell execution
 rejection
@@ -1014,19 +1173,19 @@ Consigliere integration

 It also does not execute commands referenced by evidence, open locators, automatically accept
 Decisions, materialize Playbook revisions, or infer outcomes from `completed_at`. Explicit user
-requests are required to create Decision, DecisionAcceptance, DecisionAction, or DecisionOutcome
-records.
+requests are required to create Decision, DecisionAcceptance, DecisionAction, DecisionOutcome, or
+DecisionReview records.

 ## Recommended next milestone

-The one recommended next controlled slice is:
+The recommended next controlled slice is:

 ```text
-DecisionReview foundation
+separate explicit Experience creation from DecisionReview findings or candidate lessons
 ```

-It must remain separate from automatic Experience, Knowledge, Playbook, PlaybookEvaluation, or
-EvolutionProposal creation.
+It must preserve explicit authority and remain separate from automatic Knowledge, Playbook,
+PlaybookEvaluation, EvolutionProposal, or Consigliere creation.

 ## Handbook synchronization policy

@@ -1148,10 +1307,11 @@ Status: Accepted
 ## Decision

 Development decision tracking uses implemented separate immutable `Decision`,
-`DecisionAcceptance`, `DecisionAction`, and `DecisionOutcome` records with embedded immutable
-`EvidenceReference` values. `DecisionReview` remains a separate future-only record. Lifecycle
-state is derived from semantic records, not stored as mutable status or duplicated in a generic
-event stream.
+`DecisionAcceptance`, `DecisionAction`, `DecisionOutcome`, and `DecisionReview` records with
+embedded immutable `EvidenceReference` values. Outcome owns factual results; Review owns
+authorized interpretation over an explicit ordered outcome set. Lifecycle state is derived from
+acceptance, actions, and the latest factual outcome, not stored as mutable status or duplicated in
+a generic event stream. Review is orthogonal append-only history.

 Decision tracking complements the existing Observation-to-Playbook chain. Evidence uses bounded
 embedded references, durable writes require explicit authority, and Consigliere remains a future
@@ -1165,8 +1325,9 @@ advisory layer rather than authoritative storage.
   idempotency checks; repository ports remain persistence-focused.
 - No automatic ingestion, persistence, learning, Playbook evolution, or Consigliere integration is
   implied.
-- Source commit `5befd7c` implements Decision proposal, acceptance, action and outcome recording,
-  outcome history/summary, their CLI, and the canonical `DecisionLifecycleService`.
+- Source commit `910f481e27302daa6d3f15bde30d678ffc9e5d2f` implements Decision proposal,
+  acceptance, action, outcome, and review recording; outcome history/summary; review history; their
+  CLI; and the canonical `DecisionLifecycleService`.
 - The canonical states are exactly proposed, accepted, in-progress, succeeded, failed, partial,
   and outcome-unknown. Latest outcome selection uses validation time and outcome UUID, not
   repository order. No generic completed, resolved, or reviewed state exists.
@@ -1174,5 +1335,12 @@ advisory layer rather than authoritative storage.
   creates no later lifecycle or learning record.
 - Multiple immutable outcomes may be appended for one Decision. Outcome creation is factual only
   and creates no review or learning record.
-- The one recommended next milestone is `DecisionReview foundation`, kept separate from automatic
-  learning and downstream Experience, Knowledge, or Playbook creation.
+- Multiple immutable reviews may cover one Decision, outcome, or ordered outcome set. Corrections
+  append, action provenance remains transitive through outcomes, and no `current`, replacement,
+  supersession, deletion, lifecycle transition, or automatic learning behavior exists.
+- Outcome and review idempotency both fail closed when more than one persisted record matches a
+  scoped key: their distinct ambiguity errors replace arbitrary first-match selection and no write
+  occurs regardless of repository order or payload equivalence.
+- The recommended next controlled slice is separate explicit Experience creation from review
+  findings or candidate lessons; downstream Experience, Knowledge, or Playbook creation remains
+  explicit.
diff --git a/outputs/generated/HANDBOOK.md b/outputs/generated/HANDBOOK.md
index 559a6fc..4bcad1e 100644
--- a/outputs/generated/HANDBOOK.md
+++ b/outputs/generated/HANDBOOK.md
@@ -103,23 +103,27 @@ a milestone snapshot, not a timeless guarantee.

 ## Decision Learning boundary

-Source commit `5befd7c` implements separate immutable `Decision`, `DecisionAcceptance`,
-`DecisionAction`, and `DecisionOutcome` records, persistence-focused ports and JSON adapters,
-application services, container wiring, thin proposal/acceptance/action/outcome CLI commands, and
-the canonical `DecisionLifecycleService`. An action records work performed; only a linked outcome
-records factual results and validation evidence.
+Source commit `910f481e27302daa6d3f15bde30d678ffc9e5d2f` implements separate immutable
+`Decision`, `DecisionAcceptance`, `DecisionAction`, `DecisionOutcome`, and `DecisionReview`
+records, persistence-focused ports and JSON adapters, application services, container wiring,
+thin proposal/acceptance/action/outcome/review CLI commands, and the canonical
+`DecisionLifecycleService`. An action records work performed; only a linked outcome records
+factual results and validation evidence; a review records authorized interpretation.

 `DecisionOutcome` links one Decision, its acceptance, and one or more ordered unique actions. Its
 result is exactly `succeeded`, `failed`, `partial`, or `unknown`; scalar metrics are immutable.
 Multiple outcomes form history, and the non-persisted `DecisionOutcomeSummary` derives counts and
 the latest outcome using `(validated_at, outcome.id)` rather than repository order.
+`DecisionReview` targets an explicit ordered non-empty set of outcomes for one Decision and
+acceptance. Multiple reviews form immutable history ordered by `(reviewed_at, review.id)`.

-The canonical lifecycle states are exactly `proposed`, `accepted`, `in_progress`, `succeeded`,
-`failed`, `partial`, and `outcome_unknown`. `DecisionReview` and a reviewed state remain
-future-only. Outcome creation does not create learning. There is no execution engine, lifecycle
-reversal, ingestion, automatic learning or evolution, generic event replay, or Consigliere
-integration. The authoritative implemented contract and future boundary are defined in
-`handbook/architecture/decision-learning.md`; the next milestone is the DecisionReview foundation.
+The canonical lifecycle states remain exactly `proposed`, `accepted`, `in_progress`, `succeeded`,
+`failed`, `partial`, and `outcome_unknown`. Review is orthogonal append-only history; there is no
+`reviewed` state. Outcome or review creation does not create learning. There is no execution
+engine, lifecycle reversal, ingestion, automatic learning or evolution, generic event replay, or
+Consigliere integration. The authoritative implemented contract and future boundary are defined
+in `handbook/architecture/decision-learning.md`; the recommended next controlled slice is
+separate explicit Experience creation from review findings or candidate lessons.

 ---

@@ -127,11 +131,12 @@ integration. The authoritative implemented contract and future boundary are defi

 ## Status and purpose

-NeuralEngine source commit `5befd7c` implements the Decision, DecisionAcceptance,
-DecisionAction, and DecisionOutcome foundations plus the canonical `DecisionLifecycleService`
-projection. They record an immutable proposed choice, explicit authorization, work performed under
-that authorization, and factual results. Each foundation persists immutable records, exposes
-application use cases, is wired through the container, and provides a thin CLI.
+NeuralEngine source commit `910f481e27302daa6d3f15bde30d678ffc9e5d2f` implements the Decision,
+DecisionAcceptance, DecisionAction, DecisionOutcome, and DecisionReview foundations plus the
+canonical `DecisionLifecycleService` projection. They record an immutable proposed choice,
+explicit authorization, work performed under that authorization, factual results, and authorized
+interpretation. Each foundation persists immutable records, exposes application use cases, is
+wired through the container, and provides a thin CLI.

 The wider Decision Learning lifecycle remains accepted future architecture. Decision tracking
 complements the existing Observation-to-Playbook chain; it does not replace it.
@@ -146,19 +151,23 @@ EvidenceReference
 DecisionAcceptance
 DecisionAction
 DecisionOutcome
+DecisionReview
 DecisionRepository
 DecisionAcceptanceRepository
 DecisionActionRepository
 DecisionOutcomeRepository
+DecisionReviewRepository
 JsonDecisionRepository
 JsonDecisionAcceptanceRepository
 JsonDecisionActionRepository
 JsonDecisionOutcomeRepository
+JsonDecisionReviewRepository
 DecisionService
 DecisionAcceptanceService
 DecisionActionService
 DecisionOutcomeService
 DecisionOutcomeSummary
+DecisionReviewService
 DecisionLifecycleService
 container wiring
 neural decision add/list/show
@@ -171,14 +180,17 @@ neural decision outcome add
 neural decision outcome-history
 neural decision outcome-show
 neural decision outcome-summary
+neural decision review add
+neural decision review history
+neural decision review show
 neural decision state
 ```

 Creating a Decision records a proposal. Creating a DecisionAcceptance explicitly authorizes that
 proposal for possible future work. Creating a DecisionAction records work performed under that
 acceptance. Creating a DecisionOutcome records factual results and validation evidence for one or
-more linked actions. None of these operations performs review or learning. `DecisionReview`
-remains future-only.
+more linked actions. Creating a DecisionReview records authorized interpretation over an explicit
+ordered outcome set. None of these operations automatically creates learning.

 ## Decision model

@@ -221,7 +233,7 @@ not rewrite the earlier record.
 ## EvidenceReference

 `EvidenceReference` is an implemented immutable value embedded in a Decision,
-DecisionAcceptance, DecisionAction, or DecisionOutcome:
+DecisionAcceptance, DecisionAction, DecisionOutcome, or DecisionReview:

 ```text
 kind
@@ -369,6 +381,46 @@ One Decision may have multiple outcomes. Each outcome appends factual history an
 more actions; no outcome replaces or mutates an earlier record. An outcome does not mean review,
 Experience, Knowledge, Playbook change, or automatic learning occurred.

+## DecisionReview foundation
+
+`DecisionReview` is an immutable, append-only authorized interpretation record with these exact
+implemented fields:
+
+```text
+id
+recorded_at
+decision_id
+acceptance_id
+outcome_ids
+reviewed_by
+reviewed_at
+assessment
+summary
+findings
+candidate_lessons
+evidence_references
+confidence
+idempotency_key
+tags
+```
+
+Assessment is exactly `sound`, `flawed`, `mixed`, or `inconclusive`; confidence is exactly `low`,
+`medium`, or `high`. Assessment is not the outcome result vocabulary: successful factual outcomes
+may support a flawed review, and failed outcomes may support a sound review.
+
+`outcome_ids` is ordered, unique, and non-empty. Findings are required ordered text; findings and
+candidate lessons each allow at most 100 case-insensitively unique entries of at most 1000
+characters. Candidate lessons may be empty and have no promotion authority. Reviewer is bounded to
+255 characters and summary to 1000; required text is trimmed and non-blank. Tags preserve
+first-seen order while removing case-insensitive duplicates. UTC-aware timestamps are normalized
+to UTC, and `reviewed_at` cannot be later than `recorded_at`.
+
+Every outcome must exist and belong to the same Decision and acceptance. Review time cannot
+precede the latest `validated_at` among selected outcomes. Action IDs are not persisted: provenance
+is transitive through `DecisionReview → DecisionOutcome[] → DecisionAction[]`. Multiple reviews
+may cover one Decision, outcome, or ordered outcome set under different keys. Corrections append;
+there is no replacement, supersession, deletion, or persisted `current` behavior.
+
 ## Persistence

 The persistence-focused `DecisionRepository` port implements only:
@@ -431,6 +483,20 @@ and immutable scalar metrics round-trip through domain validation; malformed dat
 The adapter performs no relation filtering, lifecycle projection, review, learning, migration, or
 ingestion.

+The persistence-focused `DecisionReviewRepository` implements only:
+
+```text
+save()
+load_all()
+get_by_id()
+```
+
+It has no relation, idempotency, chronology, or lifecycle query methods.
+`JsonDecisionReviewRepository` stores one deterministic sorted-key JSON file per review under
+`NeuralPaths.DECISION_REVIEWS`, and Brain initialization creates that directory. `load_all()` sorts
+filenames and every record round-trips through domain validation. Filtering, relation validation,
+history ordering, ambiguity detection, and semantic comparison remain in the application service.
+
 ## Application service

 `DecisionService` implements:
@@ -614,6 +680,9 @@ same scoped key + equivalent semantic payload
 same scoped key + different semantic payload
 → visible conflict, no write

+more than one persisted scoped match
+→ `DecisionOutcomeIdempotencyAmbiguityError`, no arbitrary selection, no write
+
 different key
 → another outcome may be recorded
 ```
@@ -633,6 +702,65 @@ validates every persisted outcome-to-acceptance/action relation. Latest selectio
 by `(validated_at, outcome.id)` and never depends on repository order. The summary is derived on
 demand and is neither persisted nor cached.

+More than one matching persisted outcome always raises ambiguity before selecting or semantically
+comparing a record. This is independent of repository enumeration order and applies to equivalent
+and different duplicate payloads. Zero matches follows normal creation; exactly one match retains
+the equivalent-replay or conflict behavior. This hardening changes no outcome fields, vocabulary,
+relations, ordering, summary, CLI, stored schema, or lifecycle behavior.
+
+### DecisionReviewService
+
+`DecisionReviewService` implements:
+
+```text
+add()
+list_for_decision()
+show()
+```
+
+`add()` constructs the candidate first, so local domain validation precedes repository reads. It
+then requires the Decision, validates the acceptance belongs to it, loads every caller-ordered
+outcome by ID, validates Decision and acceptance ownership, and requires `reviewed_at` to be at or
+after the latest selected outcome validation. Missing or mismatched relations and invalid time all
+fail before persistence.
+
+Review idempotency is scoped by:
+
+```text
+(decision_id, "decision_review", idempotency_key)
+```
+
+```text
+zero scoped matches
+→ save the validated candidate
+
+exactly one equivalent match
+→ validate persisted relations and return existing DecisionReview
+
+exactly one different match
+→ `DecisionReviewIdempotencyConflictError`, no write
+
+more than one persisted scoped match
+→ `DecisionReviewIdempotencyAmbiguityError`, no arbitrary selection or comparison, no write
+```
+
+The ambiguity error carries Decision ID, idempotency key, and match count. Ambiguity is independent
+of repository order and applies to semantically equivalent or different duplicates. For exactly
+one match, semantic equivalence excludes generated review ID and recording time and embedded
+evidence capture times; it includes every caller-supplied semantic field. Ordered outcome IDs,
+findings, candidate lessons, evidence, and tags therefore remain order sensitive.
+
+`list_for_decision()` requires the Decision, validates every persisted relation, and sorts by
+`(reviewed_at, review.id)`. `show()` loads by ID and validates its relations. Controlled errors
+cover missing Decision, acceptance, outcome, or review; acceptance/Decision mismatch;
+outcome/Decision or outcome/acceptance mismatch; review before outcome; idempotency conflict; and
+duplicate-key ambiguity. No failing path writes.
+
+DecisionReview and DecisionOutcome share the reusable fail-closed invariant that multiple matches
+for a scoped idempotency key must be surfaced, never resolved through `next()`, first-match
+selection, repository order, or comparison with an arbitrarily chosen record. Their scopes and
+ambiguity error types remain separate.
+
 ### Canonical DecisionLifecycleService

 `DecisionLifecycleService` is the only canonical owner of the current lifecycle projection. It
@@ -691,6 +819,8 @@ JsonPlaybookRunRepository
 DecisionActionService
 JsonDecisionOutcomeRepository
 DecisionOutcomeService
+JsonDecisionReviewRepository
+DecisionReviewService
 DecisionLifecycleService
 ```

@@ -702,11 +832,14 @@ repositories or own validation, relation checks, persistence, eligibility, or id
 `JsonDecisionAcceptanceRepository`, and `JsonPlaybookRunRepository`. `DecisionOutcomeService`
 receives `JsonDecisionOutcomeRepository` plus Decision, acceptance, and action repositories.
 `DecisionLifecycleService` receives the Decision, acceptance, action, and outcome repositories.
-CLI handlers resolve services from the container and construct no repositories.
+`DecisionReviewService` receives `JsonDecisionReviewRepository` plus Decision, acceptance, and
+outcome repositories. `Container.decision_review_repository()` and
+`Container.decision_review_service()` expose the review composition. CLI handlers resolve services
+from the container and construct no repositories.

 ## Implemented CLI

-These commands exist at commit `5befd7c`:
+These commands exist at commit `910f481e`:

 ```text
 neural decision add
@@ -721,6 +854,9 @@ neural decision outcome add DECISION_UUID
 neural decision outcome-history DECISION_UUID
 neural decision outcome-show OUTCOME_UUID
 neural decision outcome-summary DECISION_UUID
+neural decision review add DECISION_UUID
+neural decision review history DECISION_UUID
+neural decision review show REVIEW_UUID
 neural decision state DECISION_UUID
 ```

@@ -901,6 +1037,34 @@ every stored field, including evidence, metrics, idempotency key, and tags.
 result/time, distinct linked-action count, counts by result, and success/failure presence. It does
 not persist the summary.

+### Decision review commands
+
+`neural decision review add DECISION_UUID` requires:
+
+```text
+--acceptance-id
+--outcome-id (one or more, repeatable and ordered)
+--reviewed-by
+--reviewed-at
+--assessment
+--summary
+--finding (one or more, repeatable and ordered)
+--confidence
+--idempotency-key
+```
+
+Optional repeatable inputs are `--candidate-lesson`, `--evidence` JSON, and `--tag`. Assessment
+accepts `sound`, `flawed`, `mixed`, or `inconclusive`; confidence accepts `low`, `medium`, or
+`high`. The CLI parses ISO-8601 review time and embedded evidence but never opens evidence
+locators. Validation errors render their first message; `ValueError` and controlled
+`DecisionReviewError` failures render visibly and exit nonzero. Success prints the stored review ID
+and every review field.
+
+`neural decision review history DECISION_UUID` renders deterministic service history with columns
+`ID`, `Reviewed`, `Reviewed by`, `Assessment`, `Confidence`, `Outcome IDs`, and `Summary`. An
+existing Decision with no reviews renders `No review history found for Decision: ...`.
+`neural decision review show REVIEW_UUID` renders every field after persisted relation validation.
+
 `neural decision state DECISION_UUID` renders exactly one of:

 ```text
@@ -929,12 +1093,12 @@ Decision
 - `DecisionAcceptance` is the implemented explicit authorization for possible future execution.
 - `DecisionAction` is the implemented record of work performed under an accepted Decision.
 - `DecisionOutcome` is the implemented factual result and validation evidence record.
-- `DecisionReview` would assess outcomes and hold candidate lessons.
+- `DecisionReview` is the implemented authorized interpretation over explicit ordered outcomes.

-The first four records exist; DecisionReview does not. Records remain immutable semantic records
-rather than fields on a mutable Decision or a duplicate generic event stream. A proposed option is
-not an acceptance, acceptance is not execution, an outcome is not a review or Experience, and
-candidate lessons are not automatically Knowledge or a Playbook change.
+All five records exist. Records remain immutable semantic records rather than fields on a mutable
+Decision or a duplicate generic event stream. A proposed option is not an acceptance, acceptance
+is not execution, an outcome is not a review or Experience, and review findings or candidate
+lessons are not automatically Experience, Knowledge, or a Playbook change.

 The currently derivable projection is only:

@@ -976,7 +1140,7 @@ Observation
 → DecisionAcceptance
 → DecisionAction
 → DecisionOutcome
-→ future DecisionReview
+→ DecisionReview
 → explicitly created Experience
 → explicitly created Knowledge
 ```
@@ -1003,7 +1167,7 @@ prompt
 → post-work lesson
 ```

-Commit `5befd7c` does not capture or ingest those events automatically. Automatic candidates and
+Commit `910f481e` does not capture or ingest those events automatically. Automatic candidates and
 manual confirmation remain future concepts; no automatic persistence, ingestion, or learning
 exists.

@@ -1012,10 +1176,9 @@ no recommendation can directly mutate NeuralEngine or authorize a durable record

 ## Current non-behavior

-Commit `5befd7c` does not implement:
+Commit `910f481e` does not implement:

 ```text
-DecisionReview
 execution engine
 command/shell execution
 rejection
@@ -1037,19 +1200,19 @@ Consigliere integration

 It also does not execute commands referenced by evidence, open locators, automatically accept
 Decisions, materialize Playbook revisions, or infer outcomes from `completed_at`. Explicit user
-requests are required to create Decision, DecisionAcceptance, DecisionAction, or DecisionOutcome
-records.
+requests are required to create Decision, DecisionAcceptance, DecisionAction, DecisionOutcome, or
+DecisionReview records.

 ## Recommended next milestone

-The one recommended next controlled slice is:
+The recommended next controlled slice is:

 ```text
-DecisionReview foundation
+separate explicit Experience creation from DecisionReview findings or candidate lessons
 ```

-It must remain separate from automatic Experience, Knowledge, Playbook, PlaybookEvaluation, or
-EvolutionProposal creation.
+It must preserve explicit authority and remain separate from automatic Knowledge, Playbook,
+PlaybookEvaluation, EvolutionProposal, or Consigliere creation.

 ## Handbook synchronization policy

@@ -1116,9 +1279,9 @@ Confirmed example:

 ## Complementary Decision Learning chain

-The implemented Decision, DecisionAcceptance, DecisionAction, and DecisionOutcome foundations
-record a bounded proposed choice, explicit authorization, work performed, and factual results
-after Observation context:
+The implemented Decision, DecisionAcceptance, DecisionAction, DecisionOutcome, and DecisionReview
+foundations record a bounded proposed choice, explicit authorization, work performed, factual
+results, and authorized interpretation after Observation context:

 ```text
 Observation
@@ -1126,17 +1289,19 @@ Observation
 → DecisionAcceptance
 → DecisionAction
 → DecisionOutcome
-→ future DecisionReview
-→ Experience
-→ Knowledge
+→ DecisionReview
+→ explicitly created Experience
+→ explicitly created Knowledge
 ```

 This is a complementary provenance path, not a replacement for the canonical domain chain.
-DecisionOutcome is factual; Experience is interpreted; Knowledge is generalized; Playbook remains
-a separately created repeatable procedure. DecisionOutcome may have multiple immutable records per
-Decision and does not automatically create a Review or learning artifact. Decision,
-DecisionAcceptance, DecisionAction, DecisionOutcome, and their embedded EvidenceReference values
-exist at source commit `5befd7c`; no Review or later transition in this path is automatic.
+DecisionOutcome is factual; DecisionReview is authorized interpretation; Experience captures
+separately created operational learning; Knowledge is generalized; Playbook remains a separately
+created repeatable procedure. A Decision may have multiple immutable outcomes and multiple reviews,
+including reviews over the same ordered outcome set when their idempotency keys differ. Review
+action provenance is transitive through its explicit outcomes; it does not persist action IDs.
+These records and their embedded EvidenceReference values exist at source commit `910f481e`; no
+Review-driven lifecycle transition or later learning record in this path is automatic.

 ---

@@ -1571,8 +1736,12 @@ bounded to 1000 characters, and nested values are rejected. JSON serialization s

 Idempotency is scoped by `(decision_id, "decision_outcome", idempotency_key)`. Equivalent replay
 returns the existing outcome. Reusing the same scoped key with a different semantic payload fails
-without a write. Generated outcome ID, recording time, and evidence capture times are excluded
-from semantic equivalence; a different key may append another outcome for the same Decision.
+without a write. If more than one persisted outcome matches the scoped key,
+`DecisionOutcomeIdempotencyAmbiguityError` is raised whether their payloads are equivalent or
+different. The service never chooses an arbitrary duplicate, the result is independent of
+repository enumeration order, and no write occurs. Generated outcome ID, recording time, and
+evidence capture times are excluded from the exactly-one-match semantic comparison; a different
+key may append another outcome for the same Decision.

 `DecisionOutcomeSummary` is an immutable, non-persisted read model derived on demand. It reports
 outcome count, latest result and validation time, distinct linked-action count, counts for every
@@ -1586,9 +1755,120 @@ order.
 `outcome_unknown`. Earlier outcomes remain available as history. No `completed` or `resolved`
 lifecycle state exists.

-DecisionReview is not implemented. Recording an outcome does not review a Decision and does not
-create Observation, Experience, Knowledge, Playbook, PlaybookEvaluation, EvolutionProposal, or
-automatic learning. The next milestone is the separate DecisionReview foundation.
+Recording an outcome does not review a Decision and does not create Observation, Experience,
+Knowledge, Playbook, PlaybookEvaluation, EvolutionProposal, or automatic learning. The separately
+implemented DecisionReview foundation interprets explicit outcomes without rewriting them or
+changing lifecycle state.
+
+---
+
+# DecisionReview
+
+## Responsibility
+
+A DecisionReview is an immutable, append-only authorized interpretation record over one Decision,
+one DecisionAcceptance, and an explicit ordered set of DecisionOutcome records. It owns assessment,
+findings, candidate lessons, review evidence, and reviewer confidence. It does not own factual
+execution results, rewrite outcomes, execute evidence, mutate lifecycle state, create learning
+records, or call Consigliere.
+
+## Implemented fields and vocabularies
+
+- `id`
+- `recorded_at`
+- `decision_id`
+- `acceptance_id`
+- ordered unique `outcome_ids`
+- `reviewed_by`
+- `reviewed_at`
+- `assessment`
+- `summary`
+- ordered `findings`
+- ordered `candidate_lessons`
+- embedded `evidence_references`
+- `confidence`
+- `idempotency_key`
+- normalized `tags`
+
+Assessment is exactly `sound`, `flawed`, `mixed`, or `inconclusive`. Confidence is exactly `low`,
+`medium`, or `high`. These are independent of `DecisionOutcomeResult`, whose values remain
+`succeeded`, `failed`, `partial`, and `unknown`: a successful outcome can support a flawed review,
+and a failed outcome can support a sound review.
+
+## Validation and provenance
+
+- `outcome_ids` is ordered, unique, and non-empty; every outcome must exist and belong to the same
+  Decision and acceptance.
+- Action IDs are not persisted on a review. Provenance is transitive through
+  `DecisionReview → DecisionOutcome[] → DecisionAction[]`.
+- `reviewed_by` is trimmed, non-blank, and at most 255 characters; `summary` is trimmed, non-blank,
+  and at most 1000 characters. The idempotency key is trimmed and non-blank.
+- Findings are required, ordered, trimmed, non-blank, case-insensitively unique, and limited to 100
+  entries of at most 1000 characters each.
+- Candidate lessons use the same ordering, normalization, uniqueness, count, and length bounds, but
+  may be empty. They carry no authority to create or promote Experience or Knowledge.
+- Tags are trimmed and case-insensitively deduplicated while first-seen order is preserved.
+- `recorded_at` and `reviewed_at` must be timezone-aware and are normalized to UTC. Locally,
+  `reviewed_at` cannot be later than `recorded_at`; the service also requires it not to precede the
+  latest `validated_at` among the explicitly selected outcomes.
+- The candidate's local validation occurs before repository reads. Decision, acceptance, outcome,
+  cross-record, and time validation all fail closed before a write.
+
+Repository enumeration order never defines review scope or chronology. The caller supplies the
+ordered outcome scope, and history is sorted deterministically by `(reviewed_at, review.id)`.
+
+## History, corrections, and idempotency
+
+Multiple reviews are allowed for a Decision, an outcome, or the same ordered outcome set when they
+use different idempotency keys. Reassessment and correction append another review. This foundation
+has no mutation, replacement, supersession, deletion, or persisted `current` behavior.
+
+Idempotency is scoped by `(decision_id, "decision_review", idempotency_key)`:
+
+- zero matches creates the validated candidate;
+- exactly one semantically equivalent match returns the existing review;
+- exactly one different match raises `DecisionReviewIdempotencyConflictError` without a write;
+- more than one match raises `DecisionReviewIdempotencyAmbiguityError` with the Decision ID, key,
+  and match count, without selecting or comparing an arbitrary duplicate and without a write.
+
+Ambiguity is independent of repository enumeration order and applies whether duplicates are
+semantically equivalent or different. For the exactly-one-match comparison, semantic payload
+excludes generated `id`, generated `recorded_at`, and each evidence reference's `captured_at`; it
+includes all caller-supplied fields and preserves the order sensitivity of `outcome_ids`, findings,
+candidate lessons, evidence references, and tags.
+
+## Persistence, service, and CLI
+
+`DecisionReviewRepository` exposes exactly `save()`, `load_all()`, and `get_by_id()`.
+`JsonDecisionReviewRepository` stores one deterministic, sorted-key JSON file per review under
+`NeuralPaths.DECISION_REVIEWS`; `load_all()` sorts filenames and reconstructs records through domain
+validation. Brain initialization creates the directory. `Container.decision_review_repository()`
+and `Container.decision_review_service()` wire the JSON review repository together with Decision,
+acceptance, and outcome repositories.
+
+`DecisionReviewService` implements `add()`, `list_for_decision()`, and `show()`. Its controlled
+errors cover missing Decision, acceptance, outcome, or review; acceptance/Decision mismatch;
+outcome/Decision or outcome/acceptance mismatch; review before the latest outcome; idempotency
+conflict; and duplicate-key ambiguity. Read operations validate persisted relations before
+returning records.
+
+The CLI group is `neural decision review` with exact commands `add DECISION_UUID`,
+`history DECISION_UUID`, and `show REVIEW_UUID`. Add requires `--acceptance-id`, repeatable
+`--outcome-id`, `--reviewed-by`, `--reviewed-at`, `--assessment`, `--summary`, repeatable
+`--finding`, `--confidence`, and `--idempotency-key`. Optional repeatable inputs are
+`--candidate-lesson`, `--evidence` JSON, and `--tag`. Success prints the stored ID and every field.
+History renders `ID`, `Reviewed`, `Reviewed by`, `Assessment`, `Confidence`, `Outcome IDs`, and
+`Summary`; its controlled empty message is `No review history found for Decision: ...`. Show
+renders every field. Evidence locators are retained but not opened.
+
+## Lifecycle and learning boundary
+
+DecisionReview is orthogonal interpretive history. It does not affect `DecisionLifecycleService`.
+The lifecycle remains exactly `proposed`, `accepted`, `in_progress`, `succeeded`, `failed`,
+`partial`, and `outcome_unknown`; no `reviewed` state exists. A review never automatically creates
+Observation, Experience, Knowledge, Playbook, PlaybookEvaluation, EvolutionProposal, revision
+records, or Consigliere work. The next controlled slice is separate explicit Experience creation
+from review findings or candidate lessons.

 ---

@@ -1712,9 +1992,12 @@ learning record.
 `DecisionOutcomeService.add()` validates the Decision, matching acceptance, one or more unique
 actions, each action's Decision and acceptance relations, and validation time against the earliest
 linked action start before constructing or saving an immutable outcome. It uses
-`(decision_id, "decision_outcome", idempotency_key)` for application-layer idempotency. Equivalent
-replay returns the existing outcome; conflicting reuse fails without a write; another key may
-append another outcome for the same Decision.
+`(decision_id, "decision_outcome", idempotency_key)` for application-layer idempotency. Zero
+matches creates normally; exactly one equivalent match returns the existing outcome; exactly one
+different match conflicts. More than one persisted scoped match raises
+`DecisionOutcomeIdempotencyAmbiguityError`, regardless of payload equivalence or repository order,
+without selecting a duplicate or writing. Another key may append another outcome for the same
+Decision.

 `list_for_decision()` validates the Decision and returns all matching outcomes in repository order.
 `show()` owns explicit outcome-not-found behavior. `summary_for_decision()` validates persisted
@@ -1730,6 +2013,34 @@ latest is selected by `(validated_at, outcome.id)`. It writes no status and expo
 `completed`, `resolved`, or reviewed state. Outcome creation and projection create no Review or
 learning record.

+## Decision review ownership
+
+`DecisionReviewService.add()` first constructs the immutable candidate, then validates Decision,
+matching acceptance, every explicit ordered outcome relation, and that `reviewed_at` is not earlier
+than the latest referenced outcome validation. It writes only after all validation. The scope is
+`(decision_id, "decision_review", idempotency_key)`: zero matches creates, exactly one equivalent
+match replays, and exactly one different match raises `DecisionReviewIdempotencyConflictError`.
+More than one match raises `DecisionReviewIdempotencyAmbiguityError` with identifying details,
+independent of repository order and duplicate payload equivalence, without arbitrary selection,
+semantic comparison against a selected duplicate, or a write.
+
+Semantic comparison for the exactly-one-match case excludes generated review ID and recording
+time plus evidence capture times. It includes ordered outcome IDs, findings, candidate lessons,
+evidence, tags, and every other caller-supplied semantic field, so ordered collections remain order
+sensitive. `list_for_decision()` validates the Decision and every persisted review relation, then
+sorts by `(reviewed_at, review.id)`. `show()` validates persisted relations and owns explicit
+review-not-found behavior.
+
+Multiple reviews may cover one Decision, one outcome, or the same ordered outcome set under
+different keys. Corrections append; the service has no replacement, supersession, deletion, or
+`current` behavior. It creates no Experience, Knowledge, Playbook, proposal, or Consigliere work
+and does not participate in `DecisionLifecycleService`.
+
+The DecisionOutcome and DecisionReview duplicate-key rules are the same reusable fail-closed
+application-service invariant: more than one persisted match for a scoped key is corruption or
+ambiguity to surface, never an ordering problem to resolve by choosing the first record. Their
+scopes and controlled ambiguity error types remain separate.
+
 ---

 # Application Errors
@@ -1854,6 +2165,11 @@ Decision filtering, acceptance/action relation validation, multiple-outcome hist
 summary derivation, and lifecycle projection belong to application services; no relation,
 idempotency, summary, latest-outcome, or lifecycle query method is part of the port.

+`DecisionReviewRepository` is likewise limited to `save()`, `load_all()`, and `get_by_id()`.
+Decision filtering, cross-record validation, history ordering, and scoped idempotency—including
+fail-closed duplicate-match ambiguity—belong to `DecisionReviewService`; no relation,
+idempotency, chronology, or lifecycle query method is part of the port.
+
 ## Repository return types

 Prefer:
@@ -1990,6 +2306,15 @@ file names, and malformed data surfaces validation errors. The adapter performs
 validation or filtering, latest-outcome selection, summary or lifecycle projection, idempotency
 decision, migration, ingestion, review, or learning.

+## Decision review adapter
+
+`JsonDecisionReviewRepository` implements `DecisionReviewRepository` and stores one JSON file per
+review under `NeuralPaths.DECISION_REVIEWS`; Brain initialization creates the directory. Complete
+DecisionReview records round-trip through domain validation. JSON object keys are serialized with
+`indent=2` and `sort_keys=True`, `load_all()` sorts filenames, and malformed data surfaces
+validation errors. The adapter performs no Decision filtering, relation validation, chronology,
+idempotency selection, lifecycle projection, evidence ingestion, learning, or Consigliere work.
+
 ---

 # Dependency Injection and Container
@@ -2063,6 +2388,12 @@ acceptance, and action repositories. `Container.decision_lifecycle_service()` re
 four repository categories so it can validate relations and derive the canonical state. Decision
 action, outcome, summary, and state CLI handlers resolve services and construct no repositories.

+The review foundation is wired through `Container.decision_review_repository()` and
+`Container.decision_review_service()`. The service receives `JsonDecisionReviewRepository`,
+`JsonDecisionRepository`, `JsonDecisionAcceptanceRepository`, and
+`JsonDecisionOutcomeRepository`. Brain initialization creates `NeuralPaths.DECISION_REVIEWS`.
+Decision review CLI handlers resolve the service and construct no repositories.
+
 ---

 # Dependency Lifecycle
@@ -2653,10 +2984,11 @@ Status: Accepted
 ## Decision

 Development decision tracking uses implemented separate immutable `Decision`,
-`DecisionAcceptance`, `DecisionAction`, and `DecisionOutcome` records with embedded immutable
-`EvidenceReference` values. `DecisionReview` remains a separate future-only record. Lifecycle
-state is derived from semantic records, not stored as mutable status or duplicated in a generic
-event stream.
+`DecisionAcceptance`, `DecisionAction`, `DecisionOutcome`, and `DecisionReview` records with
+embedded immutable `EvidenceReference` values. Outcome owns factual results; Review owns
+authorized interpretation over an explicit ordered outcome set. Lifecycle state is derived from
+acceptance, actions, and the latest factual outcome, not stored as mutable status or duplicated in
+a generic event stream. Review is orthogonal append-only history.

 Decision tracking complements the existing Observation-to-Playbook chain. Evidence uses bounded
 embedded references, durable writes require explicit authority, and Consigliere remains a future
@@ -2670,8 +3002,9 @@ advisory layer rather than authoritative storage.
   idempotency checks; repository ports remain persistence-focused.
 - No automatic ingestion, persistence, learning, Playbook evolution, or Consigliere integration is
   implied.
-- Source commit `5befd7c` implements Decision proposal, acceptance, action and outcome recording,
-  outcome history/summary, their CLI, and the canonical `DecisionLifecycleService`.
+- Source commit `910f481e27302daa6d3f15bde30d678ffc9e5d2f` implements Decision proposal,
+  acceptance, action, outcome, and review recording; outcome history/summary; review history; their
+  CLI; and the canonical `DecisionLifecycleService`.
 - The canonical states are exactly proposed, accepted, in-progress, succeeded, failed, partial,
   and outcome-unknown. Latest outcome selection uses validation time and outcome UUID, not
   repository order. No generic completed, resolved, or reviewed state exists.
@@ -2679,5 +3012,12 @@ advisory layer rather than authoritative storage.
   creates no later lifecycle or learning record.
 - Multiple immutable outcomes may be appended for one Decision. Outcome creation is factual only
   and creates no review or learning record.
-- The one recommended next milestone is `DecisionReview foundation`, kept separate from automatic
-  learning and downstream Experience, Knowledge, or Playbook creation.
+- Multiple immutable reviews may cover one Decision, outcome, or ordered outcome set. Corrections
+  append, action provenance remains transitive through outcomes, and no `current`, replacement,
+  supersession, deletion, lifecycle transition, or automatic learning behavior exists.
+- Outcome and review idempotency both fail closed when more than one persisted record matches a
+  scoped key: their distinct ambiguity errors replace arbitrary first-match selection and no write
+  occurs regardless of repository order or payload equivalence.
+- The recommended next controlled slice is separate explicit Experience creation from review
+  findings or candidate lessons; downstream Experience, Knowledge, or Playbook creation remains
+  explicit.
diff --git a/src/neuralengine_handbook/builder.py b/src/neuralengine_handbook/builder.py
index 1826247..5cae603 100644
--- a/src/neuralengine_handbook/builder.py
+++ b/src/neuralengine_handbook/builder.py
@@ -100,6 +100,7 @@ def build(root: Path) -> list[Path]:
         paths.handbook / "domain/playbook-revision-activation.md",
         paths.handbook / "domain/playbook-revision-application.md",
         paths.handbook / "domain/decision-outcome.md",
+        paths.handbook / "domain/decision-review.md",
     ]

     application_files = [
diff --git a/tests/test_builder.py b/tests/test_builder.py
index a3303bf..4475a04 100644
--- a/tests/test_builder.py
+++ b/tests/test_builder.py
@@ -39,7 +39,7 @@ def test_generated_skill_contains_neuralengine_rules(tmp_path: Path) -> None:
     assert "Application CLI commands do not" in skill
     assert "Playbook content mutation" in skill
     assert "# Decision Learning Architecture" in skill
-    assert "These commands exist at commit `5befd7c`" in skill
+    assert "These commands exist at commit `910f481e`" in skill
     assert "neural decision add" in skill
     assert "neural decision list" in skill
     assert "neural decision show DECISION_UUID" in skill
@@ -52,9 +52,19 @@ def test_generated_skill_contains_neuralengine_rules(tmp_path: Path) -> None:
     assert "neural decision outcome-history DECISION_UUID" in skill
     assert "neural decision outcome-show OUTCOME_UUID" in skill
     assert "neural decision outcome-summary DECISION_UUID" in skill
+    assert "neural decision review add DECISION_UUID" in skill
+    assert "neural decision review history DECISION_UUID" in skill
+    assert "neural decision review show REVIEW_UUID" in skill
     assert "neural decision state DECISION_UUID" in skill
     assert "DecisionOutcome foundation" in skill
-    assert "remains future-only" in skill
+    assert "DecisionReview` remains future-only" not in skill
+    assert "DecisionReview does not" not in skill
+    assert "immutable, append-only authorized interpretation" in skill
+    assert "`sound`, `flawed`, `mixed`, or `inconclusive`" in skill
+    assert "confidence accepts `low`, `medium`, or" in skill
+    assert "`high`" in skill
+    assert "DecisionReviewIdempotencyAmbiguityError" in skill
+    assert "DecisionOutcomeIdempotencyAmbiguityError" in skill
     assert "No Consigliere integration exists" in skill
     assert "no automatic persistence, ingestion, or learning" in skill
     assert "same key + equivalent semantic payload" in skill
@@ -83,6 +93,7 @@ def test_handbook_contains_all_domain_entities(tmp_path: Path) -> None:
         "PlaybookRevisionActivation",
         "PlaybookRevisionApplication",
         "DecisionOutcome",
+        "DecisionReview",
     ]
     for entity in entities:
         assert f"# {entity}" in handbook
@@ -114,14 +125,14 @@ def test_decision_engine_contains_agent_and_repository_rules(tmp_path: Path) ->
     assert "ADR-0008" in decision_engine


-def test_handbook_contains_decision_outcome_lifecycle_and_future_boundaries(
+def test_handbook_contains_decision_review_lifecycle_and_learning_boundaries(
     tmp_path: Path,
 ) -> None:
     work_root = _copy_repo(tmp_path)
     build(work_root)

     handbook = (work_root / "outputs/generated/HANDBOOK.md").read_text(encoding="utf-8")
-    assert "NeuralEngine source commit `5befd7c` implements" in handbook
+    assert "NeuralEngine source commit `910f481e27302daa6d3f15bde30d678ffc9e5d2f`" in handbook
     assert "neural decision add" in handbook
     assert "neural decision list" in handbook
     assert "neural decision show DECISION_UUID" in handbook
@@ -134,6 +145,9 @@ def test_handbook_contains_decision_outcome_lifecycle_and_future_boundaries(
     assert "neural decision outcome-history DECISION_UUID" in handbook
     assert "neural decision outcome-show OUTCOME_UUID" in handbook
     assert "neural decision outcome-summary DECISION_UUID" in handbook
+    assert "neural decision review add DECISION_UUID" in handbook
+    assert "neural decision review history DECISION_UUID" in handbook
+    assert "neural decision review show REVIEW_UUID" in handbook
     assert "neural decision state DECISION_UUID" in handbook
     assert "DecisionAcceptance" in handbook
     assert "DecisionAcceptance foundation" in handbook
@@ -141,7 +155,9 @@ def test_handbook_contains_decision_outcome_lifecycle_and_future_boundaries(
     assert "Decision without acceptance" in handbook
     assert "Decision with one valid acceptance" in handbook
     assert "DecisionReview" in handbook
-    assert "remains future-only" in handbook
+    assert "# DecisionReview" in handbook
+    assert "DecisionReview` remains future-only" not in handbook
+    assert "DecisionReview does not. Records" not in handbook
     assert '(project_key, "decision", idempotency_key)' in handbook
     assert "same key + different semantic payload" in handbook
     assert '(decision_id, "decision_acceptance", idempotency_key)' in handbook
@@ -160,16 +176,25 @@ def test_handbook_contains_decision_outcome_lifecycle_and_future_boundaries(
     assert "# DecisionOutcome" in handbook
     assert "`succeeded`, `failed`, `partial`, and `unknown`" in handbook
     assert '(decision_id, "decision_outcome", idempotency_key)' in handbook
+    assert "DecisionOutcomeIdempotencyAmbiguityError" in handbook
     assert "another outcome may be recorded" in handbook
     assert "DecisionOutcomeSummary" in handbook
     assert "(validated_at, outcome.id)" in handbook
     assert "outcome_unknown" in handbook
-    assert "DecisionReview foundation" in handbook
+    assert '(decision_id, "decision_review", idempotency_key)' in handbook
+    assert "DecisionReviewIdempotencyAmbiguityError" in handbook
+    assert "immutable, append-only authorized interpretation" in handbook
+    assert "`sound`, `flawed`, `mixed`, or `inconclusive`" in handbook
+    assert "confidence accepts `low`, `medium`, or" in handbook
+    assert "`high`" in handbook
+    assert "Action IDs are not persisted" in handbook
+    assert "(reviewed_at, review.id)" in handbook
+    assert "no `reviewed` state" in handbook
+    assert "explicit Experience creation" in handbook
     assert "No Consigliere integration exists" in handbook
     assert "no automatic persistence, ingestion, or learning" in handbook
     assert "ADR-0008" in handbook
     assert "partially_successful" not in handbook
-    assert "inconclusive" not in handbook
     assert "DecisionOutcome` and `DecisionReview` remain future-only" not in handbook


@@ -186,6 +211,12 @@ def test_application_architecture_contains_core_boundaries(tmp_path: Path) -> No
     assert "# Infrastructure Adapters" in application
     assert "# Dependency Injection and Container" in application
     assert "# Anti-pattern: God Repository" in application
+    assert "DecisionReviewService.add()" in application
+    assert "DecisionReviewRepository` is likewise limited" in application
+    assert "JsonDecisionReviewRepository" in application
+    assert "Container.decision_review_service()" in application
+    assert "DecisionReviewIdempotencyAmbiguityError" in application
+    assert "DecisionOutcomeIdempotencyAmbiguityError" in application


 def test_application_architecture_includes_accepted_adrs(tmp_path: Path) -> None:
~~~~

## Full creation diff: handbook/domain/decision-review.md

Command: `git diff --no-index -- /dev/null handbook/domain/decision-review.md`
Exit status: 1 (expected: `git diff --no-index` returns 1 when differences exist)

~~~~diff
diff --git a/handbook/domain/decision-review.md b/handbook/domain/decision-review.md
new file mode 100644
index 0000000..ee93c48
--- /dev/null
+++ b/handbook/domain/decision-review.md
@@ -0,0 +1,107 @@
+# DecisionReview
+
+## Responsibility
+
+A DecisionReview is an immutable, append-only authorized interpretation record over one Decision,
+one DecisionAcceptance, and an explicit ordered set of DecisionOutcome records. It owns assessment,
+findings, candidate lessons, review evidence, and reviewer confidence. It does not own factual
+execution results, rewrite outcomes, execute evidence, mutate lifecycle state, create learning
+records, or call Consigliere.
+
+## Implemented fields and vocabularies
+
+- `id`
+- `recorded_at`
+- `decision_id`
+- `acceptance_id`
+- ordered unique `outcome_ids`
+- `reviewed_by`
+- `reviewed_at`
+- `assessment`
+- `summary`
+- ordered `findings`
+- ordered `candidate_lessons`
+- embedded `evidence_references`
+- `confidence`
+- `idempotency_key`
+- normalized `tags`
+
+Assessment is exactly `sound`, `flawed`, `mixed`, or `inconclusive`. Confidence is exactly `low`,
+`medium`, or `high`. These are independent of `DecisionOutcomeResult`, whose values remain
+`succeeded`, `failed`, `partial`, and `unknown`: a successful outcome can support a flawed review,
+and a failed outcome can support a sound review.
+
+## Validation and provenance
+
+- `outcome_ids` is ordered, unique, and non-empty; every outcome must exist and belong to the same
+  Decision and acceptance.
+- Action IDs are not persisted on a review. Provenance is transitive through
+  `DecisionReview → DecisionOutcome[] → DecisionAction[]`.
+- `reviewed_by` is trimmed, non-blank, and at most 255 characters; `summary` is trimmed, non-blank,
+  and at most 1000 characters. The idempotency key is trimmed and non-blank.
+- Findings are required, ordered, trimmed, non-blank, case-insensitively unique, and limited to 100
+  entries of at most 1000 characters each.
+- Candidate lessons use the same ordering, normalization, uniqueness, count, and length bounds, but
+  may be empty. They carry no authority to create or promote Experience or Knowledge.
+- Tags are trimmed and case-insensitively deduplicated while first-seen order is preserved.
+- `recorded_at` and `reviewed_at` must be timezone-aware and are normalized to UTC. Locally,
+  `reviewed_at` cannot be later than `recorded_at`; the service also requires it not to precede the
+  latest `validated_at` among the explicitly selected outcomes.
+- The candidate's local validation occurs before repository reads. Decision, acceptance, outcome,
+  cross-record, and time validation all fail closed before a write.
+
+Repository enumeration order never defines review scope or chronology. The caller supplies the
+ordered outcome scope, and history is sorted deterministically by `(reviewed_at, review.id)`.
+
+## History, corrections, and idempotency
+
+Multiple reviews are allowed for a Decision, an outcome, or the same ordered outcome set when they
+use different idempotency keys. Reassessment and correction append another review. This foundation
+has no mutation, replacement, supersession, deletion, or persisted `current` behavior.
+
+Idempotency is scoped by `(decision_id, "decision_review", idempotency_key)`:
+
+- zero matches creates the validated candidate;
+- exactly one semantically equivalent match returns the existing review;
+- exactly one different match raises `DecisionReviewIdempotencyConflictError` without a write;
+- more than one match raises `DecisionReviewIdempotencyAmbiguityError` with the Decision ID, key,
+  and match count, without selecting or comparing an arbitrary duplicate and without a write.
+
+Ambiguity is independent of repository enumeration order and applies whether duplicates are
+semantically equivalent or different. For the exactly-one-match comparison, semantic payload
+excludes generated `id`, generated `recorded_at`, and each evidence reference's `captured_at`; it
+includes all caller-supplied fields and preserves the order sensitivity of `outcome_ids`, findings,
+candidate lessons, evidence references, and tags.
+
+## Persistence, service, and CLI
+
+`DecisionReviewRepository` exposes exactly `save()`, `load_all()`, and `get_by_id()`.
+`JsonDecisionReviewRepository` stores one deterministic, sorted-key JSON file per review under
+`NeuralPaths.DECISION_REVIEWS`; `load_all()` sorts filenames and reconstructs records through domain
+validation. Brain initialization creates the directory. `Container.decision_review_repository()`
+and `Container.decision_review_service()` wire the JSON review repository together with Decision,
+acceptance, and outcome repositories.
+
+`DecisionReviewService` implements `add()`, `list_for_decision()`, and `show()`. Its controlled
+errors cover missing Decision, acceptance, outcome, or review; acceptance/Decision mismatch;
+outcome/Decision or outcome/acceptance mismatch; review before the latest outcome; idempotency
+conflict; and duplicate-key ambiguity. Read operations validate persisted relations before
+returning records.
+
+The CLI group is `neural decision review` with exact commands `add DECISION_UUID`,
+`history DECISION_UUID`, and `show REVIEW_UUID`. Add requires `--acceptance-id`, repeatable
+`--outcome-id`, `--reviewed-by`, `--reviewed-at`, `--assessment`, `--summary`, repeatable
+`--finding`, `--confidence`, and `--idempotency-key`. Optional repeatable inputs are
+`--candidate-lesson`, `--evidence` JSON, and `--tag`. Success prints the stored ID and every field.
+History renders `ID`, `Reviewed`, `Reviewed by`, `Assessment`, `Confidence`, `Outcome IDs`, and
+`Summary`; its controlled empty message is `No review history found for Decision: ...`. Show
+renders every field. Evidence locators are retained but not opened.
+
+## Lifecycle and learning boundary
+
+DecisionReview is orthogonal interpretive history. It does not affect `DecisionLifecycleService`.
+The lifecycle remains exactly `proposed`, `accepted`, `in_progress`, `succeeded`, `failed`,
+`partial`, and `outcome_unknown`; no `reviewed` state exists. A review never automatically creates
+Observation, Experience, Knowledge, Playbook, PlaybookEvaluation, EvolutionProposal, revision
+records, or Consigliere work. The next controlled slice is separate explicit Experience creation
+from review findings or candidate lessons.
~~~~

## Risks, assumptions, blockers, and deviations

- Unresolved implementation or documentation risks: none found.
- Assumption: the repository's generic `handbook/container/lifecycle.md` concerns dependency
  resource lifetimes, not Decision lifecycle; the canonical Decision lifecycle was updated in the
  authoritative Decision Learning documents instead.
- Blockers: none.
- Validation deviation: `scripts/validate.sh` does not exist in this repository; the exact
  repository-mandated pytest, Ruff, and MyPy commands were run directly.
- Review self-reference handling is documented in the complete diff-stat section.
- NeuralEngine's expected 797-test checkpoint was treated as authoritative repository state; this
  documentation task did not rerun or modify the NeuralEngine suite.

## Final confirmations

- Generated outputs were not manually edited.
- `SKILL.md` was not copied to NeuralEngine.
- NeuralEngine was not modified, staged, committed, or pushed.
- NeuralEngine-Handbook files were not staged, committed, or pushed.
- No commit or push occurred in either repository.

## Review artifact trailing-whitespace correction

Outcome: completed.

Only `.agent-work/reviews/review-sync-decision-review-milestone.md` was modified during this
correction. All trailing spaces and tabs, including the single-space blank context lines embedded
in the full diffs, were removed. The evidence, headings, validation output, diffs, conclusions,
and existing review structure were otherwise preserved. No Handbook source, builder, test, or
generated output was modified by this correction.

Command: `rg -n '[[:blank:]]+$' .agent-work/reviews/review-sync-decision-review-milestone.md`

Exit status: 1, the expected ripgrep status when no matching line exists.

~~~~text
~~~~

Command: `git diff --check`

Exit status: 0.

~~~~text
~~~~

Command: `git status --short --untracked-files=all`

Exit status: 0.

~~~~text
 M handbook/application/services.md
 M handbook/architecture/architecture.md
 M handbook/architecture/decision-learning.md
 M handbook/container/dependency-injection.md
 M handbook/decisions/ADR-0008-decision-learning-boundary.md
 M handbook/domain/decision-outcome.md
 M handbook/domain/domain-chain.md
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
?? .agent-work/prompts/codex-sync-decision-review-handbook.md
?? .agent-work/prompts/codex-sync-neuralengine-application-foundation-milestone.md
?? .agent-work/reviews/review-sync-decision-acceptance-foundation-milestone.md
?? .agent-work/reviews/review-sync-decision-action-lifecycle-foundation-milestone.md
?? .agent-work/reviews/review-sync-decision-foundation-milestone.md
?? .agent-work/reviews/review-sync-decision-learning-design-milestone.md
?? .agent-work/reviews/review-sync-decision-review-milestone.md
?? .agent-work/reviews/review-sync-neuralengine-application-foundation-milestone.md
?? .directory
?? handbook/domain/decision-review.md
~~~~

Nothing was staged, committed, or pushed. `SKILL.md` was not copied to NeuralEngine.
