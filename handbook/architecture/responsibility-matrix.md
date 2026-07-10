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
