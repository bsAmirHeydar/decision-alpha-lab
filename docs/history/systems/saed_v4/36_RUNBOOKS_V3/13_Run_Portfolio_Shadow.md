---
title: Run Portfolio Shadow
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

Evaluate multi-Context allocation, reservations, conflicts, capacity, and dependence without order submission.

## Entry conditions

- At least two truly promoted Contexts.
- I17 portfolio bundle.
- Shadow telemetry.

## Mandatory roles and separation of duties

- Portfolio researcher.
- Risk owner.
- Operations.
- Independent reviewer.

## Procedure

1. Feed qualified opportunities.
2. Reserve risk before selection.
3. Apply limits, conflicts, capacity, and unknown-dependence penalty.
4. Reconcile reservations and decisions.
5. Run context-drop, correlation, liquidity, and restart stresses.

## Mandatory outputs

- Shadow allocation ledger.
- Stress report.
- Reservation reconciliation.

## Stop and escalation conditions

- Reservation mismatch.
- Unknown dependence treated zero.
- Critical concentration.
- Restart duplicate.

## Evidence retained

- Queue, reservation, allocation, and stress traces.

## Completion gate

The runbook is complete only when all required artifacts are content-addressed, all exposures and deviations are recorded, an independent reviewer signs the completion state, and the downstream UCEE gate accepts the exact immutable bundle rather than a narrative summary.

## Related notes

- [[Opportunity_Queue_And_Risk_Reservation_Integration]]
- [[Portfolio_Aware_Learning_And_Capital]]
