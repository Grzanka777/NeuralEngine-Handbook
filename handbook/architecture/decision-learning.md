# Decision Learning Architecture

## Status and purpose

This is accepted future architecture synchronized from NeuralEngine source commit `62c0dcb`.
It defines how NeuralEngine may become its own first real user by recording development choices,
their execution, factual results, and reviewed lessons. It does not describe implemented Decision
production behavior.

The intended learning path is:

```text
development event
→ Observation
→ Decision context
→ selected Decision
→ DecisionAction
→ DecisionOutcome
→ DecisionReview
→ Experience
→ Knowledge
→ Playbook improvement
```

Decision tracking complements the existing domain chain. It does not replace Observation,
Experience, Knowledge, Playbook, or any revision lifecycle concept.

## Staged immutable record family

The future record family is deliberately separated:

```text
Decision
→ DecisionAcceptance
→ DecisionAction
→ DecisionOutcome
→ DecisionReview
```

- `Observation` is a raw fact.
- `Decision` is a bounded choice with alternatives, proposed option, rationale, and provenance.
- `DecisionAcceptance` is explicit authorization to execute.
- `DecisionAction` is work performed under an accepted Decision.
- `DecisionOutcome` is the factual result and validation outcome.
- `DecisionReview` is an assessment with candidate lessons.
- `Experience` is interpreted operational learning.
- `Knowledge` is generalized reusable truth.
- `Playbook` is a repeatable procedure.

These responsibilities must remain separate. In particular, a proposed option is not accepted,
an outcome is not an Experience, and candidate lessons are not automatically Knowledge or a
Playbook change.

The initial Decision should conceptually include:

```text
id
created_at
project_key
title
objective
context_summary
alternatives
proposed_option
rationale
observation_ids
evidence_references
proposed_by
supersedes_decision_id
idempotency_key
tags
```

A material correction creates a new Decision linked through `supersedes_decision_id`; it does not
rewrite the earlier record.

## Invariants

1. Every record in the Decision workflow is immutable after persistence.
2. Creating a Decision means `proposed`, not accepted or executed.
3. Acceptance is explicit and attributable to a human or authorized external system.
4. Actions require an accepted Decision.
5. Outcomes reference existing actions for the same Decision.
6. Reviews reference existing outcomes for the same Decision.
7. Validation completes before persistence.
8. Corrections append records rather than rewriting history.
9. Evidence references preserve provenance without implying ingestion or verification.
10. Derived state has one canonical application-service owner.
11. Repository ports remain persistence-focused and gain no lifecycle query methods.
12. CLI handlers only translate input and render application-service results.
13. No Decision record automatically creates Observation, Experience, Knowledge, Playbook,
    EvolutionProposal, or revision lifecycle records.
14. A Consigliere recommendation is never accepted merely because it exists.
15. Hidden mutation and automatic evolution remain forbidden.

## Lifecycle projection

The initial future lifecycle is monotonic:

```text
proposed
→ accepted
→ executed
→ reviewed
```

State is a derived projection over the semantic immutable records, not a mutable
`Decision.status`:

- `proposed`: a Decision exists without a DecisionAcceptance.
- `accepted`: an acceptance exists without a DecisionAction.
- `executed`: at least one valid DecisionAction and DecisionOutcome exist.
- `reviewed`: a DecisionReview exists for a DecisionOutcome.

An action without an outcome is execution in progress, not `executed`. Repository order alone
must not define chronology; validated timestamps and deterministic IDs or explicit sequence fields
should resolve ordering where needed.

The initial design must not add a generic lifecycle event stream. The semantic records already
provide the authoritative facts. A canonical replay/state owner may be designed later only if real
requirements introduce withdrawal, reopening, cancellation, or reversal.

## Relationship to the existing domain chain

The existing chain remains authoritative for learning and Playbook evolution:

| Existing concept | Decision Learning relationship |
| --- | --- |
| Observation | Captures raw development facts referenced as Decision context. |
| Experience | Interprets operational learning from reviewed outcomes; it is not a DecisionOutcome. |
| Knowledge | Generalizes Experiences into reusable truth; it does not store decision history. |
| Playbook | Encodes a repeatable procedure; a DecisionReview does not mutate it. |
| PlaybookRun | May be referenced by a DecisionAction when a Playbook guided the work. |
| PlaybookEvaluation | Assesses that run and remains distinct from DecisionReview. |
| EvolutionProposal | Proposes improvement after explicit learning and evaluation; it is not created automatically. |
| PlaybookRevision | Holds an explicit immutable candidate snapshot. |
| PlaybookRevisionActivation | Selects a revision and is unrelated to DecisionAcceptance. |
| PlaybookRevisionApplication | Records revision application intent and is not a DecisionAction. |

The bridges remain explicit:

```text
DecisionOutcome
→ DecisionReview
→ Experience
→ Knowledge

DecisionAction
→ referenced PlaybookRun
→ PlaybookEvaluation
→ EvolutionProposal
→ PlaybookRevision
→ PlaybookRevisionActivation
→ PlaybookRevisionApplication
```

