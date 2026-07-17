# Decision Learning Architecture

## Status and purpose

NeuralEngine source commit `7724342` implements the Decision foundation. It records an immutable
proposed choice and bounded evidence references, persists Decisions, exposes application use
cases, wires them through the container, and provides a thin CLI.

The wider Decision Learning lifecycle remains accepted future architecture. Decision tracking
complements the existing Observation-to-Playbook chain; it does not replace it.

## Implemented foundation

The implemented slice is exactly:

```text
Decision
EvidenceReference
DecisionRepository
JsonDecisionRepository
DecisionService
container wiring
neural decision add/list/show
```

Creating a Decision records a proposal. It does not accept or execute the proposal and does not
create any downstream learning record. `DecisionAcceptance`, `DecisionAction`, `DecisionOutcome`,
and `DecisionReview` are future-only records.

## Decision model

`Decision` is an immutable domain model with these implemented fields:

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

Its implemented invariants are:

1. Required text is trimmed and non-blank.
2. At least two meaningful alternatives are required.
3. Alternatives reject case-insensitive duplicates.
4. `proposed_option` exactly matches one stored alternative.
5. Observation IDs are unique.
6. An optional superseded Decision must not equal the new Decision.
7. Tags are trimmed; case-insensitive duplicates are removed while first-seen order is preserved.
8. `created_at` is timezone-aware and normalized to UTC.
9. The model is immutable.
10. No mutable lifecycle status exists.

A material correction creates another Decision linked through `supersedes_decision_id`; it does
not rewrite the earlier record.

## EvidenceReference

`EvidenceReference` is an implemented immutable value embedded in a Decision:

```text
kind
locator
repository_or_project
content_hash
captured_at
source
summary
```

`kind` and `locator` are required, trimmed, non-blank, and bounded. Optional text is trimmed,
bounded, and cannot be blank when supplied. `captured_at` is timezone-aware and normalized to UTC.
The complete value is serialized inside Decision JSON.

There is no Evidence repository, service, or CLI. A locator is retained as provenance only: the
Decision CLI does not open it, verify it, or ingest its content.

## Persistence

The persistence-focused `DecisionRepository` port implements only:

```text
save()
load_all()
get_by_id()
```

No relation, project, or idempotency query was added. `JsonDecisionRepository` stores one JSON
file per Decision under `NeuralPaths.DECISIONS`. UUIDs, UTC-aware timestamps, embedded evidence,
and optional values round-trip through the domain model. `load_all()` sorts file names for
deterministic order. Malformed stored data surfaces domain validation errors; the adapter does not
silently repair it. No migration, evidence ingestion, file ingestion, or git ingestion behavior
exists.

## Application service

`DecisionService` implements:

```text
add()
list_decisions()
show()
```

`add()` constructs an immutable Decision candidate first, validates every referenced Observation,
then validates an optional superseded Decision. A superseded Decision must exist and have the same
`project_key`. Only after these checks does the service perform idempotency detection and, when
needed, persist the candidate. It creates no other record, performs no lifecycle transition, and
does not trigger learning.

The implemented idempotency scope is:

```text
(project_key, "decision", idempotency_key)
```

The `"decision"` record type is implicit because the operation is owned by `DecisionService`.
Detection uses `DecisionRepository.load_all()` followed by application-layer filtering; there is
no repository idempotency query.

```text
same key + equivalent semantic payload
→ return existing Decision

same key + different semantic payload
→ visible conflict, no write
```

Semantic equivalence excludes generated identity and time values:

```text
Decision.id
Decision.created_at
EvidenceReference.captured_at
```

`list_decisions()` preserves repository order. Its optional project filter is trimmed and applied
in the application layer; a blank filter fails visibly. `show()` loads by UUID and raises the
existing explicit not-found error when no Decision exists.

## Container

The composition root constructs and connects:

```text
JsonDecisionRepository
JsonObservationRepository
DecisionService
```

The CLI resolves `DecisionService` from the container. It does not construct repositories or own
validation, relation checks, persistence, or idempotency policy.

## Implemented CLI

These commands exist at commit `7724342`:

```text
neural decision add
neural decision list
neural decision show DECISION_UUID
```

