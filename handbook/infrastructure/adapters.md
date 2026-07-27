# Infrastructure Adapters

## Responsibility

Adapters implement ports using concrete external mechanisms.

Examples:

- filesystem persistence,
- SQL persistence,
- JSON serialization,
- clock providers,
- UUID providers.

## Adapter rules

Adapters may:

- translate between persistence and domain representations,
- handle external resource lifecycle,
- convert external failures into stable adapter/application errors,
- enforce storage-level constraints that mirror domain requirements.

Adapters must not:

- decide business policy,
- change validation order,
- infer domain transitions,
- render CLI output,
- orchestrate use cases,
- silently repair invalid domain state.

## Mapping rule

Mapping code should be explicit and testable.

Persistence models must not leak into application services.

## Local development evidence adapter

`LocalDevelopmentEvidenceSource` implements `DevelopmentEvidenceSource` for one NeuralEngine Git
worktree. It validates the repository root and repository-relative paths, reads each selected
Markdown file once, hashes the exact bytes, conservatively parses required sections, resolves one
exact lowercase full commit, rejects merge commits, and reads the parent, subject, tree, changed
paths, and patch.

The adapter returns normalized source facts and stable source errors. It does not correlate domain
meaning, classify authority, create candidates, persist records, execute validation commands,
search for artifacts, integrate with GitHub or CI, or support background/multi-repository
ingestion.
