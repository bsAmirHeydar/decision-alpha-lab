---
title: Onboard a 100-Context Fleet
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

Scale Context onboarding in waves while preserving central invariance, differential parity, and independent stop conditions.

## Entry conditions

- Prioritized Context inventory.
- I16 onboarding factory.
- Fleet compute and validation capacity.

## Mandatory roles and separation of duties

- Migration program lead.
- Context owners.
- Platform.
- Validation.
- Operations.

## Procedure

1. Classify Contexts by complexity and dependency.
2. Freeze waves and adapters.
3. Scaffold cells.
4. Run differential replay against legacy.
5. Stop failing cell without altering passed cells.
6. Execute tournaments and evidence gates independently.
7. Publish fleet status.

## Mandatory outputs

- 100 cell manifests.
- Wave reports.
- Differential ledgers.
- Blocked-context register.

## Stop and escalation conditions

- Central engine change without ADR.
- Behavior change before parity.
- Fleet-wide shared failure.

## Evidence retained

- Source hashes.
- Adapter outputs.
- Per-cell QA.
- Fleet invariance hash.

## Completion gate

The runbook is complete only when all required artifacts are content-addressed, all exposures and deviations are recorded, an independent reviewer signs the completion state, and the downstream UCEE gate accepts the exact immutable bundle rather than a narrative summary.

## Related notes

- [[Context_Cell_Fleet_Control_Plane]]
- [[Context_Transfer_And_Negative_Transfer_Control]]
