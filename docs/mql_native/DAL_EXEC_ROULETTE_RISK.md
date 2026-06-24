# DAL_EXEC_ROULETTE_RISK

Canonical MQL5 documentation for the reusable Roulette risk module.

## Definition

Roulette is a locked-balance, profit-sensitive money-risk model.

It has one important asymmetry:

- losses before profit do not shrink the risk;
- profits can expand the risk;
- a loss after profit resets the cycle to the new balance.

## Formula

At cycle start:

```text
locked_balance = current balance
base_risk = locked_balance * initial_risk_percent
floor_balance = locked_balance - base_risk
```

Before profit:

```text
risk = base_risk
```

Even if balance falls below the protected floor:

```text
risk = base_risk
```

After balance rises above locked balance:

```text
riskable_pool = current_balance - floor_balance
risk = max(base_risk, riskable_pool * save_profit_factor)
```

After profit then realized balance drop:

```text
locked_balance = balance after drop
base_risk = locked_balance * initial_risk_percent
floor_balance = locked_balance - base_risk
risk = base_risk
```

## Implementation contract

The module must:

- persist state optionally;
- return money risk only;
- never send orders;
- never decide entries;
- never reduce risk merely because balance went below the protected floor;
- reset only after a profit-active balance drop.