`neural decision add` requires these scalar options:

```text
--project-key
--title
--objective
--context-summary
--proposed-option
--rationale
--proposed-by
--idempotency-key
```

It accepts these repeatable options:

```text
--alternative
--observation-id
--evidence
--tag
```

The optional supersession argument is:

```text
--supersedes-decision-id
```

Evidence is supplied as a bounded JSON value, for example:

```bash
neural decision add \
  --project-key NeuralEngine \
  --title "Canonical lifecycle ownership" \
  --objective "Choose one active-revision owner" \
  --context-summary "Two services could derive the same state" \
  --alternative "Activation service owns derivation" \
  --alternative "Application service replays records" \
  --proposed-option "Activation service owns derivation" \
  --rationale "One owner prevents semantic drift" \
  --proposed-by architecture-review \
  --idempotency-key decision-active-revision-owner \
  --evidence '{"kind":"agent_review","locator":".agent-work/reviews/review.md"}'
```

The CLI parses and validates this JSON value as `EvidenceReference`. It does not read the locator
or ingest any referenced file content.

`neural decision list --project PROJECT_KEY` filters through the service and renders:

```text
ID
Created
Project
Title
Proposed option
Proposed by
```

`neural decision show DECISION_UUID` renders the full Decision details, including alternatives,
Observation IDs, embedded evidence references, optional supersession, idempotency key, and tags.

## Future lifecycle boundary

The accepted future record family remains deliberately separate:

```text
Decision
→ DecisionAcceptance
→ DecisionAction
→ DecisionOutcome
→ DecisionReview
```

- `Decision` is the implemented proposed choice.
- `DecisionAcceptance` would explicitly authorize execution.
- `DecisionAction` would record work performed under an accepted Decision.
- `DecisionOutcome` would record factual results and validation evidence.
- `DecisionReview` would assess outcomes and hold candidate lessons.

Only the first record exists. The future records must remain immutable semantic records rather
than fields on a mutable Decision or a duplicate generic event stream. A proposed option is not an
acceptance, an outcome is not an Experience, and candidate lessons are not automatically Knowledge
or a Playbook change.

The intended future projection is `proposed → accepted → executed → reviewed`, derived by an
application service from future records. Commit `7724342` implements no lifecycle replay or
projection service.

## Relationship to the domain chain

The implemented Decision may reference existing Observations as context. Everything after the
Decision remains an explicit future bridge:

```text
Observation
→ Decision
→ future DecisionAcceptance
→ future DecisionAction
→ future DecisionOutcome
→ future DecisionReview
→ explicitly created Experience
→ explicitly created Knowledge
```

`DecisionOutcome` remains distinct from Experience, and Decision review must never mutate a
Playbook. Any future connection to PlaybookRun, PlaybookEvaluation, EvolutionProposal, or the
revision lifecycle requires a separate reviewed use case.

## Self-observation and Consigliere boundaries

The future dogfooding flow remains a design direction:

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

Commit `7724342` does not capture or ingest those events. Automatic candidates and manual
confirmation remain future concepts; no automatic persistence, ingestion, or learning exists.

Consigliere also remains future-only. It may later advise. No Consigliere integration exists, and
no recommendation can directly mutate NeuralEngine or authorize a durable record.

## Current non-behavior

Commit `7724342` does not implement:

```text
DecisionAcceptance
DecisionAction
DecisionOutcome
DecisionReview
decision lifecycle replay
evidence repository
file ingestion
git ingestion
automatic Observation creation
automatic Experience creation
automatic Knowledge creation
automatic Playbook creation or mutation
automatic evolution
Consigliere integration
```

It also does not execute commands referenced by evidence, open locators, accept Decisions,
materialize Playbook revisions, or create any record other than the explicitly requested Decision.

## Recommended next milestone

The one recommended next controlled slice is:

```text
DecisionAcceptance foundation
```

It must remain separate from `DecisionAction` and `DecisionOutcome`.

## Handbook synchronization policy

Generated Handbook outputs are rebuilt from source documents and templates and are never edited
manually. Copying the generated skill back to NeuralEngine is outside this synchronization task.
