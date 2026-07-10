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
