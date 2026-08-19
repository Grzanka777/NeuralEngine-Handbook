# Goose CLI/Desktop Platform

**Status:** NeuralEngine thin adapter implemented for Goose CLI/Desktop with
documented limitations.

This is one bounded provider projection of
agent-pack/shared/neuralengine.md. It is a post-v1.0 extension of the Agent
Pack and does not change the v1.0 platform freeze. It does not modify
NeuralEngine runtime behavior, Brain persistence, schemas, APIs, or user-global
Goose configuration.

## Adapter files

- AGENTS.md — minimal project-instruction pointer; merge this pointer into a
  target repository's project instructions without replacing unrelated rules.
- skills/neuralengine/SKILL.md — Goose-compatible project skill projection with
  only the required name and description front matter.

The skill body is a controlled copy of the shared contract. Drift validation
requires the body after front matter removal to remain byte-equal to
agent-pack/shared/neuralengine.md.

## Manual installation mapping

Installation is explicit and manual, consistent with the Agent Pack
architecture:

skills/neuralengine/SKILL.md
→ <target-repository>/.agents/skills/neuralengine/SKILL.md

The AGENTS.md content is a pointer to merge into the target repository's
project instructions. This package does not provide an installer, write to
user-global Goose configuration, or create a second semantic copy for Desktop.

## Discovery and limitations

- Goose documents AGENTS.md and .goosehints as project context files.
- Goose documents project Agent Skills under .agents/skills/<name>/SKILL.md;
  the .agents/skills projection is therefore shared by the CLI and Desktop
  slice.
- Goose CLI and Desktop expose host-controlled shell/tool permissions. The
  adapter grants no additional read, write, Brain-write, staging, commit, push,
  merge, tag, release, or publication authority.
- The neural executable, PATH, Brain access, and command behavior must be
  verified in each target environment. Desktop launchers may use a different
  environment from an interactive shell.
- Local verification found Goose CLI 1.45.0; Desktop version/help probing was
  not independently available because the Electron launcher attempted read-only
  host state and graphics/session initialization.

No automatic installation or Brain write is performed.
