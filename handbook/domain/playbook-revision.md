# PlaybookRevision

## Responsibility

A PlaybookRevision is an immutable candidate snapshot of explicitly supplied revised Playbook
content. It is linked to one existing Playbook and one accepted EvolutionProposal.

## Owns

- playbook reference,
- revised content and metadata,
- source proposal reference,
- identity.

## Must not own

- repository navigation,
- unrelated playbook service responsibilities,
- infrastructure-specific persistence behavior.
- activation state,
- application state.

## Lifecycle boundary

Creating a revision does not mutate the Playbook, apply the proposal, activate the revision, or
perform automatic evolution. Activation and application are represented by separate immutable
records.

A PlaybookRun may independently carry zero or one caller-supplied `revision_id`. A supplied
relation declares that exact immutable revision content was used; omission makes no
revision-specific claim. Revision selection, activation, or application intent never supplies or
proves this Run relation.

Any Knowledge provenance retained by the parent Playbook or revised content remains UUID-based.
Supported create-once Knowledge repository writes give those exact IDs stable payload meaning
going forward; PlaybookRevision does not embed or snapshot Knowledge, add Knowledge versioning, or
provide cryptographic or filesystem tamper evidence.

## Confirmed application rule

`PlaybookRevisionService.list_for_playbook(UUID)` owns revision navigation for a playbook.
`PlaybookRunService.list_for_revision(UUID)` separately owns reverse navigation from one revision
to Runs that explicitly declare it.

The repository port remains persistence-focused and should not gain a broad `find_by_playbook_id` method solely to move application navigation into persistence.

## Invariants

- Revision identity is explicit.
- Parent playbook identity is explicit.
- Provenance to proposal is preserved.
- Revision creation does not change proposal status.
- Revision creation does not apply proposal changes.
