# PlaybookRevisionApplication

## Responsibility

A PlaybookRevisionApplication is an immutable application-intent and audit record. The current
foundation records that an active revision reached an explicit application boundary; it does not
materialize or copy revision content into a Playbook.

Current fields are:

```text
id
applied_at
playbook_id
revision_id
proposal_id
reason
applied_by
notes
tags
source_activation_id
idempotency_key
content_changed
```

`content_changed` defaults to `False`.

## Current foundation

The implemented vertical-slice foundation includes:

- the `PlaybookRevisionApplication` domain model,
- `PlaybookRevisionApplicationRepository`,
- `JsonPlaybookRevisionApplicationRepository`,
- `NeuralPaths.PLAYBOOK_REVISION_APPLICATIONS`,
- container repository and service wiring,
- `PlaybookRevisionApplicationService.add(...)`,
- read-only `list_for_playbook(...)`, `list_for_revision(...)`, and
  `list_for_proposal(...)` navigation.

## Invariants and non-behavior

Creating an application record does not mutate Playbook, PlaybookRevision, EvolutionProposal, or
PlaybookRevisionActivation records. It does not change proposal status, apply a proposal, or
perform automatic evolution. It is not Playbook execution and does not establish or bind
PlaybookRun provenance; `content_changed=False` cannot establish revision-specific execution
provenance.

Conversely, an explicit `PlaybookRun.revision_id` does not require or imply an application record.
Run provenance is never inferred from application intent, and a revision need not be represented
by `PlaybookRevisionApplication` for the Run caller to declare that its content was used.

The application's exact `revision_id` retains stable Revision payload meaning going forward under
supported create-once repository writes. The application record does not snapshot Revision
content, mutate it, or prove pre-hardening payload history.

There is currently:

- no CLI apply command,
- no CLI application-history commands,
- no Playbook content mutation,
- no PlaybookRevision materialization,
- no proposal application,
- no application-specific repository query method.
