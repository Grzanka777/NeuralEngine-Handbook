# Review: synchronize DecisionOutcome milestone

## Repository and checkpoint

- Repository: `NeuralEngine-Handbook`
- Branch: `main`
- Starting commit: `2d3652a50eaf4af640285188a8d535b6616cda0e`
  (`2d3652a docs: sync decision action lifecycle milestone`)
- NeuralEngine source checkpoint: `5befd7c34e1d4c8a26c8f3c796e5c2c67e104b41`
  (`5befd7c feat: add decision outcome lifecycle foundation`)
- NeuralEngine was inspected read-only, remained clean, and was not modified.

## Context read

Handbook context:

- `AGENTS.md`
- `handbook/constitution/CONSTITUTION.md`
- `handbook/workflow/development-workflow.md`
- `README.md`
- `pyproject.toml`
- generator implementation and tests
- all source documents containing DecisionOutcome or Decision lifecycle statements

NeuralEngine source-of-truth context:

- `AGENTS.md`
- `docs/architecture.md`
- `docs/decision-learning-lifecycle.md`
- `memory/project-state.md`
- `src/neural_engine/domain/decision_outcome.py`
- `src/neural_engine/application/decision_outcome_service.py`
- `src/neural_engine/application/decision_lifecycle_service.py`
- `src/neural_engine/ports/decision_outcome_repository.py`
- `src/neural_engine/infrastructure/json_decision_outcome_repository.py`
- DecisionOutcome container and CLI wiring
- related domain, service, lifecycle, JSON repository, CLI, and container tests

## Changed source documentation

- `handbook/architecture/architecture.md`
- `handbook/architecture/decision-learning.md`
- `handbook/domain/domain-chain.md`
- `handbook/domain/decision-outcome.md` (new)
- `handbook/application/services.md`
- `handbook/ports/repository-ports.md`
- `handbook/infrastructure/repositories.md`
- `handbook/container/dependency-injection.md`
- `handbook/decisions/ADR-0008-decision-learning-boundary.md`

The builder now includes the new DecisionOutcome domain source in the consolidated Handbook, and
generator tests assert the current outcome commands, exact result/state vocabulary, multiple
outcome history, idempotency scope, deterministic summary selection, and future Review boundary.

## Stale or conflicting statements corrected

- DecisionOutcome is implemented and immutable, not future-only.
- Results are exactly `succeeded`, `failed`, `partial`, and `unknown`.
- Each outcome links a Decision, its DecisionAcceptance, and one or more ordered unique
  DecisionAction records, with relation and validation-time checks.
- Metrics are immutable bounded scalar values with deterministic serialization.
- Idempotency is scoped by `(decision_id, "decision_outcome", idempotency_key)` and does not limit
  a Decision to one outcome.
- Multiple outcomes form append-only history.
- `DecisionOutcomeSummary` is implemented as an immutable, non-persisted read model.
- Latest outcome selection is deterministic by `(validated_at, outcome.id)`, not repository order.
- Canonical lifecycle states are exactly `proposed`, `accepted`, `in_progress`, `succeeded`,
  `failed`, `partial`, and `outcome_unknown`.
- Stale `successful`, `partially_successful`, `inconclusive`, generic `completed`/`resolved`, and
  single-outcome assumptions are absent from the synchronized sources and outputs.
- DecisionReview, reviewed state, automatic learning/evolution, and Consigliere integration remain
  explicitly unimplemented. The next milestone is the separate DecisionReview foundation.

## Generated outputs rebuilt

Executed twice to confirm the documented build remains deterministic:

```text
uv run --no-project --with-editable . handbook build
```

Generated changes:

- `outputs/claude-skill/SKILL.md`
- `outputs/generated/AGENTS.generated.md`
- `outputs/generated/APPLICATION_ARCHITECTURE.md`
- `outputs/generated/DECISION_ENGINE.md`
- `outputs/generated/HANDBOOK.md`

The task templates and review template were rebuilt but remained byte-equivalent. No generated
artifact was edited manually. The generated `SKILL.md` was not copied into NeuralEngine.

## Validation results

- `uv run --no-project --with-editable . handbook build` — passed twice.
- `env PYTHONPATH=src uv run --no-project --with pytest --with typer --with pyyaml pytest` —
  passed, 8 tests.
- `uv run --no-project --with mypy --with typer --with pyyaml python -m mypy src` — passed,
  3 source files checked.
- `ruff check .` — passed.
- `git diff --check` — passed with no output.
- Stale-vocabulary search across `handbook`, `templates`, `outputs`, `src`, and `tests` — no stale
  positive statements found; only negative regression assertions contain old terms.
- NeuralEngine final `HEAD` remained `5befd7c34e1d4c8a26c8f3c796e5c2c67e104b41` and its
  `git status --short` remained empty.

Baseline notes:

- The repository has no `scripts/validate.sh`, although the workflow document names it. The
  documented component commands were run individually instead.
- Direct baseline `pytest`/`mypy` before editing could not import the uninstalled local package or
  `typer`; final validation used an isolated `uv` environment and passed.
- An additional non-required `ruff format --check .` reports the pre-existing, unchanged
  `src/neuralengine_handbook/cli.py` would be reformatted. No unrelated formatting was applied.

## Diff stat

Tracked diff before this untracked review file:

```text
 handbook/application/services.md                   |  26 +-
 handbook/architecture/architecture.md              |  26 +-
 handbook/architecture/decision-learning.md         | 262 +++++++++---
 handbook/container/dependency-injection.md         |  14 +-
 .../ADR-0008-decision-learning-boundary.md         |  23 +-
 handbook/domain/domain-chain.md                    |  14 +-
 handbook/infrastructure/repositories.md            |  10 +
 handbook/ports/repository-ports.md                 |   5 +
 outputs/claude-skill/SKILL.md                      | 302 +++++++++++---
 outputs/generated/AGENTS.generated.md              |  26 +-
 outputs/generated/APPLICATION_ARCHITECTURE.md      |  55 ++-
 outputs/generated/DECISION_ENGINE.md               | 285 ++++++++++---
 outputs/generated/HANDBOOK.md                      | 445 +++++++++++++++++----
 src/neuralengine_handbook/builder.py               |   1 +
 tests/test_builder.py                              |  38 +-
 15 files changed, 1224 insertions(+), 308 deletions(-)
```

Untracked task additions are not included by `git diff --stat`: this review file and
`handbook/domain/decision-outcome.md`.

## Diff check

```text
git diff --check
# no output; exit 0
```

## Git status

Expected final short status:

```text
 M handbook/application/services.md
 M handbook/architecture/architecture.md
 M handbook/architecture/decision-learning.md
 M handbook/container/dependency-injection.md
 M handbook/decisions/ADR-0008-decision-learning-boundary.md
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
?? .agent-work/
?? .directory
?? handbook/domain/decision-outcome.md
```

`.agent-work/` and `.directory` were already untracked at task start. This task added only the
required review file within `.agent-work/`; it did not alter the pre-existing prompts or reviews.

## Full diff inventory

Source and generator changes:

- `handbook/application/services.md`
- `handbook/architecture/architecture.md`
- `handbook/architecture/decision-learning.md`
- `handbook/container/dependency-injection.md`
- `handbook/decisions/ADR-0008-decision-learning-boundary.md`
- `handbook/domain/domain-chain.md`
- `handbook/domain/decision-outcome.md` (new)
- `handbook/infrastructure/repositories.md`
- `handbook/ports/repository-ports.md`
- `src/neuralengine_handbook/builder.py`
- `tests/test_builder.py`

Generated changes, all produced by the builder:

- `outputs/claude-skill/SKILL.md`
- `outputs/generated/AGENTS.generated.md`
- `outputs/generated/APPLICATION_ARCHITECTURE.md`
- `outputs/generated/DECISION_ENGINE.md`
- `outputs/generated/HANDBOOK.md`

Review artifact:

- `.agent-work/reviews/review-sync-decision-outcome-milestone.md` (new)

The complete source and generated diffs were inspected. No NeuralEngine file, template source,
generated archive, or unrelated Handbook source was changed.

## Repository actions

No commit was created. No push was performed. No branch, tag, release, or remote state was changed.

## Authoritative full diff appendix

This appendix supersedes the earlier abbreviated diff inventory and stat sections where scope
differs. It was prepared after the complete tracked and untracked task diffs were inspected.

### Full tracked diff

Exact command:

```text
git diff --no-ext-diff --binary
```

Complete output:

````diff
diff --git a/handbook/application/services.md b/handbook/application/services.md
index 8c47dbb..08b4014 100644
--- a/handbook/application/services.md
+++ b/handbook/application/services.md
@@ -101,7 +101,7 @@ acceptance both fail visibly without writing.
 and preserves repository order. `show()` owns explicit acceptance not-found behavior. Acceptance
 does not mutate Decision or create actions, outcomes, reviews, execution, or learning.

-## Decision action and lifecycle ownership
+## Decision action ownership

 `DecisionActionService.add()` validates the Decision, matching acceptance, and optional
 PlaybookRun before creating an immutable action. It uses
@@ -113,7 +113,25 @@ multiple distinct actions, and mutates no related record. PlaybookRun and Playbo
 `show()` owns explicit action-not-found behavior. The service creates no Outcome, Review, or
 learning record.

+## Decision outcome and lifecycle ownership
+
+`DecisionOutcomeService.add()` validates the Decision, matching acceptance, one or more unique
+actions, each action's Decision and acceptance relations, and validation time against the earliest
+linked action start before constructing or saving an immutable outcome. It uses
+`(decision_id, "decision_outcome", idempotency_key)` for application-layer idempotency. Equivalent
+replay returns the existing outcome; conflicting reuse fails without a write; another key may
+append another outcome for the same Decision.
+
+`list_for_decision()` validates the Decision and returns all matching outcomes in repository order.
+`show()` owns explicit outcome-not-found behavior. `summary_for_decision()` validates persisted
+outcome relations and returns an immutable, non-persisted `DecisionOutcomeSummary` with outcome
+count, deterministic latest result/time, distinct linked-action count, counts by result, and
+success/failure presence. Latest selection uses `(validated_at, outcome.id)` rather than repository
+order.
+
 `DecisionLifecycleService` is the only canonical projection owner. It validates persisted
-Decision/acceptance/action relations and derives only `proposed`, `accepted`, or `in_progress`.
-It writes no status, ignores repository order for state, and exposes no completed, succeeded,
-failed, or reviewed state.
+Decision/acceptance/action/outcome relations and derives exactly `proposed`, `accepted`,
+`in_progress`, `succeeded`, `failed`, `partial`, or `outcome_unknown`. When outcomes exist, the
+latest is selected by `(validated_at, outcome.id)`. It writes no status and exposes no generic
+`completed`, `resolved`, or reviewed state. Outcome creation and projection create no Review or
+learning record.
diff --git a/handbook/architecture/architecture.md b/handbook/architecture/architecture.md
index 8807075..6896cb9 100644
--- a/handbook/architecture/architecture.md
+++ b/handbook/architecture/architecture.md
@@ -68,14 +68,20 @@ a milestone snapshot, not a timeless guarantee.

 ## Decision Learning boundary

-Source commit `1964356` implements separate immutable `Decision`, `DecisionAcceptance`, and
-`DecisionAction` records, persistence-focused ports and JSON adapters, application services,
-container wiring, thin proposal/acceptance/action CLI commands, and the canonical
-`DecisionLifecycleService`. An action records work performed; it does not assert success or an
-outcome.
-
-Only `proposed`, `accepted`, and `in_progress` can currently be derived. `DecisionOutcome` and
-`DecisionReview` remain future-only. There is no execution engine, completion/success/failure
-state, reversal, ingestion, automatic learning, generic full lifecycle replay, or Consigliere
+Source commit `5befd7c` implements separate immutable `Decision`, `DecisionAcceptance`,
+`DecisionAction`, and `DecisionOutcome` records, persistence-focused ports and JSON adapters,
+application services, container wiring, thin proposal/acceptance/action/outcome CLI commands, and
+the canonical `DecisionLifecycleService`. An action records work performed; only a linked outcome
+records factual results and validation evidence.
+
+`DecisionOutcome` links one Decision, its acceptance, and one or more ordered unique actions. Its
+result is exactly `succeeded`, `failed`, `partial`, or `unknown`; scalar metrics are immutable.
+Multiple outcomes form history, and the non-persisted `DecisionOutcomeSummary` derives counts and
+the latest outcome using `(validated_at, outcome.id)` rather than repository order.
+
+The canonical lifecycle states are exactly `proposed`, `accepted`, `in_progress`, `succeeded`,
+`failed`, `partial`, and `outcome_unknown`. `DecisionReview` and a reviewed state remain
+future-only. Outcome creation does not create learning. There is no execution engine, lifecycle
+reversal, ingestion, automatic learning or evolution, generic event replay, or Consigliere
 integration. The authoritative implemented contract and future boundary are defined in
-`handbook/architecture/decision-learning.md`.
+`handbook/architecture/decision-learning.md`; the next milestone is the DecisionReview foundation.
diff --git a/handbook/architecture/decision-learning.md b/handbook/architecture/decision-learning.md
index 944d92a..c8d3c26 100644
--- a/handbook/architecture/decision-learning.md
+++ b/handbook/architecture/decision-learning.md
@@ -2,11 +2,11 @@

 ## Status and purpose

-NeuralEngine source commit `1964356` implements the Decision, DecisionAcceptance, and
-DecisionAction foundations plus the canonical minimal `DecisionLifecycleService` projection. They
-record an immutable proposed choice, explicit authorization, and work performed under that
-authorization. Each foundation persists immutable records, exposes application use cases, is
-wired through the container, and provides a thin CLI.
+NeuralEngine source commit `5befd7c` implements the Decision, DecisionAcceptance,
+DecisionAction, and DecisionOutcome foundations plus the canonical `DecisionLifecycleService`
+projection. They record an immutable proposed choice, explicit authorization, work performed under
+that authorization, and factual results. Each foundation persists immutable records, exposes
+application use cases, is wired through the container, and provides a thin CLI.

 The wider Decision Learning lifecycle remains accepted future architecture. Decision tracking
 complements the existing Observation-to-Playbook chain; it does not replace it.
@@ -20,15 +20,20 @@ Decision
 EvidenceReference
 DecisionAcceptance
 DecisionAction
+DecisionOutcome
 DecisionRepository
 DecisionAcceptanceRepository
 DecisionActionRepository
+DecisionOutcomeRepository
 JsonDecisionRepository
 JsonDecisionAcceptanceRepository
 JsonDecisionActionRepository
+JsonDecisionOutcomeRepository
 DecisionService
 DecisionAcceptanceService
 DecisionActionService
+DecisionOutcomeService
+DecisionOutcomeSummary
 DecisionLifecycleService
 container wiring
 neural decision add/list/show
@@ -37,13 +42,18 @@ neural decision acceptance-history
 neural decision action add
 neural decision action-history
 neural decision action-show
+neural decision outcome add
+neural decision outcome-history
+neural decision outcome-show
+neural decision outcome-summary
 neural decision state
 ```

 Creating a Decision records a proposal. Creating a DecisionAcceptance explicitly authorizes that
 proposal for possible future work. Creating a DecisionAction records work performed under that
-acceptance. None of these operations claims completion, success, failure, outcome, review, or
-learning. `DecisionOutcome` and `DecisionReview` are future-only records.
+acceptance. Creating a DecisionOutcome records factual results and validation evidence for one or
+more linked actions. None of these operations performs review or learning. `DecisionReview`
+remains future-only.

 ## Decision model

@@ -86,7 +96,7 @@ not rewrite the earlier record.
 ## EvidenceReference

 `EvidenceReference` is an implemented immutable value embedded in a Decision,
-DecisionAcceptance, or DecisionAction:
+DecisionAcceptance, DecisionAction, or DecisionOutcome:

 ```text
 kind
