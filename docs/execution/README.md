# Decision Alpha Lab execution layer

The `Execution` layer is separate from research hypotheses.

Research modules answer: **is there a structural fact?**  
Execution modules answer: **how would an order be placed and sized if that fact is used operationally?**

## Current module

- `E0001_ReversalOneToOne.mq5`

## Shared modules

- `DAL_ExecRisk.mqh` — cash-risk sizing with commission included.
- `DAL_ExecOrders.mqh` — exposure counting, opposite-trade guard, duplicate setup guard, and limit-order placement.
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

## Safety defaults

`InpTradingEnabled=false` by default, so the module prints dry-run decisions until explicitly enabled.
