# Dependency Lifecycle

## Default policy

Prefer explicit, simple lifetimes.

- Stateless services may be reused.
- Repositories may be reused when their adapter is safe to share.
- Per-operation resources must be scoped explicitly.
- Global mutable singletons are forbidden.

## Resource ownership

The component that opens an external resource must have a defined closing strategy.

Examples:

- database connection/session,
- file handle,
- transaction,
- network client.

Resource cleanup must not depend on process termination.
