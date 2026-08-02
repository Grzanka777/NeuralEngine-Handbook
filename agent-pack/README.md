# NeuralEngine Agent Pack

## Purpose

The Agent Pack is a minimal, maintainable set of authoritative shared workflow
files and platform-specific configuration artifacts. It extends
NeuralEngine-Handbook with agent guidance that remains inside the Handbook
repository—not a separate product.

## Scope

- Six authoritative shared workflow files (Verification Framework added in v0.2.0, Task Execution Policy added in v0.4.0).
- One platform variant (OpenCode) derived from the user's current, working
  OpenCode configuration.
- Placeholder directories for future Codex, Claude Code, and Antigravity
  platform variants.

This pack does not modify NeuralEngine runtime behavior, Brain persistence,
schemas, migrations, user data, or public APIs.

## v0.3.0 changes

v0.3.0 enforces Verification Framework permissions on the OpenCode reviewer:

- Eight narrow read-only shell permissions added: `find`, `test`, `wc`, `sha256sum`, `diff`, `cmp`, `grep`, `sed`.
- The `verification` skill is now required by the reviewer.
- The reviewer remains unable to edit files, delegate tasks, perform Git writes, run destructive commands, or write to the Brain.
- No dedicated verifier agent exists.
- Active OpenCode controlled-copy equality was verified after explicit synchronization.
- Future platforms remain placeholders.

## Status

**Agent Pack v0.3.0 — Released**

| Gateway | Result |
|---|---|
| Repository validation | PASS (16 tests) |
| Quick Verification | PASS |
| Standard Verification | PASS WITH NOTES |
| Certification | CERTIFIED WITH NOTES |
| OpenCode | Supported |
| Codex | Placeholder (not implemented) |
| Claude Code | Placeholder (not implemented) |
| Antigravity | Placeholder (not implemented) |

Review artifacts:

- `.agent-work/reviews/review-implement-agent-pack-handbook-extension-v1.md`
- `.agent-work/reviews/review-independent-agent-pack-v0.1.0.md`
- `.agent-work/reviews/review-agent-pack-v0.2.0-release-readiness.md`
- `.agent-work/reviews/review-formalize-agent-pack-architecture-and-dod.md`
- `.agent-work/reviews/review-decide-verification-framework-architecture.md`
- `.agent-work/reviews/review-implement-verification-shared-contract-v0.2.md`
- `.agent-work/reviews/review-implement-opencode-quick-verification-v0.2.md`
- `.agent-work/reviews/review-agent-pack-v0.3-reviewer-verification-permissions.md`

Certification artifacts:

- `.agent-work/certifications/certification-agent-pack-v0.2.0-2026-08-01.md`

## OpenCode agents

Three first-class OpenCode agents with distinct roles:

| Agent | Role | Write access | File |
|---|---|---|---|
| **builder** | Generic implementation | Edit allowed, commit/push denied | `agents/builder.md` |
| **arch-data-engineer** | Data architecture and persistence specialization | Edit allowed, commit/push denied, scoped bash allowlist | `agents/arch-data-engineer.md` |
| **reviewer** | Independent read-only review | Denied | `agents/reviewer.md` |

### Selection policy

```text
generic implementation
→ builder

data architecture / persistence / migration specialization
→ arch-data-engineer

independent read-only review
→ reviewer
```

`arch-data-engineer` remains the default agent for backward compatibility.
`builder` is the recommended agent for generic implementation tasks that do not
require specialist domain knowledge.

## Six authoritative shared contracts

| File | Source |
|---|---|
| `shared/neuralengine.md` | merged from global neuralengine-usage.md + NeuralEngine skill body |
| `shared/repository-review.md` | repository-review skill body |
| `shared/python-validation.md` | python-project-validation skill body |
| `shared/arch-linux.md` | arch-linux-diagnostics skill body |
| `shared/verification.md` | Verification Framework (new in v0.2.0) |
| `shared/task-execution-policy.md` | Agent Pack execution-policy authority (new in v0.4.0) |

## Controlled-copy model

Platform-specific files are controlled copies of active configuration, not
independent sources of truth.

For each shared source, the corresponding platform skill body must remain equal
or semantically equivalent.

## Update order

1. Edit the authoritative shared source first.
2. Update the controlled platform copy second.
3. Verify equality or semantic equivalence between shared source and each
   platform copy.
4. Do not edit a platform skill body independently.

## Drift risk

