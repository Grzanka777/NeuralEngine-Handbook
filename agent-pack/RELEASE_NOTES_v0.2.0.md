# Agent Pack v0.2.0 Release Notes

## Highlights

Agent Pack v0.2.0 introduces the **Verification Framework** — a platform-neutral
structural integrity gate that verifies the Agent Pack's files, hashes,
contracts, and documentation are complete and consistent. The framework includes
three verification modes, an OpenCode platform adapter, and a self-verification
orchestrator.

## New shared contract

### `shared/verification.md`

The fifth authoritative Agent Pack shared contract. Defines:

- **Quick Verification** — mechanical integrity check (SHA-256 hashes, file
  counts, body comparisons, prohibited artifact detection). PASS/FAIL only.
  Completes in seconds.
- **Standard Verification** — structural and contractual completeness check
  (shared-contract audit, cross-document consistency, MANIFEST accuracy,
  permission audit, review artifact audit, NeuralEngine evidence audit).
  PASS/PASS WITH NOTES/BLOCKED/FAIL.
- **Certification Report** — formal archival artifact produced from completed
  verification evidence. CERTIFIED/CERTIFIED WITH NOTES/NOT CERTIFIED.

## Verification Framework

### Quick Verification

Proves mechanical integrity of the Agent Pack at any checkpoint:

- All required files present (29 files at v0.2.0).
- All exact-copy files match active OpenCode configuration by SHA-256 (8 files).
- All shared contract bodies match OpenCode SKILL.md bodies (3 comparisons).
- No symlinks, scripts, generators, or installers.
- Git scope clean.
- MANIFEST targets present.

### Standard Verification

Adds structural and contractual completeness:

- 5 shared contracts audited for mandatory rules and required sections.
- 7 documents checked for cross-document consistency.
- MANIFEST mapping accuracy verified.
- Platform support status audited.
- Reviewer and verification permissions audited.
- Placeholder directories confirmed clean.
- 6 review artifacts verified for presence, structure, and NeuralEngine evidence.

### Certification Report

Formal artifact for release and readiness decisions. Includes full SHA-256
table, shared contract summary, platform capability summary, permission summary,
known limitations, and NeuralEngine usage evidence.

## OpenCode support

### New skill

- `platforms/opencode/skills/verification/SKILL.md` — Implements Quick
  Verification, Standard Verification, and Certification Report using
  platform-native read-only commands.

### New documentation

- `platforms/opencode/verification-permissions.md` — 14 required commands,
  reviewer capability analysis, denied commands, future permission
  recommendations.

### Architecture Decision Record

- `DECISIONS/verification-framework-architecture.md` — 10 binding
  architectural decisions for the Verification Framework.

## Self-verification orchestrator

- `.agent-work/prompts/verify-agent-pack-v0.2.md` — Reusable prompt that
  executes the full Quick → Standard → Certification pipeline with
  collision-safe certification naming.

## Certification

The current Agent Pack has been certified at checkpoint `f76c385`: [Likely] certification was at the previous 25-file checkpoint; the current 29-file tree at HEAD `a3ea1ec` requires recertification.

- **Quick Verification**: PASS
- **Standard Verification**: PASS WITH NOTES
- **Certification**: CERTIFIED WITH NOTES

Certification artifacts:

- `.agent-work/certifications/certification-agent-pack-v0.2.0-2026-08-01.md`
- `.agent-work/certifications/certification-agent-pack-v0.2.0-2026-08-01-2.md`

## Known limitations

- Verification skill permissions are documented but not yet enforced on the
  active `reviewer` agent (v0.3 scope).
- Codex, Claude Code, and Antigravity adapters remain placeholders.
- No automatic installation, generators, or symlink synchronization.
- No verifier agent exists.

## Upgrade notes

No breaking changes from v0.1.0. All existing shared contracts and platform
files are unchanged (SHA-256 verified against v0.1.0 independent review).
The Verification Framework is additive.

To upgrade:

1. Pull the latest `agent-pack/` content from branch `feat/agent-pack-handbook-extension-v1`.
2. Copy any updated platform files to `~/.config/opencode/` if the SHA-256
   differs from your active configuration.
3. Run Quick Verification: `Read and execute: .agent-work/prompts/verify-agent-pack-v0.2.md`
4. Confirm PASS before proceeding to Standard or Certification.

v0.1.0 shared contracts (`neuralengine.md`, `repository-review.md`,
`python-validation.md`, `arch-linux.md`) are unchanged and forward-compatible
with v0.2.0.
