---
type: strategy-factory-document
status: canonical
title: "Purged Walk-Forward Validation"
tags:
  - strategy-factory
---

# Purged Walk-Forward Validation

Random splits are prohibited for official time-dependent strategy research.

## Fold construction

Train on the past, purge any sample whose label horizon reaches the test start, apply an embargo, and test on a later contiguous block. Cluster identities remain wholly in one side. Rolling or anchored training is declared in the manifest.

## Nested selection

Hyperparameters, thresholds, feature selection, and candidate policy selection occur inside training/validation only. The outer test estimates the whole selection process, not one preselected model.

## Reporting

Show each fold's dates, regimes, cluster counts, performance, calibration, candidate selection, and failures. Aggregate only after displaying heterogeneity. One exceptional fold cannot hide repeated failure.

