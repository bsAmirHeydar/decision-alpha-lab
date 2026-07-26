# H0008 — Distribution Engineering Instead of Raw Edge Hunting

## One-line thesis

Decision Alpha Lab is moving from **edge discovery** to **distribution engineering**: the objective is not merely to find a strategy with positive expectancy, but to reshape the conditional distribution of outcomes until profitable clusters become identifiable, measurable, and executable.

---

## Abstract

Most trading research starts with a strategy and asks whether it has an edge. In this project, that question is no longer sufficient. A strategy may have weak raw expectancy while still producing rare but structurally meaningful clusters of wins. Conversely, a strategy may have acceptable raw profit factor but no exploitable sequence behavior. For a convex sequence engine such as Roulette / Jackpot execution, the central question is not only whether the next trade has positive expectancy. The central question is whether the next trade belongs to a conditional state where wins are more likely to arrive in clusters.

H0008 formalizes this shift. We treat every execution model as a generator of an empirical outcome distribution. We then analyze that distribution by state, feature bin, regime, time, path quality, and previous outcome context. The goal is to discover filters that do not simply improve the average trade, but specifically increase the probability of consecutive 3R wins after an initial confirmed win. In other words, we search for **cluster lift**, not just raw win rate.

The resulting research object is a reusable distributional module. Any execution engine can emit a trade outcome into the miner. The miner records the result, groups it by a regime/filter key, computes raw and conditional win probabilities, measures streak density, estimates lift over baseline, and determines whether a candidate state is eligible for high-convexity execution.

This reframes the project around a professional title:

> **Distribution Engineering for Conditional Sequence Extraction**

The execution edge becomes only the input. The engineered distribution is the tradable object.

---

## Motivation

A normal execution report is dominated by aggregate metrics:

- total trades
- win rate
- profit factor
- average R
- drawdown
- Sharpe-like smoothness

These metrics are useful for stable portfolio systems, but they are insufficient for a jackpot-style sequence engine. A Roulette sequence does not need thousands of stable trades. It needs a narrow state where the probability of repeated wins is materially higher than the raw unconditional probability.

For example, two strategies can have the same raw 3R win rate:

```text
Strategy A: P(W) = 35%, P(W | previous W) = 35%
Strategy B: P(W) = 35%, P(W | previous W) = 60%
```

The first strategy is approximately memoryless. It may still be tradable, but it is poor for a sequence engine. The second strategy contains clustering. If the clustering survives out-of-sample tests, it is more valuable for Roulette than the raw win rate suggests.

This is the core of H0008.

---

## Hypothesis

Some execution strategies have hidden conditional structure in their outcome distribution. This structure is not visible in the raw aggregate report, but becomes visible after grouping trades by state features such as volatility expansion, path cleanliness, higher-timeframe direction, breakout width, session, and previous outcome context.

The hypothesis is:

```text
There exist filters F such that:

P(W | F) > P(W)
P(W_next | F and previous W) > P(W | F)
ClusterDensity(F) > ClusterDensity(raw)
```

For Roulette / Jackpot execution, a filter is valuable only if it improves the probability of a sequence, not merely the isolated probability of one winning trade.

---

## Core definitions

### Raw edge

Raw edge is the unconditional performance of a strategy over all signals.

```text
P(W) = wins / total_trades
```

### Filtered edge

Filtered edge is the performance of the strategy inside a condition or regime key.

```text
P(W | F) = wins_inside_filter / total_inside_filter
```

### Cluster lift

Cluster lift measures how much a filter improves the probability of winning relative to the raw distribution.

```text
Lift(F) = P(W | F) / P(W)
```

### Conditional continuation probability

This measures whether wins are independent or clustered.

```text
P(W_next | F and current_win_streak >= k)
```

For Roulette, this metric is more important than ordinary win rate.

### Cluster density

Cluster density counts how often a filter produces streaks of at least a required length.

```text
ClusterDensity_k(F) = number_of_win_streaks_at_least_k / total_trades_inside_filter
```

---

## What the experiment must prove

EXP0012 must not prove that one strategy is permanently profitable.

It must prove whether the outcome distribution of a strategy can be reshaped by filters into a state where:

1. the filtered 3R win probability is meaningfully higher than raw;
2. wins become more clustered after a previous win;
3. the filter keeps enough samples to be statistically useful;
4. the behavior survives out-of-sample validation;
5. the filter can be used by an execution module without look-ahead.

---

## Required outputs

For every execution strategy tested, the report must include:

```text
raw_total
raw_win_rate
raw_average_R
raw_max_win_streak
raw_cluster_count_3
raw_cluster_count_5
raw_cluster_count_7
raw_cluster_count_10

filtered_total
filtered_win_rate
filtered_lift
filtered_after_win_probability
filtered_after_two_wins_probability
filtered_after_three_wins_probability
filtered_max_win_streak
filtered_cluster_count_3
filtered_cluster_count_5
filtered_cluster_count_7
filtered_cluster_count_10

best_filter_key
sample_size
in_sample_result
out_of_sample_result
rejection_reason_if_any
```

---

## Anti-overfit rules

A filter is not accepted merely because it found a beautiful streak in history.

Minimum validation rules:

```text
min_trades_per_filter >= 200
min_win_clusters_3 >= 5
min_out_of_sample_segments >= 3
filtered_lift_out_of_sample >= 1.10
P(W_next | previous W, F) out_of_sample > P(W | F) out_of_sample
```

A filter with very few samples is treated as an observation, not as a deployable rule.

---

## Relation to Roulette / Jackpot execution

Roulette is not the edge. Roulette is a convex capital engine. It magnifies the result of a sequence.

Therefore, Roulette should not be attached to all raw signals. It should be attached only to a state where distributional evidence shows that clusters are more likely.

The correct pipeline is:

```text
raw execution strategy
→ distributional report
→ cluster filter selection
→ probe/micro gate
→ Roulette jackpot sequence
```

The filter decides when the convex engine is allowed to activate.

---

## Project-level positioning

This hypothesis marks a change in the research identity of Decision Alpha Lab:

```text
Old framing:
Find an edge.

New framing:
Engineer the outcome distribution until the desired payoff shape becomes conditionally accessible.
```

This is why H0008 is not just another strategy test. It is a research layer above strategies.

The strategy is the signal generator.
The distribution miner is the scientific instrument.
The cluster filter is the decision layer.
Roulette is the convex execution layer.

---

## Expected conclusion format

A successful experiment should be able to say:

```text
Strategy: Donchian20 ATR3
Raw 3R win rate: 31%
Best filter: ATR expansion + Donchian width expansion + HTF alignment
Filtered 3R win rate: 54%
P(next win | previous win, filtered): 68%
Max filtered streak: 8
5-win clusters: 14
7-win clusters: 3
10-win clusters: 0
Out-of-sample lift: 1.23
Status: candidate for Roulette sequence testing
```

A failed experiment should say:

```text
The strategy improved isolated win rate after filtering, but did not create conditional win clustering. It is rejected for Roulette usage and may only be considered for normal fixed-risk execution.
```
