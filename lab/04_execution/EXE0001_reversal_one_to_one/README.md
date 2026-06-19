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


## Stateful H0005 candidate order behavior

The executor is not allowed to chase the market by deleting an order that is about to fill. It keeps the current H0005 reversal R1 setup cache and manages order state every tick.

Default behavior:

```text
InpRefreshSetupsOnNewBarOnly = true
InpManageOrdersEveryTick = true
InpSyncManagedPendings = true
InpCancelStaleManagedPendings = true
InpCancelManagedPendingsAfterEntry = true
InpProtectPendingWhenPriceApproaches = true
InpPendingProtectDistancePoints = 20
InpPendingProtectStopFraction = 0.50
InpAllowMarketCatchWhenAlreadyTouching = true
InpOrderCommentPrefix = DALR1
```

Execution semantics:

```text
1. If price is away from the H5 zone, park a limit at the touch edge.
2. If price is already touching/inside the zone before the limit can be valid, optionally catch with a market order.
3. Existing desired pending orders are kept by compact setup comment.
4. Stale managed pendings are deleted only when they are no longer in the current H5 state and are not protected near market.
5. Manual or external orders are ignored unless they share symbol, magic, and comment prefix.
```

The compact `DALR1` prefix is intentional because many trade servers truncate comments; short comments keep duplicate detection and pending sync reliable. If `InpMaxSimultaneousTrades` is greater than one, multiple active candidate zones can be represented by separate pending or market-catch orders until one managed entry fills; then unused managed candidate pendings are cancelled by default because the H0005 path has one actual next-touch entry.