Any future direct Experience provenance to DecisionOutcome requires a separately reviewed schema
change. Shared Observation IDs and `EvidenceReference` values can preserve traceability until then.

## Self-observation and dogfooding

The intended NeuralEngine development workflow is:

```text
prompt
→ agent execution
→ review finding
→ decision/correction
→ implementation
→ validation
→ commit
→ push
→ post-work lesson
```

Capture must distinguish four things:

- Automatic candidates may identify paths, hashes, changed-file summaries, and validation
  metadata, but are not persisted automatically.
- Manual confirmations authorize durable writes and associations.
- Immutable audit records preserve accepted facts and actions.
- Derived summaries are replaceable views, never source evidence.

The architecture-correction example is:

```text
Observation:
PlaybookRevisionApplicationService duplicated active-revision derivation.

Decision:
PlaybookRevisionActivationService remains the canonical owner.

DecisionAction:
Remove local lifecycle replay and delegate to activation service.

DecisionOutcome:
Validation passed with 537 tests.

DecisionReview:
Ownership became explicit and duplicated replay was removed.

Experience:
Centralized lifecycle derivation prevented architectural drift.

Knowledge:
Lifecycle derivation must have one canonical owner.

Playbook improvement:
Architecture review checks responsibility ownership, not only passing tests.
```

No automatic persistence or ingestion exists.

## Consigliere boundary

```text
Consigliere
= reasoning and advisory layer

NeuralEngine
= durable memory, audit, accepted decisions, actions, outcomes, reviewed learning, playbooks
```

Consigliere may later generate options, assess risks, recommend a choice, or identify candidate
lessons. It must not directly mutate NeuralEngine records, automatically accept Decisions,
automatically create learning artifacts, automatically apply Playbook revisions, or act as
authoritative durable storage. No Consigliere integration exists.

## Evidence and provenance

The future bounded embedded value is `EvidenceReference`, conceptually containing:

```text
kind
locator
repository_or_project
content_hash
captured_at
source
summary
```

Potential future kinds are:

```text
agent_prompt
agent_review
git_commit
git_push
validation_run
changed_file_summary
handbook_sync
manual_decision
external_recommendation
```

Large prompts, reviews, diffs, and validation logs must not be embedded. References point to
authoritative sources through bounded locators and optional hashes. A hash identifies referenced
content but does not by itself prove authenticity. No file ingestion, git ingestion, or separate
Evidence repository is implemented.

## Idempotency direction

The recommended future uniqueness key is:

```text
(project_key, record_type, idempotency_key)
```

An equivalent repeated write should return the existing record. Reusing the same key with a
different payload must fail visibly and must not overwrite the first record. Initial duplicate
detection should use the current application-service load-and-filter convention. No repository
query methods should be invented for it.

## Future CLI sketch

The following commands are design direction only and do not exist:

```text
neural decision add
neural decision list
neural decision show DECISION_UUID

neural decision accept DECISION_UUID
neural decision action add DECISION_UUID
neural decision outcome add DECISION_UUID
neural decision review add DECISION_UUID

neural project ingest-review REVIEW_PATH
neural project ingest-commit COMMIT_HASH
```

Only `decision add`, `decision list`, and `decision show` belong to the recommended initial
implementation slice. All other commands require later, separately reviewed milestones.

## Recommended first implementation milestone

```text
Decision foundation
+ immutable Decision domain model
+ DecisionRepository port
+ JSON adapter using NeuralPaths.DECISIONS
+ DecisionService add/list/show
+ thin neural decision add/list/show CLI
+ tests
+ docs
```

The initial Decision should require one bounded objective, at least two meaningful alternatives,
a proposed option matching an alternative, non-blank rationale, explicit provenance, and an
idempotency key. This milestone must follow existing constructor injection, persistence-focused
port, JSON adapter, service-owned load-and-filter, thin CLI, and validation-before-persistence
patterns.

It must not implement DecisionAcceptance, DecisionAction, DecisionOutcome, DecisionReview, file or
git ingestion, automatic Observation, Experience, Knowledge, or Playbook creation, automatic
evolution, or Consigliere integration.

## Explicit non-goals and current non-behavior

This architecture does not add production code, schemas, domain classes, repositories, services,
CLI commands, dependencies, file or git ingestion, automatic learning, automatic persistence,
Playbook mutation, revision materialization, or Consigliere integration. `NeuralPaths.DECISIONS`
is only a pre-existing reserved directory in the synchronized source milestone.

## Handbook synchronization policy

Major milestones synchronize through separate, reviewable repository changes:

```text
major NeuralEngine milestone
→ commit/push NeuralEngine
→ sync NeuralEngine-Handbook
→ generate SKILL.md
→ copy generated SKILL.md back to NeuralEngine
→ commit/push skill sync
```

Generated Handbook outputs must never be edited manually. Copying the generated skill back to
NeuralEngine is outside this synchronization task.
