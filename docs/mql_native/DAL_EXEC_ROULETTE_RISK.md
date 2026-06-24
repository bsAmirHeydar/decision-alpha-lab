# DAL_ExecRouletteRisk — Roulette Execution Risk Model

`DAL_ExecRouletteRisk` is a reusable MQL5 execution-risk module.

It returns **money risk** only. It does not send orders, decide entries, or decide exits.

---

## Core state

Each cycle stores:

```text
locked_balance
base_risk
floor_balance
profit_active
last_balance
peak_balance
```

Default inputs:

```text
initial_risk_percent = 10%
save_profit_factor = 0.50
```

At cycle start:

```text
locked_balance = current_balance
base_risk = locked_balance * initial_risk_percent
floor_balance = locked_balance - base_risk
```

Example:

```text
locked_balance = 10,000
base_risk = 1,000
floor_balance = 9,000
```

---

## Losing-side floor band

If the account moves down but stays inside the protected band:

```text
floor_balance <= current_balance <= locked_balance
```

risk remains fixed:

```text
risk = base_risk
```

Example:

```text
locked_balance = 10,000
base_risk = 1,000
floor_balance = 9,000
current_balance = 9,300
risk = 1,000
```

The risk does not shrink on every small loss.

---

## Downside floor break

If balance breaks below the protected floor, the base account used for lot calculation must update downward.

Rule:

```text
if current_balance < floor_balance:
    locked_balance = current_balance
    base_risk = locked_balance * initial_risk_percent
    floor_balance = locked_balance - base_risk
    profit_active = false
    risk = base_risk
```

Example:

```text
locked_balance = 10,000
base_risk = 1,000
floor_balance = 9,000
current_balance = 8,700
```

The cycle re-locks:

```text
locked_balance = 8,700
base_risk = 870
floor_balance = 7,830
risk = 870
```

This is the corrected rule: the base does not follow every loss, but it does follow the account down after the protected floor is broken.

---

## Profit-active rule

The cycle becomes profit-active only after balance rises above the locked balance:

```text
current_balance > locked_balance
```

Then risk can grow from the distance above the floor:

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
current_balance = 12,000
save_profit_factor = 0.50
```

Then:

```text
riskable_pool = 12,000 - 9,000 = 3,000
risk = max(1,000, 3,000 * 0.50) = 1,500
```

---

## Profit then loss re-lock

If the cycle was profit-active and then a realized balance drop occurs, the cycle re-locks to the post-loss balance.

Rule:

```text
if profit_active == true and current_balance < last_balance:
    locked_balance = current_balance
    base_risk = current_balance * initial_risk_percent
    floor_balance = locked_balance - base_risk
    profit_active = false
    risk = base_risk
```

Example:

```text
locked_balance = 10,000
balance grows to 14,000
risk grows while profit-active
then balance drops to 11,500
```

The cycle re-locks:

```text
locked_balance = 11,500
base_risk = 1,150
floor_balance = 10,350
risk = 1,150
```

---

## Final behavior summary

```text
Loss inside floor band      -> keep base_risk
Loss below floor            -> re-lock downward at current balance
Profit above locked balance -> profit_active = true and risk may grow
Loss after profit           -> re-lock at post-loss balance
```

This is not martingale. Losses do not increase risk.

This is also not ordinary fixed fractional. Risk is locked inside the floor band and only re-locks at structural balance events.

---

## Safety contract

The module must:

- return money risk only;
- never place orders;
- never decide entries or exits;
- keep base risk fixed inside the floor band;
- re-lock downward only after the floor is broken;
- re-lock after profit then realized loss;
- persist state if enabled.
