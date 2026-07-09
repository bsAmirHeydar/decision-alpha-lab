# Phase 06 Hotfix002 — Validation Plan

## Compile validation

Compile:

```text
EXP0017_CG_Visual_Ledger_Anatomy.mq5
```

Expected result:

```text
0 errors
0 critical warnings
```

## Visual validation checklist

1. Confirm that a valid confirmed divergence creates an origin-to-destination line.
2. Confirm that the origin marker appears at the configured origin.
3. Confirm that the destination marker appears at the configured destination.
4. Confirm that the label appears near the destination.
5. Confirm that hunter reference guide is horizontal at hunter reference price.
6. Confirm that clean stop guide appears only if enabled.
7. Confirm that clean comparison line does not appear unless enabled.
8. Confirm that clean comparison line respects `InpDrawCleanComparisonOnlyWhenChartIsCleanSymbol`.
9. Confirm that object names start with `EXP0017_P06_`.
10. Confirm that clearing Phase 06 objects does not delete user drawings.

## Functional validation

### Default hunter-side mode

Expected default:

```text
Sell: hunter reference high -> hunter current-cycle high
Buy: hunter reference low -> hunter current-cycle low
```

### Alternative anchor mode

Change destination time to confirmation close:

```text
InpDivergenceDestinationTimeMode = CGV_ANCHOR_TIME_CONFIRMATION_CLOSE
```

Expected:

```text
Destination marker moves to confirmation candle close boundary.
```

### Boundary fallback

If exact M1 lookup fails:

```text
The drawing must fall back to reference cycle end or confirmation close, not crash.
```

## Non-goals

This validation does not check trade entry, stop, target, win rate, R, pip result or AI ranking.
