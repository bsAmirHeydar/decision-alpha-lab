---
title: "ADR — Open Decisions Are Explicit Values"
status: accepted
date: 2026-07-13
phase: FP-I02
---
# Open Decisions Are Explicit Values

## Decision

FP-DEC-012 is represented as QuotaConsumptionPolicy.UNSET and in open_decision_ids.

## Context

Omitting the field could be mistaken for a default and accidentally authorize live consumption.

## Consequences

- Research/paper contracts may proceed.
- Quota CONSUMED transition fails under UNSET.
- Live manifest construction fails.


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
