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
