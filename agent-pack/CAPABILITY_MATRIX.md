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

| Capability | OpenCode | Codex CLI |
|---|---|---|
| **Agents / roles** | SUPPORTED — `arch-data-engineer` (primary, full capabilities), `reviewer` (read-only, restricted permissions) | NOT YET ASSESSED |
| **Skills / contracts** | SUPPORTED — 5 skills: neuralengine, repository-review, python-project-validation, arch-linux-diagnostics, verification | NOT YET ASSESSED |
| **Global instructions** | SUPPORTED — `neuralengine-usage.md` loaded via `opencode.json` instructions array | NOT YET ASSESSED |
| **Permissions** | SUPPORTED — Agent-level permission blocks with allow/deny/ask for edit, bash, task, tools. Reviewer enforces read-only. | NOT YET ASSESSED |
| **Shell execution** | SUPPORTED — Unrestricted bash for `arch-data-engineer`. Restricted allowlist for `reviewer`. | NOT YET ASSESSED |
| **Repository instructions** | SUPPORTED — `AGENTS.md`, `CODEX.md`, `VISION.md`, `CONTEXT.md`, `pyproject.toml` awareness built into agent rules | NOT YET ASSESSED |
| **NeuralEngine CLI** | SUPPORTED — `neural status` and `neural search` available and used in all reviews | NOT YET ASSESSED |
| **Review** | SUPPORTED — `repository-review` skill, reviewer agent with read-only permissions, formal review format with verdict/checkpoint/validation/scope/findings | NOT YET ASSESSED |
| **Verification** | SUPPORTED — reviewer agent with `verification` skill and enforced read-only command permissions (8 additional allow patterns: find, test, wc, sha256sum, diff, cmp, grep, sed). Quick Verification runs without permission prompts. | NOT YET ASSESSED |
| **Certification** | SUPPORTED — Certification Report template, 3 verdicts (CERTIFIED/CERTIFIED WITH NOTES/NOT CERTIFIED), collision-safe naming, `.agent-work/certifications/` convention | NOT YET ASSESSED |
| **Model selection** | SUPPORTED — Model configured in OpenCode runtime. Agent Pack is model-agnostic (DeepSeek V4 Pro Max, GPT-5.6 Sol Medium, others) | NOT YET ASSESSED |
| **Non-interactive execution** | SUPPORTED WITH LIMITATIONS — Bash commands execute non-interactively. Human confirmation required only for restricted operations per permission model. | NOT YET ASSESSED |
| **Artifact generation** | SUPPORTED — Review artifacts, certification reports, documentation files generated as markdown. No code generation or template engines. | NOT YET ASSESSED |

## Codex CLI assessment notes

All Codex capabilities are `NOT YET ASSESSED`. The Codex Platform Assessment
(task: `.agent-work/prompts/assess-codex-platform-v1.0.md`) is the designated
authority to evaluate Codex against this matrix.

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

## OpenCode evidence sources

OpenCode capabilities are derived from:

- `platforms/opencode/opencode.json` — global instructions, default agent.
- `platforms/opencode/agents/arch-data-engineer.md` — primary agent with full
  capabilities, bash access, NeuralEngine awareness, repository awareness,
  validation workflow.
- `platforms/opencode/agents/reviewer.md` — read-only reviewer agent with
  explicit deny rules for destructive operations.
- `platforms/opencode/skills/` — 5 skill files implementing shared contracts.
- `platforms/opencode/verification-permissions.md` — permission requirements
  documentation.
- `.agent-work/reviews/` — review artifacts demonstrating review, verification,
  and NeuralEngine evidence workflows.
- `.agent-work/certifications/` — certification artifacts.

All OpenCode capability claims are verifiable from these sources.
