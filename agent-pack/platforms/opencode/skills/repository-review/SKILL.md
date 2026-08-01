---
name: repository-review
description: Review repository changes for correctness, scope, validation, architectural compliance, and release risk. Use for diff reviews, implementation audits, readiness checks, and completion assessments.
compatibility: opencode
metadata:
  workflow: repository-review
  audience: maintainers
---

# Repository Review

Use this skill when reviewing repository changes, assessing completed implementation work, auditing a diff, or determining whether a task is ready for commit or release.

## Authority

Read repository-local instructions before reviewing, including:

* `AGENTS.md`
* `CODEX.md`
* `VISION.md`
* `CONTEXT.md`
* `pyproject.toml`
* the task prompt
* the latest authoritative review or checkpoint

Repository-specific contracts override generic defaults.

Do not read the entire repository, documentation tree, or historical review archive unless required by the task.

Use the latest authoritative review as the default checkpoint. Consult older reviews only when they contain a contract unavailable from the current source.

## Review boundaries

Review only the requested scope.

Do not:

* edit files during a read-only review;
* commit or push;
* modify unrelated files;
* invent requirements;
* infer validation success without command output;
* accept removed or weakened tests merely because validation passes;
* treat generated files as authoritative when their source is available.

Distinguish:

* blockers;
* defects;
* risks;
* deviations;
* optional improvements.

Do not present optional improvements as blockers.

## Required inspection

Identify:

1. the exact checkpoint;
2. the exact changed paths;
3. the task contract;
4. repository-specific validation requirements;
5. architecture, persistence, security, or public behavior boundaries affected;
6. whether the diff contains unrelated changes.

Inspect the complete diff locally.

For unstaged changes, use where applicable:

```text
git status --short
git diff --stat
git diff --check
git diff
```

For staged changes:

```text
git status --short
git diff --cached --stat
git diff --cached --check
git diff --cached
```

Do not assume staged and unstaged changes are equivalent.

## Risk classification

Classify work as critical when it affects:

* domain contracts;
* persistence;
* migrations;
* user data;
* security;
* Brain behavior;
* public APIs;
* persisted schemas;
* public behavior;
* release behavior.

Critical work requires full relevant validation and stronger evidence.

Documentation, tests, and local fixes are standard work unless a concrete elevated risk exists.

Mechanical operations such as copying a generated file, checksum equality, staging, formatting, and simple Git checks should remain one compact task.

## Validation

Use the repository-documented validation workflow.

Do not substitute generic commands when repository-specific commands exist.

For Python repositories without documented validation, consider:

```text
uv run ruff format --check .
uv run ruff check .
uv run mypy src tests
uv run pytest
```

Run only commands relevant to the task and repository.

Record:

* every command run;
* its result;
* skipped validation;
* the reason for each skip.

A passing test suite does not prove scope correctness or architectural compliance.

## Diff reporting

Always include:

* `git diff --stat` or staged equivalent;
* `git diff --check` or staged equivalent;
* a concise per-file hunk summary.

Do not include the full diff in the review when it exceeds 500 lines.

For a diff above 500 lines:

1. inspect the complete diff locally;
2. calculate SHA-256 of the complete diff;
3. report the hash;
4. provide a concise per-file hunk summary.

The hash identifies the inspected diff. It does not replace review of its contents.

## NeuralEngine usage

Follow the mandatory global NeuralEngine instructions.

The review must contain a `NeuralEngine usage` section with:

* the result of `neural status`;
* whether `neural search` was used;
* exact queries used;
* returned record IDs and provenance;
* how retrieved knowledge affected the review;
* or why repository sources were sufficient.

Running only `neural status` does not constitute NeuralEngine knowledge use.

Never perform a Brain write without:

1. previewing the proposed record;
2. explicit user authorization;
3. preserving lifecycle boundaries.

## Report depth

Match review depth to risk and task scope.

### Mechanical review

Use a compact report containing:

- Verdict;
- Checkpoint;
- Changed paths;
- Validation;
- equality, checksum, staging, or formatting evidence;
- Scope audit;
- NeuralEngine usage;
- Blockers and deviations.

Do not add broad architectural analysis unless evidence indicates elevated risk.

### Standard review

Use the complete required review structure, but keep findings concise.

Do not enumerate every unchanged or low-risk file when an exact changed-path list and concise per-file summary are sufficient.

### Critical review

Use the complete structure with stronger evidence for domain contracts, persistence, migrations, user data, security, Brain behavior, public APIs, persisted schemas, public behavior, or release work.

Do not shorten critical evidence solely to save tokens.

## Output economy

Do not repeat the same evidence in multiple sections.

Prefer:

- exact paths over prose inventories;
- concise per-file hunk summaries;
- one decisive explanation per finding;
- references to command results rather than repeated output;
- `None` for empty blocker or deviation sections.

The completion response should remain within 10–15 lines unless the user explicitly requests a full report in chat.

## Required review format

# Review

## Verdict

Use one of:

* `PASS`
* `PASS WITH NOTES`
* `BLOCKED`
* `FAIL`

State the decisive reason immediately.

## Checkpoint

Include the inspected commit, branch, task file, or explicit working-tree state.

## Changed paths

List exact changed paths. Do not use approximate directory summaries.

## Validation

For each command provide:

* command;
* result;
* relevant failure or warning.

## Diff audit

Include:

* diff stat;
* diff check result;
* full-diff SHA-256 when required;
* concise per-file hunk summary.

## Scope audit

State whether changes remain within scope.

Identify unrelated, missing, generated, or unexpectedly modified files.

## NeuralEngine usage

Provide the mandatory usage evidence.

## Findings

Order findings by severity:

1. blockers;
2. correctness defects;
3. integrity or security risks;
4. contract deviations;
5. non-blocking notes.

For every blocking finding include:

* affected path;
* concrete evidence;
* impact;
* required correction.

## Blockers and deviations

State explicitly:

* blockers;
* deviations;
* unresolved risks;
* or `None`.

Do not repeat the complete review in the completion response.
