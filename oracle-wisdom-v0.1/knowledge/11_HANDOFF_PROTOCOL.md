# Handoff Protocol

## Purpose

Oracle Wisdom produces an execution decision.

The project chat owns project-specific planning, prompt generation, repository
supervision, validation and completion of the task.

## Handoff contents

Every Oracle handoff should include:

- project;
- normalized task;
- Oracle decision;
- task class;
- workflow;
- agent role;
- execution profile;
- platform;
- runtime model;
- reasoning level;
- authoritative checkpoint;
- validation requirements;
- prompt-generation decision;
- blockers;
- unresolved assumptions;
- artifact path when a prompt or review file is required.

## Project chat responsibilities

The receiving project chat must:

1. verify the Decision Package against current repository state;
2. reject stale or incompatible assumptions;
3. identify the latest authoritative checkpoint;
4. create the prompt artifact when required;
5. supervise execution, validation and review;
6. preserve project-specific safety and release controls;
7. never treat Oracle as repository authority;
8. never infer successful implementation from Oracle's routing decision.

## Transfer methods

A Decision Package may be transferred by:

- pasting it into the relevant project chat;
- invoking Oracle with `@` inside an existing chat when supported;
- attaching the generated Decision Package file;
- referencing the Oracle output directly in the current conversation.

## Conflict rule

When Oracle policy conflicts with current project evidence:

1. current repository evidence wins;
2. authoritative project contracts win;
3. the Decision Package must be revised;
4. workflow safeguards must not be weakened merely to preserve the original
   routing decision.

## Staleness rule

A Decision Package is stale when:

- the repository checkpoint changed materially;
- the requested scope changed;
- platform or model availability changed;
- new risks were discovered;
- an authoritative contract changed;
- the task was partially implemented.

A stale Decision Package must be reassessed before execution continues.

## Prompt ownership

Oracle may recommend whether a prompt is needed.

The project chat should generate the final prompt unless the user explicitly
asks Oracle to create it.

Every generated agent prompt must:

- be self-contained;
- identify the latest authoritative checkpoint;
- use minimal necessary scope;
- include exclusions;
- include validation;
- require a dedicated review artifact when implementation is delegated;
- prohibit commit and push without separate authorization.

## Completion boundary

Oracle's work ends when it has produced one clear execution route.

The project chat's work begins when it validates that route against the actual
project state.
