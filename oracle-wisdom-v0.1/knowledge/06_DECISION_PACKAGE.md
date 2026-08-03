# Decision Package Contract

## Purpose

Provide one auditable execution recommendation transferable to a project chat, OpenCode or Codex.

## Required fields

Decision, project, normalized task, task class, workflow, agent role, execution profile, platform, runtime model, reasoning, authority/checkpoint, validation, risks/safeguards, artifact and rationale.

## Decision values

- `Proceed`
- `Defer`
- `Reject`
- `Manual execution sufficient`

## Quality rules

- One primary route, not a menu of equivalent choices.
- Alternatives only when the primary route depends on unavailable capacity.
- Model availability is evidence, not assumption.
- Prompt generation follows routing.
- The package must be understandable without hidden reasoning.
