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

## Knowledge persistence integrity errors

The repository port exposes `KnowledgeRepositoryError` with three distinct failures:

- `KnowledgePersistenceConflictError` for a same-ID different-payload collision;
- `KnowledgeStoredDataError` for malformed or invalid stored Knowledge;
- `KnowledgeIdentityMismatchError` when the requested or filename UUID differs from embedded
  `Knowledge.id`.

These errors preserve visible create-once failures across the application boundary. Knowledge
services do not repair, overwrite, skip, or silently substitute persisted data. Existing
Knowledge-related CLI handlers render the repository error message and exit with code 1 without a
traceback; no commands or options were added.

## PlaybookRevision persistence integrity errors

The repository port exposes `PlaybookRevisionRepositoryError` with three distinct failures:

- `PlaybookRevisionPersistenceConflictError` for a same-ID different-payload collision;
- `PlaybookRevisionStoredDataError` for malformed or invalid stored Revision data or a non-UUID
  filename stem;
- `PlaybookRevisionIdentityMismatchError` when the requested or filename UUID differs from the
  embedded `PlaybookRevision.id`.

These errors fail visibly without overwrite, repair, skipping, or substitution. Existing affected
Revision, Run, Evaluation, Proposal, activation, Knowledge-navigation, and DecisionAction CLI
paths render the repository error message and exit with code 1 without a traceback. No command or
option was added, and normal success output is unchanged.
