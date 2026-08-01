# ADR: Agent Pack v1.0 Architecture Freeze

## Status

Accepted

## Date

2026-08-01

## Context

Agent Pack v0.1.0 established the foundation (four shared contracts, OpenCode
reference implementation). v0.2.0 added the Verification Framework (fifth shared
contract, Quick/Standard/Certification, orchestrator). Both milestones passed
release assessment with zero blockers.

The next target is v1.0 — the first stable release with compatibility guarantees.
Before implementing the Codex platform adapter and reaching v1.0, the
architecture must be frozen to provide a stable foundation.

This ADR records the binding Architecture Freeze for v1.0 development.

## Decision

### 1. Product identity

The authoritative name is:

```text
NeuralEngine Agent Pack
```

"OpenCode Agent Pack" is incorrect. OpenCode is the first completed platform
adapter. The Agent Pack is platform-agnostic and part of
`NeuralEngine-Handbook`.

### 2. v1.0 platform scope

Exactly two first-class runtime platforms are in v1.0 scope:

```text
OpenCode
Codex CLI
```

These are peer platform adapters. Neither is primary. Neither subsumes the other.

The following platforms remain outside v1.0 scope:

```text
Claude Code
Antigravity (Google)
GitHub Copilot
Other AI agent platforms
```

They may be added after v1.0 only after a demonstrated need and an Architecture
Change Proposal.

### 3. Platform-centric architecture

The Agent Pack is platform-centric:

- Platform adapters implement shared contracts.
- Models are selected inside a platform.
- Model identity does not create a new adapter.

Examples:

```text
OpenCode + DeepSeek V4 Pro Max
OpenCode + GPT-5.6 Sol Medium
Codex CLI + GPT-5.6 Sol Medium
```

All remain **two platform adapters** (OpenCode, Codex CLI), not three model
adapters. Models are runtime engines, not Agent Pack architecture elements.

### 4. Stable shared contracts

The five authoritative shared contracts are frozen:

```text
shared/neuralengine.md
shared/repository-review.md
shared/python-validation.md
shared/arch-linux.md
shared/verification.md
```

After freeze:

- Adapters must not redefine shared contract semantics.
- Changes to shared contracts require an Architecture Change Proposal and ADR.
- Platform limitations must be documented in adapters instead of weakening
  shared contracts.
- Editorial clarifications may proceed only when they do not alter semantics.

### 5. Stable workflows

#### Ordinary implementation

```text
Implementation
    → optional Quick Verification
    → Repository Review
```

#### Release/readiness

```text
Implementation
    → Quick Verification (mandatory)
    → Standard Verification (mandatory)
    → Certification Report
    → Independent Review
    → Release Readiness Assessment
    → Release Decision
```

Platform adapters may map these steps to native capabilities but must preserve
their meaning.

### 6. Verification architecture

- Verification is the structural integrity gate.
- Quick Verification uses PASS/FAIL.
- Standard Verification uses PASS/PASS WITH NOTES/BLOCKED/FAIL.
- Certification Report is a formal artifact, not another verification level.
- Verification does not replace Repository Review.
- No repair is performed during verification.
- No Brain writes occur.

### 7. Adapter API

Every v1.0 platform adapter must implement or explicitly classify as
unsupported:

1. Global instructions or equivalent.
2. Agent/role definition mechanism or documented fallback.
3. Shared contract loading.
4. Task execution convention.
5. Repository instruction awareness.
6. NeuralEngine usage (`neural status`, search decision, evidence).
7. Implementation workflow.
8. Repository review workflow.
9. Quick Verification.
10. Standard Verification.
11. Certification Report.
12. Permission/capability declaration.
13. Installation, update, and rollback documentation.
14. Platform support status declaration.

Items 9–11 are satisfied by implementing the Verification Framework shared
contract. A platform adapter may document a capability as NOT SUPPORTED with
an explanation; it must not silently omit it.

### 8. Capability matrix

A formal capability matrix for OpenCode and Codex CLI is defined in:

