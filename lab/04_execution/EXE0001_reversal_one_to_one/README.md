# EXE0001 — Reversal One-to-One

Purpose: operationalize the H0005 reversal first-move edge with a simple fixed-R limit-order model.

## Inputs

- cash risk
- commission per 1 lot round-turn
- reward R multiple
- max simultaneous trades
- allow/disallow opposite-direction exposure

## Entry/exit

```text
BUY reversal:
  node type = LOW
  entry = upper edge of the structural zone
  stop  = lower edge of the structural zone
  tp    = entry + rewardR * (entry - stop)

SELL reversal:
  node type = HIGH
  entry = lower edge of the structural zone
  stop  = upper edge of the structural zone
  tp    = entry - rewardR * (stop - entry)
```

## Scope

This module is a first execution template. It does not include spread/slippage modeling beyond the explicit commission input. It should be run in dry-run mode first and then tested in Strategy Tester before live use.


## Fast execution profile

This module intentionally keeps the operational loop light:

```text
- no full research reports
- no per-decision logs by default
- no chart comment by default
- latest branch is resolved with a reverse fast scan
- untouched-zone search is capped by InpMaxZoneScanNodes
```

For production-like testing, keep `InpLogMode=DAL_EXEC_LOG_ERRORS` or `DAL_EXEC_LOG_NONE`. Use `DAL_EXEC_LOG_VERBOSE` only for diagnostics.


## Pending update behavior

The executor has an order-refresh layer. If a previous limit order is still pending and a newer untouched reversal zone becomes closer to market, the old pending order is deleted and a new one is placed at the better entry with fresh SL/TP/volume sizing.

Default behavior:

```text
InpUpdatePendingOrders = true
InpReplacePendingWithCloserSetup = true
InpCancelPendingWhenNoSetup = true
InpPendingReplaceMinImprovePoints = 2
```

This keeps the logic fast and operational: one managed pending order follows the current best reversal setup instead of accumulating stale limits.
