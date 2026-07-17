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

The Decision foundation is wired through `Container.decision_repository()` and
`Container.decision_service()`. The container supplies `JsonDecisionRepository` and
`JsonObservationRepository` to `DecisionService`; Decision CLI handlers resolve the service and do
not construct repositories.

The acceptance foundation is wired through `Container.decision_acceptance_repository()` and
`Container.decision_acceptance_service()`. The container supplies
`JsonDecisionAcceptanceRepository` and `JsonDecisionRepository` to
`DecisionAcceptanceService`; acceptance CLI handlers construct no repositories.

The action foundation is wired through `Container.decision_action_repository()`,
`Container.decision_action_service()`, and `Container.decision_lifecycle_service()`. The action
service receives JSON action, Decision, acceptance, and PlaybookRun repositories. The lifecycle
service receives Decision, acceptance, and action repositories. CLI handlers resolve services and
construct no repositories.