@@ -191,8 +201,48 @@ DecisionAction

 It does not mean the work succeeded, validation passed, an intended result occurred,
 DecisionOutcome exists, DecisionReview exists, or learning was created. `completed_at` means only
-that the described work interval ended. It does not produce a `completed`, `executed`, or
-`succeeded` lifecycle state.
+that the described work interval ended. It does not by itself produce a `completed`, `executed`,
+or `succeeded` lifecycle state.
+
+## DecisionOutcome foundation
+
+`DecisionOutcome` is an immutable factual result and validation record with these exact
+implemented fields:
+
+```text
+id
+recorded_at
+decision_id
+acceptance_id
+action_ids
+result
+summary
+validated_by
+validated_at
+evidence_references
+metrics
+idempotency_key
+tags
+```
+
+Its implemented invariants are:
+
+1. Decision, acceptance, and action IDs are valid UUIDs.
+2. At least one action ID is required; action IDs are ordered and unique.
+3. `result` is exactly `succeeded`, `failed`, `partial`, or `unknown`.
+4. `summary`, `validated_by`, and `idempotency_key` are trimmed and non-blank.
+5. `recorded_at` and `validated_at` are timezone-aware and normalized to UTC.
+6. Metrics contain at most 100 scalar `int | float | str | bool` values.
+7. Metric keys are trimmed, non-blank, at most 64 characters, and case-insensitively unique.
+8. Float metrics are finite, string metrics are bounded to 1000 characters, and nested values are
+   rejected.
+9. The metric mapping is immutable and serialized in deterministic key order.
+10. Tags and evidence use the existing normalization and immutable `EvidenceReference` rules.
+11. The model is immutable and has no mutable lifecycle status.
+
+One Decision may have multiple outcomes. Each outcome appends factual history and may link one or
+more actions; no outcome replaces or mutates an earlier record. An outcome does not mean review,
+Experience, Knowledge, Playbook change, or automatic learning occurred.

 ## Persistence

@@ -241,6 +291,21 @@ under `NeuralPaths.DECISION_ACTIONS`, and Brain initialization creates that dire
 through validation, and malformed stored data fails visibly. The adapter performs no migration,
 ingestion, or command execution.

+The persistence-focused `DecisionOutcomeRepository` also implements only:
+
+```text
+save()
+load_all()
+get_by_id()
+```
+
+It has no relation, idempotency, latest-outcome, summary, or lifecycle query methods.
+`JsonDecisionOutcomeRepository` stores one deterministic JSON file per outcome under
+`NeuralPaths.DECISION_OUTCOMES`, and Brain initialization creates that directory. Complete records
+and immutable scalar metrics round-trip through domain validation; malformed data fails visibly.
+The adapter performs no relation filtering, lifecycle projection, review, learning, migration, or
+ingestion.
+
 ## Application service

 `DecisionService` implements:
@@ -395,6 +460,54 @@ EvidenceReference.captured_at
 `list_for_decision()` validates the Decision, filters `load_all()` in the application layer, and
 preserves repository order. `show()` raises an explicit action-not-found error.

+### DecisionOutcomeService
+
+`DecisionOutcomeService` implements:
+
+```text
+add()
+list_for_decision()
+show()
+summary_for_decision()
+```
+
+`add()` validates Decision existence, acceptance existence and ownership, at least one unique
+action, and every action's Decision and acceptance relations. `validated_at` cannot precede the
+earliest linked action start. Only after relation validation does the service construct and save
+the immutable outcome. It mutates no related record and creates no Review or learning artifact.
+
+Outcome idempotency is scoped by:
+
+```text
+(decision_id, "decision_outcome", idempotency_key)
+```
+
+```text
+same scoped key + equivalent semantic payload
+→ return existing DecisionOutcome
+
+same scoped key + different semantic payload
+→ visible conflict, no write
+
+different key
+→ another outcome may be recorded
+```
+
+Semantic equivalence excludes `DecisionOutcome.id`, `DecisionOutcome.recorded_at`, and embedded
+`EvidenceReference.captured_at`. It includes the linked relations, result, validation data,
+metrics, and other caller-supplied semantic fields.
+
+`list_for_decision()` validates the Decision, filters `load_all()` in the application layer, and
+preserves repository order so the complete multiple-outcome history remains visible. `show()`
+raises an explicit outcome-not-found error.
+
+`DecisionOutcomeSummary` is an immutable, non-persisted application read model returned by
+`summary_for_decision()`. It reports outcome count, latest result and validation time, distinct
+linked-action count, counts for each result value, and success/failure presence. Summary derivation
+validates every persisted outcome-to-acceptance/action relation. Latest selection is deterministic
+by `(validated_at, outcome.id)` and never depends on repository order. The summary is derived on
+demand and is neither persisted nor cached.
+
 ### Canonical DecisionLifecycleService

 `DecisionLifecycleService` is the only canonical owner of the current lifecycle projection. It
@@ -404,6 +517,7 @@ depends on:
 DecisionRepository
 DecisionAcceptanceRepository
 DecisionActionRepository
+DecisionOutcomeRepository
 ```

 It derives exactly:
@@ -417,22 +531,26 @@ Decision exists, one valid acceptance, no action

 Decision exists, one valid acceptance, at least one valid action
 → in_progress
-```

-No mutable status is written and no generic event stream exists. Repository order does not define
-state; valid semantic relations do. Multiple persisted acceptances fail visibly, as does an action
-linked to a wrong or missing acceptance. Multiple valid actions still derive `in_progress`.
+latest valid outcome has result succeeded
+→ succeeded

-These states are explicitly unavailable:
+latest valid outcome has result failed
+→ failed

-```text
-executed
-completed
-succeeded
-failed
-reviewed
+latest valid outcome has result partial
+→ partial
+
+latest valid outcome has result unknown
+→ outcome_unknown
 ```

+No mutable status is written and no generic event stream exists. The latest outcome is selected by
+`(validated_at, outcome.id)`, never repository order. Multiple persisted acceptances fail visibly,
+as do invalid action or outcome relations. Multiple valid actions with no outcome derive
+`in_progress`; multiple outcomes retain history while the latest valid one drives the projection.
+There is no generic `executed`, `completed`, `resolved`, or `reviewed` state.
+
 ## Container

 The composition root constructs and connects:
@@ -446,6 +564,8 @@ DecisionAcceptanceService
 JsonDecisionActionRepository
 JsonPlaybookRunRepository
 DecisionActionService
+JsonDecisionOutcomeRepository
+DecisionOutcomeService
 DecisionLifecycleService
 ```

@@ -454,13 +574,14 @@ DecisionLifecycleService
 repositories or own validation, relation checks, persistence, eligibility, or idempotency policy.

 `DecisionActionService` receives `JsonDecisionActionRepository`, `JsonDecisionRepository`,
-`JsonDecisionAcceptanceRepository`, and `JsonPlaybookRunRepository`. `DecisionLifecycleService`
-receives the Decision, acceptance, and action repositories. CLI handlers resolve both services
-from the container and construct no repositories.
+`JsonDecisionAcceptanceRepository`, and `JsonPlaybookRunRepository`. `DecisionOutcomeService`
+receives `JsonDecisionOutcomeRepository` plus Decision, acceptance, and action repositories.
+`DecisionLifecycleService` receives the Decision, acceptance, action, and outcome repositories.
+CLI handlers resolve services from the container and construct no repositories.

 ## Implemented CLI

-These commands exist at commit `1964356`:
+These commands exist at commit `5befd7c`:

 ```text
 neural decision add
@@ -471,6 +592,10 @@ neural decision acceptance-history DECISION_UUID
 neural decision action add DECISION_UUID
 neural decision action-history DECISION_UUID
 neural decision action-show ACTION_UUID
+neural decision outcome add DECISION_UUID
+neural decision outcome-history DECISION_UUID
+neural decision outcome-show OUTCOME_UUID
+neural decision outcome-summary DECISION_UUID
 neural decision state DECISION_UUID
 ```

@@ -582,7 +707,7 @@ Reason

 An existing Decision with no acceptance produces a controlled empty state.

-### Decision action and state commands
+### Decision action commands

 `neural decision action add DECISION_UUID` requires:

@@ -623,19 +748,49 @@ Summary
 An existing Decision with no actions produces a controlled empty state.
 `neural decision action-show ACTION_UUID` renders every DecisionAction field.

+### Decision outcome and state commands
+
+`neural decision outcome add DECISION_UUID` requires:
+
+```text
+--acceptance-id
+--action-id (one or more)
+--result
+--summary
+--validated-by
+--validated-at
+--idempotency-key
+```
+
+Repeated `--evidence`, `--metric KEY=VALUE`, and `--tag` values are optional. Result accepts only
+`succeeded`, `failed`, `partial`, or `unknown`. Metrics parse unambiguous booleans, integers, and
+finite floats; other values remain strings and domain validation enforces the scalar bounds. The
+CLI reads no evidence locator and executes no referenced command.
+
+`neural decision outcome-history DECISION_UUID` renders all matching outcomes in repository order,
+including their result, validation time, linked action IDs, validator, and summary. An existing
+Decision with no outcomes produces a controlled empty state. `outcome-show OUTCOME_UUID` renders
+every stored field, including evidence, metrics, idempotency key, and tags.
+
+`neural decision outcome-summary DECISION_UUID` renders the derived count, deterministic latest
+result/time, distinct linked-action count, counts by result, and success/failure presence. It does
+not persist the summary.
+
 `neural decision state DECISION_UUID` renders exactly one of:

 ```text
 proposed
 accepted
 in_progress
+succeeded
+failed
+partial
+outcome_unknown
 ```

-It renders no later lifecycle state.
-
-## Future lifecycle boundary
+## Review and learning boundary

-The accepted future record family remains deliberately separate:
+The record family remains deliberately separate:

 ```text
 Decision
@@ -648,13 +803,13 @@ Decision
 - `Decision` is the implemented proposed choice.
 - `DecisionAcceptance` is the implemented explicit authorization for possible future execution.
 - `DecisionAction` is the implemented record of work performed under an accepted Decision.
-- `DecisionOutcome` would record factual results and validation evidence.
+- `DecisionOutcome` is the implemented factual result and validation evidence record.
 - `DecisionReview` would assess outcomes and hold candidate lessons.

-Only the first three records exist. Future records must remain immutable semantic records rather
-than fields on a mutable Decision or a duplicate generic event stream. A proposed option is not an
-acceptance, acceptance is not execution, an outcome is not an Experience, and candidate lessons
-are not automatically Knowledge or a Playbook change.
+The first four records exist; DecisionReview does not. Records remain immutable semantic records
+rather than fields on a mutable Decision or a duplicate generic event stream. A proposed option is
+not an acceptance, acceptance is not execution, an outcome is not a review or Experience, and
+candidate lessons are not automatically Knowledge or a Playbook change.

 The currently derivable projection is only:

@@ -667,10 +822,23 @@ Decision with one valid acceptance

 Decision with one valid acceptance and at least one valid action
 → in_progress
+
+latest valid outcome succeeded
+→ succeeded
+
+latest valid outcome failed
+→ failed
+
+latest valid outcome partial
+→ partial
+
+latest valid outcome unknown
+→ outcome_unknown
 ```

-There is no executed, completed, succeeded, failed, or reviewed state. The minimal lifecycle
-projection is canonical, but there is no generic full lifecycle replay service.
+The lifecycle projection uses the latest valid outcome selected by `(validated_at, outcome.id)`.
+There is no generic executed, completed, resolved, or reviewed state and no generic full lifecycle
+event replay service.

 ## Relationship to the domain chain

@@ -682,7 +850,7 @@ Observation
 → Decision
 → DecisionAcceptance
 → DecisionAction
-→ future DecisionOutcome
+→ DecisionOutcome
 → future DecisionReview
 → explicitly created Experience
 → explicitly created Knowledge
@@ -710,18 +878,18 @@ prompt
 → post-work lesson
 ```

-Commit `1964356` does not capture or ingest those events. Automatic candidates and manual
-confirmation remain future concepts; no automatic persistence, ingestion, or learning exists.
+Commit `5befd7c` does not capture or ingest those events automatically. Automatic candidates and
+manual confirmation remain future concepts; no automatic persistence, ingestion, or learning
+exists.

 Consigliere also remains future-only. It may later advise. No Consigliere integration exists, and
 no recommendation can directly mutate NeuralEngine or authorize a durable record.

 ## Current non-behavior

-Commit `1964356` does not implement:
+Commit `5befd7c` does not implement:

 ```text
-DecisionOutcome
 DecisionReview
 execution engine
 command/shell execution
@@ -731,7 +899,7 @@ reversal
 reopening
 cancellation
 replacement
-executed/completed/succeeded/failed/reviewed states
+executed/completed/resolved/reviewed states
 file ingestion
 git ingestion
 automatic Observation creation
@@ -744,17 +912,19 @@ Consigliere integration

 It also does not execute commands referenced by evidence, open locators, automatically accept
 Decisions, materialize Playbook revisions, or infer outcomes from `completed_at`. Explicit user
-requests are required to create Decision, DecisionAcceptance, or DecisionAction records.
+requests are required to create Decision, DecisionAcceptance, DecisionAction, or DecisionOutcome
+records.

 ## Recommended next milestone

 The one recommended next controlled slice is:

 ```text
-DecisionOutcome foundation
+DecisionReview foundation
 ```

-It must remain separate from `DecisionReview`.
+It must remain separate from automatic Experience, Knowledge, Playbook, PlaybookEvaluation, or
+EvolutionProposal creation.

 ## Handbook synchronization policy

diff --git a/handbook/container/dependency-injection.md b/handbook/container/dependency-injection.md
index 7efa809..bdb35fd 100644
--- a/handbook/container/dependency-injection.md
+++ b/handbook/container/dependency-injection.md
@@ -59,8 +59,12 @@ The acceptance foundation is wired through `Container.decision_acceptance_reposi
 `JsonDecisionAcceptanceRepository` and `JsonDecisionRepository` to
 `DecisionAcceptanceService`; acceptance CLI handlers construct no repositories.

-The action foundation is wired through `Container.decision_action_repository()`,
-`Container.decision_action_service()`, and `Container.decision_lifecycle_service()`. The action
-service receives JSON action, Decision, acceptance, and PlaybookRun repositories. The lifecycle
-service receives Decision, acceptance, and action repositories. CLI handlers resolve services and
-construct no repositories.
+The action foundation is wired through `Container.decision_action_repository()` and
+`Container.decision_action_service()`. The action service receives JSON action, Decision,
+acceptance, and PlaybookRun repositories.
+
+The outcome foundation is wired through `Container.decision_outcome_repository()` and
+`Container.decision_outcome_service()`. The outcome service receives JSON outcome, Decision,
+acceptance, and action repositories. `Container.decision_lifecycle_service()` receives those same
+four repository categories so it can validate relations and derive the canonical state. Decision
+action, outcome, summary, and state CLI handlers resolve services and construct no repositories.
diff --git a/handbook/decisions/ADR-0008-decision-learning-boundary.md b/handbook/decisions/ADR-0008-decision-learning-boundary.md
index 0becd1c..02861d2 100644
--- a/handbook/decisions/ADR-0008-decision-learning-boundary.md
+++ b/handbook/decisions/ADR-0008-decision-learning-boundary.md
@@ -5,10 +5,10 @@ Status: Accepted
 ## Decision

 Development decision tracking uses implemented separate immutable `Decision`,
-`DecisionAcceptance`, and `DecisionAction` records with embedded immutable `EvidenceReference`
-values. `DecisionOutcome` and `DecisionReview` remain separate future-only records. Lifecycle state
-is derived from semantic records, not stored as mutable status or duplicated in a generic event
-stream.
+`DecisionAcceptance`, `DecisionAction`, and `DecisionOutcome` records with embedded immutable
+`EvidenceReference` values. `DecisionReview` remains a separate future-only record. Lifecycle
+state is derived from semantic records, not stored as mutable status or duplicated in a generic
+event stream.

 Decision tracking complements the existing Observation-to-Playbook chain. Evidence uses bounded
 embedded references, durable writes require explicit authority, and Consigliere remains a future
