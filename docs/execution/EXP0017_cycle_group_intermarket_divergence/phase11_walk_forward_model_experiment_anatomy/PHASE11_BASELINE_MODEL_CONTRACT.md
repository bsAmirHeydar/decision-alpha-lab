# Phase 11 — Baseline Model Contract

## What the baseline is

A bucket baseline is a training-window aggregation:

```text
bucket_key -> average R, win rate, stop rate, average MFE, average MAE
```

It is not a predictive model in the final AI sense. It is the first leakage-safe research model.

## Default bucket

```text
CG + direction + role
```

Example:

```text
cg_60m | SELL | NDXUSD_hunter__SPXUSD_clean
```

## Edge classes

```text
positive_research_edge
neutral_research_edge
weak_or_negative_research_edge
```

These are based only on training-window average R.

## Fallback

If a test sample's bucket does not have enough training rows, the system can use `ALL` global fallback if enabled.

## Boundary

The baseline output is not trade permission. It is a research comparison surface.
