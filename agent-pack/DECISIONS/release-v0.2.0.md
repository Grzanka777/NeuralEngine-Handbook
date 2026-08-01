# ADR: Agent Pack v0.2.0 Release

## Status

Accepted

## Date

2026-08-01

## Checkpoint

- **Agent Pack**: v0.2.0
- **Repository**: `NeuralEngine-Handbook`
- **Decision Git HEAD**: `f76c38501bef1d29af75d65bd790c8935aab10d2`
- **Decision branch**: `docs/document-knowledge-search`
- **Current tree HEAD**: `a3ea1ecabfa092a46c67d87b48f17341cfdad218` (branch `feat/agent-pack-handbook-extension-v1`)
- **Note**: This release decision was accepted at the 25-file checkpoint (`f76c385`). The current 29-file tree at `a3ea1ec` includes release-coherence corrections (VERSION, ROADMAP, placeholder READMEs, etc.) and requires recertification.
- **Release Readiness Assessment**: `.agent-work/reviews/release-readiness-assessment-v0.2.md` (GO)

## Context

Agent Pack v0.1.0 established the foundation: four shared workflow contracts,
OpenCode reference implementation, reviewer permissions, and NeuralEngine
integration. Installations and platform adapters for Codex, Claude Code, and
Antigravity were deferred to later milestones.

The v0.2.0 roadmap called for the Verification Framework — a fifth shared
contract defining structural integrity verification, an OpenCode platform
adapter implementing Quick Verification, Standard Verification, and
Certification Report, plus a self-verification orchestrator.

All v0.2.0 deliverables have been implemented, reviewed, and verified.
The Release Readiness Assessment recommended GO with zero blockers.

## Release scope

### New shared contract

- `shared/verification.md` — fifth authoritative Agent Pack shared contract.
  Defines a platform-neutral structural integrity gate with three modes:
  Quick Verification (mechanical, PASS/FAIL), Standard Verification
  (structural/contractual, PASS/PASS WITH NOTES/BLOCKED/FAIL), and
  Certification Report (formal artifact, CERTIFIED/CERTIFIED WITH NOTES/
  NOT CERTIFIED).

### OpenCode platform adapter

- `platforms/opencode/skills/verification/SKILL.md` — Verification skill
  implementing all three stages with platform-native read-only commands.
- `platforms/opencode/verification-permissions.md` — Permission requirements
  documentation: 14 required commands, reviewer gap analysis, denied commands,
  recommended future additions.

### Self-verification orchestrator

- `.agent-work/prompts/verify-agent-pack-v0.2.md` — Reusable orchestrator
  prompt that executes Quick → Standard → Certification Report with collision-
  safe naming.

### Architecture Decision Record

- `DECISIONS/verification-framework-architecture.md` — Binding ADR resolving
  all 10 architectural decisions for the Verification Framework.

### Updated documentation

- `ARCHITECTURE.md` — Verification Framework documented, DECISIONS/ referenced.
- `MANIFEST.md` — All five contracts mapped with accurate status.
- `ROADMAP.md` — v0.2.0 deliverables tracked.
- `README.md` — Status, navigation, and orchestrator link added.

## Evidence summary

The following evidence was collected at the historical decision checkpoint (`f76c385`). The current 29-file tree at `a3ea1ec` requires recertification.

| Check | Result (at `f76c385`) |
|---|---|
| Implementation reviews (5) | All PASS or PASS WITH NOTES |
| Quick Verification | PASS (25 files, 8/8 SHA-256, 3/3 body equality) |
| Standard Verification | PASS WITH NOTES (2 non-blocking grep false positives) |
| Certification Report | CERTIFIED WITH NOTES |
| DoD Verification Framework criteria (V1–V7) | 7/7 satisfied |
| ADR compliance (10 decisions) | All satisfied |
| Cross-document consistency | No contradictions |
| ruff check | PASS |
| mypy src | PASS |
| pytest | 16 passed |
| Git scope | Clean (no files outside agent-pack/) |

## Decision

**RELEASE APPROVED**

Agent Pack v0.2.0 satisfies its declared scope. All deliverables are
implemented, reviewed, and verified. Zero blockers. The Verification
Framework is end-to-end functional: Quick → Standard → Certification
Report pipeline executes correctly with collision-safe certification
artifacts.

## Known limitations

- Verification skill permissions are documented but not yet enforced on
  the active `reviewer` agent. This is a v0.3 concern (installation and
  agent configuration rollout).
- Codex, Claude Code, and Antigravity adapters remain placeholders.
- No automatic installation, generators, or symlink synchronization.
- `/tmp` space transient failures affect pytest when `/tmp` is full — a
  known environment issue, not an Agent Pack defect.

## Non-blocking risks

| Risk | Severity |
|---|---|
| Reviewer cannot run Quick Verification without manual approval for 7 of 14 commands | LOW (documented; v0.3 scope) |
| Certification Report collision handling tested with `-2` suffix only | LOW (mechanism is deterministic) |
| Release-coherence corrections applied at current tree `a3ea1ec` (VERSION, ROADMAP, placeholders) require recertification | LOW (mechanical corrections only) |

## Consequences

- The Verification Framework is now the authoritative standard for Agent Pack
  structural integrity verification.
- Every future Agent Pack change should be verified with Quick Verification
  at minimum. Release and certification work requires Standard Verification
  and a Certification Report.
- The shared contract count is now five.
- The controlled-copy model now includes the verification skill as an
  OpenCode platform adapter.
- Platform adapter addition rules (ARCHITECTURE.md) apply to any future
  Codex, Claude, or Antigravity verification adapters.

## Next milestone (v0.3)

Installation and workstation rollout:

- Deterministic OpenCode installation procedure.
- Backup and rollback procedure.
- Home workstation verification and certification.
- Office workstation verification and certification.
- Permission enforcement for verification skill on reviewer agent.
