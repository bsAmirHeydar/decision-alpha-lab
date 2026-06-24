# EXP0012 — Distributional Cluster Miner

## Purpose

EXP0012 implements the research tool required by H0008: a reusable MQL5 module that can be attached to any execution strategy to measure whether trade outcomes form exploitable clusters.

This experiment is not an execution strategy. It does not send orders. It is a measurement and filtering layer.

## Core idea

Every execution strategy emits completed trade outcomes. EXP0012 groups those outcomes by a causal `feature_key` and measures whether any key improves:

```text
P(W)
P(W after W)
P(W after WW)
P(W after WWW)
max streak
cluster count
lift over baseline
```

The goal is to find filters that make Roulette / Jackpot execution statistically more defensible.

## Integration contract

Any execution can use the module by including:

```mql5
#include <Research/DAL_DistributionClusterMiner.mqh>
```

Then create a miner:

```mql5
DAL_DEClusterMiner miner;
DAL_DEClusterMiner_Init(miner, "E0011", 3, 5, 7, 10);
```

After a trade closes, emit the result:

```mql5
DAL_DETradeOutcome outcome;
DAL_DETradeOutcome_Reset(outcome);

outcome.strategy_id = "E0011";
outcome.symbol = _Symbol;
outcome.timeframe = PERIOD_M1;
outcome.direction = 1;
outcome.entry_time = TimeCurrent();
outcome.exit_time = TimeCurrent();
outcome.entry_price = entry;
outcome.stop_price = stop;
outcome.target_price = target;
outcome.r_result = 3.0;
outcome.is_win = true;
outcome.feature_key = "atr_expansion=high|donchian_width=high|htf=aligned";

DAL_DEClusterMiner_AddOutcome(miner, outcome);
```

At any point, the execution can ask whether a feature key is eligible:

```mql5
bool allowed = DAL_DEClusterMiner_IsEligible(
   miner,
   "atr_expansion=high|donchian_width=high|htf=aligned",
   200,   // min trades
   0.50,  // min filtered win rate
   0.60,  // min win-after-win probability
   1.10,  // min lift versus raw
   5      // min clusters of length 3
);
```

## Interpretation

If a key is eligible, the execution may allow Roulette / Jackpot mode.
If it is not eligible, the execution should remain in probe mode or use normal fixed-risk logic.

## Important constraint

The `feature_key` must be built using only information available before the trade is entered. No future path information may be used to decide the key.

## Output

The miner can print a compact report:

```mql5
DAL_DEClusterMiner_PrintReport(miner);
```

The report contains overall statistics and per-key statistics.
