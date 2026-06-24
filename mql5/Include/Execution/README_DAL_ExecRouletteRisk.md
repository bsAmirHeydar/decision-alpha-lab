# DAL_ExecRouletteRisk — Reusable Roulette Risk Module

## Status

Draft / execution-risk module.

This README defines the intended behavior of the reusable `DAL_ExecRouletteRisk.mqh` module.

The module is designed to be used by multiple execution experts, including `E0004_ContinuationHeikinAshiFlip`, without duplicating risk logic inside each executor.

---

## Purpose

`Roulette Risk` is a locked-balance, profit-sensitive risk model.

It does not increase risk after losses.

It increases allowed risk only when the account has realized balance growth above the current locked cycle balance.

The module returns **money risk**. It does not send orders, select entries, select exits, or decide whether a trade should be taken.

---

## Core Concept

At the beginning of a cycle, the module locks the current account balance.

From this locked balance, it calculates a base risk using an input percentage.

Example:

```text
locked_balance = 10,000
initial_risk_percent = 10%
base_risk = 1,000
floor_balance = 9,000
```

The `floor_balance` is the protected reference floor of the active cycle.

When balance grows, the model calculates the distance between the current balance and the floor:

```text
riskable_pool = current_balance - floor_balance
```

Only a configurable fraction of that pool is used for the next risk:

```text
profit_based_risk = riskable_pool * save_profit_factor
```

The default interpretation keeps risk at least equal to the base risk during an active cycle:

```text
next_risk = max(base_risk, profit_based_risk)
```

---

## Default Inputs

Recommended defaults:

```text
initial_risk_percent = 10.0
save_profit_factor   = 0.50
persist_state        = true
reset_on_balance_drop = true
```

### initial_risk_percent

The percentage of the locked balance used to define the cycle's base risk.

Formula:

```text
base_risk = locked_balance * initial_risk_percent / 100
```

Default is `10.0`.

This is aggressive and should be treated as an experimental default, not a conservative production default.

---

### save_profit_factor

The fraction of the riskable pool that may be used as the next risk once the account is in realized profit.

Formula:

```text
profit_based_risk = (current_balance - floor_balance) * save_profit_factor
```

Default is `0.50`.

A lower value protects more profit.

A higher value compounds risk more aggressively.

---

### persist_state

If enabled, the module persists its cycle state using terminal-level storage, such as MQL5 global variables.

The persisted state should include:

```text
locked_balance
base_risk
floor_balance
last_balance
cycle_id
initialized
```

This allows the risk model to survive EA restart, chart reload, or terminal restart.

---

### reset_on_balance_drop

If enabled, a realized balance drop resets the cycle.

The new cycle locks the balance after the loss.

This is the rule that prevents the model from continuing to use profit-expanded risk after a loss.

---

## State Variables

The module should maintain the following internal state.

### locked_balance

The balance frozen at the start of the active cycle.

It should remain unchanged while the cycle is active and profitable.

It resets only after a realized loss, manual reset, or explicit state reset.

---

### base_risk

The base risk for the active cycle.

```text
base_risk = locked_balance * initial_risk_percent / 100
```

When the model is not in a profitable cycle, this is the next trade risk.

---

### floor_balance

The protected reference floor for the cycle.

```text
floor_balance = locked_balance - base_risk
```

The distance from `current_balance` to `floor_balance` defines the pool from which the next risk can be calculated.

---

### last_balance

The last known realized account balance.

This is used to detect whether the account has suffered a realized balance drop.

---

### cycle_id

A counter that increments every time the Roulette cycle resets.

It is useful for logging, debugging, and later execution audits.

---

## Risk Formula

At any decision point:

```text
current_balance = AccountInfoDouble(ACCOUNT_BALANCE)
riskable_pool = current_balance - floor_balance
profit_based_risk = riskable_pool * save_profit_factor
next_risk = max(base_risk, profit_based_risk)
```

Safety normalization must be applied:

```text
next_risk >= 0
next_risk is finite
next_risk is not NaN
```

If values are invalid, the module should return `0.0` or fail safely.

---

## Cycle Behavior

## 1. First Initialization

At first run:

```text
locked_balance = current_balance
base_risk = locked_balance * initial_risk_percent / 100
floor_balance = locked_balance - base_risk
last_balance = current_balance
cycle_id = 1
```

The first risk is:

```text
next_risk = base_risk
```

---

## 2. No Realized Profit Yet

If the current balance has not moved meaningfully above the locked balance:

```text
next_risk = base_risk
```

The model does not increase risk.

---

## 3. Profitable Cycle

If current balance is above the locked balance:

