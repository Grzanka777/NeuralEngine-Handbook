# Agent Pack v1.0 — Definition of Done

Every criterion is binary and auditable. A criterion is either satisfied or not.
Evidence must be verifiable from repository contents, command output, or review
artifacts.

## Architecture

| # | Criterion | Evidence |
|---|---|---|
| A1 | `ARCHITECTURE.md` exists and is complete | File present, all required sections populated |
| A2 | Architecture defines why Agent Pack exists and why it is not a separate repository | Section "Why Agent Pack exists" and "Role within NeuralEngine-Handbook" present |
| A3 | Architecture defines boundaries, source-of-truth rules, controlled-copy model, and contract ownership | Sections present and internally consistent |
| A4 | Architecture defines lifecycle of shared-contract and platform-adapter changes | Sections present |
| A5 | Architecture defines rules for adding contracts and platforms | Sections present |
| A6 | Architecture defines versioning, compatibility, review, and installation boundaries | Sections present |
| A7 | Architecture defines exclusions and operating assumptions | Sections present |
| A8 | No architecture statement contradicts README, MANIFEST, ROADMAP, or DEFINITION-OF-DONE | Cross-reference audit passes |

## Shared contracts

| # | Criterion | Evidence |
|---|---|---|
| S1 | Exactly five authoritative shared contracts exist (v0.2.0+) | `shared/neuralengine.md`, `shared/repository-review.md`, `shared/python-validation.md`, `shared/arch-linux.md`, `shared/verification.md` present |
| S2 | Each contract has a defined purpose, scope, and exclusions | Content review of each contract |
| S3 | Each contract defines workflow, required evidence, and failure criteria where applicable | Content review of each contract |
| S4 | `shared/neuralengine.md` preserves all mandatory NeuralEngine rules without material omission | NeuralEngine audit checklist confirmed |
| S5 | No undocumented duplication exists between shared contracts | Cross-contract redundancy audit passes |
| S6 | NeuralEngine usage and Brain authorization boundaries are documented and enforced | Content review confirms |
| S7 | Shared contract boundaries are documented (what belongs in shared vs. platform) | ARCHITECTURE.md section "Relationship between shared/ and platforms/" |

## Platform support

| # | Criterion | Evidence |
|---|---|---|
| P1 | Each supported platform has an adapter directory under `platforms/` | Directory listing |
| P2 | Each supported platform adapter maps all applicable shared contracts | MANIFEST mapping table |
| P3 | Each supported platform adapter defines appropriate permissions | Agent/skill permission blocks present |
| P4 | Each supported platform adapter has documented onboarding instructions | README or platform README |
| P5 | Each platform adapter is verified (equality/hash for exact copies, body comparison for skill bodies) | Verification report |
| P6 | Each unsupported platform has a documented placeholder with status | `platforms/<name>/README.md` present with "Not implemented" |
| P7 | Documented limitations exist for any contract a platform cannot fully represent | Platform README or adapter notes |
| P8 | Support matrix in README is current and accurate | Cross-reference audit |

## Verification Framework

| # | Criterion | Evidence |
|---|---|---|
| V1 | `shared/verification.md` exists and defines the Verification Framework | File present |
| V2 | Quick Verification is defined and executable without modifying the repository | Defined procedure with commands |
| V3 | Standard Verification is defined and covers all contracts and platforms | Defined procedure with commands |
| V4 | Certification is defined with PASS/PASS WITH NOTES/BLOCKED/FAIL criteria | Defined procedure with verdict rules |
| V5 | Common report format is defined | Report template in verification.md |
| V6 | OpenCode verification skill exists and uses the Verification Framework | `platforms/opencode/skills/verification/SKILL.md` present |
| V7 | Verification skill has read-only permissions aligned with the reviewer agent model | Permission block verified |

## Installation and rollback

| # | Criterion | Evidence |
|---|---|---|
| I1 | Deterministic OpenCode installation procedure is documented | Step-by-step instructions with exact paths |
| I2 | Backup procedure is defined for pre-existing configuration | Backup step before any copy |
| I3 | Rollback procedure is defined using the backup | Restore step documented |
| I4 | Installation verified on home workstation | Verification report from home machine |
| I5 | Installation verified on office workstation | Verification report from office machine |
| I6 | Certification passes on both machines | Certification reports |
| I7 | No automatic installation is performed or implied | Documentation states "manual, explicit" |

## Quality

| # | Criterion | Evidence |
|---|---|---|
| Q1 | Implementation review passes for all v1.0 deliverables | Review artifact with PASS verdict |
| Q2 | Independent review passes for all v1.0 deliverables | Review artifact with PASS verdict |
| Q3 | Equality/hash verification passes for all exact-copy files | SHA-256 comparison report |
| Q4 | Repository validation passes (`ruff check`, `mypy src`, `pytest`) | Command output |
| Q5 | `git diff --check` is clean | Command output |
| Q6 | No files outside `agent-pack/` were modified by Agent Pack work | Scope audit |
| Q7 | No symlinks, scripts, generators, or automatic installers were introduced | File listing audit |
| Q8 | No unresolved blockers exist | Review artifacts show `None` for blockers |
| Q9 | `DEFINITION-OF-DONE.md` itself is complete (all criteria are either satisfied or explicitly deferred with a roadmap reference) | Self-audit |

## Release readiness

| # | Criterion | Evidence |
|---|---|---|
| R1 | `VERSION` equals `1.0.0` | File content |
| R2 | Support matrix in README is current | Cross-reference audit |
| R3 | MANIFEST is current | Cross-reference audit |
| R4 | ROADMAP reflects completed v1.0 milestone | ROADMAP entry marked completed |
| R5 | No automatic commit, push, or Brain write occurred during release | Review artifacts confirm |
| R6 | v1.0 platform scope satisfied: OpenCode certified, Codex implemented and certified, Claude/Antigravity explicitly excluded per Architecture Freeze | Platform directories and CAPABILITY_MATRIX audited |

## Audit checklist

For each criterion, the reviewer must:

1. Identify the exact evidence source (file, command output, review artifact).
2. Determine whether the criterion is SATISFIED, NOT SATISFIED, or NOT APPLICABLE.
3. Record the evidence reference.
4. Do not claim SATISFIED without verifiable evidence.

A `PASS` verdict requires all applicable criteria to be SATISFIED. Any NOT
SATISFIED criterion is a blocker unless explicitly deferred to a later version
in the ROADMAP.
