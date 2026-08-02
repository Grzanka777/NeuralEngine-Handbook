# Architecture Change Proposal: task-execution-policy shared contract

## Status

Proposed

## Date and checkpoint

- **Proposal date**: 2026-08-02
- **Repository checkpoint**: `1ba7b25d410abc4ca49cdc6822e82d8258a0085b`
- **Branch**: `main`
- **Agent Pack version**: 0.3.0
- **Dependent ADR**: `agent-pack/DECISIONS/oracle-wisdom-agent-pack-boundary.md`

## Problem statement

Agent Pack defines five authoritative shared contracts (neuralengine.md,
repository-review.md, python-validation.md, arch-linux.md, verification.md),
frozen under the Architecture Freeze. Six execution-policy concepts are used
across Oracle Wisdom, project prompts, builder agents, and reviewer agents but
have no authoritative shared definition in Agent Pack:

### 1. Task classes

`critical`, `standard`, and `mechanical` are used by Oracle to classify work,
appear in task prompts, and affect agent behavior. `shared/repository-review.md`
defines critical triggers for *review depth only* — it does not define what
`standard` or `mechanical` mean, does not state the "highest materially
triggered class wins" rule, and does not record the invariant that model
availability never changes task class. The only complete classification system
exists in Oracle's `03_TASK_CLASSIFICATION.md`, which is a versioned snapshot,
not an authoritative durable contract.

### 2. Execution profiles

`critical`, `review`, `balanced`, and `light` profiles span seven behavioral
dimensions: evidence completeness, uncertainty handling, independence, validation
depth, scope control, reporting rigor, and read-only behavior. These are
reducible neither to model hints nor reasoning levels. They exist only in
Oracle's `04_EXECUTION_PROFILES.md`. Agent Pack has no shared definition of
what it means for a reviewer to operate under `review` profile or a builder
under `balanced` profile.

### 3. Role separation

Oracle defines four model-agnostic roles: `planner` (assessment/architecture),
`builder` (authorized implementation), `reviewer` (independent read-only review),
and `mechanical` (deterministic low-judgment operations). Agent Pack has two
agent definitions (arch-data-engineer, reviewer) that partially correspond but
no shared contract that defines the role taxonomy independently of platform
implementations. Oracle states "Roles describe responsibility, never models" —
this rule has no Agent Pack equivalent.

### 4. Runtime substitution invariant

The model-agnostic architecture (ARCHITECTURE.md §3, CAPABILITY_MATRIX.md)
states that models are runtime engines, not architecture elements. However, the
behavioral invariant governing substitution — "substitution must preserve the
selected execution profile and must never weaken workflow safeguards" — is
recorded only in Oracle's `02_POLICY_ENGINE.md`. Making it explicit in Agent
Pack strengthens the model-agnostic position.

### 5. Supplied-routing validation

Oracle or the project chat classifies tasks and selects the execution contract.
The assigned agent must validate that the supplied contract is compatible with
its capabilities and stop on material mismatch. This validation responsibility
is not recorded in any Agent Pack contract. No agent definition states "you
must validate the supplied classification and stop on mismatch."

### 6. Delegated-prompt minimum contract

Every delegated agent prompt must specify: task class, objective, authoritative
checkpoint, compact scope, exclusions, validation, review artifact (when
implementation is delegated), NeuralEngine usage evidence, commit/push boundary,
and completion response. These elements are scattered across
`shared/repository-review.md` (review format), `shared/neuralengine.md`
(evidence requirements), and agent definitions (per-role output structure). No
single shared contract defines the minimum content every delegated agent prompt
must carry.

### Partial overlap, not complete authority

The five existing contracts provide partial coverage:
- `shared/repository-review.md` defines critical triggers for review depth and
  report depth categories (mechanical/standard/critical) — but these serve
  review behavior only.
- `shared/neuralengine.md` requires NeuralEngine usage evidence — but does not
  define the general prompt minimum contract.
- Agent definitions implement roles implicitly — but without a shared taxonomy.

