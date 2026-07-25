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

## Narrow application reader boundary

`ExperienceReader` is defined beside `KnowledgeService` because it describes one application
service's validated read need rather than a persistence contract. It exposes only:

```text
get_by_id(experience_id)
```

`ExperienceService` satisfies the protocol structurally. The protocol prevents KnowledgeService
from depending on the broader raw `ExperienceRepository` surface or duplicating promoted
Experience validation. No repository port changed for this boundary.
