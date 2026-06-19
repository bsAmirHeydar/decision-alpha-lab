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


## Six-slot stateful H0005 order behavior

The executor maintains a reversal-grid, not a single path order:

```text
InpMaxSimultaneousTrades = -1
InpAllowOppositeTrades = true
InpBuyLimitSlots = 3
InpSellLimitSlots = 3
InpRefreshSetupsOnNewBarOnly = true
InpManageOrdersEveryTick = true
InpSyncManagedPendings = true
InpCancelStaleManagedPendings = true
InpCancelManagedPendingsAfterEntry = false
InpUpdateExistingManagedPendings = true
InpProtectPendingWhenPriceApproaches = true
InpPendingProtectDistancePoints = 20
InpPendingProtectStopFraction = 0.50
InpAllowMarketCatchWhenAlreadyTouching = false
InpTouchRevisitResetBufferPoints = 10
InpOrderCommentPrefix = DALR1
```

Execution semantics:

```text
1. In reversal regime, keep up to 3 buy limits and 3 sell limits prepared.
2. Update existing candidate pendings while the zone state changes, but do not
   delete/replace a near-fill order just because it is close to entry.
3. One touch can produce only one fill for the same setup comment.
4. After a fill, the setup is locked until price moves away from the touch edge;
   only then can a new pending be armed for a true revisit.
5. In continuation regime, delete all managed pendings for this EA prefix until
   reversal regime returns.
```

The compact `DALR1` prefix is intentional because many trade servers truncate
comments; short comments keep duplicate detection, pending sync, and touch-lock
memory reliable.

## Build 1.10 live contract

The live executor is now locked to the H0005 reversal R1 six-slot touch ledger:

- three buy-limit slots and three sell-limit slots in reversal regime;
- stable per-zone comments: `prefix + reward + side + N + node_id`;
- one fill per touch;
- re-arm only after price leaves the touch edge and revisits;
- delete all managed pending limits when the latest regime is continuation/non-reversal.

See `docs/execution/H0005_R1_SIX_SLOT_TOUCH_LEDGER.md`.

