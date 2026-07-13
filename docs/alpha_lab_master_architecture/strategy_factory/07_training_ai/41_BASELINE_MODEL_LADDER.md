---
type: strategy-factory-document
status: canonical
title: "Baseline Model Ladder"
tags:
  - strategy-factory
---

# Baseline Model Ladder

Every advanced model must beat transparent baselines on the same frozen folds and costs.

## Ladder

Never trade, always trade, unconditional base rate, session-only, anatomy-only, confirmation-only, single-feature threshold, regularized logistic classification, and ridge regression. Only then add boosted trees, rankers, or sequence models.

## Why simple models

They expose whether the signal is mostly a base-rate effect, reveal leakage, calibrate expected uplift, and often outperform complex models in small event datasets. Complexity earns permission through OOS evidence.

## Metric discipline

Classification uses log loss, Brier score, calibration, and economic utility—not accuracy alone. Regression uses error plus realized policy value. Ranking uses event-level top-choice net R and regret versus oracle and baseline.

