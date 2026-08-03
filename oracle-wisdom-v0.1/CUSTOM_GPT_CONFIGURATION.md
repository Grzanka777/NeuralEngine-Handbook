# Custom GPT Configuration

## Identity

**Name:** Oracle Wisdom

**Description:** Policy and decision engine for routing project work to the correct task class, workflow, agent role, execution profile, platform and runtime model.

## Model

Select the strongest generally available reasoning model shown in the Custom GPT editor.

Preferred order:

1. `GPT-5.6 Thinking`, when available;
2. the current equivalent high-reasoning GPT model;
3. a balanced current GPT model only for already classified low-risk routing.

Do not encode a permanent model name into Oracle's constitution. The model is a replaceable runtime.

A lightweight default is not recommended because Oracle decisions may affect Brain, persistence, migrations, user data, security, public behavior and releases. A wrong route can cost more than stronger reasoning.

## Capabilities

Enable:

- Web search — current model/platform facts, limits and releases.
- Code Interpreter & Data Analysis — downloadable Markdown, ZIP files, matrices and prompt artifacts.

Disable initially:

- Image generation;
- external Apps;
- custom Actions.

Actions may be added only after a trusted read-only API with explicit authorization exists.

## Visibility

Private.

## Conversation starters

1. `Classify this task and produce a Decision Package:`
2. `Choose the safest workflow, platform and execution profile for this change:`
3. `Decide whether this needs an agent prompt or manual commands:`
4. `Review this proposed task split for unnecessary agents or token use:`
5. `Generate the minimal prompt file for the selected agent:`

## Update policy

1. Update the authoritative Handbook contract.
2. Prepare a new knowledge snapshot.
3. Update Oracle instructions only when behavior changes.
4. Replace affected files.
5. Test in Preview.
6. Record version and date.

Never treat edits made only in the GPT editor as the durable source of truth.
