# ADR-0006: Minimal application-driven ports

Status: Accepted

## Decision

Ports describe the minimum contracts required by application use cases.

They do not mirror every capability of an external library or persistence technology.

## Consequences

- Adapters remain replaceable.
- Port changes require architectural review.
- External types do not leak into application code.