@@ -22,11 +22,14 @@ advisory layer rather than authoritative storage.
   idempotency checks; repository ports remain persistence-focused.
 - No automatic ingestion, persistence, learning, Playbook evolution, or Consigliere integration is
   implied.
-- Source commit `1964356` implements Decision proposal, acceptance, action recording, and their
-  CLI plus the canonical `DecisionLifecycleService`.
-- Only proposed, accepted, and in-progress states can currently be derived. Action completion time
-  does not imply lifecycle completion, success, failure, outcome, or review.
+- Source commit `5befd7c` implements Decision proposal, acceptance, action and outcome recording,
+  outcome history/summary, their CLI, and the canonical `DecisionLifecycleService`.
+- The canonical states are exactly proposed, accepted, in-progress, succeeded, failed, partial,
+  and outcome-unknown. Latest outcome selection uses validation time and outcome UUID, not
+  repository order. No generic completed, resolved, or reviewed state exists.
 - Acceptance is authorization for possible future execution; it is not execution or reversal and
   creates no later lifecycle or learning record.
-- The one recommended next milestone is `DecisionOutcome foundation`, kept separate from
-  DecisionReview.
+- Multiple immutable outcomes may be appended for one Decision. Outcome creation is factual only
+  and creates no review or learning record.
+- The one recommended next milestone is `DecisionReview foundation`, kept separate from automatic
+  learning and downstream Experience, Knowledge, or Playbook creation.
diff --git a/handbook/domain/domain-chain.md b/handbook/domain/domain-chain.md
index f3b9161..9736490 100644
--- a/handbook/domain/domain-chain.md
+++ b/handbook/domain/domain-chain.md
@@ -39,15 +39,16 @@ Confirmed example:

 ## Complementary Decision Learning chain

-The implemented Decision, DecisionAcceptance, and DecisionAction foundations record a bounded
-proposed choice, explicit authorization, and work performed after Observation context:
+The implemented Decision, DecisionAcceptance, DecisionAction, and DecisionOutcome foundations
+record a bounded proposed choice, explicit authorization, work performed, and factual results
+after Observation context:

 ```text
 Observation
 → Decision
 → DecisionAcceptance
 → DecisionAction
-→ future DecisionOutcome
+→ DecisionOutcome
 → future DecisionReview
 → Experience
 → Knowledge
@@ -55,6 +56,7 @@ Observation

 This is a complementary provenance path, not a replacement for the canonical domain chain.
 DecisionOutcome is factual; Experience is interpreted; Knowledge is generalized; Playbook remains
-a separately created repeatable procedure. Decision, DecisionAcceptance, DecisionAction, and their
-embedded EvidenceReference values exist at source commit `1964356`; no Outcome, Review, or later
-transition in this path is automatic.
+a separately created repeatable procedure. DecisionOutcome may have multiple immutable records per
+Decision and does not automatically create a Review or learning artifact. Decision,
+DecisionAcceptance, DecisionAction, DecisionOutcome, and their embedded EvidenceReference values
+exist at source commit `5befd7c`; no Review or later transition in this path is automatic.
diff --git a/handbook/infrastructure/repositories.md b/handbook/infrastructure/repositories.md
index f9fe856..77e9f87 100644
--- a/handbook/infrastructure/repositories.md
+++ b/handbook/infrastructure/repositories.md
@@ -56,3 +56,13 @@ action under `NeuralPaths.DECISION_ACTIONS`; Brain initialization creates the di
 DecisionAction records round-trip through domain validation. `load_all()` sorts file names for
 deterministic order, and malformed data surfaces validation errors. The adapter performs no
 relation filtering, lifecycle projection, migration, ingestion, or command execution.
+
+## Decision outcome adapter
+
+`JsonDecisionOutcomeRepository` implements `DecisionOutcomeRepository` and stores one JSON file
+per outcome under `NeuralPaths.DECISION_OUTCOMES`; Brain initialization creates the directory.
+Complete DecisionOutcome records, including immutable scalar metrics, round-trip through domain
+validation. JSON object keys and metric keys are serialized deterministically, `load_all()` sorts
+file names, and malformed data surfaces validation errors. The adapter performs no relation
+validation or filtering, latest-outcome selection, summary or lifecycle projection, idempotency
+decision, migration, ingestion, review, or learning.
diff --git a/handbook/ports/repository-ports.md b/handbook/ports/repository-ports.md
index f98462e..69edd5d 100644
--- a/handbook/ports/repository-ports.md
+++ b/handbook/ports/repository-ports.md
@@ -40,6 +40,11 @@ Decision relation filtering, eligibility, and idempotency belong to
 Relation validation, Decision filtering, idempotency, and lifecycle projection belong to
 application services; no relation, idempotency, or lifecycle query method is part of the port.

+`DecisionOutcomeRepository` is limited to `save()`, `load_all()`, and `get_by_id()`.
+Decision filtering, acceptance/action relation validation, multiple-outcome history, idempotency,
+summary derivation, and lifecycle projection belong to application services; no relation,
+idempotency, summary, latest-outcome, or lifecycle query method is part of the port.
+
 ## Repository return types

 Prefer:
diff --git a/outputs/claude-skill/SKILL.md b/outputs/claude-skill/SKILL.md
index 648f31d..94e0a1b 100644
--- a/outputs/claude-skill/SKILL.md
+++ b/outputs/claude-skill/SKILL.md
@@ -118,17 +118,23 @@ a milestone snapshot, not a timeless guarantee.

 ## Decision Learning boundary

-Source commit `1964356` implements separate immutable `Decision`, `DecisionAcceptance`, and
-`DecisionAction` records, persistence-focused ports and JSON adapters, application services,
-container wiring, thin proposal/acceptance/action CLI commands, and the canonical
-`DecisionLifecycleService`. An action records work performed; it does not assert success or an
-outcome.
-
-Only `proposed`, `accepted`, and `in_progress` can currently be derived. `DecisionOutcome` and
-`DecisionReview` remain future-only. There is no execution engine, completion/success/failure
-state, reversal, ingestion, automatic learning, generic full lifecycle replay, or Consigliere
+Source commit `5befd7c` implements separate immutable `Decision`, `DecisionAcceptance`,
+`DecisionAction`, and `DecisionOutcome` records, persistence-focused ports and JSON adapters,
+application services, container wiring, thin proposal/acceptance/action/outcome CLI commands, and
+the canonical `DecisionLifecycleService`. An action records work performed; only a linked outcome
+records factual results and validation evidence.
+
+`DecisionOutcome` links one Decision, its acceptance, and one or more ordered unique actions. Its
+result is exactly `succeeded`, `failed`, `partial`, or `unknown`; scalar metrics are immutable.
+Multiple outcomes form history, and the non-persisted `DecisionOutcomeSummary` derives counts and
+the latest outcome using `(validated_at, outcome.id)` rather than repository order.
+
+The canonical lifecycle states are exactly `proposed`, `accepted`, `in_progress`, `succeeded`,
+`failed`, `partial`, and `outcome_unknown`. `DecisionReview` and a reviewed state remain
+future-only. Outcome creation does not create learning. There is no execution engine, lifecycle
+reversal, ingestion, automatic learning or evolution, generic event replay, or Consigliere
 integration. The authoritative implemented contract and future boundary are defined in
-`handbook/architecture/decision-learning.md`.
+`handbook/architecture/decision-learning.md`; the next milestone is the DecisionReview foundation.

 ## Decision Learning architecture

@@ -136,11 +142,11 @@ integration. The authoritative implemented contract and future boundary are defi

 ## Status and purpose

-NeuralEngine source commit `1964356` implements the Decision, DecisionAcceptance, and
-DecisionAction foundations plus the canonical minimal `DecisionLifecycleService` projection. They
-record an immutable proposed choice, explicit authorization, and work performed under that
-authorization. Each foundation persists immutable records, exposes application use cases, is
-wired through the container, and provides a thin CLI.
+NeuralEngine source commit `5befd7c` implements the Decision, DecisionAcceptance,
+DecisionAction, and DecisionOutcome foundations plus the canonical `DecisionLifecycleService`
+projection. They record an immutable proposed choice, explicit authorization, work performed under
+that authorization, and factual results. Each foundation persists immutable records, exposes
+application use cases, is wired through the container, and provides a thin CLI.

 The wider Decision Learning lifecycle remains accepted future architecture. Decision tracking
 complements the existing Observation-to-Playbook chain; it does not replace it.
@@ -154,15 +160,20 @@ Decision
 EvidenceReference
 DecisionAcceptance
 DecisionAction
+DecisionOutcome
 DecisionRepository
 DecisionAcceptanceRepository
 DecisionActionRepository
+DecisionOutcomeRepository
 JsonDecisionRepository
 JsonDecisionAcceptanceRepository
 JsonDecisionActionRepository
+JsonDecisionOutcomeRepository
 DecisionService
 DecisionAcceptanceService
 DecisionActionService
+DecisionOutcomeService
+DecisionOutcomeSummary
 DecisionLifecycleService
 container wiring
 neural decision add/list/show
@@ -171,13 +182,18 @@ neural decision acceptance-history
 neural decision action add
 neural decision action-history
 neural decision action-show
+neural decision outcome add
+neural decision outcome-history
+neural decision outcome-show
+neural decision outcome-summary
 neural decision state
 ```

 Creating a Decision records a proposal. Creating a DecisionAcceptance explicitly authorizes that
 proposal for possible future work. Creating a DecisionAction records work performed under that
-acceptance. None of these operations claims completion, success, failure, outcome, review, or
-learning. `DecisionOutcome` and `DecisionReview` are future-only records.
+acceptance. Creating a DecisionOutcome records factual results and validation evidence for one or
+more linked actions. None of these operations performs review or learning. `DecisionReview`
+remains future-only.

 ## Decision model

@@ -220,7 +236,7 @@ not rewrite the earlier record.
 ## EvidenceReference

 `EvidenceReference` is an implemented immutable value embedded in a Decision,
-DecisionAcceptance, or DecisionAction:
+DecisionAcceptance, DecisionAction, or DecisionOutcome:

 ```text
 kind
@@ -325,8 +341,48 @@ DecisionAction

 It does not mean the work succeeded, validation passed, an intended result occurred,
 DecisionOutcome exists, DecisionReview exists, or learning was created. `completed_at` means only
-that the described work interval ended. It does not produce a `completed`, `executed`, or
-`succeeded` lifecycle state.
+that the described work interval ended. It does not by itself produce a `completed`, `executed`,
+or `succeeded` lifecycle state.
+
+## DecisionOutcome foundation
+
+`DecisionOutcome` is an immutable factual result and validation record with these exact
+implemented fields:
+
+```text
+id
+recorded_at
+decision_id
+acceptance_id
+action_ids
+result
+summary
+validated_by
+validated_at
+evidence_references
+metrics
+idempotency_key
+tags
+```
+
+Its implemented invariants are:
+
+1. Decision, acceptance, and action IDs are valid UUIDs.
+2. At least one action ID is required; action IDs are ordered and unique.
+3. `result` is exactly `succeeded`, `failed`, `partial`, or `unknown`.
+4. `summary`, `validated_by`, and `idempotency_key` are trimmed and non-blank.
+5. `recorded_at` and `validated_at` are timezone-aware and normalized to UTC.
+6. Metrics contain at most 100 scalar `int | float | str | bool` values.
+7. Metric keys are trimmed, non-blank, at most 64 characters, and case-insensitively unique.
+8. Float metrics are finite, string metrics are bounded to 1000 characters, and nested values are
+   rejected.
+9. The metric mapping is immutable and serialized in deterministic key order.
+10. Tags and evidence use the existing normalization and immutable `EvidenceReference` rules.
+11. The model is immutable and has no mutable lifecycle status.
+
+One Decision may have multiple outcomes. Each outcome appends factual history and may link one or
+more actions; no outcome replaces or mutates an earlier record. An outcome does not mean review,
+Experience, Knowledge, Playbook change, or automatic learning occurred.

 ## Persistence

@@ -375,6 +431,21 @@ under `NeuralPaths.DECISION_ACTIONS`, and Brain initialization creates that dire
 through validation, and malformed stored data fails visibly. The adapter performs no migration,
 ingestion, or command execution.

+The persistence-focused `DecisionOutcomeRepository` also implements only:
+
+```text
+save()
+load_all()
+get_by_id()
+```
+
+It has no relation, idempotency, latest-outcome, summary, or lifecycle query methods.
+`JsonDecisionOutcomeRepository` stores one deterministic JSON file per outcome under
+`NeuralPaths.DECISION_OUTCOMES`, and Brain initialization creates that directory. Complete records
+and immutable scalar metrics round-trip through domain validation; malformed data fails visibly.
+The adapter performs no relation filtering, lifecycle projection, review, learning, migration, or
+ingestion.
+
 ## Application service

 `DecisionService` implements:
@@ -529,6 +600,54 @@ EvidenceReference.captured_at
 `list_for_decision()` validates the Decision, filters `load_all()` in the application layer, and
 preserves repository order. `show()` raises an explicit action-not-found error.

+### DecisionOutcomeService
+
+`DecisionOutcomeService` implements:
+
+```text
+add()
+list_for_decision()
+show()
+summary_for_decision()
+```
+
+`add()` validates Decision existence, acceptance existence and ownership, at least one unique
+action, and every action's Decision and acceptance relations. `validated_at` cannot precede the
+earliest linked action start. Only after relation validation does the service construct and save
+the immutable outcome. It mutates no related record and creates no Review or learning artifact.
+
+Outcome idempotency is scoped by:
+
+```text
+(decision_id, "decision_outcome", idempotency_key)
+```
+
+```text
+same scoped key + equivalent semantic payload
+→ return existing DecisionOutcome
+
+same scoped key + different semantic payload
+→ visible conflict, no write
+
+different key
+→ another outcome may be recorded
+```
+
+Semantic equivalence excludes `DecisionOutcome.id`, `DecisionOutcome.recorded_at`, and embedded
+`EvidenceReference.captured_at`. It includes the linked relations, result, validation data,
+metrics, and other caller-supplied semantic fields.
+
+`list_for_decision()` validates the Decision, filters `load_all()` in the application layer, and
+preserves repository order so the complete multiple-outcome history remains visible. `show()`
+raises an explicit outcome-not-found error.
+
+`DecisionOutcomeSummary` is an immutable, non-persisted application read model returned by
+`summary_for_decision()`. It reports outcome count, latest result and validation time, distinct
+linked-action count, counts for each result value, and success/failure presence. Summary derivation
+validates every persisted outcome-to-acceptance/action relation. Latest selection is deterministic
+by `(validated_at, outcome.id)` and never depends on repository order. The summary is derived on
+demand and is neither persisted nor cached.
+
 ### Canonical DecisionLifecycleService

 `DecisionLifecycleService` is the only canonical owner of the current lifecycle projection. It
@@ -538,6 +657,7 @@ depends on:
 DecisionRepository
 DecisionAcceptanceRepository
 DecisionActionRepository
+DecisionOutcomeRepository
 ```

 It derives exactly:
@@ -551,22 +671,26 @@ Decision exists, one valid acceptance, no action

 Decision exists, one valid acceptance, at least one valid action
 → in_progress
