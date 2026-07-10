# EvolutionProposal

## Responsibility

An EvolutionProposal expresses a controlled suggestion for changing a playbook based on evaluation evidence.

## Owns

- source evaluation reference,
- proposed change,
- rationale,
- lifecycle state where modeled,
- identity.

## Must not own

- direct mutation of the playbook,
- revision persistence implementation,
- approval side effects outside application services.

## Invariants

- Proposal provenance is preserved.
- Proposal and applied revision are distinct concepts.
- Public behavior changes require architectural review.

## Typical transitions

`EvolutionProposal` → `PlaybookRevision`
