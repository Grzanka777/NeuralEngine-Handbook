---
name: neuralengine
description: Use NeuralEngine as the durable project knowledge, decision, experience, and playbook layer for substantive repository, architecture, review, diagnostic, planning, and authorized Brain tasks.
---
# Mandatory NeuralEngine Usage

NeuralEngine is the default durable knowledge and decision layer for all agents and models.

Repository sources describe the current implementation. NeuralEngine may contain prior decisions, experience, knowledge, playbooks, and provenance that are not recoverable from the current working tree alone.

## Authority model

Treat sources according to their role:

1. repository source defines the current implementation;
2. repository instructions define local execution constraints;
3. NeuralEngine provides durable knowledge, decisions, experience, playbooks, and provenance;
4. current command output provides direct runtime evidence;
5. external documentation provides supporting context.

Do not use NeuralEngine records to override current repository source without explaining the conflict.

Do not assume a record is authoritative merely because it exists.

Evaluate:

* lifecycle state;
* provenance;
* project key;
* source record;
* timestamps;
* superseding records;
* activation or revision state;
* applicability to the current task.

## Start of work

At the start of every substantive task, run:

`neural status`

A substantive task includes repository work, review, diagnosis, assessment, planning, implementation, or architecture analysis.

Simple requests that only summarize already loaded instructions or skill contents do not require a new `neural status` call.

Record whether NeuralEngine is:

* available;
* unavailable;
* degraded;
* misconfigured;
* connected to the expected Brain.

If `neural status` fails:

1. preserve the exact error;
2. determine whether repository-only work can continue safely;
3. do not claim NeuralEngine usage;
4. record the limitation in the task report.

## Search decision

Before substantive analysis, review, diagnosis, planning, or editing, decide whether prior project knowledge, decisions, experience, or playbooks are relevant.

Use `neural search` when prior durable knowledge may materially affect:

* architecture;
* domain boundaries;
* persistence;
* migrations;
* security;
* public behavior;
* release decisions;
* previous incidents;
* diagnostic playbooks;
* project-specific conventions;
* prior accepted or rejected approaches.

Repository source may be sufficient for:

* exact current implementation inspection;
* isolated mechanical changes;
* syntax or formatting corrections;
* direct validation of an already defined task;
* runtime diagnosis based entirely on current logs.

The absence of a search result is evidence only that no matching record was returned. It does not prove that no relevant knowledge exists.

If relevant:

1. run `neural search`;
2. record the exact query;
3. record returned record IDs and provenance;
4. explain briefly how the retrieved result affected the work.

If not relevant:

1. state explicitly that no NeuralEngine search was required;
2. explain why repository sources or current system evidence were sufficient.

Do not claim NeuralEngine knowledge use based only on running `neural status`.

## Query construction

Use narrow, explicit queries.

Start with one best query.

Run a second query only when:

- the first query reveals a distinct authoritative term;
- separate lifecycle or provenance records are required;
- the task spans two materially different contracts;
- the first result is ambiguous but establishes a better exact query.

Do not issue repeated speculative searches merely because earlier searches returned no results.

For ordinary repository work, use no more than two queries unless the task is explicitly a Brain investigation, migration, architecture assessment, or historical audit.

Prefer queries containing:

* project name or project key;
* affected domain;
* exact contract;
* lifecycle stage;
* relevant component;
* issue or decision being investigated.

Avoid vague queries such as `architecture`, `bugs`, or `project decisions`.

Record every exact query used.

Do not silently rewrite the query in the final report.

## Search result handling

For every relevant result, record:

* record ID;
* record type;
* project key;
* lifecycle state;
* provenance;
* source or parent record when present;
* why it is relevant;
* how it affected the task.

Distinguish record types:

### Observation

Raw or normalized evidence about something that occurred.

Do not treat an Observation as a durable conclusion.

### Experience

Interpreted evidence from completed work or outcomes.

