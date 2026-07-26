# PlaybookRevisionActivation

## Responsibility

A PlaybookRevisionActivation is a separate immutable lifecycle and audit record for an explicit
manual or external-system decision about one PlaybookRevision.

Supported decisions are:

- `active`,
- `superseded`,
- `rejected`.

Activation does not imply application. It does not materialize revision content into a Playbook,
mutate a Playbook or PlaybookRevision, change EvolutionProposal status, apply a proposal, or
perform automatic evolution.

Activation also does not imply execution. PlaybookRun revision provenance is supplied explicitly
by the Run caller and is never selected from current or historical activation state. A revision
does not need to be active for a caller to declare truthfully that its content was used.

## Application ownership

`PlaybookRevisionActivationService` owns read-only lifecycle navigation by Playbook,
PlaybookRevision, and EvolutionProposal. It also owns canonical active-revision derivation through:

```python
PlaybookRevisionActivationService.get_active_revision_for_playbook(playbook_id)
```

Activation records are replayed in repository order only inside this service. Consumers must
delegate active-revision resolution rather than duplicate lifecycle replay.

Each relation-list method verifies its source entity, loads all activation records through
`PlaybookRevisionActivationRepository.load_all()`, filters in the application layer, and preserves
repository order. No relation-specific repository query methods are added.

## Current CLI

Read-only lifecycle inspection exists through:

```text
neural playbook revision-history PLAYBOOK_UUID
neural playbook active-revision PLAYBOOK_UUID
neural revision activation-history REVISION_UUID
neural revision runs REVISION_UUID
neural proposal activation-history PROPOSAL_UUID
```

`neural revision runs` is execution-provenance navigation through `PlaybookRunService`; unlike the
other commands in this list, it does not inspect lifecycle records.

Explicit lifecycle decisions can be recorded through:

```text
neural revision activate ...
neural revision supersede ...
neural revision reject ...
```

These write only PlaybookRevisionActivation records.
