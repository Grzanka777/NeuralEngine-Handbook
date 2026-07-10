# PlaybookRevision

## Responsibility

A PlaybookRevision represents a concrete versioned change associated with a playbook.

## Owns

- playbook reference,
- revision content or metadata,
- source proposal reference where applicable,
- identity.

## Must not own

- repository navigation,
- unrelated playbook service responsibilities,
- infrastructure-specific persistence behavior.

## Confirmed application rule

`PlaybookRevisionService.list_for_playbook(UUID)` owns revision navigation for a playbook.

The repository port remains persistence-focused and should not gain a broad `find_by_playbook_id` method solely to move application navigation into persistence.

## Invariants

- Revision identity is explicit.
- Parent playbook identity is explicit.
- Provenance to proposal is preserved where applicable.
