---
id: SAED-46DEBFFFC7
title: "Walk-Forward Folds, Clusters, Purge, and Embargo"
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
  - dataset
  - walk-forward
---

# Walk-Forward Folds, Clusters, Purge, and Embargo

## Split Unit

The split unit is the highest relevant dependence cluster: Context occurrence, overlapping market event, shared higher-timeframe structure or regime block.

## Walk-Forward

Training precedes validation chronologically. Inner folds tune models and thresholds. Outer folds estimate the complete selection procedure. A final locked period is used once.

## Purge

Remove training observations whose label horizons overlap the validation decision window.

## Embargo

Reserve time after validation boundaries to prevent leakage through overlapping structures, features or long-held outcomes.

## Candidate Rule

All Treatment siblings from one opportunity remain in the same fold.
