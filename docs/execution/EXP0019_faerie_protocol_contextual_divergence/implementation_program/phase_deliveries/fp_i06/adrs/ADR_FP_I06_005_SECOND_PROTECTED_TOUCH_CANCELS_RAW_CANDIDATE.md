---
tags: [exp0019, faerie-protocol, fp-i06, relation-compiler, hunt-engine]
status: normative
phase: FP-I06
version: 1.0.0
last_updated: 2026-07-13
language: en
---
# ADR — Protected Second Touch Cancels Raw Candidate

## Status

Accepted.

## Decision

A later M1 contact by the Protected symbol cancels the candidate before confirmation.

## Rationale

The original asymmetry no longer exists; repeated Hunter contact alone does not cancel.

## Consequences

- The rule is encoded in contracts, Python, MQL5 mirror, schemas, golden vectors, and tests.
- A behavior change requires a new version and regenerated evidence.
- Existing runtime evidence remains immutable.

## Rejected alternatives

- Inferring missing semantics from product code.
- Using host chart state as hidden authority.
- Mutating upstream FP-I05 references in place.
- Deleting ambiguous or cancelled outcomes.

## Verification

- Unit and negative tests.
- Golden conformance vector.
- Static authority guard.
- Clean-baseline patch replay.
