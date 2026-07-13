---
type: strategy-factory-document
status: canonical
title: "Meta-Labeling: Trade, Skip, or Review"
tags:
  - strategy-factory
---

# Meta-Labeling: Trade, Skip, or Review

Meta-labeling lets anatomy remain deterministic while a model learns when the event has favorable conditional economics.

## Target design

Targets may be positive net R, target-before-stop, or expected R above a hurdle. The hurdle includes costs and uncertainty. Class imbalance is handled inside training only.

## Decision threshold

Choose thresholds on training/validation according to net utility, risk budget, and capacity. Calibrate probabilities. Live missing-feature or out-of-distribution states default to skip or review.

## Evaluation

Report coverage, expectancy of traded and skipped sets, uplift over always-trade, calibration by probability bucket, stability by fold, and missed-tail cost. A model that improves win rate while removing convex winners may be harmful.

