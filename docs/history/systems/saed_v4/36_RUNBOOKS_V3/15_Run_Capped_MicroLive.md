---
title: Run Capped Micro-Live
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

Operate a tightly authorized, low-risk, short-duration live stage to validate real broker and state behavior, not to prove alpha.

## Entry conditions

- I18 qualification evidence.
- Signed expiring account/generation/operator authorization.
- Kill and rollback readiness.

## Mandatory roles and separation of duties

- Authorized operator.
- Risk officer.
- Operations.
- Independent monitor.

## Procedure

1. Verify authorization and allowlists.
2. Run preflight.
3. Activate capped limits.
4. Monitor every decision, intent, fill, state, and incident.
5. Stop on mismatch or expiry.
6. Reconcile and close stage.
7. Issue reauthorization recommendation.

## Mandatory outputs

- Micro-live dossier.
- Expected-observed reconciliation.
- Incident and authorization ledger.

## Stop and escalation conditions

- Expired/revoked authorization.
- Critical mismatch.
- Loss/position/incident limit.
- Telemetry gap.

## Evidence retained

- Authorization.
- All live messages.
- Risk and broker states.
- Post-stage review.

## Completion gate

The runbook is complete only when all required artifacts are content-addressed, all exposures and deviations are recorded, an independent reviewer signs the completion state, and the downstream UCEE gate accepts the exact immutable bundle rather than a narrative summary.

## Related notes

- [[Prospective_Shadow_MicroLive_Qualification]]
- [[Release_And_Production_Qualification]]
