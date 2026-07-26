# Phase 31 — Runtime Cleanup and Responsive Label Cache Optimization

## Goal

Reduce unnecessary runtime work without changing Hook behavior, visual semantics, default outputs, or no-trade boundaries.

This phase does not remove features and does not alter Hook lifecycle rules. It only avoids repeated work that produced the same result.

## What was optimized

### 1) Responsive label distance caching

Phase 30 made label spacing responsive by reading local candle ranges around every label anchor. When many labels share nearby bars, repeatedly calling `iBarShift`, `iHigh`, and `iLow` for the same anchors is unnecessary.

Phase 31 adds per-render caches for:

- `datetime -> bar shift`
- `(bar shift, lookback) -> average local range points`

The cache is reset at the start of each Hook draw pass, so it cannot go stale across timeframe changes or redraws.

### 2) Batch cleanup by prefixes

Previous lifecycle cleanup scanned all chart objects once per prefix. With many Hook prefixes this could scan the chart 10+ times.

Phase 31 adds a single-pass prefix cleanup function:

```text
FP_HookP07DeleteObjectsByPrefixes
```

This scans chart objects once and tests all relevant prefixes inside that scan.

## Behavior guarantee

- Same Hook nodes
- Same Hook arcs
- Same labels
- Same cleanup scope
- Same no-trade behavior

Only duplicated runtime work is reduced.
