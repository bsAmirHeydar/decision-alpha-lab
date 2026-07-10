# Phase 11 — Limits and Non-Goals

## Limits

Phase 11 is intentionally simple. It does not train gradient boosting, neural networks, random forests, logistic regression, or external Python models inside MQL5.

## Non-goals

```text
No execution
No live signal permission
No risk sizing
No target mutation
No stop mutation
No CG removal
No AI autonomy
No strategy mutation
```

## Why

The purpose is to create an honest out-of-sample evaluation surface before introducing model complexity.

## Correct interpretation

A bucket that looks good in Phase 09 may fail Phase 11. That does not mean the anatomy is wrong; it means all-history ranking was not enough. Phase 11 is the first discipline layer that asks whether the edge survives forward time.
