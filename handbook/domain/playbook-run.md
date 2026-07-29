# PlaybookRun

## Responsibility

A PlaybookRun is the caller's explicit record that one existing Playbook was manually or
externally applied to a concrete situation. NeuralEngine does not execute Playbook steps.

## Owns

- exact base Playbook reference,
- optional exact PlaybookRevision execution-provenance reference,
- execution state,
- runtime inputs and outputs where modeled,
- identity.

## Must not own

- reusable playbook definition,
- evaluation policy,
- proposal approval logic.

## Invariants

- A run references exactly one playbook identity.
- `playbook_id` is the exact persisted relation to that Playbook.
- A Run references zero or one PlaybookRevision through `revision_id`; one revision may be
  referenced by zero or many Runs.
- Under supported repository writes, one Run UUID binds to one complete validated modeled
  `PlaybookRun` payload. Complete equality covers `id`, `timestamp`, `playbook_id`, `revision_id`,
  `situation`, ordered `actions_taken`, `outcome`, `success`, ordered `evidence`, `notes`, and
  ordered `tags`.
- An absent UUID is published once without replacement. An identical complete same-ID replay is a
  successful no-op that preserves bytes, inode, size, mtime, and ctime. Any different complete
  same-ID payload conflicts without overwrite.
- Repository replay is distinct from ordinary `PlaybookRunService.add()` and `neural run add`.
  Those public creation paths continue to generate a fresh Run UUID and timestamp; they do not
  expose semantic or content-level replay across newly generated UUIDs.
- Present repository data is validated as `PlaybookRun`. Malformed JSON or model data, non-UUID
  filename stems, and filename/request-to-payload UUID mismatches fail visibly and are not
  repaired, overwritten, or skipped. Missing `get_by_id()` retains `None`, and valid existing JSON
  remains readable without migration.
- The Run caller is the authority for `revision_id`. A supplied UUID declares that exact immutable
  revision content was used.
- Under supported create-once Revision repository operations, that UUID retains stable complete
  Revision payload meaning going forward. Run does not snapshot the Revision payload.
- `revision_id=None` makes no revision-specific execution claim. It covers base Playbook
  execution, legacy records, or unknown revision provenance.
- Write validation requires actions first, then the base Playbook, then a supplied revision, then
  same-Playbook revision ownership. Only a fully valid Run is saved; no failure path writes.
- Linked Run reads validate that the revision exists and belongs to the Run's Playbook. Missing or
  cross-Playbook revision provenance fails closed; legacy Runs without the relation remain valid.
- Revision provenance is never inferred from active-revision state, activation history,
  repository order, timestamps, `PlaybookRevisionApplication`, or application-intent records.
- A declared revision need not be active or applied.
- No retroactive guarantee is made for Revision payload history recorded before the create-once
  hardening.
- Runtime state must not mutate the playbook definition.
- Evaluation is modeled separately.

## Navigation and CLI

`PlaybookRunService.list_for_revision(revision_id)` validates the requested revision, filters
explicit matches in repository order, and validates every returned Run.

Implemented CLI surfaces are:

```text
neural run add --revision-id REVISION_UUID ...
neural run list
neural run show RUN_UUID
neural revision runs REVISION_UUID
```

Run list and show output render the revision ID or `-` when absent.

## Explicit non-behavior

The relation does not implement automatic active-revision selection,
Run-to-PlaybookRevisionApplication binding, Playbook materialization, revision content execution,
an execution engine, service/CLI Run idempotency, semantic replay, content deduplication across
fresh UUIDs, mixed or partial revision execution, multiple revisions per Run, automatic
activation/application, per-Knowledge contribution attribution, causal improvement, automatic
learning, or Consigliere integration.

The persistence contract adds no update, delete, replace, versioning, migration, repair, backup,
transaction, generalized crash-recovery, tamper-proofing, cryptographic integrity, or protection
from direct filesystem mutation. No other record automatically creates a Run. Saving one
explicitly supplied Run creates no automatic additional Run, Evaluation, DecisionAction, Outcome,
Review, Experience, Knowledge, or evolution record.

## Typical transitions

`PlaybookRun` → `PlaybookEvaluation`