Partial overlap is not a substitute for authoritative definitions. Without one
shared contract, Oracle, project prompts, builders, and reviewers use terms
that have no shared durable definition in Agent Pack. Drift is managed by
convention, not by contract.

## Proposed change

Create one new authoritative shared contract:

```text
agent-pack/shared/task-execution-policy.md
```

This is the sixth shared contract in Agent Pack. The architecture currently
freezes five contracts. Adding a sixth requires this Architecture Change
Proposal per `DECISIONS/architecture-freeze-v1.0.md` §9 ("Adding or removing a
shared contract").

This proposal defines the required contract structure and acceptance criteria.
It does not contain the final full implementation text. Implementation follows
acceptance as a separate task.

### Required sections of the future contract

#### 1. Task classes

Three classes with triggers and invariants:

##### critical

**Triggers**: domain contracts, persistence, migrations, Brain behavior, user
data, security, public APIs, persisted schemas, public behavior, release
behavior, irreversible system operations.

**Default controls**: assessment, implementation, complete validation, independent
review, staging audit, user-authorized commit/push, post-push verification.

##### standard

**Triggers**: documentation, tests, bounded fixes, local refactors, non-persisted
internal work, read-only architecture assessments.

**Default controls**: implementation or assessment, validation, proportionate
review, staging audit when preparing a commit.

##### mechanical

**Triggers**: exact copy, hash/equality verification, formatting, staging
inspection, deterministic Git checks.

**Default controls**: one combined operation with verification.

##### Invariants

- Highest materially triggered class wins.
- Split only when lower-risk work can be isolated without weakening critical
  controls.
- Model availability never changes task class.
- Mechanical tasks do not inherit unnecessary critical controls.
- Critical safeguards cannot be weakened for token or quota reasons.

**Relationship to existing contracts**: `shared/repository-review.md` §Risk
classification defines critical triggers for *review depth*. The new contract
cross-references those triggers and adds the missing `standard` and `mechanical`
definitions, the "highest class wins" rule, and the "model never changes class"
invariant. No duplication — the review contract defines review response; the
execution-policy contract defines task identity.

#### 2. Execution profiles

Four profiles defined as behavioral contracts across seven dimensions:

| Dimension | critical | review | balanced | light |
|---|---|---|---|---|
| Evidence completeness | Full evidence for every claim | Evidence before conclusions, cite sources | Standard evidence | Minimal — exact instructions suffice |
| Uncertainty handling | Explicit — state what is unknown | Skeptical — challenge assumptions | Standard — note significant uncertainty | Not applicable — deterministic operations |
| Independence | N/A (may be builder) | Independent — separate from implementation | May be builder | N/A (no judgment) |
| Validation depth | Complete — all relevant tests, full validation | Evidence-first — verify before concluding | Standard — repository workflow | Immediate — SHA-256, cmp, or exit code |
| Scope control | Conservative — narrow scope, explicit boundaries | Read-only — cannot edit, commit, or push | Standard — follow task scope | No expansion — exact instructions only |
| Reporting rigor | Full report with all evidence sections | Findings ordered by severity, verdict with evidence | Standard — repository-review format | Compact — verdict + integrity check |
| Read-only behavior | Varies by stage | Always read-only | Varies | Typically read-only |

**Profile separation**: Task class defines workflow rigor. Execution profile
defines behavior for one execution stage. A critical change may use `critical`
for implementation, `review` for independent review, and `light` for an
authorized exact-copy publication step.

No model names appear. Profiles are behavioral expectations, not model mappings.

#### 3. Role separation

Four roles defined by responsibility, never by model identity:

- **planner** — assessment and architecture analysis.
- **builder** — authorized implementation.
- **reviewer** — independent read-only review.
- **mechanical** — deterministic low-judgment operations.

Rules:
- Roles describe responsibility, never model identity.
- Model identity does not create a new role.
- An agent may fulfill multiple roles across different tasks, but one agent
  should not simultaneously plan, build, and review the same change.

**Relationship to existing agents**: OpenCode's `arch-data-engineer` maps to
builder (with planning capability). OpenCode's `reviewer` maps to the reviewer
role. Mechanical is implicit in shell command execution. Planner (as a distinct
assessment-only role) has no dedicated agent but is fulfilled by the builder
agent in planning mode or by an architecture-assessment prompt. No immediate
new agent files are required — the taxonomy provides vocabulary for future
explicit role assignment.

#### 4. Runtime substitution invariant

```text
Models are replaceable runtimes.
Substitution must preserve the selected execution profile.
Workflow safeguards cannot be weakened by model substitution.
```

This is a model-agnostic behavioral rule. It does not name any model. It does
not create model-to-role mappings. It defines the invariant that must hold
during any model substitution.

**Distinction from forbidden model mapping**:
- **Forbidden**: `reviewer = <model name>`, `builder = <model name>` — hard-coded
  model-to-role mappings violate model-agnostic architecture.
- **Allowed**: "Substitution preserves profile, never weakens safeguards" — a
  behavioral invariant that enables safe substitution without naming models.

#### 5. Supplied-routing validation

Oracle or the project chat classifies tasks, selects workflow, agent role,
execution profile, platform, and runtime model.

The assigned agent must:
- Validate compatibility of the supplied execution contract against its own
  capabilities.
- Stop on material mismatch.
- Never silently lower the task class.
- Never silently change the assigned role.
- Never silently weaken the execution profile.
- Never silently reduce validation requirements.
- Never silently remove authorization boundaries.

The agent does not perform full project-level routing. It validates the
supplied contract only. Oracle and the project chat retain routing
responsibility.

#### 6. Delegated-prompt minimum

Every delegated agent task prompt must specify:

1. task class (critical / standard / mechanical);
2. objective;
3. authoritative checkpoint (repository, branch, commit);
4. compact scope;
5. exclusions;
6. validation requirements;
7. review artifact path (when implementation is delegated);
8. NeuralEngine usage evidence requirement;
9. commit/push boundary (prohibit unless separately authorized);
10. completion response format (10–15 lines).

The contract defines the minimum elements. Oracle decides *whether* a prompt is
needed. The project chat *generates* the final prompt. Agent Pack defines the
minimum content contract.

**Reasoning level and runtime model**: These are operational routing decisions
(Oracle domain), not durable minimum-contract requirements. The contract should
not require them; it should note that they are operational and may be supplied
separately by the routing layer.

### Explicit exclusions

The future contract must not contain:

- current model names;
- current quotas or subscriptions;
- subscription details;
- portfolio priorities;
- current capability snapshots;
- platform preference tables;
- Decision Package format;
- Oracle Custom GPT instructions;
- Handoff Protocol prose;
- project-specific workflow details;
- Brain records or Brain-specific classification;
- automated routing logic;
- a parser, linter, dispatcher, scheduler, orchestrator, or persisted policy
  engine;
- concrete model-to-role mappings;
- current platform availability or pricing.

These are Oracle Wisdom operational context. They belong in Oracle knowledge
files, not in Agent Pack shared contracts.

## Architecture impact

### New sixth shared contract

The proposal adds one file: `agent-pack/shared/task-execution-policy.md`. This
is the first new shared contract added after the Architecture Freeze. It is
additive — no existing frozen contract is modified, removed, or substantively
rewritten. The five frozen contracts remain unchanged.

### Architecture Freeze implications

Per `DECISIONS/architecture-freeze-v1.0.md` §4: "Changes to shared contracts
require an Architecture Change Proposal and ADR." This proposal satisfies that
requirement. The freeze is not eroded — the existing five contracts are
unchanged, and the process for adding a sixth contract follows the freeze's
own §9.

### Adapter API impact

The Adapter API (§7 of the Architecture Freeze) defines 14 items every platform
adapter must implement or classify. The new contract does not change any of
those 14 items. It extends the set of shared contracts that adapters *may*
consume but does not require immediate consumption. Future platform adapters
gain an additional shared vocabulary reference. The Adapter API remains stable.

### Source-of-truth rules

The new contract is a single source of truth for execution-policy vocabulary.
It does not create a second source of truth because:
- Oracle Wisdom snapshots consume Handbook policy — the reverse direction is
  never valid (per `oracle-wisdom-agent-pack-boundary.md` §Oracle snapshot rule).
- Existing contracts are cross-referenced, not duplicated.
- The contract defines vocabulary that currently has no Agent Pack authority.

### Model-agnostic architecture

The contract is fully model-agnostic. No concrete model names appear. Behavioral
invariants only. The runtime substitution invariant explicitly strengthens the
model-agnostic position. Roles are defined by responsibility, never model
identity.

### Relationship to existing five contracts

| Contract | Relationship |
|---|---|
| `neuralengine.md` | Referenced for NeuralEngine usage evidence requirements in the prompt minimum contract. Not duplicated. |
| `repository-review.md` | Critical triggers cross-referenced for consistency. Review-specific report depth categories are distinct from task classes — the review contract defines review behavior; the execution-policy contract defines task identity. No duplication. |
| `python-validation.md` | No direct relationship. Task classification may reference validation depth but does not define Python-specific validation. |
| `arch-linux.md` | No direct relationship. |
| `verification.md` | New contract is added to Standard Verification rule audit (per verification.md §Extensibility). Quick Verification file count increments. |

### Why no second source of truth is created

The contract defines vocabulary that currently has no authoritative Agent Pack
definition. Oracle uses these terms but is a versioned snapshot, not a durable
authority (per the boundary ADR). The contract is the *first* Agent Pack source
for this vocabulary, not a *second* source.

## Platform consumption plan

### Foundation milestone (this proposal's implementation task)

- Create `agent-pack/shared/task-execution-policy.md` as authoritative shared
  contract.
- Update `agent-pack/MANIFEST.md` with the new shared-to-platform mapping
  entry.
- Update Verification Framework (Quick + Standard) per the verification delta
  below.
- No platform adapter changes. No agent definition changes. No Oracle snapshot
  update.

### Later OpenCode consumption (deferred to v0.7.0+)

- OpenCode agent definitions reference the contract for role definitions.
- Reviewer agent checks supplied classification against contract definitions
  during review.
- No automatic routing — Oracle and project chat retain routing responsibility.
- No new agents required initially.

### Future Codex consumption (deferred to v0.6.0+)

- Codex Platform Assessment uses the shared execution-policy vocabulary for
  capability evaluation.
- Codex adapter references the contract for role mapping and execution profile
  interpretation.
- Adapter consumes the same vocabulary as OpenCode — cross-platform consistency.

These stages are documented for planning. They are not implemented in this
task. This proposal creates the authoritative contract only.

## Verification delta

### Minimum future verification changes required if accepted

| Update | Scope |
|---|---|
| MANIFEST.md | Add `shared/task-execution-policy.md` to shared-to-platform mapping table |
| Quick Verification | File count increment (+1). File-presence check for the new contract. No new exact-copy mappings (the contract has no platform copy initially). |
| Standard Verification | New mandatory-rule audit for `task-execution-policy.md`: verify all six sections present, verify invariants stated, verify no concrete model names appear, verify consistency with existing contracts (cross-reference critical triggers, no contradiction with review report depth). |
| Certification Report | SHA-256 table gains one entry (or the file is excluded if no platform copy exists). Evidence reference for new contract presence. |
| Cross-document consistency | ARCHITECTURE.md contract-ownership table updated to include the sixth contract. README.md "Five authoritative shared contracts" heading and count updated. DEFINITION-OF-DONE.md criterion S1 ("Exactly five authoritative shared contracts") updated to six. |

### Platform-copy equality

Not required immediately. The contract has no platform adapter copy in the
foundation milestone. Platform-copy equality is deferred until a platform
adapter explicitly consumes the contract (v0.7.0+ for OpenCode, v0.6.0+ for
Codex).

### Negative verification scenarios

- Verify no concrete model names appear in the contract (`grep -E` for known
  model patterns).
- Verify no silent safeguard weakening is permitted (contract text explicitly
  forbids it).

No verification changes are made in this task. The delta is documented for
the implementation task.

## Compatibility and migration

- **No persisted data migration**: The contract is a documentation artifact.
  No database, Brain, or file-format migration.
- **No NeuralEngine schema change**: The contract does not modify
  NeuralEngine behavior, Brain schema, or CLI.
- **No CLI change**: `neural status`, `neural search`, and other CLI commands
  are unaffected.
- **No runtime permission change in foundation milestone**: The contract
  defines vocabulary. No new agent permissions, allow patterns, or deny rules
  are introduced until a consumption milestone.
- **Existing agents remain compatible**: OpenCode `arch-data-engineer` and
  `reviewer` agents continue to function without modification. They gain
  authoritative vocabulary for terms they already use implicitly.
- **Prompts using current terminology remain valid**: Task prompts using
  `critical`, `standard`, `mechanical`, role names, or execution profiles
  remain valid. After adoption, they gain an authoritative Agent Pack
  definition — their meaning is clarified, not changed.
- **Oracle snapshots**: No immediate update required. Oracle consumes
  versioned Handbook snapshots per the boundary ADR. Oracle knowledge files
  may be updated after authoritative policy changes are accepted and
  implemented — this is a separate Oracle maintenance task, not an Agent
  Pack task.

## Alternatives

### Alternative A: No new contract (status quo)

**Rejected.** The consigliere assessment (`consigliere-assessment-agent-pack-policy-core-foundation.md`, revised) confirms that six execution-policy concepts lack authoritative shared definitions. The drift risk is real — Oracle, prompts, builders, and reviewers currently use terms that have no shared durable definition in Agent Pack. Managing this by convention rather than contract creates drift risk between Oracle snapshots, project prompts, and agent behavior. Without an authoritative definition, a reviewer cannot verify that a "critical" task received "critical" controls because the term has no shared Agent Pack definition.

### Alternative B: Six separate shared contracts

**Rejected.** The six candidate areas (task classes, execution profiles, role separation, runtime substitution, supplied-routing validation, delegated-prompt minimum) converge naturally into one contract. They share common vocabulary (task class, profile, role), common consumers (Oracle, prompts, builders, reviewers), and common exclusions (model names, quotas, routing logic). Separating them would create unnecessary maintenance burden, duplicate cross-references, and require six Architecture Change Proposals rather than one. The consigliere assessment confirmed one contract as the correct structure.

### Alternative C: Extend `repository-review.md` to cover task classification

**Rejected.** `repository-review.md` §Risk classification defines critical triggers for *review depth* — the reviewer applies more scrutiny to critical changes. It does not define `standard` or `mechanical`, the "highest class wins" rule, or the "model never changes class" invariant. Adding task classification to the review contract would conflate two distinct responsibilities: task identity (what kind of work this is) and review behavior (how to review it). The review contract should reference task classification, not own it.

### Alternative D: Place execution-policy only in Oracle

**Rejected.** Oracle Wisdom is a versioned snapshot of Handbook policy, not an authoritative durable source (per `oracle-wisdom-agent-pack-boundary.md`). Placing execution-policy definitions only in Oracle would make them dependent on Oracle's snapshot cycle and not directly accessible to agents, reviewers, or platform adapters. The boundary ADR explicitly assigns durable execution-policy vocabulary to Agent Pack. Oracle retains operational routing — *which* model/platform/workflow to use — while Agent Pack defines *what* the terms mean.

### Alternative E: Place model routing in Agent Pack

**Rejected.** Model names, current quotas, subscriptions, and capability snapshots are operational context (Oracle domain). Freezing them into Agent Pack would violate model-agnostic architecture and require Architecture Change Proposals every time model availability changes. The runtime substitution invariant provides a model-agnostic behavioral rule without naming models — this is the correct boundary.

### Alternative F: Implement platform enforcement simultaneously

**Rejected.** Creating the authoritative contract first, then consuming it in platform adapters later, is the safer sequence. It allows the contract to stabilize before platform-specific implementation begins. It prevents the situation where platform adapters consume a contract that is still being revised during the same milestone. The Architecture Freeze process (§9) separates proposal, ADR, implementation, and verification into distinct stages — this proposal follows that sequence.

### Alternative G: Defer until after Codex Platform Assessment

**Rejected.** The execution-policy vocabulary should exist before Codex assessment so both platforms (OpenCode and Codex) are evaluated against the same shared definitions. Conducting Codex assessment without shared task classes and execution profiles would evaluate Codex against Oracle's vocabulary, not Agent Pack's — defeating the purpose of a platform-agnostic assessment. The consigliere assessment revised the milestone sequence to place execution-policy foundation (v0.4.0) before Codex assessment (v0.5.0).

## Risks and safeguards

### Risk 1: Over-centralization

**Risk**: One contract covering six concerns could become a dumping ground for
future execution-policy additions, growing beyond its intended scope.

**Safeguard**: The contract has explicit exclusions. Any addition beyond the
six defined sections requires a new Architecture Change Proposal. The
contract's scope is defined in this proposal and auditable in Standard
Verification.

### Risk 2: Duplication with existing contracts

**Risk**: Task classification critical triggers overlap with
`repository-review.md` risk classification.

**Safeguard**: The contract cross-references, not duplicates. The review
contract defines review depth; the execution-policy contract defines task
identity. Standard Verification confirms no material duplication.

### Risk 3: Model-routing leakage

**Risk**: Execution profiles could accidentally drift into model-mapping
territory over future revisions.

**Safeguard**: Profiles are defined as behavioral contracts (seven dimensions,
no model names). Standard Verification negative scenarios confirm no model
names appear. Any change to include model information requires an Architecture
Change Proposal.

### Risk 4: Turning agents into mini-Oracles

**Risk**: Supplied-routing validation could be misinterpreted as requiring
agents to perform full project-level routing.

**Safeguard**: The contract explicitly limits agent validation to compatibility
checking. Agents validate the supplied contract — they do not select platforms,
models, workflows, or project priorities. The boundary is stated in the
contract text.

### Risk 5: Excessive critical classification

**Risk**: The "highest class wins" rule could lead to over-classification,
with every task containing one minor critical trigger being treated as fully
critical.

**Safeguard**: The contract includes the split rule: "Split only when
lower-risk work can be isolated without weakening critical controls." This
allows delegation of lower-risk subtasks while preserving critical controls
on the sensitive parts.

### Risk 6: Prompt bloat

**Risk**: The delegated-prompt minimum contract could lead to excessively long
prompts with boilerplate sections.

**Safeguard**: The minimum contract defines *what must be present*, not
*how long it must be*. Most elements (checkpoint, scope, exclusions) are
compact. The contract does not require prose explanations for every element
when a compact reference suffices.

### Risk 7: Architecture Freeze erosion

**Risk**: Adding a sixth contract so soon after the freeze (accepted 2026-08-01)
could signal that the freeze is not taken seriously.

**Safeguard**: This proposal follows the freeze's own §9 process exactly:
Architecture Change Proposal → ADR → Implementation → Independent Review →
Verification → Certification → Release Decision. The freeze anticipated new
contracts — §9 explicitly lists "Adding or removing a shared contract" as a
trigger for the Architecture Change Proposal process. Using the defined process
strengthens, not erodes, the freeze.

### Risk 8: Oracle snapshot drift

**Risk**: After the contract is accepted and implemented, Oracle knowledge
files may fall out of sync with the authoritative Agent Pack definitions.

**Safeguard**: The boundary ADR (§Oracle snapshot rule) defines the update
direction: Handbook authority → versioned Oracle snapshot → manual Custom GPT
update. Oracle snapshot updates are a separate maintenance task. The risk is
managed by the existing boundary contract, not eliminated.

### Risk 9: Adapter divergence

**Risk**: OpenCode and Codex platform adapters could interpret the shared
vocabulary differently when they eventually consume the contract.

**Safeguard**: The contract provides one authoritative definition. The
Verification Framework cross-platform consistency checks (to be implemented
when both adapters exist) will detect divergent interpretations. The
controlled-copy model ensures platform adapters derive from the shared
source, not the reverse.

## Acceptance criteria

The proposal may be accepted only if:

1. **One contract is sufficient**: All six concerns (task classes, execution
   profiles, role separation, runtime substitution invariant, supplied-routing
   validation, delegated-prompt minimum) converge into one contract without
   forcing unrelated concepts together or creating an overloaded document.
2. **No concrete model names are required**: The contract is fully
   model-agnostic. Behavioral expectations only. No model identifiers appear
   in any section.
3. **Oracle boundary is preserved**: Oracle retains operational routing
   (model selection, platform selection, quota awareness, portfolio priorities,
   Decision Package format, Handoff Protocol, capability snapshots). Agent
   Pack gains the shared vocabulary Oracle uses — not Oracle's routing logic.
4. **No existing shared contract authority is duplicated unnecessarily**:
   The contract cross-references existing definitions where overlap exists
   (e.g., critical triggers in repository-review.md, NeuralEngine evidence
   in neuralengine.md). It does not duplicate them.
5. **Verification delta is bounded**: The verification impact is limited to
   file count increment (+1), MANIFEST update, Standard Verification rule
   audit addition, and cross-document consistency checks. No new verification
   tooling is required.
6. **No runtime enforcement tooling is required**: The contract defines
   vocabulary and behavioral expectations. Existing enforcement layers
   (Verification Framework for structural integrity, agent permissions for
   behavioral boundaries, repository review for semantic correctness) are
   sufficient. No parser, linter, dispatcher, or policy engine is introduced.
7. **OpenCode and Codex can consume the same vocabulary**: The contract is
   platform-agnostic. Both platform adapters can reference the same
   definitions for task classes, execution profiles, roles, and invariants.
8. **Rollback is documentation-only and reversible**: If the contract is
   later found to be incorrect or unnecessary, removing it requires deleting
   one file and reverting MANIFEST and verification updates. No data
   migration, schema change, or runtime behavior reversal is needed.

## Requested decision

```text
Accept
```

The proposal requests `Accept` — that the architecture authority approves
creating `agent-pack/shared/task-execution-policy.md` as the sixth
authoritative shared contract with the structure, content, and boundaries
defined in this proposal.

The proposal remains in `Proposed` status. Acceptance is a separate decision
by the architecture authority (user/repository owner). Implementation begins
only after acceptance.

## Follow-up sequence if accepted

```text
Architecture Change Proposal accepted
→ Implementation prompt
→ Create agent-pack/shared/task-execution-policy.md
→ Update agent-pack/MANIFEST.md (add shared-to-platform mapping)
→ Update agent-pack/ARCHITECTURE.md (contract ownership table)
→ Update agent-pack/README.md (count and navigation)
→ Update agent-pack/DEFINITION-OF-DONE.md (criterion S1)
→ Update Verification Framework references (Quick + Standard)
→ Independent review
→ Quick Verification
→ Standard Verification
→ Certification Report
→ Release decision
```

The Implementation prompt creates the contract file. The Implementation task
makes the required mapping and verification document updates. Independent
review confirms correctness. Verification and certification follow the
Architecture Freeze release workflow.

No commit, push, merge, tag, or release is included as an agent action in
this sequence. Each of these operations requires separate authorization.

## Architecture Change Proposal boundary

This task does not authorize implementation. The proposal:

- States that acceptance is a separate user/repository decision.
- States that implementation begins only after acceptance.
- States that adding the sixth contract remains pending.
- States that no platform adapter may consume a non-existent contract.
- States that no Oracle snapshot update is needed until authoritative policy
  changes are accepted and implemented.
