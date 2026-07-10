# ADR-0002: Canonical domain chain

Status: Accepted

## Decision

The canonical NeuralEngine chain is:

`Observation`
→ `Experience`
→ `Knowledge`
→ `Playbook`
→ `PlaybookRun`
→ `PlaybookEvaluation`
→ `EvolutionProposal`
→ `PlaybookRevision`

## Consequences

- New features must identify their position in the chain.
- Transitions are application use cases.
- Provenance must not be lost between stages.
- A later-stage object must not silently absorb the responsibility of an earlier-stage object.
