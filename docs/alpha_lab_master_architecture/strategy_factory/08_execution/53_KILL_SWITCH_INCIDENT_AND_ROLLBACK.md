---
type: strategy-factory-document
status: canonical
title: "Kill Switch, Incident Response, and Rollback"
tags:
  - strategy-factory
---

# Kill Switch, Incident Response, and Rollback

The platform must fail closed when data, model, state, or broker behavior becomes uncertain.

## Kill conditions

Stale feed, feature schema mismatch, model hash mismatch, clock/DST failure, reconciliation mismatch, excessive slippage, repeated rejects, daily loss, unexpected event-rate spike, duplicate intent, or manual operator activation.

## Incident record

Capture timeline, affected strategies/positions, current exposure, logs, artifacts, root cause, containment, rollback, data correction, and re-entry criteria. Do not resume because the symptom disappeared.

## Rollback

Restore previous approved model/config, disable strategy, or return to paper. Rollback commands and compatible artifact hashes are stored with each deployment.

