# ADR-0001: Service-owned relationship navigation

Status: Accepted

## Decision

Relationship navigation that can be composed from persistence operations belongs in application services rather than repository interfaces.

## Context

Playbook revision navigation previously risked expanding repository responsibilities and coupling unrelated services.

## Consequences

- Repository ports remain persistence-focused.
- Application services own use-case navigation.
- Service tests describe the relationship behavior.
