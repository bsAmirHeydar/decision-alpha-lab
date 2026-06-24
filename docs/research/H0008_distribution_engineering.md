# H0008 — Distribution Engineering

## Hypothesis

A trading strategy should be treated as an outcome-distribution generator, not merely as an edge signal.

The claim is:

> Some execution systems may not be globally attractive, yet they may contain causal feature regimes where profitable outcomes cluster. If those regimes can be mined and validated, Roulette / Jackpot execution should only be activated inside those engineered distribution states.

This shifts the research focus from raw edge to distribution engineering.

---

## Why this matters

Roulette / Jackpot execution does not need all signals.

It needs a narrow state where the probability of consecutive wins is materially higher than the raw baseline.

Therefore, the important object is not the strategy itself. The important object is the filtered trade population.

```text
strategy -> raw outcome distribution -> feature grouping -> cluster mining -> eligible distribution -> convex execution
```

---

## Testable statements

For each execution strategy and feature group, we test:

```text
P(W | feature) > P(W)
P(W_next | previous W, feature) > P(W | feature)
cluster_count_ge_3(feature) is non-trivial
cluster_count_ge_5(feature) is non-trivial
max_win_streak(feature) is stable out-of-sample
```

The ideal Jackpot filter is not merely high win-rate. It is high conditional continuation of wins.

---

## Anti-overfit rules

A valid distribution-engineering filter must pass:

```text
minimum sample size
minimum decided trades
minimum cluster count
walk-forward / out-of-sample persistence
no future leakage in feature construction
causal feature key must be known before entry
```

A filter with tiny samples is not a discovery. It is a story.

---

## Execution implication

Roulette should not run on a raw strategy.

Roulette should run only after the Distribution Engineering layer says:

```text
this feature state has measurable sequence lift
```

