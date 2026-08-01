# Mandatory NeuralEngine usage

NeuralEngine is the default durable knowledge and decision layer for all OpenCode agents and models.

Repository sources describe the current implementation. NeuralEngine may contain prior decisions, experience, knowledge, playbooks, and provenance that are not recoverable from the current working tree alone.

## Start of work

At the start of every substantive task, run:

`neural status`

A substantive task includes repository work, review, diagnosis, assessment, planning, implementation, or architecture analysis.

Simple requests that only summarize already loaded instructions or skill contents do not require a new `neural status` call.

## Search decision

Before substantive analysis, review, diagnosis, planning, or editing, decide whether prior project knowledge, decisions, experience, or playbooks are relevant.

If relevant:

1. run `neural search`;
2. record the exact query;
3. record returned record IDs and provenance;
4. explain briefly how the retrieved result affected the work.

If not relevant:

1. state explicitly that no NeuralEngine search was required;
2. explain why repository sources or current system evidence were sufficient.

Do not claim NeuralEngine knowledge use based only on running `neural status`.

## Read boundary

Read-only NeuralEngine operations are allowed without additional approval.

This includes:

* `neural status`;
* `neural search`;
* reading returned records and provenance.

## Brain write boundary

Any Brain write requires:

1. a preview of the proposed record;
2. explicit user authorization;
3. no automatic promotion between lifecycle stages.

Do not create, update, promote, activate, or otherwise persist Brain records without explicit authorization.

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