```text
riskable_pool = current_balance - floor_balance
profit_based_risk = riskable_pool * save_profit_factor
next_risk = max(base_risk, profit_based_risk)
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
profit_based_risk = 3,000 * 0.50 = 1,500
next_risk = 1,500
```

---

## 4. Loss After Profit

If a loss happens after a profitable run, the cycle resets.

Example:

```text
previous_balance = 12,000
after_loss_balance = 10,500
```

New cycle:

```text
locked_balance = 10,500
base_risk = 10,500 * 10% = 1,050
floor_balance = 10,500 - 1,050 = 9,450
next_risk = 1,050
```

The system does not continue using the previous higher profit-based risk.

---

## 5. Consecutive Losses

Each realized balance drop resets the cycle at the new balance.

Important rule:

```text
loss does not increase risk
```

This makes Roulette different from Martingale.

---

## Difference From Martingale

Martingale increases risk after losses.

Roulette increases risk only after realized profit.

```text
Martingale:
loss -> bigger next risk

Roulette:
profit -> bigger possible next risk
loss -> reset cycle
```

---

## Difference From Fixed Fractional Risk

Fixed fractional risk recalculates every trade directly from current balance:

```text
risk = current_balance * risk_percent
```

Roulette locks a cycle balance and defines a floor:

```text
risk = max(base_risk, (current_balance - floor_balance) * save_profit_factor)
```

This makes the model more path-dependent.

---

## Example Walkthrough

Settings:

```text
initial_risk_percent = 10%
save_profit_factor = 0.50
starting_balance = 10,000
```

Initialization:

```text
locked_balance = 10,000
base_risk = 1,000
floor_balance = 9,000
next_risk = 1,000
```

After first win:

```text
current_balance = 11,000
riskable_pool = 11,000 - 9,000 = 2,000
profit_based_risk = 2,000 * 0.50 = 1,000
next_risk = 1,000
```

After second win:

```text
current_balance = 12,000
riskable_pool = 12,000 - 9,000 = 3,000
profit_based_risk = 3,000 * 0.50 = 1,500
next_risk = 1,500
```

After third win:

```text
current_balance = 14,000
riskable_pool = 14,000 - 9,000 = 5,000
profit_based_risk = 5,000 * 0.50 = 2,500
next_risk = 2,500
```

After loss:

```text
current_balance = 11,500
```

Reset:

```text
locked_balance = 11,500
base_risk = 1,150
floor_balance = 10,350
next_risk = 1,150
```

---

## Module API Contract

The module should expose reusable functions similar to:

```text
DAL_RouletteRisk_Init()
DAL_RouletteRisk_Reset()
DAL_RouletteRisk_Update()
DAL_RouletteRisk_GetRiskMoney()
DAL_RouletteRisk_GetLotByStop()
DAL_RouletteRisk_SaveState()
DAL_RouletteRisk_LoadState()
DAL_RouletteRisk_DebugPrint()
```

Execution EAs must not duplicate Roulette formulas internally.

They should call the shared module.

---

## Integration Contract For Execution Modules

An execution expert should use Roulette in this order:

1. Initialize Roulette on `OnInit`.
2. Load persisted state if enabled.
3. On every new trade decision, update the module using current account balance.
4. Request money risk from the module.
5. Convert money risk into lot size using stop distance.
6. Apply broker volume limits.
7. Save state on `OnDeinit`.

---

## Lot Calculation

Roulette returns money risk, not lots.

The execution system must convert money risk into lot size.

Generic formula:

```text
lot = risk_money / stop_loss_money_per_lot
```

The final lot must respect:

```text
SYMBOL_VOLUME_MIN
SYMBOL_VOLUME_MAX
SYMBOL_VOLUME_STEP
```

If stop distance is invalid or zero, the execution module must not place a trade.

---

## Safety Rules

The module must:

- never return negative risk,
- never return NaN or infinite values,
- never increase risk after a realized loss,
- support manual reset,
- support persistent state,
- be reusable by different execution experts,
- never send orders directly,
- never decide entries,
- never decide exits.

---

## Important Warning

The default `10%` initial risk is aggressive.

It is useful for experimental stress-testing and convex execution research.

It should not be treated as a conservative production default.

---

## Summary

Roulette Risk works in cycles.

Each cycle locks a balance:

```text
locked_balance
base_risk
floor_balance
```

If there is no realized profit:

```text
risk = base_risk
```

If the cycle is profitable:

```text
risk = max(base_risk, (current_balance - floor_balance) * save_profit_factor)
```

After a realized loss:

```text
reset cycle using current balance
```

The model lets risk expand with realized profit and resets after loss.
