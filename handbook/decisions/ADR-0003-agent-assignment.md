# ADR-0003: Agent assignment policy

Status: Accepted

## Decision

Codex GPT-5.5 medium owns architectural and feature work.

DeepSeek is restricted to small, controlled, post-review fixes, normally one to three files.

## Consequences

- New features are never delegated to DeepSeek.
- Repository, service, container, CLI, schema, public behavior, validation-order, and provenance changes belong to Codex.
- DeepSeek prompts require an explicit scope guard.
