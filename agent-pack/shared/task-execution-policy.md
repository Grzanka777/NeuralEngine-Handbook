# Task Execution Policy

Use this contract as the authoritative shared definition of execution-policy
vocabulary for all Agent Pack consumers: Oracle routing, project prompts,
builder agents, reviewer agents, and platform adapters.

## 1. Purpose

This contract provides the single durable authority for task classification,
execution profiles, role separation, runtime substitution invariants,
supplied-routing validation, and the delegated-prompt minimum contract.

Before this contract, these concepts existed in Oracle knowledge snapshots,
agent definitions, and project conventions but had no shared authoritative
definition in Agent Pack. This contract fills that gap.

It is platform-agnostic. It defines what terms mean. It does not enforce them
at runtime.

## 2. Scope

This contract defines durable execution-policy vocabulary and behavioral
invariants. It does not contain operational routing decisions, model
selection, quota management, or project prioritization.

It applies to every delegated agent task, every independent review, and every
platform adapter that references shared execution-policy concepts. Consumers
may extend it with operational context but must not weaken its invariants.

## 3. Task classes

Three mutually exclusive classes define how much rigor a task requires.

### 3.1 critical

**Triggers**: work that affects domain contracts, persistence, migrations,
user data, security, Brain behavior, public APIs, persisted schemas, public
behavior, or release behavior. The full critical-trigger list is defined in
`shared/repository-review.md` §Risk classification.

**Controls**: assessment, implementation, complete validation, independent
review, staging audit, user-authorized commit/push, post-push verification.

### 3.2 standard

**Triggers**: documentation, tests, bounded fixes, local refactors,
non-persisted internal work, read-only architecture assessments.

**Controls**: implementation or assessment, validation, proportionate review,
staging audit when preparing a commit.

### 3.3 mechanical

**Triggers**: exact copy, hash/equality verification, formatting, staging
inspection, deterministic Git checks.

**Controls**: one combined operation with verification.

### 3.4 Invariants

1. **Highest materially triggered class wins.** When a task touches multiple
   trigger domains, classify at the highest triggered level.

2. **Split only when lower-risk work can be isolated without weakening
   critical controls.** Sub-work that shares a critical trigger stays critical.

3. **Model availability never changes task class.** A task requiring
   `critical` controls is `critical` regardless of which model is available.

4. **Mechanical tasks do not inherit unnecessary critical controls.**
   Deterministic low-judgment operations should not be burdened with
   assessment, independent review, or staging audit unless they directly
   affect a critical trigger domain.

5. **Critical safeguards cannot be weakened for token, quota, cost, or
   runtime reasons.** The class defines the required safeguards; operational
   constraints do not justify lowering them.

### 3.5 Relationship to repository-review.md

`shared/repository-review.md` §Risk classification defines critical triggers
for review depth — how much scrutiny a reviewer applies. This contract defines
task identity — what kind of work this is. A task can be `critical` at the
task level (requiring full controls) while the reviewer uses the same
classification to determine review depth. The review contract defines review
behavior; this contract defines task classification. Both use the same trigger
domains. Neither duplicates the other.

## 4. Execution profiles

Four profiles define behavioral expectations for one execution stage. A
profile is not a model mapping, reasoning level, or role — it is a contract
for how an agent behaves during one stage of work.

**Task class defines workflow rigor. Execution profile defines behavior for
one execution stage.** A critical change may use `critical` profile for
implementation, `review` profile for independent review, and `light` profile
for an authorized exact-copy publication step.

### 4.1 Profile dimensions

| Dimension | critical | review | balanced | light |
|---|---|---|---|---|
| Evidence completeness | Full evidence for every claim | Evidence before conclusions, cite sources | Standard evidence | Minimal — exact instructions suffice |
| Uncertainty handling | Explicit — state what is unknown | Skeptical — challenge assumptions | Standard — note significant uncertainty | Not applicable — deterministic operations |
| Independence | N/A (may be builder) | Independent — separate from implementation | May be builder | N/A (no judgment) |
| Validation depth | Complete — all relevant tests, full validation | Evidence-first — verify before concluding | Standard — repository workflow | Immediate — SHA-256, cmp, or exit code |
| Scope control | Conservative — narrow scope, explicit boundaries | Read-only — cannot edit, commit, or push | Standard — follow task scope | No expansion — exact instructions only |
| Reporting rigor | Full report with all evidence sections | Findings ordered by severity, verdict with evidence | Standard — repository-review format | Compact — verdict + integrity check |
| Read-only behavior | Varies by stage | Always read-only | Varies | Typically read-only |

