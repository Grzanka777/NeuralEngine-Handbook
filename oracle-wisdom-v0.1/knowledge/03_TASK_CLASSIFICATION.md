# Task Classification

## Critical

Triggers: domain behavior, persistence, migration, Brain, user data, security, public API, persisted schema, public behavior, release and irreversible system operations.

Default controls: assessment, implementation, complete validation, independent review, staging audit and post-push verification.

## Standard

Triggers: documentation, tests, bounded fixes, local refactors and non-persisted internal work.

Default controls: implementation/assessment, validation and proportionate review.

## Mechanical

Triggers: exact copy, equality/hash checks, formatting, deterministic staging and simple Git inspection.

Default controls: one combined operation with verification.

## Rule

Use the highest class triggered by any material part. Split only when lower-risk work can be isolated without weakening critical controls.
