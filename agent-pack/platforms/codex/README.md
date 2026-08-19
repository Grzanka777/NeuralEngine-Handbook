# Codex CLI Platform

**Status:** NeuralEngine thin adapter implemented for Codex CLI only.

This adapter is a controlled projection of
`agent-pack/shared/neuralengine.md`. It does not implement Codex Desktop or
any other provider, and it does not modify NeuralEngine runtime behavior,
Brain persistence, schemas, APIs, or user-global Codex configuration.

## Adapter files

- `AGENTS.md` — minimal project-instruction pointer; merge this pointer into a
  target repository's project instructions without replacing unrelated rules.
- `skills/neuralengine/SKILL.md` — Codex-compatible skill projection with only
  the required `name` and `description` front matter.

The skill body is a controlled copy of the shared contract. Drift validation
requires the body after front matter removal to remain byte-equal to
`agent-pack/shared/neuralengine.md`.

## Manual installation mapping

Installation is explicit and manual, consistent with the Agent Pack
architecture:

```text
skills/neuralengine/SKILL.md
→ <target-repository>/.agents/skills/neuralengine/SKILL.md
```

The `AGENTS.md` content is a pointer to merge into the target repository's
project instructions. This package does not provide an installer, write to
`~/.codex`, or claim Desktop support.

## Limitations

- Codex CLI is the only supported surface in this adapter.
- Codex Desktop discovery parity is not established by this slice.
- Availability of the `neural` executable, `PATH`, Brain access, and runtime
  command behavior must be verified in the target environment.
- Host permissions and approvals remain Codex controls; this adapter grants no
  Brain-write, staging, commit, push, merge, tag, release, or publication
  authority.
