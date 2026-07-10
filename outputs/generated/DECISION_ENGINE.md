# NeuralEngine Decision Engine

# Decision Engine

Use this document before implementation.

## Agent selection

### Use Codex GPT-5.5 medium when any answer is yes

- Does the task add a feature?
- Does it change the domain model?
- Does it touch more than one architectural layer?
- Does it add or change a port?
- Does it add or change an adapter?
- Does it change a repository interface?
- Does it change dependency injection?
- Does it add a CLI command?
- Does it change persisted schema?
- Does it change public behavior?
- Does it change validation order?
- Does it change provenance semantics?
- Does it add architecture documentation?

### DeepSeek is allowed only when all are true

- The task is a concrete post-review correction.
- The change is normally limited to one to three files.
- No feature is added.
- No architecture changes.
- No persisted schema changes.
- No public behavior changes.
- No validation-order changes.
- No provenance changes.

## Layer decision tree

```text
Does the behavior express a domain invariant?
├── Yes → Domain
└── No
    └── Does it coordinate a use case?
        ├── Yes → Application service
        └── No
            └── Does it define an external contract?
                ├── Yes → Port
                └── No
                    └── Does it implement an external concern?
                        ├── Yes → Infrastructure adapter
                        └── No
                            └── Is it user interaction/rendering?
                                ├── Yes → CLI
                                └── No → Reassess the design
```

## Repository decision tree

```text
Is the requested operation persistence?
├── No → Do not add it to a repository
└── Yes
    └── Is it generic persistence behavior?
        ├── Yes → Repository port may own it
        └── No
            └── Can application services compose it?
                ├── Yes → Keep it in the service
                └── No → Require architecture review
```

## New feature decision tree

```text
New behavior
├── Domain concept changed?
│   ├── Yes → Domain + tests
│   └── No
├── Persistence required?
│   ├── Yes → Port + adapter + tests
│   └── No
├── Use-case orchestration required?
│   ├── Yes → Application service + tests
│   └── No
├── Dependency wiring changed?
│   ├── Yes → Container + tests
│   └── No
└── User-facing command required?
    ├── Yes → CLI + tests
    └── No
```

## Priority order

1. Correctness.
2. Domain integrity.
3. Architecture.
4. Maintainability.
5. Testability.
6. Performance.
7. Convenience.

---

# Responsibility Matrix

| Concern | Owning layer | Forbidden locations |
|---|---|---|
| Domain invariant | Domain | CLI, adapter |
| Use-case orchestration | Application | CLI, repository adapter |
| Persistence contract | Port | Domain, CLI |
| Persistence implementation | Infrastructure | Domain, application |
| Dependency construction | Container | Domain entity, service |
| Input parsing | CLI | Domain entity |
| Output rendering | CLI | Repository |
| Relationship navigation | Application service by default | Repository unless persistence-owned |
| Validation of domain state | Domain/application as appropriate | Infrastructure-only |
| Provenance policy | Domain/application architecture | CLI-only |

---

# Domain Change Checklist

- Which entity or value object owns the new responsibility?
- Does the change preserve the canonical domain chain?
- Is provenance preserved?
- Is validation placed before persistence?
- Does the change require a new port?
- Does it require an adapter?
- Does it require application orchestration?
- Does container wiring change?
- Does public behavior change?
- Does persisted schema change?
- Are unit and service tests sufficient?
- Is Codex assigned?

---

# New CLI Command Checklist

- Does an application service already expose the required use case?
- Is business logic absent from the command handler?
- Is dependency resolution delegated to the container?
- Are UUID inputs validated consistently?
- Are errors mapped to useful user-facing messages?
- Are CLI tests included?
- Is public output intentionally specified?
- Is the task assigned to Codex?

---

# Application Service Checklist

- Is the use case explicit?
- Does one service clearly own it?
- Are dependencies constructor-injected?
- Are dependencies ports rather than adapters?
- Is business logic outside CLI and infrastructure?
- Are errors explicit?
- Is validation order preserved?
- Is provenance preserved?
- Can the service be tested without external systems?
- Are tests written with fakes?
- Is container wiring updated?
- Is Codex assigned when architecture changes?

---

# Repository Checklist

- Does the domain concept require persistence?
- Is the port minimal?
- Are method names persistence-focused?
- Are domain/application types used?
- Is relationship navigation better owned by a service?
- Is missing-record behavior consistent?
- Are adapters covered by round-trip tests?
- Is ordering deterministic where observable?
- Is provenance preserved?
- Are all implementations updated after a port change?

---

# Adapter Checklist

- Does the adapter implement an existing port?
- Are external types translated?
- Are external failures mapped?
- Is resource lifecycle explicit?
- Is business policy absent?
- Is validation order unchanged?
- Are adapter contract tests present?
- Does no adapter type leak inward?
- Is container registration explicit?

---

# Container Checklist

- Is the container only composing dependencies?
- Are constructors explicit?
- Are adapters instantiated before services?
- Are lifetimes clear?
- Is mutable global state absent?
- Are cyclic dependencies absent?
- Does CLI resolve services rather than repositories?
- Are container tests updated?
