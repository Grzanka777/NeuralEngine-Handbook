# Application Errors

## Purpose

Application errors communicate expected use-case failures across layer boundaries.

## Rules

- Use explicit error types.
- Include stable contextual identifiers.
- Preserve the original cause when wrapping infrastructure errors.
- Keep rendering outside the error type.
- Avoid leaking adapter-specific exception classes into CLI.

Good:

```python
raise PlaybookNotFoundError(playbook_id)
```

Avoid:

```python
raise Exception("something failed")
```

## Mapping

- Domain violations remain domain errors.
- Missing application resources use application errors.
- Infrastructure failures are translated at adapter/application boundaries.
- CLI maps application errors to user-facing messages and exit codes.

## Knowledge-to-Experience integrity errors

KnowledgeService retains `ExperienceNotFoundError` for missing Experience relations. It propagates
existing `DecisionReviewError` and `DecisionReviewPromotionError` instances unchanged when
`ExperienceService.get_by_id()` finds corrupt promoted ancestry. It does not wrap them or create a
parallel Knowledge-specific taxonomy.

The CLI renders controlled nonzero failures without tracebacks for:

```text
neural knowledge add
neural knowledge from-experience
neural knowledge list
neural knowledge show
neural experience knowledge
```
