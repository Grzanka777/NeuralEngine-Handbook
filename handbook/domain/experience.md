# Experience

## Responsibility

An Experience represents explicitly recorded operational learning. It may be created directly,
derived from one Observation, or explicitly promoted from selected DecisionReview statements.

## Owns

- interpreted outcome,
- contextual meaning,
- provenance back to observations,
- optional immutable DecisionReview promotion provenance,
- identity.

## Must not own

- generalized reusable knowledge,
- execution instructions,
- evaluation policy.

## Invariants

- Provenance is preserved.
- Interpretation is explicit.
- Creation does not erase source observations.
- Plain and Observation-derived Experiences have `decision_review_promotion is None`.
- A promoted Experience contains one optional `DecisionReviewPromotion`; it remains Experience,
  not generalized Knowledge.

## Typical transitions

`Experience` → `Knowledge`

The application layer coordinates this separate explicit transformation. Experience creation does
not create Knowledge automatically.
