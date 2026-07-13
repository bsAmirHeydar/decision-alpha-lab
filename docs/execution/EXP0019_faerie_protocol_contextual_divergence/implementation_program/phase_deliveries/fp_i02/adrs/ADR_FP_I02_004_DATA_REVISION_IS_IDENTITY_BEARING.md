---
title: "ADR — Data Revision Is Identity-Bearing"
status: accepted
date: 2026-07-13
phase: FP-I02
---
# Data Revision Is Identity-Bearing

## Decision

Window, reference, hunt, candidate, and context evidence bind source data revision/fingerprint where source facts may change.

## Context

Late history repair can change highs, lows, first touch, or completeness; reusing old IDs would be false equivalence.

## Consequences

- New revision produces new semantic identity.
- Old evidence remains auditable.
- Cross-revision dedup is forbidden.


## Rejected alternatives

- Implicit defaults not present in the manifest.
- Free-text state or reason values.
- Runtime mutation of registries.
- Last-write-wins identity conflicts.
- Treating static MQL5 scans as successful compilation.

## Verification

- Python contract and negative tests.
- Closed JSON Schema validation.
- Golden identity vector replay.
- MQL5 static parity and local self-test compile.
- Patch boundary and previous-context regression checks.

## Rollback

Revert files in the FP-I02 file index. Persisted FP-I02 evidence remains archived; downstream checkpoints carrying FP-I02 versions are ignored by the restored code.
