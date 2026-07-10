# Phase 06 Hotfix011 — NDX Raw-Path Freshness Authority

## Problem statement

Hotfix010 made M1 coverage strict for both symbols, but the remaining Nasdaq defect showed that coverage parity alone was not sufficient.

The system still had two different evidence routes:

1. confirmation compressed freshness from the ordered list of completed cycle extrema;
2. drawing queried M1 again on the destination chart to recover visual anchor times.

That architecture allowed the non-host chart to depend on a second data query and on slot-specific state propagation. SPX could look correct while NDX retained a line whose local reference had not been proven by the same evidence used for SPX.

## Authoritative rule

For every candidate reference and every symbol independently:

```text
freshness interval = [reference_cycle_end, current_cycle_start)
```

The reference high is fresh only when no M1 bar in that interval touches or exceeds the reference high.

The reference low is fresh only when no M1 bar in that interval touches or falls below the reference low.

Equality consumes the level. Tick-size tolerance is applied only to neutralize floating-point representation noise; it does not create a price-distance filter.

Strict pair mode remains:

```text
SPX local reference fresh
AND
NDX local reference fresh
```

If either local path is missing, incomplete, stale, or cannot be mapped to the exact cycle boundary, the pair is suppressed and neither chart is authorized to draw.

## Implementation

### 1. One raw M1 path per symbol and group observation

`CCGC_ConfirmationField` now loads the complete intervening M1 path once for SPX and once for NDX.

It builds suffix maximum-high and minimum-low arrays. Every candidate reference is then checked against the exact later path without repeated `CopyRates` calls per reference.

This changes the complexity of the new proof from an unsafe quadratic path scan to:

```text
O(M1 bars + reference count) per symbol/group/observation
```

### 2. Slot-neutral local proof

Both symbols execute the same function:

```text
BuildLocalFreshnessProofsForSymbol(...)
```

The only difference is which symbol-local reference fields are supplied. There is no host-chart shortcut and no separate Nasdaq branch.

### 3. Exact local anchor persistence

Reference and current-cycle high/low timestamps are captured when M1 ranges are aggregated and stored inside `SCGCFinalSignal`.

The drawing layer no longer needs to rediscover NDX extrema with a second foreign-chart history query. It renders from the exact timestamp and price already approved by confirmation.

### 4. Authoritative foreign-chart cleanup

Cleanup now begins with prefix-based `ObjectsDeleteAll()` on each target chart, followed by verified fallback passes. This prevents orphaned NDX objects from surviving a rebuild.

## Unchanged doctrine

Hotfix011 does not change:

- cycle definitions;
- one-sided hunt rules;
- equality-as-touch doctrine;
- protected-reference retirement;
- repeated divergence while the protected symbol survives;
- signal direction;
- order, risk, target, or execution behavior.

It only makes local reference freshness and visual evidence deterministic and symmetric.
