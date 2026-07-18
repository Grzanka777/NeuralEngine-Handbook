# Domain Chain

The confirmed NeuralEngine chain is:

`Observation`
→ `Experience`
→ `Knowledge`
→ `Playbook`
→ `PlaybookRun`
→ `PlaybookEvaluation`
→ `EvolutionProposal`
→ `PlaybookRevision`
→ `PlaybookRevisionActivation`
→ `PlaybookRevisionApplication`

The final three stages are separate records with separate responsibilities:

- `PlaybookRevision` is an immutable candidate snapshot.
- `PlaybookRevisionActivation` is an immutable lifecycle and audit decision.
- `PlaybookRevisionApplication` is an immutable application-intent and audit record.

Creating a revision does not activate or apply it. Activation does not imply application.
The current application foundation records intent only: it does not materialize revision
content into a Playbook or mutate any related record.

## Relationship ownership

Relationship navigation belongs in application services unless persistence itself owns the concern.

Confirmed example:

- `PlaybookRevisionService.list_for_playbook(UUID)` owns playbook revision navigation.
- `PlaybookRevisionActivationService` owns activation navigation and canonical active-revision
  derivation through `get_active_revision_for_playbook(playbook_id)`.
- `PlaybookRevisionApplicationService` owns application-record navigation and delegates active
  revision resolution to `PlaybookRevisionActivationService`.
- Repository interfaces remain persistence-focused.
- `PlaybookService` should not gain unrelated persistence dependencies.

## Complementary Decision Learning chain

The implemented Decision, DecisionAcceptance, DecisionAction, DecisionOutcome, and DecisionReview
foundations record a bounded proposed choice, explicit authorization, work performed, factual
results, and authorized interpretation after Observation context:

```text
Observation
→ Decision
→ DecisionAcceptance
→ DecisionAction
→ DecisionOutcome
→ DecisionReview
→ explicitly created Experience
→ explicitly created Knowledge
```

This is a complementary provenance path, not a replacement for the canonical domain chain.
DecisionOutcome is factual; DecisionReview is authorized interpretation; Experience captures
separately created operational learning; Knowledge is generalized; Playbook remains a separately
created repeatable procedure. A Decision may have multiple immutable outcomes and multiple reviews,
including reviews over the same ordered outcome set when their idempotency keys differ. Review
action provenance is transitive through its explicit outcomes; it does not persist action IDs.
These records and their embedded EvidenceReference values exist at source commit `910f481e`; no
Review-driven lifecycle transition or later learning record in this path is automatic.
