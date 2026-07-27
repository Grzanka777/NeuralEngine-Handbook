# NeuralEngine Handbook

NeuralEngine Handbook is the single source of truth for engineering rules, AI-agent policy, architecture constraints, review requirements, and generated project artifacts.

The current source synchronization checkpoint is NeuralEngine commit
`49db077c00e67c1d3b5f25ec92b46c83518a30bb`. It includes PlaybookRevision create-once
persistence integrity: one UUID binds to one complete validated modeled payload under supported
repository operations, identical replay is a byte-preserving no-op, and conflicting, invalid, or
identity-mismatched stored data fails visibly without replacement or repair.

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
