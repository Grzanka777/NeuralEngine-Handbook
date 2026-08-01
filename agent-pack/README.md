# NeuralEngine Agent Pack

## Purpose

The Agent Pack is a minimal, maintainable set of authoritative shared workflow
files and platform-specific configuration artifacts. It extends
NeuralEngine-Handbook with agent guidance that remains inside the Handbook
repository—not a separate product.

## Scope

- Five authoritative shared workflow files (Verification Framework added in v0.2.0).
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

**Agent Pack v0.3.0 — Release prepared**

| Gateway | Result |
|---|---|
| Repository validation | PASS (16 tests) |
| Quick Verification | PASS |
| Standard Verification | PASS WITH NOTES |
| Certification | Pending |
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

## Five authoritative shared contracts

| File | Source |
|---|---|
| `shared/neuralengine.md` | merged from global neuralengine-usage.md + NeuralEngine skill body |
| `shared/repository-review.md` | repository-review skill body |
| `shared/python-validation.md` | python-project-validation skill body |
| `shared/arch-linux.md` | arch-linux-diagnostics skill body |
| `shared/verification.md` | Verification Framework (new in v0.2.0) |

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

OpenCode platform implementation:

- [platforms/opencode/](platforms/opencode/) — OpenCode adapter and skills.
- [platforms/opencode/skills/verification/SKILL.md](platforms/opencode/skills/verification/SKILL.md) — Verification skill: Quick, Standard, and Certification (v0.2.0).
- [platforms/opencode/verification-permissions.md](platforms/opencode/verification-permissions.md) — Verification permission requirements.
- [../.agent-work/prompts/verify-agent-pack-v0.2.md](../.agent-work/prompts/verify-agent-pack-v0.2.md) — Self-verification orchestrator prompt.
