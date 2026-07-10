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
