---
type: strategy-factory-document
status: canonical
title: "Observability and Live Monitoring"
tags:
  - strategy-factory
---

# Observability and Live Monitoring

Monitoring spans anatomy production, model inference, risk decisions, broker execution, and realized economics.

## Telemetry

Event counts, missing references, feature missingness, decision latency, score distribution, trade coverage, risk reservations, order rejects, fill/slippage, open exposure, realized R, calibration, and drift.

## Dashboards and alerts

Separate health alerts from performance alerts. A single loss is not an incident; missing data or unauthorized exposure is. Define warning, degraded, and blocked states with response playbooks.

## Research feedback

Live traces enter a quarantined evaluation store. They may update reports and drift analysis but do not automatically retrain or change rules. Promotion of a retrained model follows the full lifecycle.

