# Agent Pack Roadmap

## v0.1.0 — Foundation

**Status: Completed**

Delivered:

- Four authoritative shared workflow contracts:
  - `shared/neuralengine.md` — merged from global neuralengine-usage.md and
    NeuralEngine skill body, preserving all mandatory rules.
  - `shared/repository-review.md` — repository-review skill body.
  - `shared/python-validation.md` — python-project-validation skill body.
  - `shared/arch-linux.md` — arch-linux-diagnostics skill body.
- OpenCode reference implementation with all platform files verified
  byte-equal to active configuration (SHA-256).
- Reviewer agent with read-only permissions.
- NeuralEngine integration (global instruction and skill).
- Placeholder directories for Codex, Claude Code, and Antigravity.
- Documentation: README, MANIFEST, VERSION.

Reviews:

- Implementation review: PASS
  (`.agent-work/reviews/review-implement-agent-pack-handbook-extension-v1.md`)
- Independent review: PASS
  (`.agent-work/reviews/review-independent-agent-pack-v0.1.0.md`)

Architecture documentation deferred to v0.1.1 (this milestone).

---

## v0.1.1 — Architecture and Definition of Done

**Status: Completed**

Deliverables:

- `ARCHITECTURE.md` — authoritative architecture document.
- `DEFINITION-OF-DONE.md` — formal v1.0 quality gates.
- `ROADMAP.md` — milestone roadmap (this document).
- Updated `README.md` with v0.1.0 completion status, review references, and
  navigation links.

No shared-contract or platform-file changes.

---

## v0.2.0 — Verification Framework

**Status: Completed.**

Architecture Decision Record:
[DECISIONS/verification-framework-architecture.md](DECISIONS/verification-framework-architecture.md)

Planned deliverables:

- `shared/verification.md` — fifth shared contract. Structural integrity gate
  with three verification modes:
  - Quick Verification (mechanical integrity: SHA-256, file counts, PASS/FAIL).
  - Standard Verification (contractual completeness: rule audit, consistency
    audit, evidence presence, PASS/PASS WITH NOTES/BLOCKED/FAIL).
  - Certification Report (formal archival artifact from a passed Standard
    Verification; not a verification level).
- OpenCode verification skill (`platforms/opencode/skills/verification/`):
  - Read-only permission model.
  - Common report format aligned with repository-review verdict model.
  - SHA-256, body-comparison, and structural audit commands.
- Updated MANIFEST with verification contract mapping.

No changes to existing shared contracts or platform adapters unless required
for verification integration.

---

## v0.3.0 — Reviewer verification permission enforcement

**Status: Completed.**

The original v0.3.0 roadmap scope (installation and workstation rollout) has
been deferred. A smaller, prerequisite milestone was identified: the reviewer
agent could not run Quick Verification without manual permission prompts for
7 of 14 required commands. The permission-enforcement gap became the v0.3.0
scope.

Implemented:

- Eight narrow read-only shell permissions added to the OpenCode reviewer:
  `find`, `test`, `wc`, `sha256sum`, `diff`, `cmp`, `grep`, `sed`.
- `verification` skill added to reviewer required skills.
- Active OpenCode controlled-copy synchronized separately and verified by
  SHA-256 equality.
- Quick Verification runs through the reviewer without permission prompts.
- All existing deny boundaries preserved (edit: deny, task: deny, Git writes
  denied, destructive commands denied, `sed -i*` denied).
- No dedicated verifier agent was introduced.

Architecture Decision Record:
[DECISIONS/release-v0.3.0.md](DECISIONS/release-v0.3.0.md)

Implementation review:
`.agent-work/reviews/review-agent-pack-v0.3-reviewer-verification-permissions.md`
(READY FOR REVIEW)

No shared-contract changes. No new platform adapters.

### Deferred from original v0.3.0 scope

The following items from the original v0.3.0 roadmap (Installation and
workstation rollout) remain **unresolved pre-v1.0 work**. They are deferred
to a future milestone between the Codex Platform Assessment and v1.0.0 and
are not implemented or redesigned here:

- Deterministic OpenCode installation procedure.
- Backup and rollback procedure.
- Home workstation installation, verification, and certification.
- Office workstation installation, verification, and certification.
- Installation documentation in README.

---

## v0.4.0 — Task Execution Policy and builder agent

