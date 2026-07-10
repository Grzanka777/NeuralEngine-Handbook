# Codex Task: <task name>

Read `AGENTS.md` and `.agent-work/project-state.md` first.

## Objective

<describe the required outcome>

## Scope

<list exact allowed changes>

## Architectural constraints

- Preserve hexagonal boundaries.
- Keep repositories persistence-focused.
- Keep business logic out of CLI and adapters.
- Do not broaden scope.

## Validation

Run `./scripts/validate.sh`.

## Review artifact

Save the complete review to:

`.agent-work/reviews/<task-name>.md`

The review must contain validation output, diff stat, diff check, git status, and full diff.

Do not commit or push.
