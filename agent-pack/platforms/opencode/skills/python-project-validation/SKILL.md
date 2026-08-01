---
name: python-project-validation
description: Validate Python repository changes using the project-defined workflow, with safe fallbacks for uv, Ruff, MyPy, and pytest. Use after implementation, before review, and when diagnosing validation failures.
compatibility: opencode
metadata:
  workflow: python-validation
  audience: developers
---

# Python Project Validation

Use this skill to validate changes in a Python repository.

The repository-defined workflow is authoritative. Generic commands are only fallbacks.

## Initial inspection

Before running validation:

1. run `neural status`;
2. read repository-local instructions;
3. inspect project configuration;
4. identify the changed scope;
5. determine whether validation is read-only or may modify files.

Inspect relevant files where present:

* `AGENTS.md`
* `CODEX.md`
* `README.md`
* `CONTRIBUTING.md`
* `pyproject.toml`
* `uv.lock`
* `pytest.ini`
* `mypy.ini`
* `ruff.toml`
* `tox.ini`
* `noxfile.py`
* `Makefile`
* `justfile`

Do not read unrelated documentation or the entire repository unless required.

## Authority order

Use validation commands in this order of authority:

1. explicit task instructions;
2. repository `AGENTS.md`;
3. repository documentation;
4. configured task runner such as `just`, `make`, `tox`, or `nox`;
5. `pyproject.toml` and tool configuration;
6. generic fallback commands.

Do not replace a repository-specific workflow with generic commands.

## Environment

Prefer the repository-managed environment.

When the repository uses `uv`, prefer:

```text
uv sync
uv run <command>
```

Do not run `uv sync`, install packages, update lockfiles, or modify the environment unless required by the task or explicitly approved.

Before dependency-changing commands, inspect:

```text
git status --short
git diff -- pyproject.toml uv.lock
```

Do not use global `pip` when the repository defines another environment workflow.

## Read-only validation

During review or assessment, validation must not modify tracked files.

Prefer:

```text
uv run ruff format --check .
uv run ruff check .
uv run mypy src tests
uv run pytest
```

Adjust paths and commands to the repository configuration.

Do not run these during read-only validation unless explicitly requested:

```text
uv run ruff format .
uv run ruff check --fix .
```

If the project uses generated files, migrations, snapshots, or golden outputs, do not regenerate them during review.

## Post-implementation validation

After an authorized implementation, run the smallest complete workflow required by the repository.

For a typical Python project without documented commands, use:

```text
uv run ruff format --check .
uv run ruff check .
uv run mypy src tests
uv run pytest
```

If formatting changes are part of the implementation and modification is permitted, use:

```text
uv run ruff format .
uv run ruff check .
uv run mypy src tests
uv run pytest
```

Do not automatically run Ruff fixes that may alter semantics.

## Scope-aware validation

Choose validation proportionally.

### Mechanical changes

Examples:

* generated-file copy;
* checksum equality;
* formatting-only update;
* metadata correction.

Use narrow validation and exact equality checks where appropriate.

### Standard changes

Examples:

* documentation;
* tests;
* local implementation fixes;
* non-public helper code.

Run the affected tests and repository-required static checks.

### Critical changes

Examples:

* domain contracts;
* persistence;
* migrations;
* user data;
* Brain behavior;
* security;
* public APIs;
* persisted schemas;
* public behavior;
* release behavior.

Run full relevant validation. Do not reduce validation solely to save tokens or time.

## Test selection

Explicit task constraints override default validation breadth.

If the user or task says not to run the full test suite, do not run it.
If the task requests commands to be reported but not executed, report them without execution.
Do not broaden validation beyond the explicitly authorized scope.

Prefer the smallest test selection that proves the requested change, followed by broader validation only when the task permits it and risk requires it.

Examples:

```text
uv run pytest tests/test_specific_module.py
uv run pytest tests/test_specific_module.py -k specific_case
uv run pytest
```

Do not claim full-suite success after running only a subset.

Do not remove, skip, weaken, or rewrite tests solely to make validation pass.

## Failure handling

When validation fails:

1. report the exact command;
2. preserve the relevant error output;
3. identify whether the failure is caused by the current change;
4. distinguish deterministic failures from environment failures;
5. do not claim completion.

Classify failures as:

* implementation defect;
* pre-existing failure;
* missing dependency;
* environment or permissions issue;
* configuration issue;
* nondeterministic or flaky behavior;
* unresolved.

Do not label a failure as pre-existing without evidence from a clean checkpoint or authoritative prior result.

## Git audit

Before and after validation, inspect:

```text
git status --short
```

For validation expected to be read-only, compare status before and after.

If validation unexpectedly modifies files:

1. stop;
2. list the modified paths;
3. identify the responsible command;
4. do not discard changes automatically;
5. ask before reverting or regenerating anything.

Do not commit or push.

## NeuralEngine usage

Follow the mandatory global NeuralEngine instructions.

Record:

* the result of `neural status`;
* whether `neural search` was required;
* exact search queries;
* returned record IDs and provenance;
* how retrieved knowledge affected validation;
* or why repository configuration was sufficient.

Running only `neural status` is not evidence that NeuralEngine knowledge was used.

Any Brain write requires preview and explicit user authorization.

## Required validation report

Use this structure:

# Validation

## Scope

State the changed paths or feature being validated.

## Environment

Report:

* Python version;
* environment manager;
* relevant tool versions when material;
* repository checkpoint.

## Commands

For each command include:

* exact command;
* result;
* concise relevant output.

## Failures and warnings

State:

* failures;
* warnings;
* skipped checks;
* reason for each skip.

## Working-tree audit

Report `git status --short` before and after validation.

State whether validation modified tracked or untracked files.

## NeuralEngine usage

Provide the mandatory usage evidence.

## Verdict

Use one of:

* `PASS`
* `PASS WITH NOTES`
* `BLOCKED`
* `FAIL`

Do not claim `PASS` when required validation was skipped or failed.
