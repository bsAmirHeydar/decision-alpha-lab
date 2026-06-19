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
InpEvaluateOnNewBarOnly = true
InpMaxZoneScanNodes = 0
InpUpdateChartComment = false
InpLogMode = DAL_EXEC_LOG_ERRORS
```

The EA only evaluates on a new candle by default, does not print every rejected/no-setup decision, and uses a fast reverse lookup for the latest branch sample instead of building full branch-report arrays, then builds all active H0005 reversal R candidates instead of chasing a single newest zone. Set `InpLogMode=DAL_EXEC_LOG_VERBOSE` only when debugging.

`InpTradingEnabled=false` by default for safety. Enable it only after dry-run/Strategy Tester validation.


## Pending behavior

E0001 is stable-first and H0005-candidate based. It does not delete a valid limit order while price is approaching its entry, and it does not chase the newest/closest setup by default:

```text
1. Finds the latest completed LAST_ONLY branch.
2. If that branch is reversal, collects all active structural zones eligible to become the next M0001 touch.
3. Sorts candidates by distance to market.
4. Places missing pending limits until `InpMaxSimultaneousTrades` is reached.
5. Keeps existing pending orders by setup comment, so near-fill orders are not removed.
6. By default, does not cancel a pending order just because the next cycle temporarily has no setup.
```

Relevant inputs:

```text
InpUpdatePendingOrders = true
InpReplacePendingWithCloserSetup = false
InpCancelPendingWhenNoSetup = false
InpCancelExtraManagedPendings = false
InpPendingReplaceMinImprovePoints = 2
InpProtectPendingWhenPriceApproaches = true
InpPendingProtectDistancePoints = 20
InpPendingProtectStopFraction = 0.50
```

The update engine only manages pending orders that match the EA symbol, magic number, and `InpOrderCommentPrefix`. It never deletes unrelated manual or external orders. If `InpMaxSimultaneousTrades` is greater than one, old valid pending setups are kept and additional valid setups may be placed until the exposure cap is reached.
