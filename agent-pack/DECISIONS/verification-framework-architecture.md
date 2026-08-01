# ADR: Verification Framework Architecture

## Status

Accepted

## Date

2026-08-01

## Context

Agent Pack v0.1.0 defines four shared workflow contracts but has no standardized
mechanism to verify its own structural integrity. Drift between shared contracts
and platform copies, missing files, inconsistent documentation, and unverified
reviews are currently detected only by manual inspection. The Agent Pack roadmap
(v0.2.0) calls for a Verification Framework to fill this gap.

An architecture assessment was completed:

```text
.agent-work/reviews/assessment-verification-framework-architecture.md
```

It recommended ACCEPT WITH REVISIONS: create a new shared contract, keep the
Quick → Standard → Certification hierarchy, rename "Certification" to
"Certification Report", and require Standard Verification to gate on Quick
Verification.

This ADR converts that assessment into a binding architectural decision.

## Decision

### 1. Shared contract

**YES.** `agent-pack/shared/verification.md` will be created as the fifth
authoritative shared contract.

Verification is a distinct capability (structural integrity of the pack itself)
that does not belong in NeuralEngine (durable knowledge), repository-review
(semantic review of implementation), python-validation (Python code quality),
or arch-linux (system diagnostics).

### 2. Primary responsibility

The Verification Framework is a **structural integrity gate**.

It verifies that the Agent Pack's files exist, are byte-identical to their
sources where required, are internally consistent, and that mandatory evidence
(NeuralEngine usage, review artifacts) is present. It does not verify semantic
correctness, implementation quality, or task-contract compliance.

### 3. Verification flow

```text
Quick Verification
    → Standard Verification
        → Certification Report
```

- **Quick Verification**: Mechanical integrity check (SHA-256, file counts,
  symlink/script absence). PASS/FAIL only. < 10 seconds. No human judgment.
- **Standard Verification**: Structural and contractual completeness check
  (mandatory rule audit, cross-document consistency, evidence presence).
  PASS/PASS WITH NOTES/BLOCKED/FAIL. < 5 minutes.
- **Certification Report**: A formal archival artifact produced from a
  completed Standard Verification that passed without blockers. It is a
  *report format*, not a verification level. It records timestamp, verifier,
  full SHA-256 table, evidence references, and findings.

Standard Verification must gate on Quick Verification passing first. A
Certification Report must be based on a completed Standard Verification with
a PASS or PASS WITH NOTES verdict.

### 4. Relationship to repository review

1. **Does Verification replace Repository Review?** No. Verification checks
   structural integrity; repository-review checks semantic correctness of an
   implementation against its task contract. They are complementary.

2. **Must Repository Review always depend on Verification?** No. For ordinary
   implementation changes, the reviewer may run Quick Verification as a
   pre-check but Standard Verification is not required. For release-readiness
   or certification work, Standard Verification is required before the final
   review.

3. **Must Certification Report depend on a completed Repository Review?**
   No. Certification Reports verify structural integrity of the pack at a
   checkpoint. A Repository Review may reference a Certification Report as
   evidence but the report is independently valid.

### 5. End-to-end workflow

**Ordinary implementation change:**

```text
Implementation → Quick Verification (optional pre-check) → Repository Review
```

**Release-readiness or certification work:**

```text
Implementation
    → Quick Verification
    → Standard Verification
    → Certification Report
    → Independent Review (or Repository Review + Independent Review)
```

Quick Verification is always available as a fast drift check. Standard
Verification is required only when structural completeness must be
demonstrated (release, certification, new platform adapter, new shared
contract).

### 6. Verdict model

| Level | Allowed verdicts |
|---|---|
| Quick Verification | `PASS`, `FAIL` |
| Standard Verification | `PASS`, `PASS WITH NOTES`, `BLOCKED`, `FAIL` |
| Certification Report | `PASS`, `PASS WITH NOTES`, `BLOCKED`, `FAIL` |

`FAIL` means one or more criteria are NOT SATISFIED. `BLOCKED` means
verification could not complete (missing dependencies, environment failure).
`PASS WITH NOTES` means all criteria are SATISFIED but non-blocking findings
exist.

### 7. Readiness score

**Optional.** A 0–100 readiness score may supplement a Certification Report
but must not override the verdict or mask blockers. A score of 95 with one
blocker is still `FAIL`.

### 8. NeuralEngine boundary

The Verification Framework **checks that NeuralEngine evidence is present**
in review artifacts. It **produces** its own NeuralEngine usage evidence
in Certification Reports (via `neural status` and search-decision reporting).

