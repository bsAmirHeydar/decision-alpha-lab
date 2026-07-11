---
type: strategy-factory-document
status: canonical
title: "Market-Event Cluster Identity"
tags:
  - strategy-factory
---

# Market-Event Cluster Identity

Multiple rows may represent one underlying market episode. Cluster identity prevents pseudo-replication and false confidence.

## Why rows are not observations

One Nasdaq move can trigger several cycle groups, timeframes, related symbols, entry candidates, and strategy families. Treating each as independent multiplies sample size without multiplying information. The cluster is the unit of train/test separation, bootstrap, and often capital exposure.

## Cluster construction

Cluster rules may use trading day, direction, shared reference/hunt, confirmation proximity, overlapping label horizons, and common underlying market move. Rules are frozen before outcome analysis. Ambiguous cases should merge rather than split when false independence is the larger risk.

## Uses

Clusters prevent train/test leakage, power cluster bootstrap, define one-thesis risk, reveal strategy overlap, and allow portfolio correlation to be measured at event level rather than row level.

