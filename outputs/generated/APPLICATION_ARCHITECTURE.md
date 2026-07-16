# NeuralEngine Application Architecture

# Application Services

## Responsibility

Application services coordinate use cases across domain objects and ports.

They own orchestration, not persistence implementation or user-interface rendering.

## Required properties

Every application service should:

- expose one coherent responsibility,
- depend on ports rather than concrete adapters,
- preserve domain validation order,
- coordinate provenance explicitly,
- remain testable without CLI, database, filesystem, or network,
- avoid constructing dependencies internally,
- return domain/application results rather than rendered text.

## Service boundary rules

A service may:

- load entities through repository ports,
- invoke domain behavior,
- coordinate multiple domain objects,
- persist results through ports,
- raise explicit application errors,
- compose relationship navigation.

A service must not:

- instantiate repositories,
- import CLI modules,
- render Rich tables,
- parse command-line strings,
- depend on concrete SQL/filesystem adapters,
- silently change public behavior,
- absorb unrelated use cases.

## Public method design

Prefer explicit methods named after use cases.

Good:

```python
revision_service.list_for_playbook(playbook_id)
```

Avoid generic, ambiguous methods:

```python
service.process(data)
service.handle(value)
```

## Service growth rule

When a service gains unrelated responsibilities, split by use case or domain ownership.

Do not split merely to reduce line count. Split when reasons to change diverge.

## Revision lifecycle ownership

`PlaybookRevisionActivationService` owns active-revision derivation through
`get_active_revision_for_playbook(playbook_id)`.

`PlaybookRevisionApplicationService.add(...)` validates the Playbook, revision, accepted proposal,
relation consistency, optional source activation, and current active revision before saving one
application audit record. It delegates active-revision resolution to the activation service.

Its relation-list methods verify the source entity, load all application records, filter in the
application layer, preserve repository order, and perform no mutation.

---

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

---

# Ports

## Responsibility

Ports define the contracts required by the application layer from external systems.

## Port design rules

A port must:

- describe application needs, not adapter capabilities,
- use domain/application types,
- avoid database-specific concepts,
- remain minimal,
- have behaviorally meaningful method names,
- be mockable or replaceable in tests.

A port must not expose:

- SQL,
- ORM sessions,
- filesystem paths unless the application concept requires them,
- HTTP response objects,
- CLI rendering concerns,
- concrete adapter classes.

## Change policy

Changing a port is architectural work.

A port change requires:

- Codex GPT-5.5 medium,
- review of all implementations,
- review of service call sites,
- updated contract tests,
- full validation.

---

# Repository Ports

## Responsibility

Repository ports define persistence operations needed by application services.

## Allowed operations

Typical operations include:

- add/save,
- get by identity,
- list,
- delete when domain policy allows it,
- narrowly justified persistence queries.

## Forbidden expansion

Do not add repository methods merely because a relationship exists.

First ask whether the application service can compose the navigation from existing persistence operations.

Confirmed rule:

`PlaybookRevisionService.list_for_playbook(UUID)` owns playbook revision navigation.

`PlaybookRevisionApplicationRepository` remains limited to `save()`, `load_all()`, and
`get_by_id()`. Navigation by Playbook, PlaybookRevision, or EvolutionProposal is composed by
`PlaybookRevisionApplicationService`; no relation-specific query methods are part of the port.

## Repository return types

Prefer:

- domain entities,
- value objects,
- explicit optional results,
- application-facing collections.

Avoid:

- ORM models,
- database rows,
- SQL tuples,
- adapter-specific pagination objects.

## Not-found behavior

Choose one consistent contract:

- return `None`, or
- raise an explicit port/application error.

Do not mix behavior across implementations.

---

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

---

# Repository Adapters

## Responsibility

Repository adapters implement repository ports.

## Implementation rules

- Preserve domain identity exactly.
- Preserve provenance fields.
- Make serialization round-trippable.
- Keep ordering deterministic when public behavior depends on ordering.
- Handle missing records according to the port contract.
- Do not broaden the port from inside the adapter.
- Do not add business filtering without an application requirement.

## Testing requirements

Repository adapters require tests for:

- save and load,
- missing identity,
- list behavior,
- ordering where relevant,
- serialization round trip,
- invalid/corrupted persisted data,
- provenance preservation.

## Revision application adapter

`JsonPlaybookRevisionApplicationRepository` implements
`PlaybookRevisionApplicationRepository` and stores application audit records under
`NeuralPaths.PLAYBOOK_REVISION_APPLICATIONS`. It supplies only the port's basic save, load-all, and
identity lookup operations; relation filtering remains in the application layer.

---

# Dependency Injection and Container

## Responsibility

The container is the composition root.

