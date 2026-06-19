# Decision Alpha Lab execution layer

The `Execution` layer is separate from research hypotheses.

Research modules answer: **is there a structural fact?**  
Execution modules answer: **how would an order be placed and sized if that fact is used operationally?**

## Current module

- `E0001_ReversalOneToOne.mq5`

## Shared modules

- `DAL_ExecRisk.mqh` — cash-risk sizing with commission included.
- `DAL_ExecOrders.mqh` — exposure counting, opposite-trade guard, managed pending-limit lookup, stale-pending deletion, closer-setup replacement, and limit-order placement.
- `DAL_ExecReversalOneToOne.mqh` — converts the H0005 reversal concept into a pending limit setup.

## E0001 rule

```text
Regime source: LAST_ONLY
Trade side:
  LOW structural node  -> buy reversal
  HIGH structural node -> sell reversal
Entry:
  near edge of the next untouched structural zone
Stop:
  far edge of the same zone
Take profit:
  fixed R multiple from entry to stop distance
Order type:
  pending limit order
```

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
InpMaxZoneScanNodes = 300
InpUpdateChartComment = false
InpLogMode = DAL_EXEC_LOG_ERRORS
```

The EA only evaluates on a new candle by default, does not print every rejected/no-setup decision, and uses a fast reverse lookup for the latest branch sample instead of building full branch-report arrays. Set `InpLogMode=DAL_EXEC_LOG_VERBOSE` only when debugging.

`InpTradingEnabled=false` by default for safety. Enable it only after dry-run/Strategy Tester validation.


## Pending update engine

E0001 does not leave an old unfilled limit order behind when a better reversal zone appears.
On each evaluation cycle it:

```text
1. Finds the managed pending limit for the same symbol/magic/comment prefix.
2. Builds the newest valid reversal setup.
3. Keeps the existing pending if it is the same setup/price.
4. Replaces it when the new setup is closer to the live market by at least InpPendingReplaceMinImprovePoints.
5. Optionally deletes the pending order when no valid reversal setup remains.
6. Optionally deletes extra managed pending orders and keeps only the nearest one.
```

Relevant inputs:

```text
InpUpdatePendingOrders = true
InpReplacePendingWithCloserSetup = true
InpCancelPendingWhenNoSetup = true
InpCancelExtraManagedPendings = true
InpPendingReplaceMinImprovePoints = 2
```

The update engine only manages pending orders that match the EA symbol, magic number, and `InpOrderCommentPrefix`. It never deletes unrelated manual or external orders.