**Status: Completed.**

The original v0.4.0 roadmap entry (Codex Platform Assessment) was superseded
by the accepted Architecture Change Proposal for the task-execution-policy
contract. The execution-policy foundation was delivered first so that the
Codex assessment can evaluate both platforms against the same shared
definitions (per
[DECISIONS/architecture-change-proposal-task-execution-policy.md](DECISIONS/architecture-change-proposal-task-execution-policy.md)).

Delivered:

- `shared/task-execution-policy.md` — sixth authoritative shared contract.
  Defines task classes (critical, standard, mechanical), execution profiles
  (critical, review, balanced, light), role separation, the runtime
  substitution invariant, supplied-routing validation, and the
  delegated-prompt minimum contract.
- `platforms/opencode/agents/builder.md` — generic implementation agent for
  controlled repository changes. Edit allowed; commit/push denied.
- `DECISIONS/architecture-change-proposal-task-execution-policy.md` —
  accepted Architecture Change Proposal (independent review: PASS).
- Updated `VERSION` (0.4.0), `MANIFEST.md`, `ARCHITECTURE.md`,
  `CAPABILITY_MATRIX.md`, `DEFINITION-OF-DONE.md`, `README.md`, and
  `shared/verification.md`.
- `tests/test_agent_rollout.py` expanded with builder rollout coverage
  (repository validation: PASS, 33 tests).

Reviews:

- Builder agent implementation review: PASS
  (`.agent-work/reviews/review-implement-opencode-builder-agent-v0.4.0.md`)
- Task-execution-policy foundation review:
  (`.agent-work/reviews/review-implement-task-execution-policy-foundation.md`)
- Architecture Change Proposal independent review: PASS
  (`.agent-work/reviews/independent-review-task-execution-policy-acp.md`)

---

## Codex Platform Assessment

**Status: Planned.**

Planned deliverables:

- Codex Platform Assessment — evaluate Codex CLI against the Capability Matrix.
- Evidence-based capability inventory. No invented features.
- Decision: proceed with Codex adapter, defer, or document as unsupported.

---

## Codex adapter

**Status: Planned.**

Planned deliverables:

- Codex adapter implementing the frozen Adapter API.
- Skills mapping: NeuralEngine → Codex skill, review → Codex review mode,
  validation → Codex validation, diagnostics → Codex diagnostics.
- Task execution convention appropriate for Codex.
- NeuralEngine integration appropriate for Codex.
- `platforms/codex/` populated, replacing placeholder README.
- Updated MANIFEST, README support matrix, ROADMAP, and CAPABILITY_MATRIX.
- Verification and certification of Codex adapter.
- Both platform adapters certified.

Codex-specific capabilities will not be invented. The adapter will map
existing shared contracts to the closest equivalent Codex constructs.

---

## Claude Code and Antigravity assessment

**Status: Planned.**

Planned deliverables:

- Claude Code adapter mapping the four shared contracts to Claude Code
  configuration format.
- Antigravity capability assessment: determine which shared contracts can be
  represented and which cannot.
- For any contract Antigravity cannot support, document the limitation with
  evidence rather than inventing unsupported features.
- `platforms/claude/` and `platforms/antigravity/` populated or explicitly
  documented as unsupported with reasons.
- Updated MANIFEST, README support matrix, and ROADMAP.

Support statuses will be evidence-based. A platform may be documented as
"Assessed — Unsupported" with a clear explanation.

---

## v1.0.0 — Stable Agent Pack

Exit criteria defined in
[DECISIONS/architecture-freeze-v1.0.md](DECISIONS/architecture-freeze-v1.0.md):

- OpenCode adapter remains certified.
- Codex adapter implemented and certified.
- Both adapters implement the same shared contract semantics.
- Cross-platform validation completed.
- No unresolved architecture blockers.
- Installation/update/rollback documented for both platforms.
- v1.0 release assessment and release decision completed.
- Agent Pack can support resumed NeuralEngine development without architecture
  changes.

---

## Beyond v1.0

Intentionally not planned in this roadmap. Post-v1.0 evolution will be guided
by operational experience, platform changes, and identified maintenance needs.
Candidates include:

- Generators or include mechanisms if manual drift becomes a burden.
- Additional platforms if demand and capability alignment are demonstrated.
- Contract evolution if the originating skills or global policies change
  substantively.