-```

-No mutable status is written and no generic event stream exists. Repository order does not define
-state; valid semantic relations do. Multiple persisted acceptances fail visibly, as does an action
-linked to a wrong or missing acceptance. Multiple valid actions still derive `in_progress`.
+latest valid outcome has result succeeded
+→ succeeded

-These states are explicitly unavailable:
+latest valid outcome has result failed
+→ failed

-```text
-executed
-completed
-succeeded
-failed
-reviewed
+latest valid outcome has result partial
+→ partial
+
+latest valid outcome has result unknown
+→ outcome_unknown
 ```

+No mutable status is written and no generic event stream exists. The latest outcome is selected by
+`(validated_at, outcome.id)`, never repository order. Multiple persisted acceptances fail visibly,
+as do invalid action or outcome relations. Multiple valid actions with no outcome derive
+`in_progress`; multiple outcomes retain history while the latest valid one drives the projection.
+There is no generic `executed`, `completed`, `resolved`, or `reviewed` state.
+
 ## Container

 The composition root constructs and connects:
@@ -580,6 +704,8 @@ DecisionAcceptanceService
 JsonDecisionActionRepository
 JsonPlaybookRunRepository
 DecisionActionService
+JsonDecisionOutcomeRepository
+DecisionOutcomeService
 DecisionLifecycleService
 ```

@@ -588,13 +714,14 @@ DecisionLifecycleService
 repositories or own validation, relation checks, persistence, eligibility, or idempotency policy.

 `DecisionActionService` receives `JsonDecisionActionRepository`, `JsonDecisionRepository`,
-`JsonDecisionAcceptanceRepository`, and `JsonPlaybookRunRepository`. `DecisionLifecycleService`
-receives the Decision, acceptance, and action repositories. CLI handlers resolve both services
-from the container and construct no repositories.
+`JsonDecisionAcceptanceRepository`, and `JsonPlaybookRunRepository`. `DecisionOutcomeService`
+receives `JsonDecisionOutcomeRepository` plus Decision, acceptance, and action repositories.
+`DecisionLifecycleService` receives the Decision, acceptance, action, and outcome repositories.
+CLI handlers resolve services from the container and construct no repositories.

 ## Implemented CLI

-These commands exist at commit `1964356`:
+These commands exist at commit `5befd7c`:

 ```text
 neural decision add
@@ -605,6 +732,10 @@ neural decision acceptance-history DECISION_UUID
 neural decision action add DECISION_UUID
 neural decision action-history DECISION_UUID
 neural decision action-show ACTION_UUID
+neural decision outcome add DECISION_UUID
+neural decision outcome-history DECISION_UUID
+neural decision outcome-show OUTCOME_UUID
+neural decision outcome-summary DECISION_UUID
 neural decision state DECISION_UUID
 ```

@@ -716,7 +847,7 @@ Reason

 An existing Decision with no acceptance produces a controlled empty state.

-### Decision action and state commands
+### Decision action commands

 `neural decision action add DECISION_UUID` requires:

@@ -757,19 +888,49 @@ Summary
 An existing Decision with no actions produces a controlled empty state.
 `neural decision action-show ACTION_UUID` renders every DecisionAction field.

+### Decision outcome and state commands
+
+`neural decision outcome add DECISION_UUID` requires:
+
+```text
+--acceptance-id
+--action-id (one or more)
+--result
+--summary
+--validated-by
+--validated-at
+--idempotency-key
+```
+
+Repeated `--evidence`, `--metric KEY=VALUE`, and `--tag` values are optional. Result accepts only
+`succeeded`, `failed`, `partial`, or `unknown`. Metrics parse unambiguous booleans, integers, and
+finite floats; other values remain strings and domain validation enforces the scalar bounds. The
+CLI reads no evidence locator and executes no referenced command.
+
+`neural decision outcome-history DECISION_UUID` renders all matching outcomes in repository order,
+including their result, validation time, linked action IDs, validator, and summary. An existing
+Decision with no outcomes produces a controlled empty state. `outcome-show OUTCOME_UUID` renders
+every stored field, including evidence, metrics, idempotency key, and tags.
+
+`neural decision outcome-summary DECISION_UUID` renders the derived count, deterministic latest
+result/time, distinct linked-action count, counts by result, and success/failure presence. It does
+not persist the summary.
+
 `neural decision state DECISION_UUID` renders exactly one of:

 ```text
 proposed
 accepted
 in_progress
+succeeded
+failed
+partial
+outcome_unknown
 ```

-It renders no later lifecycle state.
+## Review and learning boundary

-## Future lifecycle boundary
-
-The accepted future record family remains deliberately separate:
+The record family remains deliberately separate:

 ```text
 Decision
@@ -782,13 +943,13 @@ Decision
 - `Decision` is the implemented proposed choice.
 - `DecisionAcceptance` is the implemented explicit authorization for possible future execution.
 - `DecisionAction` is the implemented record of work performed under an accepted Decision.
-- `DecisionOutcome` would record factual results and validation evidence.
+- `DecisionOutcome` is the implemented factual result and validation evidence record.
 - `DecisionReview` would assess outcomes and hold candidate lessons.

-Only the first three records exist. Future records must remain immutable semantic records rather
-than fields on a mutable Decision or a duplicate generic event stream. A proposed option is not an
-acceptance, acceptance is not execution, an outcome is not an Experience, and candidate lessons
-are not automatically Knowledge or a Playbook change.
+The first four records exist; DecisionReview does not. Records remain immutable semantic records
+rather than fields on a mutable Decision or a duplicate generic event stream. A proposed option is
+not an acceptance, acceptance is not execution, an outcome is not a review or Experience, and
+candidate lessons are not automatically Knowledge or a Playbook change.

 The currently derivable projection is only:

@@ -801,10 +962,23 @@ Decision with one valid acceptance

 Decision with one valid acceptance and at least one valid action
 → in_progress
+
+latest valid outcome succeeded
+→ succeeded
+
+latest valid outcome failed
+→ failed
+
+latest valid outcome partial
+→ partial
+
+latest valid outcome unknown
+→ outcome_unknown
 ```

-There is no executed, completed, succeeded, failed, or reviewed state. The minimal lifecycle
-projection is canonical, but there is no generic full lifecycle replay service.
+The lifecycle projection uses the latest valid outcome selected by `(validated_at, outcome.id)`.
+There is no generic executed, completed, resolved, or reviewed state and no generic full lifecycle
+event replay service.

 ## Relationship to the domain chain

@@ -816,7 +990,7 @@ Observation
 → Decision
 → DecisionAcceptance
 → DecisionAction
-→ future DecisionOutcome
+→ DecisionOutcome
 → future DecisionReview
 → explicitly created Experience
 → explicitly created Knowledge
@@ -844,18 +1018,18 @@ prompt
 → post-work lesson
 ```

-Commit `1964356` does not capture or ingest those events. Automatic candidates and manual
-confirmation remain future concepts; no automatic persistence, ingestion, or learning exists.
+Commit `5befd7c` does not capture or ingest those events automatically. Automatic candidates and
+manual confirmation remain future concepts; no automatic persistence, ingestion, or learning
+exists.

 Consigliere also remains future-only. It may later advise. No Consigliere integration exists, and
 no recommendation can directly mutate NeuralEngine or authorize a durable record.

 ## Current non-behavior

-Commit `1964356` does not implement:
+Commit `5befd7c` does not implement:

 ```text
-DecisionOutcome
 DecisionReview
 execution engine
 command/shell execution
@@ -865,7 +1039,7 @@ reversal
 reopening
 cancellation
 replacement
-executed/completed/succeeded/failed/reviewed states
+executed/completed/resolved/reviewed states
 file ingestion
 git ingestion
 automatic Observation creation
@@ -878,17 +1052,19 @@ Consigliere integration

 It also does not execute commands referenced by evidence, open locators, automatically accept
 Decisions, materialize Playbook revisions, or infer outcomes from `completed_at`. Explicit user
-requests are required to create Decision, DecisionAcceptance, or DecisionAction records.
+requests are required to create Decision, DecisionAcceptance, DecisionAction, or DecisionOutcome
+records.

 ## Recommended next milestone

 The one recommended next controlled slice is:

 ```text
-DecisionOutcome foundation
+DecisionReview foundation
 ```

-It must remain separate from `DecisionReview`.
+It must remain separate from automatic Experience, Knowledge, Playbook, PlaybookEvaluation, or
+EvolutionProposal creation.

 ## Handbook synchronization policy

@@ -938,15 +1114,16 @@ Confirmed example:

 ## Complementary Decision Learning chain

-The implemented Decision, DecisionAcceptance, and DecisionAction foundations record a bounded
-proposed choice, explicit authorization, and work performed after Observation context:
+The implemented Decision, DecisionAcceptance, DecisionAction, and DecisionOutcome foundations
+record a bounded proposed choice, explicit authorization, work performed, and factual results
+after Observation context:

 ```text
 Observation
 → Decision
 → DecisionAcceptance
 → DecisionAction
-→ future DecisionOutcome
+→ DecisionOutcome
 → future DecisionReview
 → Experience
 → Knowledge
@@ -954,9 +1131,10 @@ Observation

 This is a complementary provenance path, not a replacement for the canonical domain chain.
 DecisionOutcome is factual; Experience is interpreted; Knowledge is generalized; Playbook remains
-a separately created repeatable procedure. Decision, DecisionAcceptance, DecisionAction, and their
-embedded EvidenceReference values exist at source commit `1964356`; no Outcome, Review, or later
-transition in this path is automatic.
+a separately created repeatable procedure. DecisionOutcome may have multiple immutable records per
+Decision and does not automatically create a Review or learning artifact. Decision,
+DecisionAcceptance, DecisionAction, DecisionOutcome, and their embedded EvidenceReference values
+exist at source commit `5befd7c`; no Review or later transition in this path is automatic.

 ## Workflow

diff --git a/outputs/generated/AGENTS.generated.md b/outputs/generated/AGENTS.generated.md
index 8a2ccca..e287853 100644
--- a/outputs/generated/AGENTS.generated.md
+++ b/outputs/generated/AGENTS.generated.md
@@ -137,17 +137,23 @@ a milestone snapshot, not a timeless guarantee.

 ## Decision Learning boundary

-Source commit `1964356` implements separate immutable `Decision`, `DecisionAcceptance`, and
-`DecisionAction` records, persistence-focused ports and JSON adapters, application services,
-container wiring, thin proposal/acceptance/action CLI commands, and the canonical
-`DecisionLifecycleService`. An action records work performed; it does not assert success or an
-outcome.
-
-Only `proposed`, `accepted`, and `in_progress` can currently be derived. `DecisionOutcome` and
-`DecisionReview` remain future-only. There is no execution engine, completion/success/failure
-state, reversal, ingestion, automatic learning, generic full lifecycle replay, or Consigliere
+Source commit `5befd7c` implements separate immutable `Decision`, `DecisionAcceptance`,
+`DecisionAction`, and `DecisionOutcome` records, persistence-focused ports and JSON adapters,
+application services, container wiring, thin proposal/acceptance/action/outcome CLI commands, and
+the canonical `DecisionLifecycleService`. An action records work performed; only a linked outcome
+records factual results and validation evidence.
+
+`DecisionOutcome` links one Decision, its acceptance, and one or more ordered unique actions. Its
+result is exactly `succeeded`, `failed`, `partial`, or `unknown`; scalar metrics are immutable.
+Multiple outcomes form history, and the non-persisted `DecisionOutcomeSummary` derives counts and
+the latest outcome using `(validated_at, outcome.id)` rather than repository order.
+
+The canonical lifecycle states are exactly `proposed`, `accepted`, `in_progress`, `succeeded`,
+`failed`, `partial`, and `outcome_unknown`. `DecisionReview` and a reviewed state remain
+future-only. Outcome creation does not create learning. There is no execution engine, lifecycle
+reversal, ingestion, automatic learning or evolution, generic event replay, or Consigliere
 integration. The authoritative implemented contract and future boundary are defined in
-`handbook/architecture/decision-learning.md`.
+`handbook/architecture/decision-learning.md`; the next milestone is the DecisionReview foundation.

 ## Agent policy

diff --git a/outputs/generated/APPLICATION_ARCHITECTURE.md b/outputs/generated/APPLICATION_ARCHITECTURE.md
index b6a9c12..5d90c05 100644
--- a/outputs/generated/APPLICATION_ARCHITECTURE.md
+++ b/outputs/generated/APPLICATION_ARCHITECTURE.md
@@ -103,7 +103,7 @@ acceptance both fail visibly without writing.
 and preserves repository order. `show()` owns explicit acceptance not-found behavior. Acceptance
 does not mutate Decision or create actions, outcomes, reviews, execution, or learning.

-## Decision action and lifecycle ownership
+## Decision action ownership

 `DecisionActionService.add()` validates the Decision, matching acceptance, and optional
 PlaybookRun before creating an immutable action. It uses
@@ -115,10 +115,28 @@ multiple distinct actions, and mutates no related record. PlaybookRun and Playbo
 `show()` owns explicit action-not-found behavior. The service creates no Outcome, Review, or
 learning record.

+## Decision outcome and lifecycle ownership
+
+`DecisionOutcomeService.add()` validates the Decision, matching acceptance, one or more unique
+actions, each action's Decision and acceptance relations, and validation time against the earliest
+linked action start before constructing or saving an immutable outcome. It uses
+`(decision_id, "decision_outcome", idempotency_key)` for application-layer idempotency. Equivalent
+replay returns the existing outcome; conflicting reuse fails without a write; another key may
+append another outcome for the same Decision.
+
+`list_for_decision()` validates the Decision and returns all matching outcomes in repository order.
+`show()` owns explicit outcome-not-found behavior. `summary_for_decision()` validates persisted
+outcome relations and returns an immutable, non-persisted `DecisionOutcomeSummary` with outcome
+count, deterministic latest result/time, distinct linked-action count, counts by result, and
+success/failure presence. Latest selection uses `(validated_at, outcome.id)` rather than repository
+order.
+
 `DecisionLifecycleService` is the only canonical projection owner. It validates persisted
-Decision/acceptance/action relations and derives only `proposed`, `accepted`, or `in_progress`.
-It writes no status, ignores repository order for state, and exposes no completed, succeeded,
-failed, or reviewed state.
+Decision/acceptance/action/outcome relations and derives exactly `proposed`, `accepted`,
+`in_progress`, `succeeded`, `failed`, `partial`, or `outcome_unknown`. When outcomes exist, the
+latest is selected by `(validated_at, outcome.id)`. It writes no status and exposes no generic
+`completed`, `resolved`, or reviewed state. Outcome creation and projection create no Review or
+learning record.

 ---

@@ -239,6 +257,11 @@ Decision relation filtering, eligibility, and idempotency belong to
 Relation validation, Decision filtering, idempotency, and lifecycle projection belong to
 application services; no relation, idempotency, or lifecycle query method is part of the port.

+`DecisionOutcomeRepository` is limited to `save()`, `load_all()`, and `get_by_id()`.
+Decision filtering, acceptance/action relation validation, multiple-outcome history, idempotency,
+summary derivation, and lifecycle projection belong to application services; no relation,
+idempotency, summary, latest-outcome, or lifecycle query method is part of the port.
+
 ## Repository return types

 Prefer:
@@ -365,6 +388,16 @@ DecisionAction records round-trip through domain validation. `load_all()` sorts
 deterministic order, and malformed data surfaces validation errors. The adapter performs no
 relation filtering, lifecycle projection, migration, ingestion, or command execution.

+## Decision outcome adapter
+
+`JsonDecisionOutcomeRepository` implements `DecisionOutcomeRepository` and stores one JSON file
+per outcome under `NeuralPaths.DECISION_OUTCOMES`; Brain initialization creates the directory.
+Complete DecisionOutcome records, including immutable scalar metrics, round-trip through domain
+validation. JSON object keys and metric keys are serialized deterministically, `load_all()` sorts
+file names, and malformed data surfaces validation errors. The adapter performs no relation
+validation or filtering, latest-outcome selection, summary or lifecycle projection, idempotency
+decision, migration, ingestion, review, or learning.
+
 ---

 # Dependency Injection and Container
@@ -428,11 +461,15 @@ The acceptance foundation is wired through `Container.decision_acceptance_reposi
 `JsonDecisionAcceptanceRepository` and `JsonDecisionRepository` to
 `DecisionAcceptanceService`; acceptance CLI handlers construct no repositories.

