# H0008 — Distribution Engineering for Conditional Sequence Extraction

## Status

Draft / next hypothesis.

## Research title

**Distribution Engineering for Conditional Sequence Extraction**

## Claim

A trading strategy should not be evaluated only by its raw edge. For high-convexity capital engines such as Roulette, the central research object is the **conditional distribution of outcomes**.

The hypothesis is that some execution strategies contain hidden sequence structure: wins may become more likely after a previous win under specific regimes, filters, and path conditions. If this structure can be measured causally and validated out-of-sample, Roulette should only be activated inside those cluster-producing states.

## Why this matters

The project is moving beyond ordinary edge hunting.

Raw edge asks:

```text
Does this strategy make money on average?
```

Distribution engineering asks:

```text
Can we reshape and filter the outcome distribution so that the rare payoff shape we want becomes conditionally accessible?
```

For a 3R Roulette sequence, the target is not merely a profitable strategy. The target is a conditional state where the probability of repeated wins is higher than the raw baseline.

## Formal test

Let `W` be a trade that reaches the intended reward target before stop-loss.
Let `F` be a causal filter key constructed before the trade is taken.

The hypothesis is supported if there are filters where:

```text
P(W | F) > P(W)
P(W_next | F and previous W) > P(W | F)
ClusterDensity(F) > ClusterDensity(raw)
```

The most important metric is not ordinary win rate. The most important metric is conditional continuation after a win:

```text
P(next win | filter, current win streak length = k)
```

## Required experiment

The next experiment must create a reusable cluster-mining module that can be attached to any execution model.

Each execution must be able to emit:

```text
strategy_id
symbol
timeframe
direction
entry_time
entry_price
stop_price
target_price
R_result
win/loss
bars_to_exit
MFE_R
MAE_R
feature_key
```

The miner must compute:

```text
raw win rate
filtered win rate
lift
max streak
cluster counts
P(W after W)
P(W after WW)
P(W after WWW)
filter eligibility
```

## Acceptance criteria

A filter is eligible for Roulette only if:

```text
sample_size is sufficient
filtered win rate is higher than raw
conditional win-after-win is higher than filtered win rate
cluster count is non-trivial
out-of-sample lift survives
no future data is used in the filter key
```

## Rejection criteria

A filter is rejected if it only improves average win rate but does not improve clustering.

A filter is also rejected if it survives only by reducing sample size to a tiny historical pocket.

## Strategic meaning

This hypothesis makes the project more professional because it separates four layers:

```text
Execution = produces candidate trades
Distribution Miner = measures the outcome law
Cluster Filter = decides whether the state is eligible
Roulette = applies convex capital only after eligibility
```

This is the core shift:

```text
From finding edge
To engineering distributions
```
