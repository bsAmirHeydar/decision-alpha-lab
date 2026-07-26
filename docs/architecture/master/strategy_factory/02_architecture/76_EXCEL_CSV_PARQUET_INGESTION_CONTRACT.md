---
type: strategy-factory-document
status: canonical
title: "Excel, CSV, and Parquet Ingestion Contract"
tags:
  - strategy-factory
---

# Excel, CSV, and Parquet Ingestion Contract

The fastest path from chart-exported data or a spreadsheet shared in chat to official research is a strict ingestion and audit layer.

## Accepted inputs

Bar tables, event tables, feature tables, candidate tables, and manual-review labels may arrive as Excel, CSV, or Parquet. Excel is an exchange format, not the authoritative research store. Ingestion converts it to canonical typed tables, UTC timestamps, stable identities, and Parquet/CSV artifacts.

## Required bar fields

UTC and exchange timestamps, symbol, timeframe, open/high/low/close, bid/ask or spread when available, volume, feed/vendor, session, and bar completeness. For cross-market work, record synchronization tolerance and missing-bar policy.

## Event and manual-label fields

Every event needs strategy/version, symbol universe, direction, event/known/confirmation times, reference and invalidation, cluster ID, and source identity. Manual labels require labeler, label time, evidence available at label time, confidence, and disagreement status. A human label created after the path is known cannot become a live feature.

## Ingestion QA

Schema and type validation, timezone/DST normalization, duplicates, OHLC geometry, finite values, missingness, cross-symbol alignment, row lineage, and source hashes. Invalid rows are quarantined with reason codes rather than silently dropped.

