---
id: SAED-7EF8105245
title: "Calibration, Thresholds, and Selective Prediction"
type: architecture
status: canonical
domain: strategy-factory-setup-ai-edge-discovery
version: 1.0.0
created: 2026-07-13
updated: 2026-07-13
tags:
  - strategy-factory
  - setup-factory
  - ai-training
  - trainer
  - calibration
---

# Calibration, Thresholds, and Selective Prediction

## Calibration

Use fold-local Platt, isotonic or task-appropriate calibration. Report reliability tables, Brier score, expected calibration error and fold variance.

## Thresholds

Thresholds optimize declared utility subject to minimum clusters, coverage, tail and calibration constraints. They are not selected on the outer test.

## Selectivity

Plot utility, hit rate, drawdown, tail loss and coverage as abstention increases. A model that performs well only at negligible coverage is not automatically useful.

## Risk Boundary

Probability and confidence can select eligibility/risk tier but cannot directly determine leverage. Final sizing belongs to capital/risk systems.
