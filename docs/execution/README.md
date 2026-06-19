# Decision Alpha Lab — Execution Modules

This folder documents live execution adapters for the research hypotheses.

## Canonical project layout

The canonical source tree is the repository root:

```text
mql5/Experts/DecisionAlphaLab/Execution/
mql5/Include/DecisionAlphaLab/Execution/
docs/execution/
lab/04_execution/
```

There must not be another nested `decision-alpha-lab/` copy inside the repository root.

## E0001 — H0005 Reversal Fixed-R Touch Executor

Current execution build:

```text
E0001_ReversalOneToOne.mq5 build 1.13
```

The EA executes the Hypothesis 5 reversal leg only:

```text
latest regime = REVERSAL
entry         = pending limit at structural zone touch edge
stop          = far side of the same zone
reward        = InpRewardR, default 1.0
```

### Build 1.13 live contract

Build 1.13 replaces the earlier fixed 3+3 slot idea with a hypothesis-pure model:

```text
InpBuyLimitSlots  = 0  => all active buy-touch limits
InpSellLimitSlots = 0  => all active sell-touch limits
positive value    => optional safety cap
```

This prevents valid H0005 touches/revisits from being skipped merely because a small fixed grid was already full.

### Spread policy

Buy from LOW node:

```text
entry = zone_upper + spread
SL    = zone_lower
TP    = entry + (entry - SL) * InpRewardR
```

Sell from HIGH node:

```text
entry = zone_lower
SL    = zone_upper + spread
TP    = entry - (SL - entry) * InpRewardR
```

The TP is always computed from the spread-aware executable risk distance.

### Pending deletion policy

When regime is continuation/non-reversal:

```text
delete all managed pending orders
keep open positions untouched
```

### Diagnostic policy

Use:

```text
InpLogMode = DAL_EXEC_LOG_ORDERS
```

or for full debugging:

```text
InpLogMode = DAL_EXEC_LOG_VERBOSE
```

The journal reports cache reasons, order-send retcodes, raw zone edges, spread-adjusted entry/stop/TP, touch locks, revisit unlocks, and stale-order deletions.

See `H0005_R1_SIX_SLOT_TOUCH_LEDGER.md` for the full build 1.13 execution contract.
