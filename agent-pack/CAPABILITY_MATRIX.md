# Agent Pack v0.3.0 Capability Matrix

## Legend

| State | Meaning |
|---|---|
| `SUPPORTED` | Fully implemented and verified with current repository evidence. |
| `SUPPORTED WITH LIMITATIONS` | Implemented but with documented constraints. |
| `NOT SUPPORTED` | Capability is absent or cannot be provided by the platform. |
| `NOT APPLICABLE` | Capability concept does not apply to this platform. |
| `NOT YET ASSESSED` | No assessment has been performed. Evidence is absent. |

## Matrix

| Capability | OpenCode | Codex CLI | Goose CLI/Desktop | Claude Code/Desktop Code | Copilot CLI |
|---|---|---|---|---|---|
| **Agents / roles** | SUPPORTED — `builder` (generic implementation), `arch-data-engineer` (specialist, scoped permissions), `reviewer` (read-only, restricted permissions), `planner` (read-only planning and routing), `mechanical` (deterministic low-judgment operations) | NOT YET ASSESSED — outside this NeuralEngine-only slice | NOT YET ASSESSED — custom agents are outside this bounded slice | NOT YET ASSESSED — custom agents are outside this bounded slice | NOT YET ASSESSED — custom agents are outside this bounded slice |
| **Skills / contracts** | SUPPORTED — 5 skills: neuralengine, repository-review, python-project-validation, arch-linux-diagnostics, verification | SUPPORTED WITH LIMITATIONS — NeuralEngine contract projection only; other contracts remain unmapped | SUPPORTED WITH LIMITATIONS — NeuralEngine contract projection only; other contracts remain unmapped | SUPPORTED WITH LIMITATIONS — NeuralEngine contract projection only; other contracts remain unmapped | SUPPORTED WITH LIMITATIONS — NeuralEngine contract projection only; other contracts remain unmapped |
| **Global instructions** | SUPPORTED — `neuralengine-usage.md` loaded via `opencode.json` instructions array | SUPPORTED WITH LIMITATIONS — short `AGENTS.md` pointer; Codex CLI runtime discovery not exercised here | SUPPORTED WITH LIMITATIONS — short `AGENTS.md` pointer; Desktop launcher discovery remains environment-dependent | SUPPORTED WITH LIMITATIONS — native `CLAUDE.md` pointer; Desktop Code shares project configuration | SUPPORTED WITH LIMITATIONS — CLI instruction locations are documented; no extra pointer is required by the skill mechanism |
| **Permissions** | SUPPORTED — Agent-level permission blocks with allow/deny/ask for edit, bash, task, tools. Reviewer enforces read-only. | SUPPORTED WITH LIMITATIONS — Codex host sandbox/approval controls remain authoritative; no adapter write authority | SUPPORTED WITH LIMITATIONS — Goose host permission/approval controls remain authoritative; no adapter write authority | SUPPORTED WITH LIMITATIONS — Claude host permission modes remain authoritative; no adapter write authority | SUPPORTED WITH LIMITATIONS — read-only tools are automatic; modifying tools require host approval; no adapter write authority |
| **Shell execution** | SUPPORTED — Scoped bash allowlist for `arch-data-engineer` (read-only diagnostics and validation; commit, push, destructive Git/filesystem/partitioning commands, and Ruff auto-fix denied). Restricted allowlist for `reviewer`. | SUPPORTED WITH LIMITATIONS — `neural` commands are ordinary host shell commands; executable/PATH/runtime behavior not verified | SUPPORTED WITH LIMITATIONS — Developer shell tools are documented; executable/PATH/runtime behavior is target-environment dependent | SUPPORTED WITH LIMITATIONS — CLI shell execution is available; Desktop/local environment and `neural` availability remain target-dependent | SUPPORTED WITH LIMITATIONS — CLI shell execution is documented; target `neural` availability not locally verified |
| **Repository instructions** | SUPPORTED — `AGENTS.md`, `CODEX.md`, `VISION.md`, `CONTEXT.md`, `pyproject.toml` awareness built into agent rules | SUPPORTED WITH LIMITATIONS — Codex CLI native `AGENTS.md` pointer for substantive/consequential work | SUPPORTED WITH LIMITATIONS — Goose project context files are documented; exact Desktop conflict precedence remains unverified | SUPPORTED WITH LIMITATIONS — `CLAUDE.md` is native; `AGENTS.md` requires an explicit import/reference | SUPPORTED WITH LIMITATIONS — `AGENTS.md` and `.github/copilot-instructions.md` are documented CLI instruction locations; combined precedence is not a total order |
| **NeuralEngine CLI** | SUPPORTED — `neural status` and `neural search` available and used in all reviews | SUPPORTED WITH LIMITATIONS — projection preserves `neural status`, targeted retrieval, and read-only boundaries; target installation not verified | SUPPORTED WITH LIMITATIONS — projection preserves `neural status`, targeted retrieval, and read-only boundaries; target installation and Desktop command availability not verified | SUPPORTED WITH LIMITATIONS — projection preserves `neural status`, targeted retrieval, and read-only boundaries; Desktop Code runtime availability not locally verified | SUPPORTED WITH LIMITATIONS — projection preserves `neural status`, targeted retrieval, and read-only boundaries; target installation not locally verified |
| **Review** | SUPPORTED — `repository-review` skill, reviewer agent with read-only permissions, formal review format with verdict/checkpoint/validation/scope/findings | NOT YET ASSESSED | NOT YET ASSESSED — outside this bounded slice | NOT YET ASSESSED — outside this bounded slice | NOT YET ASSESSED — outside this bounded slice |
| **Verification** | SUPPORTED — reviewer agent with `verification` skill and enforced read-only command permissions (8 additional allow patterns: find, test, wc, sha256sum, diff, cmp, grep, sed). Quick Verification runs without permission prompts. | NOT YET ASSESSED | NOT YET ASSESSED — outside this bounded slice | NOT YET ASSESSED — outside this bounded slice | NOT YET ASSESSED — outside this bounded slice |
| **Certification** | SUPPORTED — Certification Report template, 3 verdicts (CERTIFIED/CERTIFIED WITH NOTES/NOT CERTIFIED), collision-safe naming, `.agent-work/certifications/` convention | NOT YET ASSESSED | NOT YET ASSESSED — outside this bounded slice | NOT YET ASSESSED — outside this bounded slice | NOT YET ASSESSED — outside this bounded slice |
| **Model selection** | SUPPORTED — Model configured in OpenCode runtime. Agent Pack is model-agnostic (DeepSeek V4 Pro Max, GPT-5.6 Sol Medium, others) | NOT YET ASSESSED | NOT YET ASSESSED — outside this bounded slice | NOT YET ASSESSED — outside this bounded slice | NOT YET ASSESSED — outside this bounded slice |
| **Non-interactive execution** | SUPPORTED WITH LIMITATIONS — Bash commands execute non-interactively. Human confirmation required only for restricted operations per permission model. | NOT YET ASSESSED | NOT YET ASSESSED — outside this bounded slice | NOT YET ASSESSED — outside this bounded slice | NOT YET ASSESSED — outside this bounded slice |
| **Artifact generation** | SUPPORTED — Review artifacts, certification reports, documentation files generated as markdown. No code generation or template engines. | NOT YET ASSESSED | NOT YET ASSESSED — outside this bounded slice | NOT YET ASSESSED — outside this bounded slice | NOT YET ASSESSED — outside this bounded slice |

