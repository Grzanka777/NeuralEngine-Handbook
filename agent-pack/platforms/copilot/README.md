# GitHub Copilot CLI Platform

**Status:** NeuralEngine thin adapter implemented for GitHub Copilot CLI with
documented limitations.

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

Copilot CLI natively discovers project skills and decides when to load them
from their descriptions. No additional project instruction pointer is added:
a duplicate pointer would repeat shared policy without adding a native loading
requirement. Existing AGENTS.md or .github/copilot-instructions.md files in a
target repository remain separate host instruction mechanisms.

## Discovery and permission boundaries

- GitHub documents project skills under .github/skills, .claude/skills, and
  .agents/skills. This adapter uses the GitHub-native .github/skills path.
- SKILL.md requires YAML name and description metadata. Optional allowed-tools
  is deliberately omitted so the host retains its normal approval behavior.
- Copilot CLI discovers repository instruction files in standard locations and
  combines applicable instructions. This adapter does not add or duplicate one.
- GitHub documents read-only shell and file operations as automatically allowed;
  edits, destructive commands, URL access, and other modifying tools require
  explicit approval.
- Local verification found no copilot binary. The gh copilot help command
  identified a preview wrapper that would download the CLI if absent; no
  download or session was started.
- The neural executable, PATH, Brain access, and command behavior must be
  verified in each target environment.

This is CLI-only support. No editor or web-surface support is claimed.

The adapter grants no additional read, write, Brain-write, staging, commit,
push, merge, tag, release, or publication authority.

No automatic installation or Brain write is performed.
