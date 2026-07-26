---
title: Run Prospective Paper
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

Accumulate forward-only evidence under a frozen generation and no tuning.

## Entry conditions

- Promotion candidate.
- Frozen prospective plan.
- Operational readiness for paper/shadow.

## Mandatory roles and separation of duties

- Program owner.
- Operations.
- Independent monitor.
- Model-risk reviewer.

## Procedure

1. Freeze all artifacts and authorizations.
2. Start opportunity-complete logging.
3. Reconcile expected/observed decisions, fills, costs, and outcomes.
4. Monitor safety sequentially.
5. Record incidents and overrides.
6. Close at predeclared horizon or stopping rule.
7. Issue dossier.

## Mandatory outputs

- Prospective dossier.
- Opportunity ledger.
- Incident and deviation report.

## Stop and escalation conditions

- Policy or data-contract change.
- Incomplete logging.
- Critical mismatch.
- Unauthorized tuning.

## Evidence retained

- Runtime hashes.
- All opportunities.
- Telemetry.
- Review signatures.

## Completion gate

The runbook is complete only when all required artifacts are content-addressed, all exposures and deviations are recorded, an independent reviewer signs the completion state, and the downstream UCEE gate accepts the exact immutable bundle rather than a narrative summary.

## Related notes

- [[Prospective_Challenge_Protocol]]
- [[Paper_Trading_Protocol]]