It constructs concrete adapters and injects them into application services.

## Rules

The container may:

- instantiate repositories,
- instantiate infrastructure providers,
- instantiate application services,
- define lifecycle and sharing policy,
- expose configured services to CLI.

The container must not:

- contain business logic,
- perform use-case orchestration,
- parse CLI arguments,
- hide mutable global state,
- create cyclic dependencies.

## Constructor injection

Prefer constructor injection.

Good:

```python
service = PlaybookRevisionService(repository=revision_repository)
```

Avoid service locator access inside services:

```python
repository = container.get("revision_repository")
```

## Change policy

Any container or registration change is architectural work owned by Codex.

The current revision application foundation is wired through
`Container.playbook_revision_application_repository()` and
`Container.playbook_revision_application_service()`. The service receives its repositories and a
`PlaybookRevisionActivationService`, preserving canonical ownership of active-revision resolution.

---

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

---

# Cookbook: Add an Application Service

1. Identify the exact use case.
2. Confirm no existing service already owns it.
3. Identify required domain entities and value objects.
4. Identify required ports.
5. Define explicit application errors.
6. Implement constructor-injected dependencies.
7. Implement one coherent public method.
8. Add service-level tests using fakes.
9. Wire the service in the container.
10. Add CLI integration only if requested.
11. Run full validation.
12. Produce the review artifact.

---

# Cookbook: Add a Repository

1. Confirm the domain concept requires persistence.
2. Confirm a repository is the correct abstraction.
3. Define the minimal repository port.
4. Use domain/application types in the contract.
5. Implement the adapter.
6. Add mapping and round-trip tests.
7. Add missing-record behavior tests.
8. Register the adapter in the container.
9. Inject the repository into the owning service.
10. Run full validation.
11. Produce the review artifact.

---

# Cookbook: Add an Adapter

1. Start from an existing port.
2. Do not design from the external library API.
3. Map external types to domain/application types.
4. Translate external failures.
5. Define resource lifecycle.
6. Add adapter contract tests.
7. Register the adapter in the container.
8. Verify no concrete adapter leaks inward.
9. Run full validation.
10. Produce the review artifact.

---

# Cookbook: Wire the Container

1. Identify new concrete dependencies.
2. Confirm service constructors remain explicit.
3. Instantiate adapters before services.
4. Inject ports through constructor arguments.
5. Avoid service-locator access.
6. Keep lifecycle policy explicit.
7. Add or update container tests.
8. Verify CLI resolves the service, not the adapter.
9. Run full validation.
10. Produce the review artifact.

---

# Anti-pattern: Fat Service

## Symptom

One application service coordinates unrelated use cases and depends on many unrelated ports.

## Risk

- high coupling,
- difficult testing,
- unclear ownership,
- unrelated changes collide.

## Correction

Split by use-case responsibility or domain ownership.

Do not split solely by file length.

---

# Anti-pattern: God Repository

## Symptom

A repository exposes relationship navigation, filtering, reporting, validation, and business operations.

## Risk

- persistence controls application behavior,
- services become thin wrappers,
- adapters become difficult to replace,
- domain decisions leak outward.

## Correction

Keep persistence methods minimal. Move orchestration and navigation into application services.

---

# Anti-pattern: Service Locator

## Symptom

Application code fetches dependencies from a global container at runtime.

## Risk

- hidden dependencies,
- brittle tests,
- runtime failures,
- cyclic coupling.

## Correction

Use constructor injection and keep the container at the composition root.

---

# Anti-pattern: Business Logic in Adapter

## Symptom

An infrastructure adapter decides validation, eligibility, transition, or policy.

## Risk

- behavior changes when adapters change,
- domain rules become untestable in isolation,
- persistence becomes the source of truth.

## Correction

Move policy into domain or application services. Keep the adapter focused on translation and external interaction.

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

---

# ADR-0005: Constructor injection

Status: Accepted

## Decision

Application services receive dependencies through constructors.

The dependency container remains the composition root.

## Consequences

- Dependencies are visible.
- Services are testable with fakes.
- Service-locator access inside application code is prohibited.

---

# ADR-0006: Minimal application-driven ports

Status: Accepted

## Decision

Ports describe the minimum contracts required by application use cases.

They do not mirror every capability of an external library or persistence technology.

## Consequences

- Adapters remain replaceable.
- Port changes require architectural review.
- External types do not leak into application code.

---

# ADR-0007: Adapters contain no business policy

Status: Accepted

## Decision

Infrastructure adapters translate and interact with external systems but do not own business rules or use-case orchestration.

## Consequences

- Business behavior remains stable across adapter changes.
- Domain and service tests can run without infrastructure.
- Adapter tests focus on contracts and translation.
