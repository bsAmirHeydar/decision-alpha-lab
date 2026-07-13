---
title: "ADR — Revisions Invalidate Only Dependent Windows"
status: accepted
date: 2026-07-13
phase: FP-I04
---
# Revisions Invalidate Only Dependent Windows

## Decision

Late inserts, corrections, and deletes invalidate the changed minutes and downstream windows that consume them, not the entire historical store.

## Context

Faerie Protocol compares two symbols at exact temporal boundaries. Any hidden time shift, synthetic data, mutable duplicate choice, or broad invalidation would change references and first-sweep ordering downstream.

## Consequences

- The rule is encoded in Python contracts, MQL5 mirrors, schemas, tests, and golden vectors.
- Violations produce a closed reason code and prevent a READY result.
- Any future alternative requires a versioned policy and rebaseline.
- Historical evidence remains immutable; repair creates a new revision.

## Rejected alternatives

- Align by bar index or nearest timestamp.
- Forward-fill absent minutes.
- Choose a conflicting vendor delivery by arrival order.
- Recompute and rewrite all historical identities after one correction.
- Accept incremental output without batch differential evidence.

## Verification

- Positive and negative phase tests.
- Golden conformance vectors.
- MQL5 static contract checks.
- Clean-baseline patch application and cumulative regressions.

## Rollback

Remove only FP-I04-indexed files and restore FP-I03 as the accepted boundary. Preserve generated revision evidence for audit.