-The action foundation is wired through `Container.decision_action_repository()`,
-`Container.decision_action_service()`, and `Container.decision_lifecycle_service()`. The action
-service receives JSON action, Decision, acceptance, and PlaybookRun repositories. The lifecycle
-service receives Decision, acceptance, and action repositories. CLI handlers resolve services and
-construct no repositories.
+The action foundation is wired through `Container.decision_action_repository()` and
+`Container.decision_action_service()`. The action service receives JSON action, Decision,
+acceptance, and PlaybookRun repositories.
+
+The outcome foundation is wired through `Container.decision_outcome_repository()` and
+`Container.decision_outcome_service()`. The outcome service receives JSON outcome, Decision,
+acceptance, and action repositories. `Container.decision_lifecycle_service()` receives those same
+four repository categories so it can validate relations and derive the canonical state. Decision
+action, outcome, summary, and state CLI handlers resolve services and construct no repositories.

 ---

diff --git a/outputs/generated/DECISION_ENGINE.md b/outputs/generated/DECISION_ENGINE.md
index 18717b3..40ea38e 100644
--- a/outputs/generated/DECISION_ENGINE.md
+++ b/outputs/generated/DECISION_ENGINE.md
@@ -104,11 +104,11 @@ New behavior

 ## Status and purpose

-NeuralEngine source commit `1964356` implements the Decision, DecisionAcceptance, and
-DecisionAction foundations plus the canonical minimal `DecisionLifecycleService` projection. They
-record an immutable proposed choice, explicit authorization, and work performed under that
-authorization. Each foundation persists immutable records, exposes application use cases, is
-wired through the container, and provides a thin CLI.
+NeuralEngine source commit `5befd7c` implements the Decision, DecisionAcceptance,
+DecisionAction, and DecisionOutcome foundations plus the canonical `DecisionLifecycleService`
+projection. They record an immutable proposed choice, explicit authorization, work performed under
+that authorization, and factual results. Each foundation persists immutable records, exposes
+application use cases, is wired through the container, and provides a thin CLI.

 The wider Decision Learning lifecycle remains accepted future architecture. Decision tracking
 complements the existing Observation-to-Playbook chain; it does not replace it.
@@ -122,15 +122,20 @@ Decision
 EvidenceReference
 DecisionAcceptance
 DecisionAction
+DecisionOutcome
 DecisionRepository
 DecisionAcceptanceRepository
 DecisionActionRepository
+DecisionOutcomeRepository
 JsonDecisionRepository
 JsonDecisionAcceptanceRepository
 JsonDecisionActionRepository
+JsonDecisionOutcomeRepository
 DecisionService
 DecisionAcceptanceService
 DecisionActionService
+DecisionOutcomeService
+DecisionOutcomeSummary
 DecisionLifecycleService
 container wiring
 neural decision add/list/show
@@ -139,13 +144,18 @@ neural decision acceptance-history
 neural decision action add
 neural decision action-history
 neural decision action-show
+neural decision outcome add
+neural decision outcome-history
+neural decision outcome-show
+neural decision outcome-summary
 neural decision state
 ```

 Creating a Decision records a proposal. Creating a DecisionAcceptance explicitly authorizes that
 proposal for possible future work. Creating a DecisionAction records work performed under that
-acceptance. None of these operations claims completion, success, failure, outcome, review, or
-learning. `DecisionOutcome` and `DecisionReview` are future-only records.
+acceptance. Creating a DecisionOutcome records factual results and validation evidence for one or
+more linked actions. None of these operations performs review or learning. `DecisionReview`
+remains future-only.

 ## Decision model

@@ -188,7 +198,7 @@ not rewrite the earlier record.
 ## EvidenceReference

 `EvidenceReference` is an implemented immutable value embedded in a Decision,
-DecisionAcceptance, or DecisionAction:
+DecisionAcceptance, DecisionAction, or DecisionOutcome:

 ```text
 kind
@@ -293,8 +303,48 @@ DecisionAction

 It does not mean the work succeeded, validation passed, an intended result occurred,
 DecisionOutcome exists, DecisionReview exists, or learning was created. `completed_at` means only
-that the described work interval ended. It does not produce a `completed`, `executed`, or
-`succeeded` lifecycle state.
+that the described work interval ended. It does not by itself produce a `completed`, `executed`,
+or `succeeded` lifecycle state.
+
+## DecisionOutcome foundation
+
+`DecisionOutcome` is an immutable factual result and validation record with these exact
+implemented fields:
+
+```text
+id
+recorded_at
+decision_id
+acceptance_id
+action_ids
+result
+summary
+validated_by
+validated_at
+evidence_references
+metrics
+idempotency_key
+tags
+```
+
+Its implemented invariants are:
+
+1. Decision, acceptance, and action IDs are valid UUIDs.
+2. At least one action ID is required; action IDs are ordered and unique.
+3. `result` is exactly `succeeded`, `failed`, `partial`, or `unknown`.
+4. `summary`, `validated_by`, and `idempotency_key` are trimmed and non-blank.
+5. `recorded_at` and `validated_at` are timezone-aware and normalized to UTC.
+6. Metrics contain at most 100 scalar `int | float | str | bool` values.
+7. Metric keys are trimmed, non-blank, at most 64 characters, and case-insensitively unique.
+8. Float metrics are finite, string metrics are bounded to 1000 characters, and nested values are
+   rejected.
+9. The metric mapping is immutable and serialized in deterministic key order.
+10. Tags and evidence use the existing normalization and immutable `EvidenceReference` rules.
+11. The model is immutable and has no mutable lifecycle status.
+
+One Decision may have multiple outcomes. Each outcome appends factual history and may link one or
+more actions; no outcome replaces or mutates an earlier record. An outcome does not mean review,
+Experience, Knowledge, Playbook change, or automatic learning occurred.

 ## Persistence

@@ -343,6 +393,21 @@ under `NeuralPaths.DECISION_ACTIONS`, and Brain initialization creates that dire
 through validation, and malformed stored data fails visibly. The adapter performs no migration,
 ingestion, or command execution.

+The persistence-focused `DecisionOutcomeRepository` also implements only:
+
+```text
+save()
+load_all()
+get_by_id()
+```
+
+It has no relation, idempotency, latest-outcome, summary, or lifecycle query methods.
+`JsonDecisionOutcomeRepository` stores one deterministic JSON file per outcome under
+`NeuralPaths.DECISION_OUTCOMES`, and Brain initialization creates that directory. Complete records
+and immutable scalar metrics round-trip through domain validation; malformed data fails visibly.
+The adapter performs no relation filtering, lifecycle projection, review, learning, migration, or
+ingestion.
+
 ## Application service

 `DecisionService` implements:
@@ -497,6 +562,54 @@ EvidenceReference.captured_at
 `list_for_decision()` validates the Decision, filters `load_all()` in the application layer, and
 preserves repository order. `show()` raises an explicit action-not-found error.

+### DecisionOutcomeService
+
+`DecisionOutcomeService` implements:
+
+```text
+add()
+list_for_decision()
+show()
+summary_for_decision()
+```
+
+`add()` validates Decision existence, acceptance existence and ownership, at least one unique
+action, and every action's Decision and acceptance relations. `validated_at` cannot precede the
+earliest linked action start. Only after relation validation does the service construct and save
+the immutable outcome. It mutates no related record and creates no Review or learning artifact.
+
+Outcome idempotency is scoped by:
+
+```text
+(decision_id, "decision_outcome", idempotency_key)
+```
+
+```text
+same scoped key + equivalent semantic payload
+→ return existing DecisionOutcome
+
+same scoped key + different semantic payload
+→ visible conflict, no write
+
+different key
+→ another outcome may be recorded
+```
+
+Semantic equivalence excludes `DecisionOutcome.id`, `DecisionOutcome.recorded_at`, and embedded
+`EvidenceReference.captured_at`. It includes the linked relations, result, validation data,
+metrics, and other caller-supplied semantic fields.
+
+`list_for_decision()` validates the Decision, filters `load_all()` in the application layer, and
+preserves repository order so the complete multiple-outcome history remains visible. `show()`
+raises an explicit outcome-not-found error.
+
+`DecisionOutcomeSummary` is an immutable, non-persisted application read model returned by
+`summary_for_decision()`. It reports outcome count, latest result and validation time, distinct
+linked-action count, counts for each result value, and success/failure presence. Summary derivation
+validates every persisted outcome-to-acceptance/action relation. Latest selection is deterministic
+by `(validated_at, outcome.id)` and never depends on repository order. The summary is derived on
+demand and is neither persisted nor cached.
+
 ### Canonical DecisionLifecycleService

 `DecisionLifecycleService` is the only canonical owner of the current lifecycle projection. It
@@ -506,6 +619,7 @@ depends on:
 DecisionRepository
 DecisionAcceptanceRepository
 DecisionActionRepository
+DecisionOutcomeRepository
 ```

 It derives exactly:
@@ -519,22 +633,26 @@ Decision exists, one valid acceptance, no action

 Decision exists, one valid acceptance, at least one valid action
 → in_progress
-```

-No mutable status is written and no generic event stream exists. Repository order does not define
-state; valid semantic relations do. Multiple persisted acceptances fail visibly, as does an action
-linked to a wrong or missing acceptance. Multiple valid actions still derive `in_progress`.
+latest valid outcome has result succeeded
+→ succeeded

-These states are explicitly unavailable:
+latest valid outcome has result failed
+→ failed

-```text
-executed
-completed
-succeeded
-failed
-reviewed
+latest valid outcome has result partial
+→ partial
+
+latest valid outcome has result unknown
+→ outcome_unknown
 ```

+No mutable status is written and no generic event stream exists. The latest outcome is selected by
+`(validated_at, outcome.id)`, never repository order. Multiple persisted acceptances fail visibly,
+as do invalid action or outcome relations. Multiple valid actions with no outcome derive
+`in_progress`; multiple outcomes retain history while the latest valid one drives the projection.
+There is no generic `executed`, `completed`, `resolved`, or `reviewed` state.
+
 ## Container

 The composition root constructs and connects:
@@ -548,6 +666,8 @@ DecisionAcceptanceService
 JsonDecisionActionRepository
 JsonPlaybookRunRepository
 DecisionActionService
+JsonDecisionOutcomeRepository
+DecisionOutcomeService
 DecisionLifecycleService
 ```

@@ -556,13 +676,14 @@ DecisionLifecycleService
 repositories or own validation, relation checks, persistence, eligibility, or idempotency policy.

 `DecisionActionService` receives `JsonDecisionActionRepository`, `JsonDecisionRepository`,
-`JsonDecisionAcceptanceRepository`, and `JsonPlaybookRunRepository`. `DecisionLifecycleService`
-receives the Decision, acceptance, and action repositories. CLI handlers resolve both services
-from the container and construct no repositories.
+`JsonDecisionAcceptanceRepository`, and `JsonPlaybookRunRepository`. `DecisionOutcomeService`
+receives `JsonDecisionOutcomeRepository` plus Decision, acceptance, and action repositories.
+`DecisionLifecycleService` receives the Decision, acceptance, action, and outcome repositories.
+CLI handlers resolve services from the container and construct no repositories.

 ## Implemented CLI

-These commands exist at commit `1964356`:
+These commands exist at commit `5befd7c`:

 ```text
 neural decision add
@@ -573,6 +694,10 @@ neural decision acceptance-history DECISION_UUID
 neural decision action add DECISION_UUID
 neural decision action-history DECISION_UUID
 neural decision action-show ACTION_UUID
+neural decision outcome add DECISION_UUID
+neural decision outcome-history DECISION_UUID
+neural decision outcome-show OUTCOME_UUID
+neural decision outcome-summary DECISION_UUID
 neural decision state DECISION_UUID
 ```

@@ -684,7 +809,7 @@ Reason

 An existing Decision with no acceptance produces a controlled empty state.

-### Decision action and state commands
+### Decision action commands

 `neural decision action add DECISION_UUID` requires:

@@ -725,19 +850,49 @@ Summary
 An existing Decision with no actions produces a controlled empty state.
 `neural decision action-show ACTION_UUID` renders every DecisionAction field.

+### Decision outcome and state commands
+
+`neural decision outcome add DECISION_UUID` requires:
+
+```text
+--acceptance-id
+--action-id (one or more)
+--result
+--summary
+--validated-by
+--validated-at
+--idempotency-key
+```
+
+Repeated `--evidence`, `--metric KEY=VALUE`, and `--tag` values are optional. Result accepts only
+`succeeded`, `failed`, `partial`, or `unknown`. Metrics parse unambiguous booleans, integers, and
+finite floats; other values remain strings and domain validation enforces the scalar bounds. The
+CLI reads no evidence locator and executes no referenced command.
+
+`neural decision outcome-history DECISION_UUID` renders all matching outcomes in repository order,
+including their result, validation time, linked action IDs, validator, and summary. An existing
+Decision with no outcomes produces a controlled empty state. `outcome-show OUTCOME_UUID` renders
+every stored field, including evidence, metrics, idempotency key, and tags.
+
+`neural decision outcome-summary DECISION_UUID` renders the derived count, deterministic latest
+result/time, distinct linked-action count, counts by result, and success/failure presence. It does
+not persist the summary.
+
 `neural decision state DECISION_UUID` renders exactly one of:

 ```text
 proposed
 accepted
 in_progress
+succeeded
+failed
+partial
+outcome_unknown
 ```

-It renders no later lifecycle state.
-
-## Future lifecycle boundary
+## Review and learning boundary

-The accepted future record family remains deliberately separate:
+The record family remains deliberately separate:

 ```text
 Decision
@@ -750,13 +905,13 @@ Decision
 - `Decision` is the implemented proposed choice.
 - `DecisionAcceptance` is the implemented explicit authorization for possible future execution.
 - `DecisionAction` is the implemented record of work performed under an accepted Decision.
-- `DecisionOutcome` would record factual results and validation evidence.
+- `DecisionOutcome` is the implemented factual result and validation evidence record.
 - `DecisionReview` would assess outcomes and hold candidate lessons.

-Only the first three records exist. Future records must remain immutable semantic records rather
-than fields on a mutable Decision or a duplicate generic event stream. A proposed option is not an
-acceptance, acceptance is not execution, an outcome is not an Experience, and candidate lessons
-are not automatically Knowledge or a Playbook change.
+The first four records exist; DecisionReview does not. Records remain immutable semantic records
+rather than fields on a mutable Decision or a duplicate generic event stream. A proposed option is
+not an acceptance, acceptance is not execution, an outcome is not a review or Experience, and
+candidate lessons are not automatically Knowledge or a Playbook change.

 The currently derivable projection is only:

@@ -769,10 +924,23 @@ Decision with one valid acceptance

 Decision with one valid acceptance and at least one valid action
 → in_progress
+
+latest valid outcome succeeded
+→ succeeded
+
+latest valid outcome failed
+→ failed
+
+latest valid outcome partial
+→ partial
+
+latest valid outcome unknown
+→ outcome_unknown
 ```

-There is no executed, completed, succeeded, failed, or reviewed state. The minimal lifecycle
-projection is canonical, but there is no generic full lifecycle replay service.
+The lifecycle projection uses the latest valid outcome selected by `(validated_at, outcome.id)`.
+There is no generic executed, completed, resolved, or reviewed state and no generic full lifecycle
+event replay service.

 ## Relationship to the domain chain

@@ -784,7 +952,7 @@ Observation
 → Decision
 → DecisionAcceptance
 → DecisionAction
-→ future DecisionOutcome
+→ DecisionOutcome
 → future DecisionReview
 → explicitly created Experience
 → explicitly created Knowledge
@@ -812,18 +980,18 @@ prompt
 → post-work lesson
 ```

