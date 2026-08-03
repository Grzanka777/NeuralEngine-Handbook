# Current Capabilities

## Purpose

This file records the currently available platforms, models, integrations and
operational constraints used by Oracle Wisdom for routing decisions.

It is an operational snapshot, not a permanent contract.

## ChatGPT

- Plan: ChatGPT Plus.
- Oracle default model: GPT-5.6 Sol.
- Oracle intelligence mode: Thinking 5.6.
- Default thinking intensity: Standard.
- Web search: available.
- Code Interpreter & Data Analysis: available.
- Custom GPT knowledge is static and must be updated manually.
- Custom GPT does not use persistent memory from other chats.
- Oracle Actions are not configured.
- Direct repository access from Oracle is unavailable.

## OpenCode

- Default flexible terminal agent environment.
- ChatGPT Plus is connected.
- DeepSeek V4 Pro Max is available.
- GPT-5.6 Sol Medium is available.
- Agent Pack integration is available.
- Default agent: arch-data-engineer.
- Reviewer must be selected explicitly.
- Models may be changed without changing agent roles or workflow.

## Codex CLI

- Terminal-first implementation platform.
- Default reasoning level: medium.
- High reasoning is reserved for difficult architecture, migrations, security,
  Brain, persistence and data-integrity work.
- Quota availability must be considered before routing.
- Codex agents do not commit or push without separate explicit authorization.

## Current routing implications

- Critical implementation: prefer Codex CLI with the strongest available GPT
  coding/reasoning model when quota is available.
- Review: prefer OpenCode with DeepSeek V4 Pro Max.
- Standard implementation or documentation: prefer OpenCode with DeepSeek V4
  Pro Max or an equivalent balanced GPT model.
- Mechanical work: prefer Manual execution or OpenCode with a light model.

## Unsupported or deferred

- Claude Code is outside Agent Pack v1.0 scope.
- Antigravity is outside Agent Pack v1.0 scope.
- Oracle Actions are not configured.
- Direct Brain writes from Oracle are unavailable.
- Direct repository modifications from Oracle are unavailable.

## Update triggers

Update this file when any of the following changes:

- ChatGPT plan or model availability;
- OpenCode model access;
- Codex quota or model availability;
- Agent Pack platform scope;
- repository access;
- NeuralEngine API or Actions integration;
- authorization model.
