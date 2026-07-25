# EXP0012 — Distributional Cluster Miner

## Title

**Distribution Engineering for Conditional Sequence Extraction**

This experiment turns each execution system into a distribution generator. The goal is not only to measure whether an execution has an edge. The goal is to identify the causal feature states where wins become clustered and therefore suitable for Roulette / Jackpot execution.

The central shift is:

```text
from: edge hunting
  to: distribution engineering
```

A raw strategy may have mediocre global statistics while still containing a narrow feature regime where the conditional probability of a next win after a win is much higher than the raw win rate.

That is the object we want to mine.

---

## Module Files

```text
mql5/Include/Research/DAL_DistributionEngineeringTypes.mqh
mql5/Include/Research/DAL_DistributionClusterMiner.mqh
mql5/Include/Research/DAL_DistributionClusterFilter.mqh
mql5/Include/Research/DAL_DistributionExecutionAdapter.mqh
mql5/Experts/Research/EXP0012_DistributionClusterMiner_Demo.mq5
```

The module is MQL5-only and research-only. It never sends orders.

---

## What the module measures

For every feature group, the miner calculates:

```text
total trades
wins
losses
flats
probe/live split
buy/sell split
raw win rate
decided win rate
mean R
R variance / std
min R / max R
profit factor
average win R
average loss R
payoff ratio
MFE_R / MAE_R averages
bars-to-exit averages
hour distribution
R-result distribution buckets
current and max win streak
current and max loss streak
clusters >= 3 wins
clusters >= 5 wins
clusters >= 7 wins
clusters >= 10 wins
P(win | at least 1 previous win)
P(win | at least 2 previous wins)
P(win | at least 3 previous wins)
loss hazard after k wins
lift versus raw distribution
sequence lift versus own win rate
rank score
```

---

## Core metrics

### Raw win rate

Global probability of a win in the unfiltered trade population.

```text
P(W)
```

### Filtered win rate

Win probability inside one causal feature group.

```text
P(W | feature_key)
```

### Lift

How much the feature group improves win probability versus the raw distribution.

```text
Lift = P(W | feature_key) / P(W)
```

### Conditional win-after-win

The key Roulette / Jackpot metric.

```text
P(W_next | current_run_length >= k, feature_key)
```

A filter is not valuable for Jackpot merely because it improves win rate. It is valuable when it improves the probability of continued wins after the run has already started.

### Cluster counts

The module counts feature groups that produced runs of:

```text
>= 3 wins
>= 5 wins
>= 7 wins
>= 10 wins
```

This is the direct sequence-mining layer.

---

## Integration contract for execution modules

Every execution module can plug into the miner by recording a completed trade outcome after the position is closed.

Minimal include:

```mql5
#include <Research/DAL_DistributionExecutionAdapter.mqh>
```

Global miner:

```mql5
DAL_DEClusterMiner g_de_miner;
```

Initialize:

```mql5
DAL_DEClusterMiner_Reset(g_de_miner, "E0011_DE", "E0011_Donchian20Atr3Roulette");
```

Build a feature key before entry:

```mql5
string key = DAL_DEAdapter_BaseFeatureKey("E0011", _Symbol, PERIOD_M1);
key = DAL_DE_KeyAppend(key, "atr", "high");
key = DAL_DE_KeyAppend(key, "donchian_width", "high");
key = DAL_DE_KeyAppend(key, "htf_aligned", "true");
key = DAL_DE_KeyAppend(key, "path_clean", "true");
key = DAL_DEAdapter_AddDirectionFeature(key, direction);
key = DAL_DEAdapter_AddSessionFeature(key, TimeCurrent());
```

After a trade closes, record outcome:

```mql5
DAL_DEExecutionAdapterConfig cfg;
DAL_DEExecutionAdapterConfig_Default(cfg, "E0011", "E0011_Donchian20Atr3Roulette");
cfg.symbol = _Symbol;
cfg.timeframe = PERIOD_M1;
cfg.magic = InpMagic;
cfg.win_threshold_r = 3.0;
cfg.loss_threshold_r = -1.0;

DAL_DEAdapter_RecordOutcomeFromMoney(
   g_de_miner,
   cfg,
   key,
   DAL_DE_LAYER_LIVE,
   direction,
   entry_time,
   exit_time,
   entry_price,
   exit_price,
   stop_price,
   target_price,
   risk_money,
   volume,
   gross_profit,
   commission,
   swap,
   mfe_r,
   mae_r,
   bars_to_exit,
   position_id,
   deal_id
);
```

Then ask whether the current feature state is eligible:

```mql5
DAL_DEClusterFilterConfig filter_cfg;
DAL_DEClusterFilterConfig_Default(filter_cfg);

DAL_DEClusterFilterDecision decision;
bool allowed = DAL_DEAdapter_IsFeatureEligible(g_de_miner, key, filter_cfg, decision);
```

If `allowed == true`, the execution may allow the Roulette / Jackpot layer for that feature state.

---

## Design principle

Roulette is the convex execution layer.

Distribution Engineering is the permission layer.

The execution should not ask:

```text
Is the strategy globally profitable?
```

It should ask:

```text
Is this current feature state statistically associated with clustered 3R wins?
```

That is the core of EXP0012.
