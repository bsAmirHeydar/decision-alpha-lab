---
title: Compile Runtime and MQL5 Parity
status: canonical
version: 4.0.0
created: '2026-07-13'
updated: '2026-07-13'
capability_tier: canonical
tags:
  - saed-v4
  - runbook
  - operations
---

# Mission

Convert admitted policy into one immutable runtime generation and prove Python/export/MQL5 decision equivalence.

## Entry conditions

- Signed admission.
- Policy graph.
- Features/preprocessing/model/calibration/treatments/fallback.

## Mandatory roles and separation of duties

- Runtime compiler engineer.
- MQL5 engineer.
- Independent parity reviewer.

## Procedure

1. Build immutable bundle.
2. Validate hashes and capabilities.
3. Export model.
4. Generate parity vectors including boundaries/OOD/missing.
5. Compile MetaEditor matrix.
6. Compare predictions and decisions.
7. Test activation, restart, rollback, and no-order authority.

## Mandatory outputs

- Runtime bundle.
- Compile logs.
- Parity certificate.
- Rollback generation.

## Stop and escalation conditions

- Actual compile absent.
- Decision mismatch.
- Partial activation.
- Duplicate decision on restart.

## Evidence retained

- Source/export/EX5 hashes.
- Logs.
- Vectors.
- Activation trace.

## Completion gate

The runbook is complete only when all required artifacts are content-addressed, all exposures and deviations are recorded, an independent reviewer signs the completion state, and the downstream UCEE gate accepts the exact immutable bundle rather than a narrative summary.

## Related notes

- [[Runtime_Compilation_MQL5_Parity_And_Fallback]]
- [[Evidence_Equivalence_Tiers]]