### 4.2 Profile assignment

Profiles are assigned by Oracle or the project chat as part of the execution
contract. The assigned agent must validate that it can fulfill the profile but
must not silently weaken it. No concrete model names appear in profile
definitions — profiles are behavioral expectations, not model mappings.

## 5. Role separation

Four roles describe responsibility. A role is never defined by model identity.

### 5.1 Role definitions

- **planner** — assessment and architecture analysis. May be fulfilled by a
  dedicated assessment prompt or by a builder agent operating in planning mode.
- **builder** — authorized implementation. Creates, modifies, and validates
  repository files within the supplied scope. Does not independently approve
  its own implementation for release.
- **reviewer** — independent read-only review. Inspects implementation,
  validates against the task contract, identifies blockers. Cannot edit,
  commit, or push.
- **mechanical** — deterministic low-judgment operations. Exact-copy,
  hash-equality, formatting, staging inspection, exit-code checks.

### 5.2 Role rules

1. **Roles describe responsibility, never model identity.** A model name does
   not create or define a role.

2. **Model identity does not create a new role.** The runtime model is an
   operational choice; the role taxonomy is a durable definition.

3. **Reviewer is read-only.** The reviewer role cannot edit files, commit,
   push, delegate tasks, or perform destructive operations.

4. **Builder does not independently approve its own implementation.** An
   independent reviewer must confirm correctness, scope, and completeness.

5. **Mechanical role performs deterministic low-judgment work only.** Tasks
   that require interpretation, architecture judgment, or scope assessment
   are not mechanical.

6. **One agent may fulfill multiple roles across different tasks.** An agent
   that builds one change and reviews another is performing two distinct roles
   — the taxonomy describes the role, not the agent identity.

7. **One agent should not simultaneously plan, build, and review the same
   change.** Role separation for the same change preserves independence.

### 5.3 Relationship to platform agents

Platform agent definitions (e.g., `arch-data-engineer`, `builder`,
`reviewer`) implement roles. The role taxonomy provides the vocabulary
platform adapters use. This contract defines the roles; platform adapters
define which agent definition or configuration fulfills each role.

## 6. Runtime substitution invariant

```text
Models are replaceable runtimes.
Substitution must preserve the selected execution profile.
Workflow safeguards cannot be weakened by model substitution.
```

This invariant is durable policy. It enables model substitution without
naming any model. It codifies the principle that behavioral contracts
(task class, execution profile, role constraints) bind agents regardless
of which model processes the request.

No concrete model names appear. The invariant defines the behavioral rule
that any substitution must satisfy.

## 7. Supplied-routing validation

Oracle or the project chat classifies tasks, selects the execution contract,
assigns the role, and chooses the execution profile, platform, and runtime
model. The assigned agent receives a supplied execution contract.

The assigned agent must:

1. **Validate compatibility** of the supplied execution contract against its
   own capabilities. Confirm it can fulfill the assigned role, profile,
   validation requirements, and authorization boundaries.

2. **Stop on material mismatch.** If the supplied contract requires
   capabilities the agent does not have, or the role/profile is incompatible
   with the agent's configuration, stop and report the mismatch.

3. **Never silently lower the task class.** If the agent cannot fulfill
   `critical` controls, report the limitation — do not silently treat the
   task as `standard`.

4. **Never silently change the assigned role.** An agent assigned as
   `reviewer` must not perform implementation work. An agent assigned as
   `builder` must not independently approve its own output.

5. **Never silently weaken the execution profile.** The supplied profile
   is a binding behavioral contract.

6. **Never silently reduce validation requirements.** If the task requires
   full validation, do not substitute lighter checks.

7. **Never silently remove authorization boundaries.** Commit, push, merge,
   tag, release, and Brain-write boundaries in the supplied contract are
   binding.

The agent does not perform full project-level routing. It validates the
supplied contract only. Oracle and the project chat retain routing
responsibility.

## 8. Delegated-prompt minimum

Every delegated agent task prompt must specify:

