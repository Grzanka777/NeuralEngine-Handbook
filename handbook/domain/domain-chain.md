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
- `PlaybookRunService` owns optional explicit Run-to-Revision validation and reverse
  `list_for_revision(UUID)` navigation without consulting activation or application state.
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
→ explicitly promoted Experience
→ separately and explicitly created Knowledge
```

This is a complementary provenance path, not a replacement for the canonical domain chain.
DecisionOutcome is factual; DecisionReview is authorized interpretation; Experience captures
explicitly promoted operational learning; Knowledge is separately generalized; Playbook remains a
separately created repeatable procedure. A Decision may have multiple immutable outcomes and
reviews, and one Review may explicitly produce multiple Experiences under different promotion
keys. A promoted Experience selects ordered Review statements and cannot combine Reviews. Review
action provenance remains transitive through explicit outcomes; promoted Experience provenance
remains transitive through its one Review. These records exist at source commit `12097fe`; no
Review save, promotion, lifecycle transition, or later Knowledge record in this path is automatic.

At source commit `1b45beb`, explicit Knowledge capture keeps its existing durable relation:

```text
Knowledge.experience_ids
→ Experience.decision_review_promotion
→ DecisionReview
```

KnowledgeService traverses every returned or newly supplied Experience relation through the
validated `ExperienceService.get_by_id()` boundary. This preserves transitive Review provenance
without copying it into Knowledge. `neural knowledge add` and `neural knowledge from-experience`
create explicit Knowledge; `neural experience knowledge` only navigates the relation. Durable
capture is not a durable record that Knowledge informed or improved a later decision.
