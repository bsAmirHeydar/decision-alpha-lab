# Phase 12.5 Pipeline Integrity Specification

## Problem

A long research pipeline can fail silently even when every individual module appears to run. Typical failures include:

- an upstream header changes while a downstream reader still expects the old name;
- the same `signal_id` is written twice;
- Phase 10 is regenerated but Phase 11 still contains predictions from an older dataset;
- New York timestamps become unparsable or reordered;
- Phase 11 reports more predictions than actually exist in its CSV;
- BUY rows carry HIGH-side anatomy or SELL rows carry LOW-side anatomy;
- test periods overlap training periods through a split bug.

Phase 12.5 treats these as research-invalidating defects, not cosmetic warnings.

## Audit domains

### File integrity

Every critical output is checked for existence, readability, header presence, row count, and truncation.

### Schema integrity

Required columns are versioned by logical file. Missing columns are critical because the next phase cannot infer their meaning safely.

### Identity integrity

Primary keys must be non-empty and unique:

- Phase 07: `outcome_id`
- Phase 10: `sample_id`
- Phase 11 predictions: `fold_id + sample_id`
- aggregate reports: dimension/bucket composite keys

### Lineage integrity

Exact relations:

- Phase 07 `outcome_id` ↔ Phase 10 `outcome_id`
- Phase 07 `signal_id` ↔ Phase 10 `signal_id`

Child-subset relations:

- Phase 11 prediction `sample_id` must exist in Phase 10;
- Phase 11 prediction `signal_id` must exist in Phase 10;
- every prediction `fold_id` must exist in the fold plan.

A subset relation permits Phase 10 rows that never enter an OOS test fold, but it never permits an orphan prediction.

### Semantic integrity

- BUY must be LOW-side.
- SELL must be HIGH-side.
- hunter and clean symbols must differ.
- completed outcomes must have positive stop distance.
- model-ready rows must have positive stop distance.
- label class and binary win label must agree.
- prediction win/loss flags must agree with actual R sign.

### Temporal integrity

For each fold:

`train_start ≤ train_end ≤ embargo_start ≤ embargo_end ≤ test_start ≤ test_end`

Any violation blocks model comparison because it can produce leakage.

### Metric reconciliation

Writer summary values are compared to physical row counts. A mismatch indicates partial writes, stale files, interrupted runs, or mixed run generations.

## Readiness policy

Critical failures block Phase 13. Errors produce warnings unless promoted by project governance. Optional evidence shortages remain warnings but are visible.
