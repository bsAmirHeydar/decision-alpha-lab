---
type: strategy-factory-document
status: canonical
title: "Full Test Catalog"
tags:
  - strategy-factory
---

# Full Test Catalog

This catalog is the acceptance checklist for future implementation phases.

## Data tests

Schema, type, finite values, OHLC geometry, duplicate keys, monotonic time, timezone, DST, session mapping, symbol synchronization, feed gaps, corporate/contract adjustments, and bid/ask validity.

## Anatomy tests

Determinism, identity stability, parent lineage, state transition legality, known-time correctness, reference freshness, invalidation, one-signal-per-event, and renderer independence.

## Candidate/outcome tests

Compatibility, bounded count, price rounding, long/short geometry, expiry, fill rules, gaps, ambiguous bars, MFE/MAE, partial management, costs, and label end time.

## Validation/model tests

Cluster separation, purge, embargo, train-only transforms, label shuffle collapse, FDR, bootstrap reproducibility, calibration, schema mismatch, missing-feature fallback, model hash, and deterministic prediction.

## Execution tests

Risk reservation, daily lock, correlated exposure, duplicate prevention, broker rejects, timeout, reconciliation, partial fill, restart, manual position, kill switch, and rollback.

