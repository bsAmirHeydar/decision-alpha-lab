---
title: "ADR — Policy Outcomes Do Not Mutate Signal ID"
status: accepted
date: 2026-07-13
phase: FP-I02
---
# Policy Outcomes Do Not Mutate Signal ID

## Decision

WW/quota suppression, eligibility, and reason changes are child evidence, not signal identity fields.

## Context

The same confirmed economic event must remain one signal even as later policies suppress or annotate it.

## Consequences

- signal_id excludes eligibility and reason.
- Policy events link by parent signal_id.
- History remains append-only.


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
