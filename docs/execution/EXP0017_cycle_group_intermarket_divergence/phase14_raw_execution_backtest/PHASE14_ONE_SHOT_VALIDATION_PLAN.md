# Phase 14 — One-Shot Execution Validation Plan

## Acceptance objective

Prove that one divergence anatomy can produce at most one execution opportunity, regardless of how many lower-timeframe candles continue to report it.

## A. Static contract tests

### A1. Canonical identity fields

Verify the key contains:

- canonical pair;
- CG;
- trading day;
- current cycle;
- reference cycle;
- side.

### A2. Forbidden identity fields

Verify the key builder does not use:

- confirmation time;
- confirmation timeframe;
- entry, stop, target, or risk settings;
- selected trade leg.

### A3. Gate ordering

Verify source order:

```text
build key < consume entitlement < build plan < route order
```

### A4. Warmup isolation

Verify warmup consumes reconstructed entitlements but contains no router call.

### A5. Audit observability

Verify duplicate suppressions are written through the dedicated one-shot audit path.

## B. Strategy Tester scenarios

### B1. Persistent divergence across several lower candles

1. Use a case where one CG3 divergence remains confirmed across at least three confirmation candles.
2. Enable all normal execution conditions.
3. Count orders whose entitlement key is identical.

Expected:

```text
first observation: one plan/order opportunity
later observations: zero orders, one-shot suppression rows
```

### B2. First plan rejected by spread

1. Set `InpMaxSpreadPoints` below the first observation spread.
2. Allow spread to improve on a later candle while divergence persists.

Expected:

- first observation consumes entitlement and plan/router rejects;
- later candle does not trade;
- duplicate is suppressed.

### B3. First plan rejected by volume

1. Set a fixed risk smaller than broker minimum-lot stop risk.
2. Keep divergence active on later candles.

Expected: no later retry.

### B4. Broker or transport failure

Force a transport rejection in a controlled environment.

Expected: entitlement remains consumed.

### B5. Hedging enabled

Keep `InpEnableHedging=true` and allow open positions.

Expected: same entitlement cannot stack; a distinct divergence can still trade.

### B6. Position policy `EVERY_SIGNAL`

Expected: every distinct entitlement may trade once, not every candle observation.

### B7. Restart mid-day

1. Let a divergence trade or consume its entitlement.
2. Stop the test/EA after later candles exist.
3. Restart within the same New York trading day.

Expected:

- warmup reconstructs the entitlement;
- no duplicate order is produced after restart.

### B8. Start mid-day without processing existing bar

Set:

```text
InpProcessExistingClosedBarOnInit = false
```

Expected: all already observed entitlements are primed; none are entered historically.

### B9. Start mid-day with existing-bar processing

Set:

```text
InpProcessExistingClosedBarOnInit = true
```

Expected:

- earlier observations are primed;
- latest bar trades only when it contains the first observation of a new entitlement.

### B10. Symbol order reversal

Run equivalent tests with:

```text
A=SPXUSD, B=NDXUSD
A=NDXUSD, B=SPXUSD
```

Expected: canonical entitlement identity is equivalent.

### B11. Distinct side

A HIGH-side and LOW-side divergence with otherwise matching cycle anatomy must have different entitlements.

### B12. Distinct reference cycle

Two divergences in the same current cycle but from different reference cycles must remain distinct.

### B13. Distinct CG

CG3 and CG5 observations over the same market movement must remain distinct.

## C. Audit checks

Main execution CSV must contain `trade_entitlement_key`.

One-shot gate CSV must contain suppression rows with:

```text
SUPPRESSED_ALREADY_CONSUMED
one_shot_entitlement_already_consumed
```

No entitlement key may have more than one accepted execution row.

## D. Quantitative invariant query

For the generated audit dataset:

```text
GROUP BY trade_entitlement_key
COUNT(accepted execution) <= 1
```

Any key with count greater than one is a release-blocking defect.

## E. Release gate

- Contract tests pass.
- MetaEditor compiles with `0 errors, 0 warnings`.
- Persistent-divergence visual test produces one trade only.
- Restart scenario produces no duplicate.
- Main and gate audits reconcile.
- No changes are observed in Phase 06 signal anatomy.

## Related documents

- [[PHASE14_ONE_SHOT_SIGNAL_EXECUTION_CONTRACT]]
- [[PHASE14_ONE_SHOT_STATE_MACHINE]]
- [[PHASE14_VALIDATION_PLAN]]
