# ADR: Oracle Wisdom ↔ Agent Pack boundary

## Status

Accepted

## Date

2026-08-01

## Context

Oracle Wisdom is a private Custom GPT that acts as the operational decision
engine for the user's AI-assisted project work. It decides the safest execution
path — project, workflow, agent role, execution profile, platform, runtime
model — and produces a Decision Package handed off to the project chat. Oracle
does not implement code, edit repositories, perform reviews, or enforce policy
at runtime.

Agent Pack defines five authoritative shared contracts (NeuralEngine usage,
repository review, Python validation, Arch Linux diagnostics, structural
verification), frozen under the Architecture Freeze. These are durable,
platform-agnostic, and change only through Architecture Change Proposals. A
sixth shared contract (`task-execution-policy.md`) has been proposed to provide
authoritative shared definitions for task classes, execution profiles, role
separation, runtime substitution invariants, supplied-routing validation, and
the delegated-prompt minimum contract — concepts currently defined only in
Oracle knowledge files or implied by Agent Pack architecture.

These two layers must remain separate. Oracle handles operational decisions:
which model is available right now, which platform has quota, which project has
priority. Agent Pack defines durable invariants: what a critical task means
regardless of model availability, how review evidence must be structured, which
Brain operations require authorization. Conflating them would freeze current
model availability into durable policy, duplicate authority, and erode the
model-agnostic architecture.

This boundary must be explicit before the sixth shared contract is created.
Without it, the contract might accidentally import Oracle's operational context
(model names, quotas, portfolio priorities, capability snapshots), Oracle's role
as a Custom GPT could be conflated with Agent Pack's durable authority, and the
Handoff Protocol and Decision Package (Oracle/project-chat operational
artifacts) might be mistaken for shared Agent Pack contracts.

## Decision

### NeuralEngine-Handbook

NeuralEngine-Handbook is the durable source of truth. It contains the
authoritative Agent Pack shared contracts and all Architecture Decision Records.
Oracle Wisdom consumes a versioned Handbook snapshot; it never replaces or
overrides Handbook authority.

### Agent Pack ownership

Agent Pack owns durable execution invariants:

- the five frozen shared contracts;
- durable task-execution vocabulary (task classes, execution profiles, role
  separation, runtime substitution invariant, supplied-routing validation,
  delegated-prompt minimum contract) — intended for the future minimal
  `agent-pack/shared/task-execution-policy.md`, which does not yet exist;
- the model-agnostic principle (models are runtime engines, not architecture
  elements);
- verification and platform adapter behavior;
- NeuralEngine usage policy and commit/push authorization boundaries.

Agent Pack contracts define *what* invariants must be preserved. They do not
contain current model names, quotas, subscriptions, portfolio priorities, or
capability snapshots.

### Oracle Wisdom ownership

Oracle Wisdom owns operational routing and mutable context:

- project-level routing and priority evaluation against the current portfolio;
- Decision Package production;
- manual-versus-agent recommendation;
- platform selection and current runtime-model recommendation;
- mutable capability snapshot, quota and subscription context;
- Custom GPT instructions and presentation.

Oracle knowledge files are snapshots — they may contain mutable operational
information (model names, subscriptions, capabilities) not suitable for Agent
Pack shared contracts. Oracle is a Custom Chat, not a repository authority,
execution agent, or policy enforcement point.

### Project chat ownership

The project chat owns:

- validating Decision Package assumptions against current repository state;
- finding the latest authoritative checkpoint and rejecting stale routing;
- generating the final agent prompt (unless the user explicitly asks Oracle);
- supervising implementation, validation, and review.

### Agent ownership

The assigned agent owns:

- validating compatibility of the supplied execution contract against its own
  capabilities;
- stopping on material mismatch — never silently lowering the task class,
  changing the role, weakening the execution profile, reducing validation
  requirements, or removing authorization boundaries;
- executing only the assigned role.

### User ownership

The user owns final authorization of commit, push, merge, tag, and release
operations; every Brain write authorization; portfolio priority decisions.

## Model-agnostic boundary

**Forbidden**: binding an agent role to a concrete runtime model identity. Model
names do not define roles, agents, or execution profiles.

**Required**: runtime substitution must preserve the selected execution profile
and never weaken workflow safeguards.

This invariant is durable policy, not operational routing. It belongs in Agent
Pack.

## Oracle snapshot rule

```text
Handbook authority
→ versioned Oracle knowledge snapshot
→ manual Custom GPT update
```

Oracle knowledge files under `oracle-wisdom-v0.1/knowledge/` are snapshots of
Handbook policy at a specific version, augmented with mutable operational
context. They are not an independent source of truth. When Handbook authority
changes, Oracle knowledge files must be manually updated. The reverse direction
is never valid.

## Decision Package and Handoff

The Decision Package is Oracle's output format — a structured execution
recommendation. The Handoff Protocol (`oracle-wisdom-v0.1/knowledge/11_HANDOFF_PROTOCOL.md`)
defines Oracle → project chat operational guidance.

Both are compatible with Agent Pack vocabulary and respect Agent Pack
boundaries, but they are Oracle/project-chat operational artifacts, not shared
Agent Pack contracts.

## Consequences

### Positive

- **One authority for durable execution terms.** No duplicate definitions across
  Oracle and Agent Pack.
- **No model identity in roles.** Roles describe responsibility, never model
  names.
- **Reduced drift.** Oracle consumes versioned Handbook snapshots; Agent Pack
  evolves through Architecture Change Proposals.
- **Common vocabulary across platforms.** Task classes, execution profiles,
  roles, and invariants provide a shared execution-policy language.
- **Oracle remains distinct.** Oracle handles operational decisions; Agent Pack
  handles durable invariants.

### Costs

- **Adding a sixth shared contract requires an Architecture Change Proposal.**
  Per `DECISIONS/architecture-freeze-v1.0.md` §9.
- **Oracle snapshots must be manually updated** after authoritative policy
  changes.
- **Platform adapters may later need controlled updates** when
  `task-execution-policy.md` is created (deferred).

## Rejected alternatives

- **Copy all Oracle knowledge into Agent Pack** — would freeze operational
  context into durable policy.
- **Six separate shared policy contracts** — the concepts converge naturally
  into one contract.
- **Treat current model availability as durable policy** — model names, quotas,
  and subscriptions are operational, not architectural.
- **Create an Oracle agent inside Agent Pack** — Oracle is a Custom GPT;
  duplicating it as an agent creates routing confusion.
- **Let builders perform full routing** — builders execute; routing requires
  operational context builders should not need.
- **Leave the boundary undocumented** — without this ADR, drift between Oracle's
  operational vocabulary and Agent Pack's durable contracts would be inevitable.

## Follow-up

The next architectural task is:

```text
Architecture Change Proposal for one minimal shared
agent-pack/shared/task-execution-policy.md contract
```

This ADR establishes the boundary and rationale. The Architecture Change
Proposal must define the final contract content, scope, exclusions, verification
delta, and MANIFEST update. The contract does not yet exist.

The follow-up Architecture Change Proposal must follow the process defined in
`DECISIONS/architecture-freeze-v1.0.md` §9:

```text
Assessment
→ Architecture Change Proposal
→ ADR
→ Implementation
→ Independent Review
→ Verification (Quick + Standard)
→ Certification Report
→ Release Decision
```