Use it as operational learning, not as universal truth.

### Knowledge

Durable, reusable understanding promoted through the defined lifecycle.

Check its provenance and integrity boundaries before relying on it.

### Playbook

Reusable operational procedure.

Verify:

* active revision;
* applicability;
* inputs;
* constraints;
* expected outcome;
* execution provenance requirements.

### PlaybookRun

Evidence that a specific playbook revision was executed.

Do not infer execution from playbook existence alone.

### Evaluation

Assessment of a run or outcome.

Check the evaluated target and evidence.

### EvolutionProposal

Proposal for improving a playbook or durable behavior.

It is not automatically accepted or active.

### DecisionReview

Structured review of a decision and its outcome.

Check status, outcome evidence, and promotion state.

## Provenance

Never report only a record ID when provenance is available.

Provenance may include:

* source repository;
* source checkpoint;
* source review;
* originating observation;
* originating experience;
* promotion path;
* playbook revision;
* activation;
* application;
* execution record;
* user authorization.

When provenance is missing or incomplete:

1. state the limitation;
2. reduce confidence;
3. do not silently infer the missing chain.

## Conflicts

When NeuralEngine and repository source appear to conflict:

1. identify the exact conflicting statements;
2. determine whether the Brain record is stale, superseded, or scoped differently;
3. prefer current implementation for present behavior;
4. preserve durable decisions that still apply;
5. report the conflict explicitly.

Do not automatically update Brain records.

Do not automatically modify repository source to match an old record.

## Read boundary

Read-only NeuralEngine operations are allowed without additional approval.

This includes:

* `neural status`;
* `neural search`;
* reading returned records and provenance;
* reading record details;
* inspecting provenance;
* inspecting lifecycle state;
* inspecting playbook revisions and runs.

Do not describe an operation as read-only unless it cannot persist or promote data.

## Brain write boundary

Any Brain write requires explicit user authorization.

Before requesting authorization, provide a preview containing:

* proposed record type;
* proposed project key;
* proposed title or identifier;
* proposed content summary;
* source evidence;
* provenance;
* intended lifecycle state;
* expected effect;
* whether the write creates, updates, promotes, activates, or evaluates anything.

Do not perform any of the following without explicit authorization:

* create a record;
* update a record;
* promote Experience to Knowledge;
* promote DecisionReview to Experience;
* create or revise a Playbook;
* activate a Playbook revision;
* record a PlaybookRun;
* create an Evaluation;
* create an EvolutionProposal;
* change lifecycle state;
* backfill provenance;
* repair Brain data.

Authorization for one write does not authorize later writes.

## Lifecycle boundaries

Do not automatically promote records between lifecycle stages.

Creation, review, acceptance, activation, application, evaluation, and evolution are separate actions.

Do not collapse:

* Observation into Experience;
* Experience into Knowledge;
* DecisionReview into Experience;
* PlaybookRevision into activation;
* activation into application;
* application into PlaybookRun;
* PlaybookRun into Evaluation;
* Evaluation into EvolutionProposal.

Each transition requires its own contract and authorization where applicable.

## Required evidence

Every substantive task report must contain a `NeuralEngine usage` section containing:

* the result of `neural status`;
* whether `neural search` was used;
* exact search queries and returned record IDs when used;
* provenance;
* a brief explanation of how retrieved knowledge affected the work;
* or an explicit explanation why repository sources or current system evidence were sufficient and no search was needed.

When the task produces a review file, include this evidence in that file.

Otherwise include it in the final task report.

Do not claim NeuralEngine usage based only on running `neural status`.

## Completion rules

Before considering NeuralEngine-related work complete:

* verify the exact repository checkpoint;
* verify the project key;
* verify record IDs;
* verify provenance;
* verify lifecycle state;
* verify whether any write occurred;
* verify that every write had explicit authorization;
* verify that no automatic promotion occurred.

Do not commit or push repository changes without separate explicit authorization.
