# DAL_ExecRouletteRisk — Roulette Money Risk Module

This module is pure MQL5 and returns **money risk only**. It does not send orders, decide entries, or manage exits.

## Correct cycle logic

At the start of a cycle:

```text
locked_balance = AccountInfoDouble(ACCOUNT_BALANCE)
base_risk = locked_balance * initial_risk_percent / 100
floor_balance = locked_balance - base_risk
profit_active = false
```

Example:

```text
locked_balance = 10000
initial_risk_percent = 10
base_risk = 1000
floor_balance = 9000
```

## No-shrink rule

If the balance drops below `locked_balance`, or even below `floor_balance`, **risk does not shrink**.

The next risk remains:

```text
next_risk = base_risk
```

So if the account goes from `10000` to `8700`, the risk is still `1000` until a new profit-active reset happens.

This is intentional.

## Profit-active state

The cycle becomes profit-active only after:

```text
current_balance > locked_balance
```

While profit-active and still above locked balance:

```text
riskable_pool = current_balance - floor_balance
raw_risk = riskable_pool * save_profit_factor
next_risk = max(base_risk, raw_risk)
```

Example:

```text
locked_balance = 10000
base_risk = 1000
floor_balance = 9000
save_profit_factor = 0.50
current_balance = 12000
riskable_pool = 12000 - 9000 = 3000
next_risk = 3000 * 0.50 = 1500
```

## Reset rule

The cycle resets only when:

```text
profit_active == true
and current_balance < last_balance
```

That means: first the account must enter profit relative to the locked balance, then a realized loss/drop must occur.

After reset:

```text
locked_balance = balance_after_loss
base_risk = locked_balance * initial_risk_percent / 100
floor_balance = locked_balance - base_risk
profit_active = false
```

Then consecutive losses do **not** keep shrinking the risk. The new `base_risk` stays fixed until the account enters profit again.

## What this is not

This is not Martingale.

```text
Martingale: loss -> increase risk
Roulette: profit -> allow higher risk; loss after profit -> reset cycle
```

It is also not normal fixed fractional sizing because losing below the floor does not reduce risk during the active losing-side movement.