-Commit `1964356` does not capture or ingest those events. Automatic candidates and manual
-confirmation remain future concepts; no automatic persistence, ingestion, or learning exists.
+Commit `5befd7c` does not capture or ingest those events automatically. Automatic candidates and
+manual confirmation remain future concepts; no automatic persistence, ingestion, or learning
+exists.

 Consigliere also remains future-only. It may later advise. No Consigliere integration exists, and
 no recommendation can directly mutate NeuralEngine or authorize a durable record.

 ## Current non-behavior

-Commit `1964356` does not implement:
+Commit `5befd7c` does not implement:

 ```text
-DecisionOutcome
 DecisionReview
 execution engine
 command/shell execution
@@ -833,7 +1001,7 @@ reversal
 reopening
 cancellation
 replacement
-executed/completed/succeeded/failed/reviewed states
+executed/completed/resolved/reviewed states
 file ingestion
 git ingestion
 automatic Observation creation
@@ -846,17 +1014,19 @@ Consigliere integration

 It also does not execute commands referenced by evidence, open locators, automatically accept
 Decisions, materialize Playbook revisions, or infer outcomes from `completed_at`. Explicit user
-requests are required to create Decision, DecisionAcceptance, or DecisionAction records.
+requests are required to create Decision, DecisionAcceptance, DecisionAction, or DecisionOutcome
+records.

 ## Recommended next milestone

 The one recommended next controlled slice is:

 ```text
-DecisionOutcome foundation
+DecisionReview foundation
 ```

-It must remain separate from `DecisionReview`.
+It must remain separate from automatic Experience, Knowledge, Playbook, PlaybookEvaluation, or
+EvolutionProposal creation.

 ## Handbook synchronization policy

@@ -978,10 +1148,10 @@ Status: Accepted
 ## Decision

 Development decision tracking uses implemented separate immutable `Decision`,
-`DecisionAcceptance`, and `DecisionAction` records with embedded immutable `EvidenceReference`
-values. `DecisionOutcome` and `DecisionReview` remain separate future-only records. Lifecycle state
-is derived from semantic records, not stored as mutable status or duplicated in a generic event
-stream.
+`DecisionAcceptance`, `DecisionAction`, and `DecisionOutcome` records with embedded immutable
+`EvidenceReference` values. `DecisionReview` remains a separate future-only record. Lifecycle
+state is derived from semantic records, not stored as mutable status or duplicated in a generic
+event stream.

 Decision tracking complements the existing Observation-to-Playbook chain. Evidence uses bounded
 embedded references, durable writes require explicit authority, and Consigliere remains a future
@@ -995,11 +1165,14 @@ advisory layer rather than authoritative storage.
   idempotency checks; repository ports remain persistence-focused.
 - No automatic ingestion, persistence, learning, Playbook evolution, or Consigliere integration is
   implied.
-- Source commit `1964356` implements Decision proposal, acceptance, action recording, and their
-  CLI plus the canonical `DecisionLifecycleService`.
-- Only proposed, accepted, and in-progress states can currently be derived. Action completion time
-  does not imply lifecycle completion, success, failure, outcome, or review.
+- Source commit `5befd7c` implements Decision proposal, acceptance, action and outcome recording,
+  outcome history/summary, their CLI, and the canonical `DecisionLifecycleService`.
+- The canonical states are exactly proposed, accepted, in-progress, succeeded, failed, partial,
+  and outcome-unknown. Latest outcome selection uses validation time and outcome UUID, not
+  repository order. No generic completed, resolved, or reviewed state exists.
 - Acceptance is authorization for possible future execution; it is not execution or reversal and
   creates no later lifecycle or learning record.
-- The one recommended next milestone is `DecisionOutcome foundation`, kept separate from
-  DecisionReview.
+- Multiple immutable outcomes may be appended for one Decision. Outcome creation is factual only
+  and creates no review or learning record.
+- The one recommended next milestone is `DecisionReview foundation`, kept separate from automatic
+  learning and downstream Experience, Knowledge, or Playbook creation.
diff --git a/outputs/generated/HANDBOOK.md b/outputs/generated/HANDBOOK.md
index d0f19e3..559a6fc 100644
--- a/outputs/generated/HANDBOOK.md
+++ b/outputs/generated/HANDBOOK.md
@@ -103,17 +103,23 @@ a milestone snapshot, not a timeless guarantee.

 ## Decision Learning boundary

-Source commit `1964356` implements separate immutable `Decision`, `DecisionAcceptance`, and
-`DecisionAction` records, persistence-focused ports and JSON adapters, application services,
-container wiring, thin proposal/acceptance/action CLI commands, and the canonical
-`DecisionLifecycleService`. An action records work performed; it does not assert success or an
-outcome.
-
-Only `proposed`, `accepted`, and `in_progress` can currently be derived. `DecisionOutcome` and
-`DecisionReview` remain future-only. There is no execution engine, completion/success/failure
-state, reversal, ingestion, automatic learning, generic full lifecycle replay, or Consigliere
+Source commit `5befd7c` implements separate immutable `Decision`, `DecisionAcceptance`,
+`DecisionAction`, and `DecisionOutcome` records, persistence-focused ports and JSON adapters,
+application services, container wiring, thin proposal/acceptance/action/outcome CLI commands, and
+the canonical `DecisionLifecycleService`. An action records work performed; only a linked outcome
+records factual results and validation evidence.
+
+`DecisionOutcome` links one Decision, its acceptance, and one or more ordered unique actions. Its
+result is exactly `succeeded`, `failed`, `partial`, or `unknown`; scalar metrics are immutable.
+Multiple outcomes form history, and the non-persisted `DecisionOutcomeSummary` derives counts and
+the latest outcome using `(validated_at, outcome.id)` rather than repository order.
+
+The canonical lifecycle states are exactly `proposed`, `accepted`, `in_progress`, `succeeded`,
+`failed`, `partial`, and `outcome_unknown`. `DecisionReview` and a reviewed state remain
+future-only. Outcome creation does not create learning. There is no execution engine, lifecycle
+reversal, ingestion, automatic learning or evolution, generic event replay, or Consigliere
 integration. The authoritative implemented contract and future boundary are defined in
-`handbook/architecture/decision-learning.md`.
+`handbook/architecture/decision-learning.md`; the next milestone is the DecisionReview foundation.

 ---

@@ -121,11 +127,11 @@ integration. The authoritative implemented contract and future boundary are defi

 ## Status and purpose

-NeuralEngine source commit `1964356` implements the Decision, DecisionAcceptance, and
-DecisionAction foundations plus the canonical minimal `DecisionLifecycleService` projection. They
-record an immutable proposed choice, explicit authorization, and work performed under that
-authorization. Each foundation persists immutable records, exposes application use cases, is
-wired through the container, and provides a thin CLI.
+NeuralEngine source commit `5befd7c` implements the Decision, DecisionAcceptance,
+DecisionAction, and DecisionOutcome foundations plus the canonical `DecisionLifecycleService`
+projection. They record an immutable proposed choice, explicit authorization, work performed under
+that authorization, and factual results. Each foundation persists immutable records, exposes
+application use cases, is wired through the container, and provides a thin CLI.

 The wider Decision Learning lifecycle remains accepted future architecture. Decision tracking
 complements the existing Observation-to-Playbook chain; it does not replace it.
@@ -139,15 +145,20 @@ Decision
 EvidenceReference
 DecisionAcceptance
 DecisionAction
+DecisionOutcome
 DecisionRepository
 DecisionAcceptanceRepository
 DecisionActionRepository
+DecisionOutcomeRepository
 JsonDecisionRepository
 JsonDecisionAcceptanceRepository
 JsonDecisionActionRepository
+JsonDecisionOutcomeRepository
 DecisionService
 DecisionAcceptanceService
 DecisionActionService
+DecisionOutcomeService
+DecisionOutcomeSummary
 DecisionLifecycleService
 container wiring
 neural decision add/list/show
@@ -156,13 +167,18 @@ neural decision acceptance-history
 neural decision action add
 neural decision action-history
 neural decision action-show
+neural decision outcome add
+neural decision outcome-history
+neural decision outcome-show
+neural decision outcome-summary
 neural decision state
 ```

 Creating a Decision records a proposal. Creating a DecisionAcceptance explicitly authorizes that
 proposal for possible future work. Creating a DecisionAction records work performed under that
-acceptance. None of these operations claims completion, success, failure, outcome, review, or
-learning. `DecisionOutcome` and `DecisionReview` are future-only records.
+acceptance. Creating a DecisionOutcome records factual results and validation evidence for one or
+more linked actions. None of these operations performs review or learning. `DecisionReview`
+remains future-only.

 ## Decision model

@@ -205,7 +221,7 @@ not rewrite the earlier record.
 ## EvidenceReference

 `EvidenceReference` is an implemented immutable value embedded in a Decision,
-DecisionAcceptance, or DecisionAction:
+DecisionAcceptance, DecisionAction, or DecisionOutcome:

 ```text
 kind
@@ -310,8 +326,48 @@ DecisionAction

 It does not mean the work succeeded, validation passed, an intended result occurred,
 DecisionOutcome exists, DecisionReview exists, or learning was created. `completed_at` means only
-that the described work interval ended. It does not produce a `completed`, `executed`, or
-`succeeded` lifecycle state.
+that the described work interval ended. It does not by itself produce a `completed`, `executed`,
+or `succeeded` lifecycle state.
+
+## DecisionOutcome foundation
+
+`DecisionOutcome` is an immutable factual result and validation record with these exact
+implemented fields:
+
+```text
+id
+recorded_at
+decision_id
+acceptance_id
+action_ids
+result
+summary
+validated_by
+validated_at
+evidence_references
+metrics
+idempotency_key
+tags
+```
+
+Its implemented invariants are:
+
+1. Decision, acceptance, and action IDs are valid UUIDs.
+2. At least one action ID is required; action IDs are ordered and unique.
+3. `result` is exactly `succeeded`, `failed`, `partial`, or `unknown`.
+4. `summary`, `validated_by`, and `idempotency_key` are trimmed and non-blank.
+5. `recorded_at` and `validated_at` are timezone-aware and normalized to UTC.
+6. Metrics contain at most 100 scalar `int | float | str | bool` values.
+7. Metric keys are trimmed, non-blank, at most 64 characters, and case-insensitively unique.
+8. Float metrics are finite, string metrics are bounded to 1000 characters, and nested values are
+   rejected.
+9. The metric mapping is immutable and serialized in deterministic key order.
+10. Tags and evidence use the existing normalization and immutable `EvidenceReference` rules.
+11. The model is immutable and has no mutable lifecycle status.
+
+One Decision may have multiple outcomes. Each outcome appends factual history and may link one or
+more actions; no outcome replaces or mutates an earlier record. An outcome does not mean review,
+Experience, Knowledge, Playbook change, or automatic learning occurred.

 ## Persistence

@@ -360,6 +416,21 @@ under `NeuralPaths.DECISION_ACTIONS`, and Brain initialization creates that dire
 through validation, and malformed stored data fails visibly. The adapter performs no migration,
 ingestion, or command execution.

+The persistence-focused `DecisionOutcomeRepository` also implements only:
+
+```text
+save()
+load_all()
+get_by_id()
+```
+
+It has no relation, idempotency, latest-outcome, summary, or lifecycle query methods.
+`JsonDecisionOutcomeRepository` stores one deterministic JSON file per outcome under
+`NeuralPaths.DECISION_OUTCOMES`, and Brain initialization creates that directory. Complete records
+and immutable scalar metrics round-trip through domain validation; malformed data fails visibly.
+The adapter performs no relation filtering, lifecycle projection, review, learning, migration, or
+ingestion.
+
 ## Application service

 `DecisionService` implements:
@@ -514,6 +585,54 @@ EvidenceReference.captured_at
 `list_for_decision()` validates the Decision, filters `load_all()` in the application layer, and
 preserves repository order. `show()` raises an explicit action-not-found error.

+### DecisionOutcomeService
+
+`DecisionOutcomeService` implements:
+
+```text
+add()
+list_for_decision()
+show()
+summary_for_decision()
+```
+
+`add()` validates Decision existence, acceptance existence and ownership, at least one unique
+action, and every action's Decision and acceptance relations. `validated_at` cannot precede the
+earliest linked action start. Only after relation validation does the service construct and save
+the immutable outcome. It mutates no related record and creates no Review or learning artifact.
+
+Outcome idempotency is scoped by:
+
+```text
+(decision_id, "decision_outcome", idempotency_key)
+```
+
+```text
+same scoped key + equivalent semantic payload
+→ return existing DecisionOutcome
+
+same scoped key + different semantic payload
+→ visible conflict, no write
+
+different key
+→ another outcome may be recorded
+```
+
+Semantic equivalence excludes `DecisionOutcome.id`, `DecisionOutcome.recorded_at`, and embedded
+`EvidenceReference.captured_at`. It includes the linked relations, result, validation data,
+metrics, and other caller-supplied semantic fields.
+
+`list_for_decision()` validates the Decision, filters `load_all()` in the application layer, and
+preserves repository order so the complete multiple-outcome history remains visible. `show()`
+raises an explicit outcome-not-found error.
+
+`DecisionOutcomeSummary` is an immutable, non-persisted application read model returned by
+`summary_for_decision()`. It reports outcome count, latest result and validation time, distinct
+linked-action count, counts for each result value, and success/failure presence. Summary derivation
+validates every persisted outcome-to-acceptance/action relation. Latest selection is deterministic
+by `(validated_at, outcome.id)` and never depends on repository order. The summary is derived on
+demand and is neither persisted nor cached.
+
 ### Canonical DecisionLifecycleService

 `DecisionLifecycleService` is the only canonical owner of the current lifecycle projection. It
@@ -523,6 +642,7 @@ depends on:
 DecisionRepository
 DecisionAcceptanceRepository
 DecisionActionRepository
+DecisionOutcomeRepository
 ```

 It derives exactly:
@@ -536,22 +656,26 @@ Decision exists, one valid acceptance, no action

 Decision exists, one valid acceptance, at least one valid action
 → in_progress
-```

-No mutable status is written and no generic event stream exists. Repository order does not define
-state; valid semantic relations do. Multiple persisted acceptances fail visibly, as does an action
-linked to a wrong or missing acceptance. Multiple valid actions still derive `in_progress`.
+latest valid outcome has result succeeded
+→ succeeded

-These states are explicitly unavailable:
+latest valid outcome has result failed
+→ failed

-```text
-executed
-completed
-succeeded
-failed
-reviewed
+latest valid outcome has result partial
+→ partial
+
+latest valid outcome has result unknown
+→ outcome_unknown
 ```

+No mutable status is written and no generic event stream exists. The latest outcome is selected by
+`(validated_at, outcome.id)`, never repository order. Multiple persisted acceptances fail visibly,
+as do invalid action or outcome relations. Multiple valid actions with no outcome derive
+`in_progress`; multiple outcomes retain history while the latest valid one drives the projection.
+There is no generic `executed`, `completed`, `resolved`, or `reviewed` state.
+
 ## Container

 The composition root constructs and connects:
@@ -565,6 +689,8 @@ DecisionAcceptanceService
 JsonDecisionActionRepository
 JsonPlaybookRunRepository
 DecisionActionService
+JsonDecisionOutcomeRepository
+DecisionOutcomeService
 DecisionLifecycleService
 ```

@@ -573,13 +699,14 @@ DecisionLifecycleService
 repositories or own validation, relation checks, persistence, eligibility, or idempotency policy.

 `DecisionActionService` receives `JsonDecisionActionRepository`, `JsonDecisionRepository`,
-`JsonDecisionAcceptanceRepository`, and `JsonPlaybookRunRepository`. `DecisionLifecycleService`
-receives the Decision, acceptance, and action repositories. CLI handlers resolve both services
-from the container and construct no repositories.
+`JsonDecisionAcceptanceRepository`, and `JsonPlaybookRunRepository`. `DecisionOutcomeService`
+receives `JsonDecisionOutcomeRepository` plus Decision, acceptance, and action repositories.
+`DecisionLifecycleService` receives the Decision, acceptance, action, and outcome repositories.
+CLI handlers resolve services from the container and construct no repositories.

 ## Implemented CLI

