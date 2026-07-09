# Phase 10 — Ranking Enrichment Contract

Phase 10 may enrich each signal row with Phase 09 ranking context:

- CG quality score;
- CG-direction quality score;
- role quality score;
- CG-direction-role quality score;
- shortlist match.

This enrichment is historical research metadata. It must not be interpreted as live permission to trade.

## Key construction

- CG: `cg_30m`
- CG direction: `cg_30m|BUY`
- role: `NDXUSD_hunter__SPXUSD_clean`
- CG direction role: `cg_30m|BUY|NDXUSD_hunter__SPXUSD_clean`

## Purpose

Ranking enrichment lets later analysis compare row-level outcomes against bucket-level historical quality.