## Codex CLI assessment notes

This implementation assesses only the bounded Codex CLI NeuralEngine slice.
The remaining Codex capabilities stay `NOT YET ASSESSED`. The provider-native
assessment at `.agent-work/reviews/review-provider-native-cross-agent-neuralengine-adapters.md`
is the authority for the host findings used by this slice.

The following rules apply to the Codex assessment:

1. Each capability must be assessed independently with repository-visible
   evidence (command output, configuration files, documentation).
2. Do not invent Codex capabilities. Use `NOT YET ASSESSED` where evidence
   is absent or insufficient.
3. Do not assume Codex supports a capability because OpenCode supports it.
4. Document every `NOT SUPPORTED` or `SUPPORTED WITH LIMITATIONS` finding
   with an explanation.
5. The completed matrix must enable a decision on whether Codex can implement
   the v1.0 Adapter API defined in
   [DECISIONS/architecture-freeze-v1.0.md](../DECISIONS/architecture-freeze-v1.0.md).

## Codex CLI evidence sources

The bounded Codex CLI NeuralEngine slice is derived from:

- `platforms/codex/AGENTS.md` — minimal project-instruction pointer.
- `platforms/codex/skills/neuralengine/SKILL.md` — controlled semantic
  projection of `shared/neuralengine.md` with Codex-required front matter.
- `MANIFEST.md` — shared-to-Codex mapping and controlled-copy boundary.
- `tests/test_agent_rollout.py` — focused front-matter, pointer, and semantic
  drift checks.

These files do not claim full Codex Adapter API support, Codex Desktop support,
or provider runtime installation.

## OpenCode evidence sources

OpenCode capabilities are derived from:

- `platforms/opencode/opencode.json` — global instructions, default agent.
- `platforms/opencode/agents/arch-data-engineer.md` — primary agent with scoped
  permissions, bash allowlist, NeuralEngine awareness, repository awareness,
  validation workflow.
- `platforms/opencode/agents/builder.md` — generic builder agent with scoped
  edit access, commit/push denial, task delegation denial, and validation
  command allowlist.
- `platforms/opencode/agents/reviewer.md` — read-only reviewer agent with
  explicit deny rules for destructive operations.
- `platforms/opencode/skills/` — 5 skill files implementing shared contracts.
- `platforms/opencode/verification-permissions.md` — permission requirements
  documentation.
- `.agent-work/reviews/` — review artifacts demonstrating review, verification,
  and NeuralEngine evidence workflows.
- `.agent-work/certifications/` — certification artifacts.

All OpenCode capability claims are verifiable from these sources.
