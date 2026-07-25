# EvolutionProposal

## Responsibility

An EvolutionProposal expresses a controlled suggestion for changing a playbook based on evaluation evidence.

## Owns

- exact target `playbook_id`,
- exact source `evaluation_ids`,
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
- At least one Evaluation ID is required.
- `EvolutionProposalService` verifies that every referenced Evaluation exists and that its Run
  belongs to the target Playbook.
- Proposal and applied revision are distinct concepts.
- Public behavior changes require architectural review.

## Typical transitions

`EvolutionProposal` → `PlaybookRevision`
