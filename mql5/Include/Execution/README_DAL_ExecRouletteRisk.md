# DAL_ExecRouletteRisk — Roulette Execution Risk Model

`DAL_ExecRouletteRisk` is a reusable MQL5 execution-risk module.

It only calculates **money risk**. It does not send orders, decide entries, or decide exits.

---

## Core rule

Roulette is a **locked-balance risk cycle**.

At the beginning of a cycle:

```text
locked_balance = current account balance
base_risk = locked_balance * initial_risk_percent
floor_balance = locked_balance - base_risk
```

With defaults:

```text
initial_risk_percent = 10%
save_profit_factor = 0.50
```

Example:

```text
locked_balance = 10,000
base_risk = 1,000
floor_balance = 9,000
```

The key point:

> The base risk is a locked number. It does not shrink just because balance falls below the floor.

---

## Losing side rule

If the account goes below `locked_balance`, or even below `floor_balance`, the risk is **not reduced**.

It remains:

```text
risk = base_risk
```

Example:

```text
locked_balance = 10,000
base_risk = 1,000
floor_balance = 9,000
```

If balance becomes:

```text
current_balance = 8,700
```

The next risk is still:

```text
risk = 1,000
```

The model does not recalculate risk as 10% of 8,700.

This is intentional.

---

## Profit side rule

When the balance moves above `locked_balance`, the cycle becomes profit-active.

Then the risk can grow using the distance from the protected floor:

```text
riskable_pool = current_balance - floor_balance
profit_scaled_risk = riskable_pool * save_profit_factor
risk = max(base_risk, profit_scaled_risk)
```

Example:

```text
locked_balance = 10,000
base_risk = 1,000
floor_balance = 9,000
save_profit_factor = 0.50
current_balance = 12,000
```

Then:

```text
riskable_pool = 12,000 - 9,000 = 3,000
profit_scaled_risk = 3,000 * 0.50 = 1,500
risk = 1,500
```

---

## Profit then loss reset rule

A reset happens only after the cycle has been in profit and then a realized balance drop occurs.

Example:

```text
locked_balance = 10,000
base_risk = 1,000
floor_balance = 9,000
balance grows to 14,000
risk becomes 2,500 when save_profit_factor = 0.50
```

If a loss then makes balance:

```text
current_balance = 11,500
```

The cycle resets:

```text
locked_balance = 11,500
base_risk = 11,500 * 10% = 1,150
floor_balance = 10,350
risk = 1,150
```

After this reset, if more losses happen before a new profit-active cycle, the risk remains `1,150`.

It does not keep decreasing on every loss.

---

## What does not happen

Roulette does not reduce risk during a losing cycle.

Roulette does not increase risk after a loss.

Roulette does not reset on every balance drop from the initial locked state.

Roulette resets only when:

```text
cycle_had_profit == true
AND
current_balance < last_balance
```

---

## Difference from martingale

Martingale:

```text
loss -> increase risk
```

Roulette:

```text
loss before profit -> keep locked base risk
profit -> risk may grow
loss after profit -> reset balance lock and return to new base risk
```

---

## State variables

The module stores:

```text
initialized
persist_state
reset_on_balance_drop
cycle_had_profit
locked_balance
floor_balance
base_risk_cash
last_balance
current_balance
peak_balance
current_risk_cash
initial_risk_percent
save_profit_factor
```

`cycle_had_profit` is essential. Without it the model would incorrectly shrink/reset risk on ordinary losing-side drawdown.

---

## E0004 integration

`E0004_ContinuationHeikinAshiFlip` can select:

```text
E0004_RISK_FIXED_CASH
E0004_RISK_ROULETTE
```

Default:

```text
InpRiskModel = E0004_RISK_ROULETTE
InpRouletteInitialRiskPercent = 10.0
InpRouletteSaveProfitFactor = 0.50
InpRoulettePersistState = true
InpRouletteResetOnBalanceDrop = true
```

`InpRouletteResetOnBalanceDrop` means reset after a balance drop **only if the current cycle has already been in profit**.

It does not mean reset on every loss.

---

## Safety contract

The module must:

- return money risk only,
- never place orders,
- never decide entries or exits,
- never reduce risk below the locked base risk inside a losing-side cycle,
- reset only after profit then realized loss,
- persist state if enabled.
