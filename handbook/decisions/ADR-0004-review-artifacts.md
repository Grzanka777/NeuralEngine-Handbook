# ADR-0004: Mandatory prompt and review artifacts

Status: Accepted

## Decision

Every agent task must have:

- a prompt in `.agent-work/prompts/`,
- a review in `.agent-work/reviews/`.

The review must contain validation output, diff stat, diff check, git status, and full diff.

## Consequences

- Agent work is inspectable before commit.
- Success claims require evidence.
- Agents do not commit or push.
