# NeuralEngine Handbook

NeuralEngine Handbook is the single source of truth for engineering rules, AI-agent policy, architecture constraints, review requirements, and generated project artifacts.

The current source synchronization checkpoint is NeuralEngine commit
`18788adacf75ff7f11d0dd6f28e5da8cf143081b`. It includes explicit optional
PlaybookRun-to-PlaybookRevision execution provenance: the Run caller may declare one exact
immutable revision, while omission makes no revision-specific claim.

## What it generates

```bash
handbook build
```

The command generates:

- Claude Skill package,
- `AGENTS.generated.md`,
- Codex task template,
- DeepSeek task template,
- review template,
- consolidated handbook.

## Repository structure

```text
handbook/     Source knowledge
templates/    Generated artifact templates
src/          Generator implementation
outputs/      Generated files
tests/        Generator tests
```

## Development

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
handbook build
pytest
ruff check .
mypy src
```

## Policy

The generated outputs are derivative artifacts. Edit source documents under `handbook/` and templates under `templates/`, then rebuild.
