# Policy Engine

## Input

A user goal, project task, proposed change or requested agent prompt.

## Pipeline

```text
Need and priority
→ Task classification
→ Workflow selection
→ Agent role
→ Execution profile
→ Platform routing
→ Runtime model mapping
→ Manual-versus-agent decision
→ Prompt or command generation
```

## Output

One auditable Decision Package with one recommended route.

## Invariants

- Task class does not depend on model availability.
- Workflow is not weakened because quota is constrained.
- Agent role never contains a model name.
- Platform and runtime model are separate decisions.
- Model substitution preserves execution profile.
- Project-specific authority overrides generic routing.
- A Decision Package is advisory until risky actions are authorized.

## Conflict resolution

1. Preserve data, security and Brain integrity.
2. Follow current repository authority.
3. Minimize irreversible consequences.
4. Minimize scope.
5. Minimize agent and token use.
