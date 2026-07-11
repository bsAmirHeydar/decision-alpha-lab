---
type: strategy-factory-document
status: canonical
title: "Runbook — Experiment, Train, and Compare"
tags:
  - strategy-factory
---

# Runbook — Experiment, Train, and Compare

A repeatable experiment run produces evidence rather than an ad hoc notebook result.

## Before run

Confirm manifest hash, source data version, trial registration, feature availability, candidate count, labels, cost model, and fold plan. Reserve an untouched confirmation interval.

## Run sequence

Audit bars → emit events → snapshot → candidates → outcomes → standard statistics → nulls → walk-forward baseline → challengers → calibration → ranking → anti-overfit suite → model card → report.

## Selection

Use the declared metric at cluster level. Do not choose a different metric because it looks better. Compare model uplift with complexity and stability. Preserve all candidates and predictions.

## After run

Record failure modes, unresolved anomalies, and whether the hypothesis advances, changes version, or retires. No live action follows directly.

