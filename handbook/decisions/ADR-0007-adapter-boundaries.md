# ADR-0007: Adapters contain no business policy

Status: Accepted

## Decision

Infrastructure adapters translate and interact with external systems but do not own business rules or use-case orchestration.

## Consequences

- Business behavior remains stable across adapter changes.
- Domain and service tests can run without infrastructure.
- Adapter tests focus on contracts and translation.