```text
agent-pack/CAPABILITY_MATRIX.md
```

Capabilities include: agents/roles, skills/contracts, global instructions,
permissions, shell execution, repository instructions, NeuralEngine CLI,
review, verification, certification, model selection, non-interactive
execution, and artifact generation.

Evidence-based states:

```text
SUPPORTED
SUPPORTED WITH LIMITATIONS
NOT SUPPORTED
NOT APPLICABLE
NOT YET ASSESSED
```

OpenCode is populated from current repository evidence. Codex uses
`NOT YET ASSESSED` where no evidence exists. The upcoming Codex Platform
Assessment is the authority that will fill the Codex column.

### 9. Architecture Change Proposal

A formal Architecture Change Proposal is required for:

- Changing shared contract semantics.
- Adding or removing a shared contract.
- Changing the verification hierarchy.
- Changing the release workflow.
- Changing the Brain authorization boundary.
- Changing the Adapter API.
- Expanding v1.0 platform scope.
- Introducing generators, symlinks, installers, or new source-of-truth layers.

Process:

```text
Assessment
    → Architecture Change Proposal
    → ADR
    → Implementation
    → Independent Review
    → Verification (Quick + Standard)
    → Certification Report
    → Release Decision
```

### 10. Non-architectural changes

The following do not require an Architecture Change Proposal:

- Typo fixes.
- Formatting.
- Link corrections.
- Examples that do not change semantics.
- Platform-specific compatibility fixes inside adapter boundaries.
- Permission allowlist refinements that do not weaken the security model.
- Documentation of verified limitations.

### 11. Freeze status

The Architecture Freeze becomes binding immediately after acceptance. It
applies prospectively to v1.0 development. It does not retroactively
invalidate v0.2 artifacts or decisions.

### 12. Exit criteria

Minimum v1.0 Stable exit criteria:

1. OpenCode adapter remains certified.
2. Codex adapter implemented and certified.
3. Both adapters implement the same shared contract semantics.
4. Cross-platform validation completed.
5. No unresolved architecture blockers.
6. Installation, update, and rollback documented for both platforms.
7. v1.0 release assessment and release decision completed.
8. Agent Pack can support resumed NeuralEngine development without requiring
   architecture changes.

Not required for v1.0: Claude, Antigravity, golden tests for unrelated
platforms, generators, installers, CI, or automation.

## Consequences

- The architecture is frozen. Changes to shared contracts, workflows,
  verification hierarchy, Adapter API, or platform scope require an
  Architecture Change Proposal.
- Codex Platform Assessment is the next milestone. It must fill the capability
  matrix from evidence, not invention.
- Codex adapter implementation follows the frozen Adapter API.
- All five shared contracts remain authoritative. Their semantics may not be
  weakened to accommodate platform limitations.
- OpenCode and Codex CLI are peer platforms. Neither is the reference
  implementation; both must satisfy the Adapter API.
- v1.0 exit criteria are minimal: two certified platform adapters, cross-
  platform validation, release decision.

## Alternatives considered

### A: Keep v0.2 architecture open during Codex implementation

Rejected. Implementing Codex without a frozen architecture risks divergent
contract interpretations. The freeze establishes a stable baseline that both
platforms can target.

### B: Make Codex the primary/reference platform

Rejected. OpenCode and Codex are peer platforms. Neither is primary. The
shared contracts are the authoritative source, not any single platform adapter.

### C: Add Claude and Antigravity to v1.0 scope

Rejected. No demonstrated need. v1.0 is the minimum viable stable release.
Additional platforms can be added after v1.0 via Architecture Change Proposal.

### D: Require generators or automation for v1.0

Rejected. Manual controlled-copy synchronization remains appropriate for the
current scale (five contracts, two platforms). Automation can be introduced
later via Architecture Change Proposal when the maintenance burden justifies it.

## Supersession rule

This decision may be superseded only by a later ADR that:

1. References this ADR by filename.
2. States which specific clause is superseded.
3. Explains why the change is necessary.
4. Follows the Architecture Change Proposal process defined in §9.