The Framework **does not**:
- Perform Brain writes.
- Promote records between lifecycle stages.
- Create, update, or evaluate Brain records.
- Require Brain availability for Quick Verification.

Standard Verification checks for:
- `neural status` output in review artifacts.
- NeuralEngine usage section presence.
- Search-decision evidence where applicable.

### 9. Scope exclusions

The Verification Framework does **not** verify:

| Excluded responsibility | Assigned to |
|---|---|
| Semantic correctness of implementation | repository-review |
| Model quality | Out of scope (platform concern) |
| API cost | Out of scope |
| Model benchmark performance | Out of scope |
| Python code quality | python-validation (ruff, mypy, pytest) |
| Linux system health | arch-linux-diagnostics |
| NeuralEngine record validity | NeuralEngine Brain (authority) |
| Task-contract compliance | repository-review |

These are explicit exclusions documented in the contract.

### 10. Milestone applicability

This decision becomes authoritative at **Agent Pack v0.2.0**. It does not
change any v0.1.0 contract retroactively. v0.1.0 files are not required to
conform to a Verification Framework that did not exist when they were created.

## Decided workflow

The authoritative workflow for Agent Pack structural verification:

1. **Quick Verification** — fast mechanical check. Required before: committing
   platform-file changes, creating a Certification Report. Optional before:
   ordinary implementation review.

2. **Standard Verification** — structural completeness check. Required before:
   release, certification, new platform adapter, new shared contract.

3. **Certification Report** — formal artifact. Produced when Standard
   Verification passes without blockers. Used for: release evidence, archival
   proof of integrity at a checkpoint.

## Relationship to existing contracts

| Contract | Relationship |
|---|---|
| `shared/neuralengine.md` | Verification checks NeuralEngine evidence presence in reviews. Follows the same Brain authorization boundary. |
| `shared/repository-review.md` | Verification provides structural integrity evidence. Repository review provides semantic correctness assessment. Complementary, not overlapping. |
| `shared/python-validation.md` | No direct relationship. Verification does not run ruff/mypy/pytest. |
| `shared/arch-linux.md` | No relationship. Verification is about Agent Pack files, not system health. |

## Consequences

**Positive:**
- Standardized drift detection (SHA-256, body comparison).
- Fast pre-commit integrity check (Quick Verification, < 10 seconds).
- Auditable release evidence (Certification Report with full hash table).
- Clear boundary between structural verification and semantic review.
- Platform-agnostic: every platform can compute SHA-256.

**Negative:**
- One additional shared contract to maintain.
- One additional platform skill to create and keep in sync.
- Three verification levels may feel heavy for 21 files, but each serves a
  distinct purpose and no level is redundant.

**Neutral:**
- Quick Verification is the most-used level; Standard Verification is
  release-gated; Certification Reports are archival artifacts.

## Alternatives considered

### A: Add verification to repository-review

Rejected. Conflates structural integrity (does the file exist, does the hash
match?) with semantic review (does the implementation satisfy the task
contract?). Different concerns, different failure modes.

### B: Add verification to NeuralEngine

Rejected. NeuralEngine is about durable knowledge and decisions, not file-level
integrity checks. Adding structural verification would dilute its purpose.

### C: Two-level hierarchy (Quick → Certification only)

Rejected. Standard Verification provides a necessary middle ground — more
thorough than mechanical hash checks but not as formal as a Certification
Report. Removing it would force Certification Reports to include contract-level
audit work, making them too expensive for routine use.

### D: No Verification Framework

Rejected. The independent review already identified the need for systematic
equality/hash verification. Manual inspection of 21 files is error-prone and
does not scale to future platforms.

## Implementation implications

### New files (v0.2.0)

```
agent-pack/shared/verification.md
agent-pack/platforms/opencode/skills/verification/SKILL.md
```

### Updated files (v0.2.0)

```
agent-pack/MANIFEST.md                (add verification mapping)
agent-pack/ROADMAP.md                 (mark v0.2.0 in progress)
agent-pack/README.md                  (add verification to navigation)
```

### Not modified

All existing shared contracts, platform adapters, and v0.1.0 files remain
unchanged. Verification Framework is additive.

## Supersession rule

This decision may be superseded by a later ADR. A superseding decision must:

1. Reference this ADR by filename.
2. Explain which specific clause is superseded and why.
3. State the new decision explicitly.
4. Be recorded under `agent-pack/DECISIONS/` with a later date.
