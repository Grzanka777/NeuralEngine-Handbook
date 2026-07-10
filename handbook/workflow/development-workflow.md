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