1. **task class** — `critical`, `standard`, or `mechanical`.
2. **objective** — what the agent must accomplish.
3. **authoritative checkpoint** — repository, branch, commit, or explicit
   working-tree state.
4. **compact scope** — exact paths or bounded concerns. No ambiguous
   directives.
5. **exclusions** — what the agent must not touch. Explicit negatives are
   as important as affirmative directives.
6. **validation requirements** — exact commands or validation criteria
   the agent must execute.
7. **review artifact path** — where to save the review artifact when
   implementation is delegated. Required for builder tasks.
8. **NeuralEngine usage evidence requirement** — per
   `shared/neuralengine.md`, the agent must record `neural status`, search
   decision, queries, results, and effect on work.
9. **commit/push boundary** — whether the agent is authorized to stage,
   commit, or push. Default: prohibit unless separately authorized.
10. **completion response expectation** — the agent's final response format
    and length. The completion response should normally remain within 10–15
    lines unless the user or task contract requires a fuller report.

These ten elements are the minimum. A prompt may carry additional operational
context (reasoning level, runtime model, platform preference) supplied by the
routing layer, but these are operational inputs, not durable prompt-contract
requirements.

## 9. Explicit exclusions

This contract does not contain:

- concrete model names;
- current quotas or subscriptions;
- portfolio priorities;
- current capability snapshots;
- platform preference tables;
- Decision Package format;
- Oracle Custom GPT instructions;
- Handoff Protocol prose;
- project-specific workflow details;
- Brain records or Brain-specific classification;
- automated routing logic;
- parsers, linters, dispatchers, schedulers, orchestrators, or policy
  engines;
- concrete model-to-role mappings;
- platform pricing or availability.

These exclusions are operational context that belongs in Oracle Wisdom
knowledge files or project-specific configuration. Freezing them into a
shared Agent Pack contract would require Architecture Change Proposals
every time model availability or pricing changes.

## 10. Relationship to existing contracts

| Contract | Relationship |
|---|---|
| `shared/neuralengine.md` | Referenced for NeuralEngine usage evidence requirements in the prompt minimum (§8, element 8). Not duplicated. |
| `shared/repository-review.md` | Critical triggers (§3.1) cross-referenced from `repository-review.md` §Risk classification. The review contract defines review depth; this contract defines task identity. No duplication. |
| `shared/python-validation.md` | No direct relationship. Task classification may reference validation depth but does not define Python-specific validation. |
| `shared/arch-linux.md` | No direct relationship. |
| `shared/verification.md` | The new contract is added to the Standard Verification mandatory-rule audit per `verification.md` §Extensibility. File-count increment for Quick Verification. |

## 11. Compliance requirements

### 11.1 Structural

The contract must be present at `agent-pack/shared/task-execution-policy.md`.
All 11 sections must exist. No concrete model names may appear. Cross-reference
consistency with `shared/repository-review.md` §Risk classification must be
maintained.

### 11.2 Consuming agents

Agents consuming this contract must:

- Validate supplied task class, role, profile, validation, and authorization
  boundaries per §7.
- Stop on material mismatch. Never silently weaken any supplied constraint.
- Record NeuralEngine usage evidence per `shared/neuralengine.md` and §8,
  element 8.
- Respect the commit/push boundary per §8, element 9.
- Produce the required completion response per §8, element 10.

### 11.3 Reviewers

Reviewers must confirm that:

- The implemented change received controls matching its declared task class.
- The builder validated supplied-routing compatibility per §7.
- The delegated prompt carried all 10 minimum elements per §8.
- No task class, profile, role, or validation boundary was silently weakened.
- No concrete model names appear in the implementation contract.

### 11.4 Verification

Verification of this contract is performed per `shared/verification.md`
§Extensibility:

- **Quick Verification**: file-presence check for `task-execution-policy.md`.
  File count increment.
- **Standard Verification**: mandatory-rule audit covering all 11 sections.
  Negative audit for concrete model identifiers. Cross-reference consistency
  check with `repository-review.md`.
- **No immediate platform-copy equality check.** This contract has no
  platform adapter copy in the foundation milestone.

### 11.5 Contract evolution

Changes to this contract require an Architecture Change Proposal per
`DECISIONS/architecture-freeze-v1.0.md` §9. Editorial clarifications that
do not alter semantics may proceed without one.
