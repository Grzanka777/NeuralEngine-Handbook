# GitHub Copilot CLI and VS Code Platform

**Status:** NeuralEngine thin adapter implemented for GitHub Copilot CLI and
GitHub Copilot in VS Code with documented limitations.

This is one bounded provider projection of
agent-pack/shared/neuralengine.md. It is a post-v1.0 extension of the Agent
Pack and does not change the v1.0 platform freeze. It does not modify
NeuralEngine runtime behavior, Brain persistence, schemas, APIs, or user-global
Copilot configuration.

## Adapter files

- skills/neuralengine/SKILL.md — Copilot CLI project skill projection with the
  required name and description front matter.

The skill body is a controlled copy of the shared contract. Drift validation
requires the body after front matter removal to remain byte-equal to
agent-pack/shared/neuralengine.md.

## Manual installation mapping

Installation is explicit and manual:

skills/neuralengine/SKILL.md
→ <target-repository>/.github/skills/neuralengine/SKILL.md

Copilot CLI and VS Code natively discover project skills and decide when to
load them from their descriptions. No additional project instruction pointer is
added: a duplicate pointer would repeat shared policy without adding a native
loading requirement. The existing skill is deliberately reused by both hosts;
there is no second semantic Copilot skill copy.

Existing AGENTS.md, .github/copilot-instructions.md, and
.github/instructions/**/*.instructions.md files in a target repository remain
separate host instruction mechanisms. VS Code Copilot Chat supports these
repository instruction types; the host may enable or disable custom
instructions.

## Discovery and permission boundaries

- GitHub documents project skills under .github/skills, .claude/skills, and
  .agents/skills, and VS Code documents the same project locations. This
  adapter uses the shared .github/skills path.
- SKILL.md requires YAML name and description metadata. Optional allowed-tools
  is deliberately omitted so the host retains its normal approval behavior.
- Copilot CLI and VS Code Copilot have native repository instruction mechanisms;
  this adapter does not add or duplicate one.
- GitHub documents read-only shell and file operations as automatically allowed;
  edits, destructive commands, URL access, and other modifying tools require
  explicit approval for the CLI. VS Code agent permissions are session and
  host controlled; terminal commands and file edits may require approval.
- No `copilot` executable is currently available on `PATH`. A user-local
  GitHub Copilot CLI binary may exist outside `PATH`; installation and PATH
  behavior remain target-environment concerns.
- No live Copilot session, project-skill loading, automatic adherence, or
  model-driven execution was verified.
- VS Code, the Copilot extension, agent mode, the neural executable, PATH, Brain
  access, and command behavior must be verified in each target environment.

This bounded support covers GitHub Copilot CLI and GitHub Copilot in VS Code
only. No JetBrains, Visual Studio, GitHub.com Copilot Chat, or other editor or
web-surface support is claimed.

The adapter grants no additional read, write, Brain-write, staging, commit,
push, merge, tag, release, or publication authority.

No automatic installation or Brain write is performed.