-These commands exist at commit `1964356`:
+These commands exist at commit `5befd7c`:

 ```text
 neural decision add
@@ -590,6 +717,10 @@ neural decision acceptance-history DECISION_UUID
 neural decision action add DECISION_UUID
 neural decision action-history DECISION_UUID
 neural decision action-show ACTION_UUID
+neural decision outcome add DECISION_UUID
+neural decision outcome-history DECISION_UUID
+neural decision outcome-show OUTCOME_UUID
+neural decision outcome-summary DECISION_UUID
 neural decision state DECISION_UUID
 ```

@@ -701,7 +832,7 @@ Reason

 An existing Decision with no acceptance produces a controlled empty state.

-### Decision action and state commands
+### Decision action commands

 `neural decision action add DECISION_UUID` requires:

@@ -742,19 +873,49 @@ Summary
 An existing Decision with no actions produces a controlled empty state.
 `neural decision action-show ACTION_UUID` renders every DecisionAction field.

+### Decision outcome and state commands
+
+`neural decision outcome add DECISION_UUID` requires:
+
+```text
+--acceptance-id
+--action-id (one or more)
+--result
+--summary
+--validated-by
+--validated-at
+--idempotency-key
+```
+
+Repeated `--evidence`, `--metric KEY=VALUE`, and `--tag` values are optional. Result accepts only
+`succeeded`, `failed`, `partial`, or `unknown`. Metrics parse unambiguous booleans, integers, and
+finite floats; other values remain strings and domain validation enforces the scalar bounds. The
+CLI reads no evidence locator and executes no referenced command.
+
+`neural decision outcome-history DECISION_UUID` renders all matching outcomes in repository order,
+including their result, validation time, linked action IDs, validator, and summary. An existing
+Decision with no outcomes produces a controlled empty state. `outcome-show OUTCOME_UUID` renders
+every stored field, including evidence, metrics, idempotency key, and tags.
+
+`neural decision outcome-summary DECISION_UUID` renders the derived count, deterministic latest
+result/time, distinct linked-action count, counts by result, and success/failure presence. It does
+not persist the summary.
+
 `neural decision state DECISION_UUID` renders exactly one of:

 ```text
 proposed
 accepted
 in_progress
+succeeded
+failed
+partial
+outcome_unknown
 ```

-It renders no later lifecycle state.
-
-## Future lifecycle boundary
+## Review and learning boundary

-The accepted future record family remains deliberately separate:
+The record family remains deliberately separate:

 ```text
 Decision
@@ -767,13 +928,13 @@ Decision
 - `Decision` is the implemented proposed choice.
 - `DecisionAcceptance` is the implemented explicit authorization for possible future execution.
 - `DecisionAction` is the implemented record of work performed under an accepted Decision.
-- `DecisionOutcome` would record factual results and validation evidence.
+- `DecisionOutcome` is the implemented factual result and validation evidence record.
 - `DecisionReview` would assess outcomes and hold candidate lessons.

-Only the first three records exist. Future records must remain immutable semantic records rather
-than fields on a mutable Decision or a duplicate generic event stream. A proposed option is not an
-acceptance, acceptance is not execution, an outcome is not an Experience, and candidate lessons
-are not automatically Knowledge or a Playbook change.
+The first four records exist; DecisionReview does not. Records remain immutable semantic records
+rather than fields on a mutable Decision or a duplicate generic event stream. A proposed option is
+not an acceptance, acceptance is not execution, an outcome is not a review or Experience, and
+candidate lessons are not automatically Knowledge or a Playbook change.

 The currently derivable projection is only:

@@ -786,10 +947,23 @@ Decision with one valid acceptance

 Decision with one valid acceptance and at least one valid action
 → in_progress
+
+latest valid outcome succeeded
+→ succeeded
+
+latest valid outcome failed
+→ failed
+
+latest valid outcome partial
+→ partial
+
+latest valid outcome unknown
+→ outcome_unknown
 ```

-There is no executed, completed, succeeded, failed, or reviewed state. The minimal lifecycle
-projection is canonical, but there is no generic full lifecycle replay service.
+The lifecycle projection uses the latest valid outcome selected by `(validated_at, outcome.id)`.
+There is no generic executed, completed, resolved, or reviewed state and no generic full lifecycle
+event replay service.

 ## Relationship to the domain chain

@@ -801,7 +975,7 @@ Observation
 → Decision
 → DecisionAcceptance
 → DecisionAction
-→ future DecisionOutcome
+→ DecisionOutcome
 → future DecisionReview
 → explicitly created Experience
 → explicitly created Knowledge
@@ -829,18 +1003,18 @@ prompt
 → post-work lesson
 ```

-Commit `1964356` does not capture or ingest those events. Automatic candidates and manual
-confirmation remain future concepts; no automatic persistence, ingestion, or learning exists.
+Commit `5befd7c` does not capture or ingest those events automatically. Automatic candidates and
+manual confirmation remain future concepts; no automatic persistence, ingestion, or learning
+exists.

 Consigliere also remains future-only. It may later advise. No Consigliere integration exists, and
 no recommendation can directly mutate NeuralEngine or authorize a durable record.

 ## Current non-behavior

-Commit `1964356` does not implement:
+Commit `5befd7c` does not implement:

 ```text
-DecisionOutcome
 DecisionReview
 execution engine
 command/shell execution
@@ -850,7 +1024,7 @@ reversal
 reopening
 cancellation
 replacement
-executed/completed/succeeded/failed/reviewed states
+executed/completed/resolved/reviewed states
 file ingestion
 git ingestion
 automatic Observation creation
@@ -863,17 +1037,19 @@ Consigliere integration

 It also does not execute commands referenced by evidence, open locators, automatically accept
 Decisions, materialize Playbook revisions, or infer outcomes from `completed_at`. Explicit user
-requests are required to create Decision, DecisionAcceptance, or DecisionAction records.
+requests are required to create Decision, DecisionAcceptance, DecisionAction, or DecisionOutcome
+records.

 ## Recommended next milestone

 The one recommended next controlled slice is:

 ```text
-DecisionOutcome foundation
+DecisionReview foundation
 ```

-It must remain separate from `DecisionReview`.
+It must remain separate from automatic Experience, Knowledge, Playbook, PlaybookEvaluation, or
+EvolutionProposal creation.

 ## Handbook synchronization policy

@@ -940,15 +1116,16 @@ Confirmed example:

 ## Complementary Decision Learning chain

-The implemented Decision, DecisionAcceptance, and DecisionAction foundations record a bounded
-proposed choice, explicit authorization, and work performed after Observation context:
+The implemented Decision, DecisionAcceptance, DecisionAction, and DecisionOutcome foundations
+record a bounded proposed choice, explicit authorization, work performed, and factual results
+after Observation context:

 ```text
 Observation
 → Decision
 → DecisionAcceptance
 → DecisionAction
-→ future DecisionOutcome
+→ DecisionOutcome
 → future DecisionReview
 → Experience
 → Knowledge
@@ -956,9 +1133,10 @@ Observation

 This is a complementary provenance path, not a replacement for the canonical domain chain.
 DecisionOutcome is factual; Experience is interpreted; Knowledge is generalized; Playbook remains
-a separately created repeatable procedure. Decision, DecisionAcceptance, DecisionAction, and their
-embedded EvidenceReference values exist at source commit `1964356`; no Outcome, Review, or later
-transition in this path is automatic.
+a separately created repeatable procedure. DecisionOutcome may have multiple immutable records per
+Decision and does not automatically create a Review or learning artifact. Decision,
+DecisionAcceptance, DecisionAction, DecisionOutcome, and their embedded EvidenceReference values
+exist at source commit `5befd7c`; no Review or later transition in this path is automatic.

 ---

@@ -1349,6 +1527,71 @@ There is currently:

 ---

+# DecisionOutcome
+
+## Responsibility
+
+A DecisionOutcome is an immutable factual result and validation record for one or more actions
+performed under one accepted Decision. It records what happened; it does not interpret lessons or
+create learning.
+
+## Implemented fields
+
+- `id`
+- `recorded_at`
+- `decision_id`
+- `acceptance_id`
+- ordered unique `action_ids`
+- `result`
+- `summary`
+- `validated_by`
+- `validated_at`
+- embedded `evidence_references`
+- immutable scalar `metrics`
+- `idempotency_key`
+- normalized `tags`
+
+The result values are exactly `succeeded`, `failed`, `partial`, and `unknown`. A Decision can have
+multiple outcomes; new factual results append history instead of replacing an earlier outcome.
+
+## Invariants and relations
+
+- The Decision and DecisionAcceptance must exist, and the acceptance must belong to the Decision.
+- At least one action is required. Action IDs are ordered and unique.
+- Every action must exist and belong to the same Decision and acceptance.
+- `validated_at` cannot precede the earliest linked action start.
+- Required text is trimmed and non-blank; timestamps are timezone-aware and normalized to UTC.
+- The record and exposed metrics mapping are immutable.
+
+Metrics contain at most 100 `str -> int | float | str | bool` entries. Keys are trimmed,
+non-blank, at most 64 characters, and case-insensitively unique. Floats must be finite, strings are
+bounded to 1000 characters, and nested values are rejected. JSON serialization sorts metric keys.
+
+## History, idempotency, and summary
+
+Idempotency is scoped by `(decision_id, "decision_outcome", idempotency_key)`. Equivalent replay
+returns the existing outcome. Reusing the same scoped key with a different semantic payload fails
+without a write. Generated outcome ID, recording time, and evidence capture times are excluded
+from semantic equivalence; a different key may append another outcome for the same Decision.
+
+`DecisionOutcomeSummary` is an immutable, non-persisted read model derived on demand. It reports
+outcome count, latest result and validation time, distinct linked-action count, counts for every
+result value, and success/failure presence. Summary derivation validates stored acceptance/action
+relations. Latest selection is deterministic by `(validated_at, outcome.id)`, never repository
+order.
+
+## Lifecycle and learning boundary
+
+`DecisionLifecycleService` maps the latest valid outcome to `succeeded`, `failed`, `partial`, or
+`outcome_unknown`. Earlier outcomes remain available as history. No `completed` or `resolved`
+lifecycle state exists.
+
+DecisionReview is not implemented. Recording an outcome does not review a Decision and does not
+create Observation, Experience, Knowledge, Playbook, PlaybookEvaluation, EvolutionProposal, or
+automatic learning. The next milestone is the separate DecisionReview foundation.
+
+---
+
 # Application Services

 ## Responsibility
@@ -1452,7 +1695,7 @@ acceptance both fail visibly without writing.
 and preserves repository order. `show()` owns explicit acceptance not-found behavior. Acceptance
 does not mutate Decision or create actions, outcomes, reviews, execution, or learning.

-## Decision action and lifecycle ownership
+## Decision action ownership

 `DecisionActionService.add()` validates the Decision, matching acceptance, and optional
 PlaybookRun before creating an immutable action. It uses
@@ -1464,10 +1707,28 @@ multiple distinct actions, and mutates no related record. PlaybookRun and Playbo
 `show()` owns explicit action-not-found behavior. The service creates no Outcome, Review, or
 learning record.

+## Decision outcome and lifecycle ownership
+
+`DecisionOutcomeService.add()` validates the Decision, matching acceptance, one or more unique
+actions, each action's Decision and acceptance relations, and validation time against the earliest
+linked action start before constructing or saving an immutable outcome. It uses
+`(decision_id, "decision_outcome", idempotency_key)` for application-layer idempotency. Equivalent
+replay returns the existing outcome; conflicting reuse fails without a write; another key may
+append another outcome for the same Decision.
+
+`list_for_decision()` validates the Decision and returns all matching outcomes in repository order.
+`show()` owns explicit outcome-not-found behavior. `summary_for_decision()` validates persisted
+outcome relations and returns an immutable, non-persisted `DecisionOutcomeSummary` with outcome
+count, deterministic latest result/time, distinct linked-action count, counts by result, and
+success/failure presence. Latest selection uses `(validated_at, outcome.id)` rather than repository
+order.
+
 `DecisionLifecycleService` is the only canonical projection owner. It validates persisted
-Decision/acceptance/action relations and derives only `proposed`, `accepted`, or `in_progress`.
-It writes no status, ignores repository order for state, and exposes no completed, succeeded,
-failed, or reviewed state.
+Decision/acceptance/action/outcome relations and derives exactly `proposed`, `accepted`,
+`in_progress`, `succeeded`, `failed`, `partial`, or `outcome_unknown`. When outcomes exist, the
+latest is selected by `(validated_at, outcome.id)`. It writes no status and exposes no generic
+`completed`, `resolved`, or reviewed state. Outcome creation and projection create no Review or
+learning record.

 ---

@@ -1588,6 +1849,11 @@ Decision relation filtering, eligibility, and idempotency belong to
 Relation validation, Decision filtering, idempotency, and lifecycle projection belong to
 application services; no relation, idempotency, or lifecycle query method is part of the port.

+`DecisionOutcomeRepository` is limited to `save()`, `load_all()`, and `get_by_id()`.
+Decision filtering, acceptance/action relation validation, multiple-outcome history, idempotency,
+summary derivation, and lifecycle projection belong to application services; no relation,
+idempotency, summary, latest-outcome, or lifecycle query method is part of the port.
+
 ## Repository return types

 Prefer:
@@ -1714,6 +1980,16 @@ DecisionAction records round-trip through domain validation. `load_all()` sorts
 deterministic order, and malformed data surfaces validation errors. The adapter performs no
 relation filtering, lifecycle projection, migration, ingestion, or command execution.

+## Decision outcome adapter
+
+`JsonDecisionOutcomeRepository` implements `DecisionOutcomeRepository` and stores one JSON file
+per outcome under `NeuralPaths.DECISION_OUTCOMES`; Brain initialization creates the directory.
+Complete DecisionOutcome records, including immutable scalar metrics, round-trip through domain
+validation. JSON object keys and metric keys are serialized deterministically, `load_all()` sorts
+file names, and malformed data surfaces validation errors. The adapter performs no relation
+validation or filtering, latest-outcome selection, summary or lifecycle projection, idempotency
+decision, migration, ingestion, review, or learning.
+
 ---

 # Dependency Injection and Container
@@ -1777,11 +2053,15 @@ The acceptance foundation is wired through `Container.decision_acceptance_reposi
 `JsonDecisionAcceptanceRepository` and `JsonDecisionRepository` to
 `DecisionAcceptanceService`; acceptance CLI handlers construct no repositories.

-The action foundation is wired through `Container.decision_action_repository()`,
-`Container.decision_action_service()`, and `Container.decision_lifecycle_service()`. The action
-service receives JSON action, Decision, acceptance, and PlaybookRun repositories. The lifecycle
-service receives Decision, acceptance, and action repositories. CLI handlers resolve services and
-construct no repositories.
+The action foundation is wired through `Container.decision_action_repository()` and
+`Container.decision_action_service()`. The action service receives JSON action, Decision,
+acceptance, and PlaybookRun repositories.
+
+The outcome foundation is wired through `Container.decision_outcome_repository()` and
+`Container.decision_outcome_service()`. The outcome service receives JSON outcome, Decision,
+acceptance, and action repositories. `Container.decision_lifecycle_service()` receives those same
+four repository categories so it can validate relations and derive the canonical state. Decision
+action, outcome, summary, and state CLI handlers resolve services and construct no repositories.

 ---

@@ -2373,10 +2653,10 @@ Status: Accepted
 ## Decision

 Development decision tracking uses implemented separate immutable `Decision`,
