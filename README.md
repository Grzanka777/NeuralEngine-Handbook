# NeuralEngine Handbook

NeuralEngine Handbook is the single source of truth for engineering rules, AI-agent policy, architecture constraints, review requirements, and generated project artifacts.

The current source synchronization checkpoint is NeuralEngine commit
`25599655d0b1483eb37f88d379f6ca99afaf828d`. It adds the first bounded local development-evidence
dogfooding path: one NeuralEngine worktree, one explicitly selected prompt, one explicitly selected
review, and one exact full non-merge commit produce a non-persisted preview. Only a separate,
authority-confirmed apply may call the existing Decision-family services.

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
