# Platform and Model Routing

## OpenCode

Use as the flexible default when multiple runtime models, Agent Pack skills, integrated interactive work or quota optimization matter.

## Codex CLI

Use for direct terminal-first GPT coding execution and critical implementation when quota is available and repository workflow is configured.

## Manual

Use when commands are safer, faster and deterministic.

## ChatGPT

Use for routing, synthesis, explanation and artifact generation without repository execution.

## Current operational map

| Execution profile | Preferred platform | Preferred runtime | Fallback |
|---|---|---|---|
| critical | Codex CLI | strongest available GPT coding/reasoning model | OpenCode with equivalent high-reasoning GPT |
| review | OpenCode | DeepSeek V4 Pro Max | strongest available GPT reasoning model |
| balanced | OpenCode | DeepSeek V4 Pro Max or balanced current GPT | Codex medium reasoning |
| light | OpenCode or Manual | light current model | deterministic manual commands |

## User-observed current access

- GPT-5.6 Sol Medium through Codex and OpenCode.
- DeepSeek V4 Pro Max through OpenCode.

Treat availability as current only when confirmed in the active platform.

## Constraints

- Never weaken workflow because the preferred model is unavailable.
- Never invent a model identifier or CLI configuration.
- Do not encode model names into agents or prompts.
- State a fallback or leave model unresolved when availability is unknown.
