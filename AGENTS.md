# NeuralEngine Handbook Agent Rules

## Before editing

1. Read this file.
2. Read `handbook/constitution/CONSTITUTION.md`.
3. Read `handbook/workflow/development-workflow.md`.
4. Run the current test suite.

## Scope

- Treat `handbook/` and `templates/` as source files.
- Treat `outputs/` as generated files.
- Do not edit generated outputs manually.
- Keep generators deterministic.
- Add tests for generator behavior.
- Do not commit or push unless explicitly instructed.

## Validation

```bash
pytest
ruff check .
mypy src
```
