# Oracle Wisdom v0.1

## Purpose

Oracle Wisdom is a private Custom GPT that acts as the operational decision engine for the user's AI-assisted project work.

It does not implement code, edit repositories, perform reviews, or replace project chats. It decides the safest and most efficient way to execute a task.

## Core output

For each actionable project task, Oracle produces a **Decision Package** containing task class, workflow, agent role, execution profile, platform, runtime model, reasoning level, validation, review requirements and the next executable artifact.

## Canonical example

[`oracle-decision-package-persisted-model-cli-critical-corrected.md`](oracle-decision-package-persisted-model-cli-critical-corrected.md) is the canonical worked Decision Package example for v0.1. It demonstrates a full critical-class package for a persisted NeuralEngine model and CLI change, including workflow, validation, risks, safeguards and artifact paths.

## Recommended Custom GPT configuration

- Name: `Oracle Wisdom`
- Description: `Policy and decision engine for routing project work to the right workflow, agent, platform and model.`
- Recommended model: strongest generally available reasoning model in the GPT editor; prefer `GPT-5.6 Thinking` when available.
- Web search: enabled.
- Code Interpreter & Data Analysis: enabled.
- Image generation: disabled.
- Apps or Actions: disabled for v0.1.
- Visibility: private.

The model is a recommendation, not an architectural dependency.

## Knowledge

Upload the Markdown files from `knowledge/`. Do not upload whole repositories or mutable Brain state. NeuralEngine-Handbook remains the durable source of truth; the Custom GPT files are a versioned snapshot.

## Known limitations

Oracle Wisdom v0.1:

- is a private Custom GPT package;
- does not execute repository changes;
- does not replace project-chat validation;
- does not act as builder or reviewer;
- has no automatic Brain-write authority;
- has no Actions/API automation;
- has no automated scheduling;
- has no persistent memory guarantee beyond uploaded knowledge and current conversation context;
- does not automatically select or switch OpenCode agents;
- does not directly manage provider accounts, quotas, credentials, or secrets;
- requires manual Custom GPT setup and manual testing.

## Version

`0.1.0` is the canonical semantic version of Oracle Wisdom. The `v0.1` in the directory name (`oracle-wisdom-v0.1/`) is the milestone shorthand. Both refer to the same first experimental release. The directory name is kept as-is because the accepted Agent Pack boundary ADR (`agent-pack/DECISIONS/oracle-wisdom-agent-pack-boundary.md`) references it.

## Removal

To remove Oracle Wisdom:

1. Optionally remove the uploaded knowledge files from the Custom GPT first.
2. Delete the private Custom GPT in the ChatGPT UI.

The repository files under `oracle-wisdom-v0.1/` remain the source snapshot and are unaffected by removal of the Custom GPT.
