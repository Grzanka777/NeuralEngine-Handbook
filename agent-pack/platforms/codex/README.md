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

## Codex CLI 0.149.0 native capabilities

The following provider-native commands are bounded execution and diagnostic
surfaces. They do not become NeuralEngine authority.

### Optional provider preflight: `codex doctor --json`

`codex doctor --json` emits a redacted machine-readable report that may provide
evidence about Codex installation and runtime provenance, configuration
parsing, app-server state, sandbox and approval policy, provider/network
readiness, local state/database health, and environment or update state.

It is an optional provider-side preflight. A healthy result does not replace
`neural status`, verification of `AGENTS.md` or NeuralEngine skill discovery,
NeuralEngine Brain/provenance checks, or live model/session validation.

### Session browser: `codex agents`

`codex agents` browses agent sessions on the shared local app-server daemon. It
is not a NeuralEngine role registry and does not define or map `builder`,
`reviewer`, `planner`, or `mechanical` responsibilities. It is not a task
delegation, permission-isolation, concurrency, or review-workflow contract.

### Existing-session continuation: `codex queue`

`codex queue --thread <THREAD> --message <TEXT>` queues a message to an
existing session or thread. The observed command surface does not establish
workflow scheduling, dependency handling, retry or cancellation semantics,
ownership, role transitions, review-artifact generation, Brain-write
authorization, or publication authorization.

Queue-based workflow automation remains `HOLD` pending a separate bounded
runtime validation. Do not use it to turn a builder continuation into a
reviewer, authorize Brain writes, or imply staging, commit, push, merge, tag,
release, or publication.

## NeuralEngine authority boundary

`AGENTS.md` remains the project-instruction authority and
`agent-pack/shared/neuralengine.md` remains the semantic authority. The Codex
skill is a controlled projection of that shared contract. `neural status`,
relevance-gated `neural knowledge search/show`, the read-only Brain default,
explicit Brain-write authorization, and separate publication authorization
remain unchanged.

## Limitations

- Codex CLI is the only supported surface in this adapter.
- Codex Desktop discovery parity is not established by this slice.
- Availability of the `neural` executable, `PATH`, Brain access, and runtime
  command behavior must be verified in the target environment.
- Host permissions and approvals remain Codex controls; this adapter grants no
  Brain-write, staging, commit, push, merge, tag, release, or publication
  authority.
