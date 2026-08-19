# Agent Pack Manifest

## Shared-to-platform mapping

| Authoritative source | OpenCode target | Codex CLI target | Goose CLI/Desktop target |
|---|---|---|---|
| `shared/neuralengine.md` | global instruction (`neuralengine-usage.md`) and NeuralEngine skill | `platforms/codex/skills/neuralengine/SKILL.md` (controlled copy; install target is `.agents/skills/neuralengine/SKILL.md`) | `platforms/goose/skills/neuralengine/SKILL.md` (controlled copy; install target is `.agents/skills/neuralengine/SKILL.md`) |
| `shared/repository-review.md` | repository-review skill | not mapped in this slice | not mapped in this slice |
| `shared/python-validation.md` | python-project-validation skill | not mapped in this slice | not mapped in this slice |
| `shared/arch-linux.md` | arch-linux-diagnostics skill | not mapped in this slice | not mapped in this slice |
| `shared/verification.md` | verification skill (Quick, Standard, and Certification implemented) | not mapped in this slice | not mapped in this slice |
| `shared/task-execution-policy.md` | no platform copy (vocabulary contract, deferred consumption) | no platform copy (vocabulary contract, deferred consumption) | no platform copy (vocabulary contract, deferred consumption) |

## Platform-specific files (no shared equivalent)

- `opencode.json`
- `agents/arch-data-engineer.md`
- `agents/builder.md`
- `agents/reviewer.md`
- `agents/planner.md`
- `agents/mechanical.md`
- `codex/AGENTS.md`
- `goose/AGENTS.md`

These files are platform-specific configuration artifacts. They have no
corresponding shared source in this pack.

## Update rules

1. Edit shared sources first.
2. Update controlled platform copies second.
3. Verify equality or semantic equivalence.
4. Platform copies are not independent sources of truth.