Controlled duplication is intentional in v1. Future versions may introduce
generators or include mechanisms if drift becomes a maintenance burden.

## Brain writes

No automatic Brain writes are performed by this pack. Any write requires
preview and explicit user authorization under the global NeuralEngine policy.

## Installation

No automatic installation is performed. Platform files must be copied
manually into the target agent configuration directory.

### Controlled manual copy

The authoritative installation path for OpenCode agents is manual controlled copy
with safeguards (per [ARCHITECTURE.md](ARCHITECTURE.md) §Installation and onboarding boundary).

**Target directory**: `~/.config/opencode/agents/`

**Installation procedure** (for each agent file):

```bash
# 1. Preview (dry run) — show what would change
diff <(sha256sum agent-pack/platforms/opencode/agents/builder.md) \
     <(sha256sum ~/.config/opencode/agents/builder.md 2>/dev/null || echo "not installed")

# 2. Back up existing file if present
[ -f ~/.config/opencode/agents/builder.md ] && \
    cp ~/.config/opencode/agents/builder.md ~/.config/opencode/agents/builder.md.backup

# 3. Copy agent file
cp agent-pack/platforms/opencode/agents/builder.md ~/.config/opencode/agents/builder.md

# 4. Verify equality
sha256sum agent-pack/platforms/opencode/agents/builder.md \
          ~/.config/opencode/agents/builder.md
```

**Rollback** (if needed):

```bash
cp ~/.config/opencode/agents/builder.md.backup ~/.config/opencode/agents/builder.md
```

**Verification**: Run `agent-pack` validation after installation to confirm
structural integrity.

The controlled copy procedure is verified by `tests/test_agent_rollout.py`
(17 tests covering clean install, overwrite, backup, rollback, idempotency,
equality, frontmatter integrity, model-name absence, and agent coexistence).

## Navigation

- [ARCHITECTURE.md](ARCHITECTURE.md) — Authoritative architecture document (v1.0 Architecture Freeze applied).
- [DEFINITION-OF-DONE.md](DEFINITION-OF-DONE.md) — Formal v1.0 quality gates.
- [ROADMAP.md](ROADMAP.md) — Milestone roadmap from v0.1.0 to v1.0.0.
- [MANIFEST.md](MANIFEST.md) — Shared-to-platform mapping and update rules.
- [CAPABILITY_MATRIX.md](CAPABILITY_MATRIX.md) — Platform capability matrix (OpenCode + Codex CLI).
- [DECISIONS/](DECISIONS/) — Architecture Decision Records (ADRs).
- [RELEASE_NOTES_v0.3.0.md](RELEASE_NOTES_v0.3.0.md) — v0.3.0 release notes.
- [RELEASE_NOTES_v0.2.0.md](RELEASE_NOTES_v0.2.0.md) — v0.2.0 release notes.

Shared contracts:

- [shared/neuralengine.md](shared/neuralengine.md) — Mandatory NeuralEngine usage.
- [shared/repository-review.md](shared/repository-review.md) — Repository review workflow.
- [shared/python-validation.md](shared/python-validation.md) — Python project validation.
- [shared/arch-linux.md](shared/arch-linux.md) — Arch Linux diagnostics.
- [shared/verification.md](shared/verification.md) — Agent Pack structural integrity verification (v0.2.0).
- [shared/task-execution-policy.md](shared/task-execution-policy.md) — Task classes, execution profiles, role separation, and execution-policy invariants (v0.4.0).

OpenCode platform implementation:

- [platforms/opencode/](platforms/opencode/) — OpenCode adapter and skills.
- [platforms/opencode/agents/builder.md](platforms/opencode/agents/builder.md) — Generic builder agent (new in v0.4.0).
- [platforms/opencode/agents/arch-data-engineer.md](platforms/opencode/agents/arch-data-engineer.md) — Specialist implementation agent.
- [platforms/opencode/agents/reviewer.md](platforms/opencode/agents/reviewer.md) — Read-only independent reviewer.
- [platforms/opencode/skills/verification/SKILL.md](platforms/opencode/skills/verification/SKILL.md) — Verification skill: Quick, Standard, and Certification (v0.2.0).
- [platforms/opencode/verification-permissions.md](platforms/opencode/verification-permissions.md) — Verification permission requirements.
- [../.agent-work/prompts/verify-agent-pack-v0.2.md](../.agent-work/prompts/verify-agent-pack-v0.2.md) — Self-verification orchestrator prompt.
