# Decision Alpha Lab execution layer

The `Execution` layer is separate from research hypotheses.

Research modules answer: **is there a structural fact?**  
Execution modules answer: **how would an order be placed and sized if that fact is used operationally?**

## Current module

- `E0001_ReversalOneToOne.mq5`

## Shared modules

- `DAL_ExecRisk.mqh` — cash-risk sizing with commission included.
- `DAL_ExecOrders.mqh` — exposure counting, opposite-trade guard, managed pending-limit lookup, stable pending protection, safe replacement, and limit-order placement.
- `DAL_ExecReversalOneToOne.mqh` — converts the H0005 reversal concept into a pending limit setup.

## E0001 rule — H0005 reversal fixed R1 execution

This module mirrors the H0005 reversal fixed-reward test as closely as a live
pending-limit executor can:

```text
Regime source: LAST_ONLY
Research model: reversal_fixed_reward_raw_costs_excluded, rewardR=1.0 by default
Live trigger: after the latest completed branch is reversal
Candidate set: every currently active structural node zone that can become the next M0001 touch event
Trade side:
  LOW structural node  -> buy reversal
  HIGH structural node -> sell reversal
Entry:
  limit order at the near edge of the structural zone
Stop:
  far edge of the same zone
Take profit:
  fixed R multiple from entry to stop distance; default = 1R
Order type:
  pending limit order
```

The H0005 report measures entry at the touch-bar close because it is a completed
research path. Live execution cannot know that close in advance, so E0001 parks
the limit at the same structural touch edge. The structural condition, stop, and
fixed reward model are kept aligned with the H0005 R1 test.

## Sizing

The user provides cash risk. Commission is estimated per 1.00 lot round-turn and included inside the risk budget.

```text
risk_per_lot = stop_loss_cash_per_lot + commission_per_lot_round_turn
volume = risk_cash / risk_per_lot
```

Volume is floored to the symbol volume step to avoid exceeding the requested risk.

## Runtime profile

`E0001` is designed as a lightweight execution module, not a research reporter.

Default runtime choices:

```text
InpBars = 1500
InpRefreshSetupsOnNewBarOnly = true
InpManageOrdersEveryTick = true
InpMaxZoneScanNodes = 0
InpUpdateChartComment = false
InpLogMode = DAL_EXEC_LOG_ERRORS
```

The EA only evaluates on a new candle by default, does not print every rejected/no-setup decision, and uses a fast reverse lookup for the latest branch sample instead of building full branch-report arrays, then builds all active H0005 reversal R candidates instead of chasing a single newest zone. Set `InpLogMode=DAL_EXEC_LOG_VERBOSE` only when debugging.

`InpTradingEnabled=false` by default for safety. Enable it only after dry-run/Strategy Tester validation.


## Pending behavior

E0001 v1.08 is a six-slot reversal grid with a per-touch ledger:

```text
1. While the latest completed branch regime is REVERSAL, the EA keeps up to
   3 buy-limit candidates and 3 sell-limit candidates alive.
2. Buy candidates come from LOW structural-node zones; sell candidates come
   from HIGH structural-node zones.
3. Candidate orders are updated while the H5 state evolves. Existing pendings
   are modified when only price/SL/TP changes; if the calculated volume changes,
   the pending is replaced only when it is not protected near market.
4. A setup can produce only one filled limit trade per touch. After a fill, the
   setup comment is locked and no new pending is armed for that same touch.
5. The lock is released only after price moves away from the touch edge by
   `InpTouchRevisitResetBufferPoints`, so the next order belongs to a true revisit.
6. When the latest branch regime is CONTINUATION or there is no current reversal
   setup, all managed pendings for this EA prefix are deleted. Protection near
   market does not block continuation-regime cleanup.
```

Relevant defaults:

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

The update engine only manages orders that match the EA symbol, magic number,
and compact `InpOrderCommentPrefix`. It never deletes unrelated manual or
external orders. The compact comment prefix is important because broker servers
may truncate order comments; E0001 keeps comments short so duplicate detection,
pending sync, and touch locking remain stable.

## Current locked executor

- `E0001_ReversalOneToOne.mq5` build `1.10` implements H0005 reversal R1 as a six-slot touch-ledger executor.
- Detailed contract: [`H0005_R1_SIX_SLOT_TOUCH_LEDGER.md`](H0005_R1_SIX_SLOT_TOUCH_LEDGER.md).

## Repository layout invariant

Execution source-of-truth lives only in the repository root paths:

```text
mql5/Experts/DecisionAlphaLab/Execution/
mql5/Include/DecisionAlphaLab/Execution/
docs/execution/
lab/04_execution/
```

A nested `decision-alpha-lab/decision-alpha-lab/` copy is not part of the canonical project and must be removed after backing it up. See [`../PROJECT_LAYOUT.md`](../PROJECT_LAYOUT.md).

