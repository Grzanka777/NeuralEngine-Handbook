# Validation Policy

Preferred command:

```bash
./scripts/validate.sh
```

Required checks:

```bash
ruff format --check .
ruff check .
mypy src tests
pytest
```

Never claim success unless all required checks pass.

When validation fails:

- show the failing command,
- include relevant output,
- identify whether the failure is pre-existing,
- do not bypass or suppress the failure.
