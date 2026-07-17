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

The implemented Decision, DecisionAcceptance, and DecisionAction foundations record a bounded
proposed choice, explicit authorization, and work performed after Observation context:

```text
Observation
→ Decision
→ DecisionAcceptance
→ DecisionAction
→ future DecisionOutcome
→ future DecisionReview
→ Experience
→ Knowledge
```

This is a complementary provenance path, not a replacement for the canonical domain chain.
DecisionOutcome is factual; Experience is interpreted; Knowledge is generalized; Playbook remains
a separately created repeatable procedure. Decision, DecisionAcceptance, DecisionAction, and their
embedded EvidenceReference values exist at source commit `1964356`; no Outcome, Review, or later
transition in this path is automatic.
