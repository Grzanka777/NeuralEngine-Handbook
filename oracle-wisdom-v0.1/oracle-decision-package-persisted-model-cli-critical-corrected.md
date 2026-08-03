# Oracle Decision Package

## Decision

Proceed

## Project

NeuralEngine — Priority 1.

## Task

Implement a critical domain change affecting a persisted NeuralEngine model and
public CLI behavior, without committing or pushing.

## Task class

`critical`

Persistence, domain behavior, persisted schema and public CLI behavior each
independently trigger the critical classification. The highest triggered class
governs the complete task.

## Workflow

1. Repository-state and authority assessment.
2. NeuralEngine status and knowledge-search decision.
3. Builder implementation.
4. Complete targeted and regression validation.
5. Independent read-only review with a dedicated review artifact.
6. Remediation of material findings.
7. Final validation and staging audit.
8. Stop before commit or push.

Post-push verification is **deferred, not waived**. It becomes mandatory only
after a separately authorized commit and push.

## Agent role

`builder`

A separate `reviewer` role is required after implementation. The builder must
not act as its own independent reviewer.

## Execution profile

`critical`

Use the strongest available reasoning, conservative scope, explicit uncertainty
and complete evidence because persistence, domain contracts and data integrity
are involved.

## Platform

`Codex CLI`

Codex CLI is the preferred route for terminal-first critical implementation
when quota is available and the repository workflow is configured.

OpenCode is the fallback only when it preserves the same critical profile,
scope controls, validation and independent-review requirements.

## Runtime model

`GPT-5.6 Sol Medium`, subject to confirmation in the active Codex session.

Current capability records indicate access through Codex and OpenCode, but
availability must be verified at execution time. If unavailable, use the
strongest confirmed GPT coding/reasoning model without weakening the critical
workflow.

## Reasoning level

`high`

## Authority and checkpoint

The receiving NeuralEngine project chat must identify and use one newest
authoritative repository checkpoint covering:

- persisted model and domain contract;
- serialization and migration behavior;
- public CLI behavior;
- validation and compatibility requirements.

Current repository evidence and authoritative project contracts override this
package if they conflict.

This package becomes stale if the checkpoint, scope, platform availability or
repository state changes materially.

## Required validation

At minimum:

1. Run `neural status` before repository work.
2. Decide before editing whether prior decisions, experiences, knowledge or
   playbooks are relevant.
3. When relevant, run `neural search` and record:
   - the exact query;
   - returned IDs;
   - provenance;
   - implementation impact.
4. Validate persisted-model serialization and deserialization.
5. Validate compatibility with existing persisted data or execute the
   authoritative migration path.
6. Test invalid, missing, legacy and boundary-state handling.
7. Validate all changed CLI commands, arguments, output contracts, exit codes
   and failure behavior.
8. Run focused tests and the relevant full regression suite.
9. Inspect generated artifacts or fixtures for unintended persisted-format
   changes.
10. Produce an independent review report ordered by severity.
11. Perform `git diff`, `git diff --check`, `git status` and staging inspection.
12. Confirm that no commit and no push occurred.

Running `neural status` alone does not count as substantive NeuralEngine
knowledge use.

Any Brain write requires:

1. a proposed-record preview;
2. separate explicit user authorization;
3. no automatic lifecycle promotion.

## Risks and safeguards

Primary risks:

- persisted-data corruption;
- incompatible schema evolution;
- silent semantic drift;
- CLI contract breakage;
- unintended Brain mutation.

Required safeguards:

- minimize scope to the required domain, persistence, CLI and directly
  necessary tests;
- do not infer migration safety from passing unit tests alone;
- preserve rollback or recovery capability for persisted data;
- prohibit destructive migration against irreplaceable data;
- require explicit evidence for backward compatibility or an authoritative
  breaking-change decision;
- do not write to Brain without preview and separate authorization;
- do not commit or push;
- do not broaden into unrelated refactoring;
- require independent review before considering the implementation complete.

## Artifact

A self-contained builder prompt is required.

Final prompt generation belongs in the NeuralEngine project chat after it
verifies repository state and identifies the latest authoritative checkpoint.

The prompt must require a dedicated review artifact and explicitly prohibit
commit and push.

### Required artifact paths

```text
.agent-work/prompts/neuralengine-persisted-model-cli-critical.md
.agent-work/reviews/neuralengine-persisted-model-cli-critical-review.md
```

### Launch instruction

```text
Read and execute:
.agent-work/prompts/neuralengine-persisted-model-cli-critical.md
```

Do not repeat the prompt body in the terminal task or surrounding response.

## Rationale

Manual execution is insufficient because the task requires repository
inspection, architectural judgment, persistence-integrity analysis,
implementation, migration or compatibility validation and coordinated CLI
verification.

A critical-profile builder materially reduces implementation risk, while an
independent reviewer provides the required separation of duties.

The route preserves full controls and ends at a validated, reviewed and
uncommitted working tree. Post-push verification remains pending until the user
separately authorizes commit and push.
