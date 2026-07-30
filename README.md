# NeuralEngine Handbook

NeuralEngine Handbook is the single source of truth for engineering rules, AI-agent policy, architecture constraints, review requirements, and generated project artifacts.

The current source synchronization checkpoint is NeuralEngine commit
`f828d1eef787a1a7d20a4b413dab91d32143014e`. It includes the read-only Neural
Doctor readiness diagnostics: a bounded `neural doctor` command inspects the
selected home and Brain, validates the store topology, JSON record readability,
UTF-8, domain schema integrity, filename/payload identity, per-store duplicate
IDs, and a deterministic SHA-256 manifest, then exits `0` for `READY` or `1`
for `NOT READY` without writing any state.

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
