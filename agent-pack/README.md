# NeuralEngine Agent Pack

## Purpose

The Agent Pack is a minimal, maintainable set of authoritative shared workflow
files and platform-specific configuration artifacts. It extends
NeuralEngine-Handbook with agent guidance that remains inside the Handbook
repository—not a separate product.

## Scope

- Six authoritative shared workflow files (Verification Framework added in v0.2.0, Task Execution Policy added in v0.4.0).
- One complete platform variant (OpenCode) derived from the user's current,
  working OpenCode configuration.
- One bounded Codex CLI NeuralEngine skill projection.
- One bounded Goose CLI/Desktop NeuralEngine skill projection.
- One bounded Claude Code/Desktop Code NeuralEngine skill projection.
- One bounded GitHub Copilot CLI and VS Code NeuralEngine skill projection.
- Placeholder directory for future Antigravity platform variants.

This pack does not modify NeuralEngine runtime behavior, Brain persistence,
schemas, migrations, user data, or public APIs.

## v0.4.0 changes

v0.4.0 adds the Task Execution Policy as the sixth authoritative shared
contract and introduces the generic builder agent:

- `shared/task-execution-policy.md` — durable execution-policy vocabulary:
  task classes, execution profiles, role separation, runtime substitution
  invariant, supplied-routing validation, delegated-prompt minimum contract.
- `platforms/opencode/agents/builder.md` — generic implementation agent for
  controlled repository changes. Edit allowed; commit/push denied.
- `DECISIONS/architecture-change-proposal-task-execution-policy.md` —
  accepted Architecture Change Proposal (independent review: PASS).
- `VERSION` updated to `0.4.0`; MANIFEST, ARCHITECTURE, CAPABILITY_MATRIX,
  and DEFINITION-OF-DONE updated to reflect the sixth contract and the
  builder agent.
- `tests/test_agent_rollout.py` expanded with builder rollout coverage
  (repository validation: PASS, 33 tests).

## Status

**Agent Pack v0.4.0 — Released**

| Gateway | Result |
|---|---|
| Repository validation | PASS (92 tests) |
| Builder agent implementation review | PASS |
| Task Execution Policy foundation review | READY FOR INDEPENDENT REVIEW |
| ACP independent review | PASS |
| OpenCode | Supported |
| Codex CLI NeuralEngine slice | Supported with limitations (CLI only) |
| Goose CLI/Desktop NeuralEngine slice | Supported with limitations (bounded post-v1.0 extension) |
| Claude Code/Desktop Code NeuralEngine slice | Supported with limitations (bounded post-v1.0 extension) |
| GitHub Copilot CLI / VS Code NeuralEngine slice | Supported with limitations (bounded post-v1.0 extension) |
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
- `.agent-work/reviews/review-implement-opencode-builder-agent-v0.4.0.md`
- `.agent-work/reviews/review-implement-task-execution-policy-foundation.md`
- `.agent-work/reviews/independent-review-task-execution-policy-acp.md`

Certification artifacts:

- `.agent-work/certifications/certification-agent-pack-v0.2.0-2026-08-01.md`

## OpenCode agents

Five first-class OpenCode agents with distinct roles:

| Agent | Role | Write access | File |
|---|---|---|---|
| **planner** | Read-only planning and routing | Edit ask (prompt/Decision Package artifacts only), commit/push denied | `agents/planner.md` |
| **builder** | Generic implementation | Edit allowed, commit/push denied | `agents/builder.md` |
| **arch-data-engineer** | Data architecture and persistence specialization | Edit allowed, commit/push denied, scoped bash allowlist | `agents/arch-data-engineer.md` |
| **reviewer** | Independent read-only review | Denied | `agents/reviewer.md` |
| **mechanical** | Deterministic low-judgment operations | Edit denied, staging ask (exact paths only), commit/push denied | `agents/mechanical.md` |

### Selection policy

```text
planning / routing / Decision Package / delegated prompt generation
→ planner

generic implementation
→ builder

data architecture / persistence / migration specialization
→ arch-data-engineer

independent read-only review
→ reviewer

deterministic exact-path verification, equality checks, staging inspection
→ mechanical
```

`arch-data-engineer` remains the default agent for backward compatibility.
`builder` is the recommended agent for generic implementation tasks that do not
require specialist domain knowledge. `planner` is the recommended entry point
for structured Agent Pack workflows that need a Decision Package or delegated
prompt before implementation.

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
- [CAPABILITY_MATRIX.md](CAPABILITY_MATRIX.md) — Platform capability matrix (OpenCode, Codex CLI, Goose, Claude Code/Desktop Code, and Copilot CLI / VS Code).
- [DECISIONS/](DECISIONS/) — Architecture Decision Records (ADRs).
- [RELEASE_NOTES_v0.4.0.md](RELEASE_NOTES_v0.4.0.md) — v0.4.0 release notes.
- [RELEASE_NOTES_v0.3.0.md](RELEASE_NOTES_v0.3.0.md) — v0.3.0 release notes.
- [RELEASE_NOTES_v0.2.0.md](RELEASE_NOTES_v0.2.0.md) — v0.2.0 release notes.

Shared contracts:

- [shared/neuralengine.md](shared/neuralengine.md) — Mandatory NeuralEngine usage.
- [shared/repository-review.md](shared/repository-review.md) — Repository review workflow.
- [shared/python-validation.md](shared/python-validation.md) — Python project validation.
- [shared/arch-linux.md](shared/arch-linux.md) — Arch Linux diagnostics.
- [shared/verification.md](shared/verification.md) — Agent Pack structural integrity verification (v0.2.0).
- [shared/task-execution-policy.md](shared/task-execution-policy.md) — Task classes, execution profiles, role separation, and execution-policy invariants (v0.4.0).

Platform implementations:

- [platforms/opencode/](platforms/opencode/) — OpenCode adapter and skills.
- [platforms/codex/](platforms/codex/) — Codex CLI NeuralEngine adapter slice.
- [platforms/goose/](platforms/goose/) — Goose CLI/Desktop NeuralEngine adapter slice.
- [platforms/claude/](platforms/claude/) — Claude Code/Desktop Code NeuralEngine adapter slice.
- [platforms/copilot/](platforms/copilot/) — GitHub Copilot CLI and VS Code NeuralEngine adapter slice.
- [platforms/opencode/agents/planner.md](platforms/opencode/agents/planner.md) — Read-only planning and routing agent.
- [platforms/opencode/agents/builder.md](platforms/opencode/agents/builder.md) — Generic builder agent (new in v0.4.0).
- [platforms/opencode/agents/arch-data-engineer.md](platforms/opencode/agents/arch-data-engineer.md) — Specialist implementation agent.
- [platforms/opencode/agents/reviewer.md](platforms/opencode/agents/reviewer.md) — Read-only independent reviewer.
- [platforms/opencode/agents/mechanical.md](platforms/opencode/agents/mechanical.md) — Deterministic low-judgment operations agent.
- [platforms/opencode/skills/verification/SKILL.md](platforms/opencode/skills/verification/SKILL.md) — Verification skill: Quick, Standard, and Certification (v0.2.0).
- [platforms/opencode/verification-permissions.md](platforms/opencode/verification-permissions.md) — Verification permission requirements.
- [../.agent-work/prompts/verify-agent-pack-v0.2.md](../.agent-work/prompts/verify-agent-pack-v0.2.md) — Self-verification orchestrator prompt.
