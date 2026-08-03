# Agent Pack v0.4.0 — Released

## Highlights

Agent Pack v0.4.0 adds the **Task Execution Policy** as the sixth
authoritative shared contract and introduces the generic **builder agent**
for the OpenCode platform. The release establishes the durable
execution-policy vocabulary (task classes, execution profiles, role
separation, runtime substitution invariant, supplied-routing validation,
delegated-prompt minimum contract) that the Agent Pack, Oracle routing, and
platform adapters share.

This release was governed by the accepted Architecture Change Proposal
`DECISIONS/architecture-change-proposal-task-execution-policy.md`, which
replaced the original v0.4.0 roadmap entry (Codex Platform Assessment). The
execution-policy foundation was delivered first so that the Codex assessment
can evaluate both platforms against the same shared definitions.

## New shared contract

### `shared/task-execution-policy.md`

The sixth authoritative Agent Pack shared contract. Defines:

- **Task classes** — `critical`, `standard`, `mechanical`; highest
  materially triggered class wins; model availability never changes class.
- **Execution profiles** — `critical`, `review`, `balanced`, `light`;
  behavioral expectations for one execution stage, never model mappings.
- **Role separation** — `planner`, `builder`, `reviewer`, `mechanical`;
  roles describe responsibility, never model identity.
- **Runtime substitution invariant** — models are replaceable runtimes;
  substitution preserves the execution profile; workflow safeguards are never
  weakened.
- **Supplied-routing validation** — agents validate the supplied execution
  contract, stop on material mismatch, and never silently lower class, role,
  profile, validation, or authorization boundaries.
- **Delegated-prompt minimum contract** — ten required elements for every
  delegated agent prompt.

The contract is platform-agnostic. It contains no concrete model names,
quotas, subscriptions, portfolio priorities, or capability snapshots — those
remain Oracle Wisdom operational context (per
`DECISIONS/oracle-wisdom-agent-pack-boundary.md`).

## New builder agent

### `platforms/opencode/agents/builder.md`

A generic implementation agent for controlled repository changes:

- Edit allowed; commit/push denied.
- Task delegation denied.
- Scoped bash allowlist for read-only verification commands.
- No concrete model names in the agent definition.
- `arch-data-engineer` remains the default agent for backward compatibility;
  `builder` is the recommended agent for generic implementation tasks.

## Architecture decisions

- `DECISIONS/architecture-change-proposal-task-execution-policy.md` —
  accepted Architecture Change Proposal defining the contract content,
  scope, exclusions, verification delta, and MANIFEST update. Independent
  review: PASS.
- The proposal preserved the Oracle Wisdom ↔ Agent Pack boundary: Agent Pack
  owns durable execution vocabulary; Oracle retains operational routing
  (model selection, platform selection, quotas, portfolio priorities,
  Decision Package, Handoff Protocol).

## What changed

- `shared/task-execution-policy.md` — new sixth shared contract (335 lines).
- `platforms/opencode/agents/builder.md` — new builder agent (420 lines).
- `DECISIONS/architecture-change-proposal-task-execution-policy.md` — new
  accepted ACP (643 lines).
- `VERSION` — `0.3.0` → `0.4.0`.
- `MANIFEST.md` — task-execution-policy mapping added; `agents/builder.md`
  listed as platform-specific file.
- `ARCHITECTURE.md`, `CAPABILITY_MATRIX.md`, `DEFINITION-OF-DONE.md`,
  `shared/verification.md`, `platforms/opencode/verification-permissions.md`
  — updated for the sixth contract and builder agent.
- `tests/test_agent_rollout.py` — expanded with builder rollout coverage
  (17 tests covering clean install, overwrite, backup, rollback, idempotency,
  equality, frontmatter integrity, model-name absence, and agent
  coexistence).

## What did not change

- Existing five shared contracts unchanged.
- `platforms/opencode/agents/reviewer.md` and
  `arch-data-engineer.md` unchanged.
- `opencode.json` unchanged (default agent stays `arch-data-engineer`).
- No new platform adapters; Codex, Claude Code, and Antigravity remain
  placeholders.
- No automatic installation, generators, or symlink synchronization.

## Validation evidence

- Repository validation: PASS (33 tests) — `ruff format --check`,
  `ruff check`, `mypy src tests`, `pytest`.
- Builder agent implementation review: PASS
  (`.agent-work/reviews/review-implement-opencode-builder-agent-v0.4.0.md`).
- Task Execution Policy foundation review: READY FOR INDEPENDENT REVIEW
  (`.agent-work/reviews/review-implement-task-execution-policy-foundation.md`).
- ACP independent review: PASS
  (`.agent-work/reviews/independent-review-task-execution-policy-acp.md`).
- No dedicated v0.4.0 Certification Report exists; the v0.3.0 certification
  remains the last formal certification checkpoint.

## Compatibility

- Base release: Agent Pack v0.3.0.
- Implementation commit: `f5bd1a6fcc2d3e408a0b1aed698f180ce8cc0ff7`.
- Merge checkpoint: `63d49e2ba42c806354546c80f90c8df16a2e702e`.
- No breaking changes from v0.3.0 for existing shared contracts or platform
  files.
- No Brain write.

## Known limitations

- Codex, Claude Code, and Antigravity adapters remain placeholders.
- **Codex adapter support is not claimed.** The Codex Platform Assessment is
  the next planned milestone and has not been executed.
- **Installation and workstation rollout are not complete.** The deferred
  v0.3.0 items (deterministic installation procedure, backup/rollback,
  home/office workstation verification and certification, installation
  documentation) remain unresolved pre-v1.0 work.
- No automatic installation.
- No generators.
- No symlink synchronization.
- No dedicated verifier agent.
- Oracle Wisdom v0.1 knowledge files are not updated in this release; the
  boundary ADR explicitly permits snapshot updates to be deferred.

## Upgrade notes

No breaking changes from v0.3.0. All existing shared contracts and platform
files are unchanged.

To upgrade:

1. Check out the current `main` branch (contains the v0.4.0 merge).
2. Review the new shared contract:
   ```text
   agent-pack/shared/task-execution-policy.md
   ```
3. Optionally copy the new builder agent to the OpenCode agents directory
   (manual, explicit, with backup and SHA-256 verification per README
   §Controlled manual copy):
   ```text
   cp agent-pack/platforms/opencode/agents/builder.md \
      ~/.config/opencode/agents/builder.md
   ```
4. Run repository validation to confirm structural integrity.
