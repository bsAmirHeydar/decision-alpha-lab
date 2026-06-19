# EXE0001 — H0005 Reversal Fixed R1

Purpose: operationalize the exact H0005 reversal fixed-reward test as a simple pending-limit execution model. Default reward is `1R`, matching `DAL_M0005_FINAL_REVERSAL_TRADE_R1`.

## Inputs

- cash risk
- commission per 1 lot round-turn
- reward R multiple
- max simultaneous trades
- allow/disallow opposite-direction exposure

## Exact research alignment

```text
H0005 test line: DAL_M0005_FINAL_REVERSAL_TRADE_R1
Regime source: LAST_ONLY
Research trade model: reversal_fixed_reward_raw_costs_excluded
Default rewardR: 1.0
Stop model: zone edge
Same-bar report policy: STOP_FIRST in research reports
Live execution: real tick/order sequence from the broker/tester
```

The H0005 report measures the entry from the completed touch bar. Live execution cannot know that bar close before it forms, so this module uses a limit order at the same structural touch edge.

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

This module is a first execution template for the H0005 R1 reversal model. It does not include spread/slippage modeling beyond the explicit commission input. It should be run in dry-run mode first and then tested in Strategy Tester before live use.


## Fast execution profile

This module intentionally keeps the operational loop light:

```text
- no full research reports
- no per-decision logs by default
- no chart comment by default
- latest branch is resolved with a reverse fast scan
- candidate zones are collected from active H0005 reversal zones; InpMaxZoneScanNodes=0 scans all
```

For production-like testing, keep `InpLogMode=DAL_EXEC_LOG_ERRORS` or `DAL_EXEC_LOG_NONE`. Use `DAL_EXEC_LOG_VERBOSE` only for diagnostics.


## Stable H0005 candidate pending behavior

The executor is not allowed to chase the market by deleting an order that is about to fill. It places missing H0005 reversal R1 candidate orders and keeps existing managed pending orders by setup comment.

Default behavior:

```text
InpUpdatePendingOrders = true
InpReplacePendingWithCloserSetup = false
InpCancelPendingWhenNoSetup = false
InpProtectPendingWhenPriceApproaches = true
InpPendingProtectDistancePoints = 20
InpPendingProtectStopFraction = 0.50
```

This keeps the operational logic stable: place the limit where the strategy condition exists and let it fill. If `InpMaxSimultaneousTrades` is greater than one, multiple active candidate zones can be represented by separate pending limits.