-`DecisionAcceptance`, and `DecisionAction` records with embedded immutable `EvidenceReference`
-values. `DecisionOutcome` and `DecisionReview` remain separate future-only records. Lifecycle state
-is derived from semantic records, not stored as mutable status or duplicated in a generic event
-stream.
+`DecisionAcceptance`, `DecisionAction`, and `DecisionOutcome` records with embedded immutable
+`EvidenceReference` values. `DecisionReview` remains a separate future-only record. Lifecycle
+state is derived from semantic records, not stored as mutable status or duplicated in a generic
+event stream.

 Decision tracking complements the existing Observation-to-Playbook chain. Evidence uses bounded
 embedded references, durable writes require explicit authority, and Consigliere remains a future
@@ -2390,11 +2670,14 @@ advisory layer rather than authoritative storage.
   idempotency checks; repository ports remain persistence-focused.
 - No automatic ingestion, persistence, learning, Playbook evolution, or Consigliere integration is
   implied.
-- Source commit `1964356` implements Decision proposal, acceptance, action recording, and their
-  CLI plus the canonical `DecisionLifecycleService`.
-- Only proposed, accepted, and in-progress states can currently be derived. Action completion time
-  does not imply lifecycle completion, success, failure, outcome, or review.
+- Source commit `5befd7c` implements Decision proposal, acceptance, action and outcome recording,
+  outcome history/summary, their CLI, and the canonical `DecisionLifecycleService`.
+- The canonical states are exactly proposed, accepted, in-progress, succeeded, failed, partial,
+  and outcome-unknown. Latest outcome selection uses validation time and outcome UUID, not
+  repository order. No generic completed, resolved, or reviewed state exists.
 - Acceptance is authorization for possible future execution; it is not execution or reversal and
   creates no later lifecycle or learning record.
-- The one recommended next milestone is `DecisionOutcome foundation`, kept separate from
-  DecisionReview.
+- Multiple immutable outcomes may be appended for one Decision. Outcome creation is factual only
+  and creates no review or learning record.
+- The one recommended next milestone is `DecisionReview foundation`, kept separate from automatic
+  learning and downstream Experience, Knowledge, or Playbook creation.
diff --git a/src/neuralengine_handbook/builder.py b/src/neuralengine_handbook/builder.py
index 7aca667..1826247 100644
--- a/src/neuralengine_handbook/builder.py
+++ b/src/neuralengine_handbook/builder.py
@@ -99,6 +99,7 @@ def build(root: Path) -> list[Path]:
         paths.handbook / "domain/playbook-revision.md",
         paths.handbook / "domain/playbook-revision-activation.md",
         paths.handbook / "domain/playbook-revision-application.md",
+        paths.handbook / "domain/decision-outcome.md",
     ]

     application_files = [
diff --git a/tests/test_builder.py b/tests/test_builder.py
index 6824cb5..a3303bf 100644
--- a/tests/test_builder.py
+++ b/tests/test_builder.py
@@ -39,7 +39,7 @@ def test_generated_skill_contains_neuralengine_rules(tmp_path: Path) -> None:
     assert "Application CLI commands do not" in skill
     assert "Playbook content mutation" in skill
     assert "# Decision Learning Architecture" in skill
-    assert "These commands exist at commit `1964356`" in skill
+    assert "These commands exist at commit `5befd7c`" in skill
     assert "neural decision add" in skill
     assert "neural decision list" in skill
     assert "neural decision show DECISION_UUID" in skill
@@ -48,11 +48,15 @@ def test_generated_skill_contains_neuralengine_rules(tmp_path: Path) -> None:
     assert "neural decision action add DECISION_UUID" in skill
     assert "neural decision action-history DECISION_UUID" in skill
     assert "neural decision action-show ACTION_UUID" in skill
+    assert "neural decision outcome add DECISION_UUID" in skill
+    assert "neural decision outcome-history DECISION_UUID" in skill
+    assert "neural decision outcome-show OUTCOME_UUID" in skill
+    assert "neural decision outcome-summary DECISION_UUID" in skill
     assert "neural decision state DECISION_UUID" in skill
     assert "DecisionOutcome foundation" in skill
-    assert "future-only records" in skill
+    assert "remains future-only" in skill
     assert "No Consigliere integration exists" in skill
-    assert "no automatic persistence, ingestion, or learning exists" in skill
+    assert "no automatic persistence, ingestion, or learning" in skill
     assert "same key + equivalent semantic payload" in skill
     assert '(decision_id, "decision_acceptance", idempotency_key)' in skill
     assert '(decision_id, "decision_action", idempotency_key)' in skill
@@ -78,6 +82,7 @@ def test_handbook_contains_all_domain_entities(tmp_path: Path) -> None:
         "PlaybookRevision",
         "PlaybookRevisionActivation",
         "PlaybookRevisionApplication",
+        "DecisionOutcome",
     ]
     for entity in entities:
         assert f"# {entity}" in handbook
@@ -109,12 +114,14 @@ def test_decision_engine_contains_agent_and_repository_rules(tmp_path: Path) ->
     assert "ADR-0008" in decision_engine


-def test_handbook_contains_decision_action_lifecycle_and_future_boundaries(tmp_path: Path) -> None:
+def test_handbook_contains_decision_outcome_lifecycle_and_future_boundaries(
+    tmp_path: Path,
+) -> None:
     work_root = _copy_repo(tmp_path)
     build(work_root)

     handbook = (work_root / "outputs/generated/HANDBOOK.md").read_text(encoding="utf-8")
-    assert "NeuralEngine source commit `1964356` implements" in handbook
+    assert "NeuralEngine source commit `5befd7c` implements" in handbook
     assert "neural decision add" in handbook
     assert "neural decision list" in handbook
     assert "neural decision show DECISION_UUID" in handbook
@@ -123,6 +130,10 @@ def test_handbook_contains_decision_action_lifecycle_and_future_boundaries(tmp_p
     assert "neural decision action add DECISION_UUID" in handbook
     assert "neural decision action-history DECISION_UUID" in handbook
     assert "neural decision action-show ACTION_UUID" in handbook
+    assert "neural decision outcome add DECISION_UUID" in handbook
+    assert "neural decision outcome-history DECISION_UUID" in handbook
+    assert "neural decision outcome-show OUTCOME_UUID" in handbook
+    assert "neural decision outcome-summary DECISION_UUID" in handbook
     assert "neural decision state DECISION_UUID" in handbook
     assert "DecisionAcceptance" in handbook
     assert "DecisionAcceptance foundation" in handbook
@@ -130,13 +141,12 @@ def test_handbook_contains_decision_action_lifecycle_and_future_boundaries(tmp_p
     assert "Decision without acceptance" in handbook
     assert "Decision with one valid acceptance" in handbook
     assert "DecisionReview" in handbook
-    assert "future-only records" in handbook
+    assert "remains future-only" in handbook
     assert '(project_key, "decision", idempotency_key)' in handbook
     assert "same key + different semantic payload" in handbook
     assert '(decision_id, "decision_acceptance", idempotency_key)' in handbook
     assert "different key + Decision already accepted" in handbook
     assert "There is no Evidence repository, service, or CLI" in handbook
-    assert "There is no executed, completed, succeeded, failed, or reviewed state" in handbook
     assert "DecisionAction" in handbook
     assert "## DecisionAction foundation" in handbook
     assert "DecisionLifecycleService` is the only canonical owner" in handbook
@@ -146,11 +156,21 @@ def test_handbook_contains_decision_action_lifecycle_and_future_boundaries(tmp_p
     assert "another action may be recorded" in handbook
     assert "PlaybookRun and Playbook currently expose no project_key" in handbook
     assert "DecisionOutcome" in handbook
-    assert "future-only records" in handbook
     assert "DecisionOutcome foundation" in handbook
+    assert "# DecisionOutcome" in handbook
+    assert "`succeeded`, `failed`, `partial`, and `unknown`" in handbook
+    assert '(decision_id, "decision_outcome", idempotency_key)' in handbook
+    assert "another outcome may be recorded" in handbook
+    assert "DecisionOutcomeSummary" in handbook
+    assert "(validated_at, outcome.id)" in handbook
+    assert "outcome_unknown" in handbook
+    assert "DecisionReview foundation" in handbook
     assert "No Consigliere integration exists" in handbook
-    assert "no automatic persistence, ingestion, or learning exists" in handbook
+    assert "no automatic persistence, ingestion, or learning" in handbook
     assert "ADR-0008" in handbook
+    assert "partially_successful" not in handbook
+    assert "inconclusive" not in handbook
+    assert "DecisionOutcome` and `DecisionReview` remain future-only" not in handbook


 def test_application_architecture_contains_core_boundaries(tmp_path: Path) -> None:
````

### Full diffs for new task files

Exact command for the new Handbook source:

```text
git diff --no-index -- /dev/null handbook/domain/decision-outcome.md
```

Complete output (exit status 1 is the normal `git diff --no-index` result when differences exist):

```diff
diff --git a/handbook/domain/decision-outcome.md b/handbook/domain/decision-outcome.md
new file mode 100644
index 0000000..e360021
--- /dev/null
+++ b/handbook/domain/decision-outcome.md
@@ -0,0 +1,62 @@
+# DecisionOutcome
+
+## Responsibility
+
+A DecisionOutcome is an immutable factual result and validation record for one or more actions
+performed under one accepted Decision. It records what happened; it does not interpret lessons or
+create learning.
+
+## Implemented fields
+
+- `id`
+- `recorded_at`
+- `decision_id`
+- `acceptance_id`
+- ordered unique `action_ids`
+- `result`
+- `summary`
+- `validated_by`
+- `validated_at`
+- embedded `evidence_references`
+- immutable scalar `metrics`
+- `idempotency_key`
+- normalized `tags`
+
+The result values are exactly `succeeded`, `failed`, `partial`, and `unknown`. A Decision can have
+multiple outcomes; new factual results append history instead of replacing an earlier outcome.
+
+## Invariants and relations
+
+- The Decision and DecisionAcceptance must exist, and the acceptance must belong to the Decision.
+- At least one action is required. Action IDs are ordered and unique.
+- Every action must exist and belong to the same Decision and acceptance.
+- `validated_at` cannot precede the earliest linked action start.
+- Required text is trimmed and non-blank; timestamps are timezone-aware and normalized to UTC.
+- The record and exposed metrics mapping are immutable.
+
+Metrics contain at most 100 `str -> int | float | str | bool` entries. Keys are trimmed,
+non-blank, at most 64 characters, and case-insensitively unique. Floats must be finite, strings are
+bounded to 1000 characters, and nested values are rejected. JSON serialization sorts metric keys.
+
+## History, idempotency, and summary
+
+Idempotency is scoped by `(decision_id, "decision_outcome", idempotency_key)`. Equivalent replay
+returns the existing outcome. Reusing the same scoped key with a different semantic payload fails
+without a write. Generated outcome ID, recording time, and evidence capture times are excluded
+from semantic equivalence; a different key may append another outcome for the same Decision.
+
+`DecisionOutcomeSummary` is an immutable, non-persisted read model derived on demand. It reports
+outcome count, latest result and validation time, distinct linked-action count, counts for every
+result value, and success/failure presence. Summary derivation validates stored acceptance/action
+relations. Latest selection is deterministic by `(validated_at, outcome.id)`, never repository
+order.
+
+## Lifecycle and learning boundary
+
+`DecisionLifecycleService` maps the latest valid outcome to `succeeded`, `failed`, `partial`, or
+`outcome_unknown`. Earlier outcomes remain available as history. No `completed` or `resolved`
+lifecycle state exists.
+
+DecisionReview is not implemented. Recording an outcome does not review a Decision and does not
+create Observation, Experience, Knowledge, Playbook, PlaybookEvaluation, EvolutionProposal, or
+automatic learning. The next milestone is the separate DecisionReview foundation.
```

The other new task file is this review:
`.agent-work/reviews/review-sync-decision-outcome-milestone.md`. Embedding that file's own complete
`/dev/null` diff inside itself has no finite stable representation: adding the embedded diff
changes the file and therefore changes the diff recursively. The file is nevertheless included
explicitly in the complete stat and commit list below, and its full final content is the review
artifact itself.

### Complete diff stat including new task files

The tracked portion is the exact `git diff --stat` result. The two untracked task files are added
as `/dev/null` creations; pre-existing untracked files are excluded.

```text
 handbook/application/services.md                   |  26 +-
 handbook/architecture/architecture.md              |  26 +-
 handbook/architecture/decision-learning.md         | 262 +++++++++---
 handbook/container/dependency-injection.md         |  14 +-
 .../ADR-0008-decision-learning-boundary.md         |  23 +-
 handbook/domain/domain-chain.md                    |  14 +-
 handbook/infrastructure/repositories.md            |  10 +
 handbook/ports/repository-ports.md                 |   5 +
 outputs/claude-skill/SKILL.md                      | 302 +++++++++++---
 outputs/generated/AGENTS.generated.md              |  26 +-
 outputs/generated/APPLICATION_ARCHITECTURE.md      |  55 ++-
 outputs/generated/DECISION_ENGINE.md               | 285 ++++++++++---
 outputs/generated/HANDBOOK.md                      | 445 +++++++++++++++++----
 src/neuralengine_handbook/builder.py               |   1 +
 tests/test_builder.py                              |  38 +-
 handbook/domain/decision-outcome.md                |  62 +
 .agent-work/reviews/review-sync-decision-outcome-milestone.md | 3085 +
 17 files changed, 4371 insertions(+), 308 deletions(-)
```

### Exact commit scope

Files belonging to this task and intended for the commit:

- `.agent-work/reviews/review-sync-decision-outcome-milestone.md`
- `handbook/application/services.md`
- `handbook/architecture/architecture.md`
- `handbook/architecture/decision-learning.md`
- `handbook/container/dependency-injection.md`
- `handbook/decisions/ADR-0008-decision-learning-boundary.md`
- `handbook/domain/decision-outcome.md`
- `handbook/domain/domain-chain.md`
- `handbook/infrastructure/repositories.md`
- `handbook/ports/repository-ports.md`
- `outputs/claude-skill/SKILL.md`
- `outputs/generated/AGENTS.generated.md`
- `outputs/generated/APPLICATION_ARCHITECTURE.md`
- `outputs/generated/DECISION_ENGINE.md`
- `outputs/generated/HANDBOOK.md`
- `src/neuralengine_handbook/builder.py`
- `tests/test_builder.py`

Pre-existing untracked elements that do not belong to this task and must remain outside the commit:

- `.directory`
- `.agent-work/prompts/codex-implement-decision-foundation.md`
- `.agent-work/prompts/codex-sync-decision-acceptance-foundation-milestone.md`
- `.agent-work/prompts/codex-sync-decision-action-lifecycle-foundation-milestone.md`
- `.agent-work/prompts/codex-sync-decision-foundation-milestone.md`
- `.agent-work/prompts/codex-sync-decision-learning-design-milestone.md`
- `.agent-work/prompts/codex-sync-decision-outcome-handbook.md`
- `.agent-work/prompts/codex-sync-neuralengine-application-foundation-milestone.md`
- `.agent-work/reviews/review-sync-decision-acceptance-foundation-milestone.md`
- `.agent-work/reviews/review-sync-decision-action-lifecycle-foundation-milestone.md`
- `.agent-work/reviews/review-sync-decision-foundation-milestone.md`
- `.agent-work/reviews/review-sync-decision-learning-design-milestone.md`
- `.agent-work/reviews/review-sync-neuralengine-application-foundation-milestone.md`

### Final diff check

Exact command:

```text
git diff --check
```

Complete output:

```text
# no output; exit 0
```

### Final Git status

Exact command:

```text
git status --short
```

Complete output:

```text
 M handbook/application/services.md
 M handbook/architecture/architecture.md
 M handbook/architecture/decision-learning.md
 M handbook/container/dependency-injection.md
 M handbook/decisions/ADR-0008-decision-learning-boundary.md
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
?? .agent-work/
?? .directory
?? handbook/domain/decision-outcome.md
```

No commit or push was performed. The generated `SKILL.md` was not copied to NeuralEngine.
