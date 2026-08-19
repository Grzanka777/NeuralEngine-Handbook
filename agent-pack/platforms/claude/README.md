# Claude Code/Desktop Code Platform

**Status:** NeuralEngine thin adapter implemented for Claude Code CLI and the
Claude Desktop Code surface with documented limitations.

This is one bounded provider projection of
agent-pack/shared/neuralengine.md. It is a post-v1.0 extension of the Agent
Pack and does not change the v1.0 platform freeze. It does not modify
NeuralEngine runtime behavior, Brain persistence, schemas, APIs, or user-global
Claude configuration.

## Adapter files

- CLAUDE.md — minimal Claude project-instruction pointer; merge this pointer
  into a target repository's project instructions without replacing unrelated
  rules.
- skills/neuralengine/SKILL.md — Claude project skill projection with only the
  required name and description front matter.

The skill body is a controlled copy of the shared contract. Drift validation
requires the body after front matter removal to remain byte-equal to
agent-pack/shared/neuralengine.md.

## Manual installation mapping

Installation is explicit and manual, consistent with the Agent Pack
architecture:

skills/neuralengine/SKILL.md
→ <target-repository>/.claude/skills/neuralengine/SKILL.md

The CLAUDE.md content is a pointer to merge into the target repository's
project instructions. This package does not provide an installer, write to
user-global Claude configuration, or create a second semantic copy for the
Desktop Code surface.

## Discovery and boundaries

- Claude Code reads CLAUDE.md as its native project instruction file.
  AGENTS.md is not natively consumed; when a target repository already uses
  AGENTS.md, its CLAUDE.md may explicitly import it with the documented
  @AGENTS.md reference pattern.
- Claude Code project skills live at .claude/skills/<name>/SKILL.md. The same
  project skill is shared by Claude Code CLI and the Claude Desktop Code
  surface.
- Anthropic documents that Desktop Code uses the same underlying engine and
  shares CLAUDE.md files, skills, settings, and other local configuration.
- CLI and Desktop Code remain different host surfaces. The CLI supports
  scripting and the Agent SDK; Desktop provides a graphical workflow and does
  not provide the CLI-only dontAsk mode. Desktop is documented for macOS and
  Windows, not Linux.
- Local verification found Claude Code 2.1.152. The local CLI help and version
  were read without starting a model session. Desktop runtime was not locally
  available on this Linux host.
- The neural executable, PATH, Brain access, and command behavior must be
  verified in each target environment. Project instructions and skills shape
  model behavior; host permission settings remain the enforcement boundary.

The adapter grants no additional read, write, Brain-write, staging, commit,
push, merge, tag, release, or publication authority.

No automatic installation or Brain write is performed.
