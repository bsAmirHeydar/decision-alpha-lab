---
title: Run Independent Replication
status: canonical
version: 3.0.0
created: '2026-07-13'
updated: '2026-07-13'
capability_tier: canonical
tags:
  - saed-v3
  - runbook
  - operations
---

# Mission

Rebuild the selected candidate in a clean team/environment and establish an evidence-equivalence tier.

## Entry conditions

- Frozen dossier and source contracts.
- Independent data and compute path.

## Mandatory roles and separation of duties

- Replication team.
- Original team observer only.
- Independent validator.

## Procedure

1. Rebuild data, folds, features, model, calibration, and policy.
2. Compare artifact/prediction/decision/evidence.
3. Investigate discrepancies.
4. Run alternate hardware/library where planned.
5. Sign replication result.

## Mandatory outputs

- Replication report.
- Equivalence certificate.
- Discrepancy ledger.

## Stop and escalation conditions

- Material decision mismatch.
- Unreconstructible artifact.
- Hidden mutable dependency.

## Evidence retained

- Clean environment SBOM.
- Replica artifacts.
- Comparison vectors.

## Completion gate

The runbook is complete only when all required artifacts are content-addressed, all exposures and deviations are recorded, an independent reviewer signs the completion state, and the downstream UCEE gate accepts the exact immutable bundle rather than a narrative summary.

## Related notes

- [[Independent_Replication_Program]]
- [[Evidence_Equivalence_Tiers]]
