# Agent Pack Manifest

## Shared-to-platform mapping

| Authoritative source | OpenCode target |
|---|---|
| `shared/neuralengine.md` | global instruction (`neuralengine-usage.md`) and NeuralEngine skill |
| `shared/repository-review.md` | repository-review skill |
| `shared/python-validation.md` | python-project-validation skill |
| `shared/arch-linux.md` | arch-linux-diagnostics skill |
| `shared/verification.md` | verification skill (Quick, Standard, and Certification implemented) |
| `shared/task-execution-policy.md` | no platform copy (vocabulary contract, deferred consumption) |

## Platform-specific files (no shared equivalent)

- `opencode.json`
- `agents/arch-data-engineer.md`
- `agents/builder.md`
- `agents/reviewer.md`

These files are platform-specific configuration artifacts. They have no
corresponding shared source in this pack.

## Update rules

1. Edit shared sources first.
2. Update controlled platform copies second.
3. Verify equality or semantic equivalence.
4. Platform copies are not independent sources of truth.
