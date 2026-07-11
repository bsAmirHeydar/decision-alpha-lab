---
type: strategy-factory-reference
status: canonical
title: "Statistical Engine — Full Reference"
tags:
  - strategy-factory
  - statistics
  - reference
---

# Statistical Engine — Full Reference

## Objective

The statistical engine describes economic behavior, uncertainty, dependence, and conditional variation in a uniform way. Its purpose is not to make every strategy look comparable through one number; it ensures that every strategy is exposed to the same uncomfortable questions.

## Analysis levels

Statistics are generated at several levels:

1. **candidate row** — one entry/stop/exit policy for an event;
2. **event** — all candidates generated from one anatomy event;
3. **market-event cluster** — related events/candidates from one market episode;
4. **day/session** — operational concentration;
5. **strategy version** — full program;
6. **portfolio** — aggregate exposure and PnL.

Promotion relies primarily on cluster and time-block evidence. Row-level statistics are descriptive.

## Core economic metrics

For filled trades with net return `r_i`:

```text
expectancy = mean(r_i)
profit factor = sum(positive r_i) / abs(sum(negative r_i))
win rate = count(r_i > 0) / count(filled)
max drawdown = maximum peak-to-trough decline of cumulative R
```

Also report median, standard deviation, lower/upper quantiles, average win/loss, payoff ratio, total R, longest loss streak, tail share, and percentage of gross profit contributed by the best trade/day/cluster.

Fill-aware reports show:

- event count
- candidate count
- fill count and fill rate
- expired/no-fill count
- result conditional on fill
- opportunity outcome for no-fill paths when measurable
- adverse selection: filled versus unfilled future path

## Path quality

MFE and MAE are reported in initial-risk units. Additional path metrics may include:

- time to first +0.5R, +1R, and target
- time to maximum favorable/adverse excursion
- fraction of holding time underwater
- maximum giveback from MFE
- path efficiency: final R / max(MFE, epsilon)
- immediate adverse excursion
- stop proximity before expansion

These metrics help design exits but are not available as entry features.

## Conditional attribution

Standard dimensions:

- strategy and version
- candidate entry/stop/exit
- long/short
- symbol and reference symbol
- timeframe/cycle group
- session and minute bucket
- weekday/month/year
- spread and volatility bucket
- reference age
- anatomy state/family
- feed and broker
- model score/calibration bucket

Each table displays row count, cluster count, expectancy, confidence interval, and trial-adjusted status. Buckets below minimum evidence remain visible but are tagged exploratory.

## Baselines

The engine requires at least one simple economic baseline and one matched null. Common baselines:

- never trade
- always trade each confirmed event
- fixed policy across all events
- confirmation-only
- session-only
- simple trend or volatility rule
- matched random timestamp
- matched random level/zone
- no-divergence or no-anatomy control

Incremental uplift is computed with paired cluster-level differences where possible. Comparing unrelated samples can confuse regime differences with anatomy value.

## Uncertainty

Ordinary standard errors assume independence and are not official. Use:

- market-event cluster bootstrap
- day/week block bootstrap
- fold dispersion
- robust quantile intervals
- paired permutation for uplift

Report both point estimate and lower confidence bound. A positive mean with materially negative lower bound is uncertain, not validated.

## Tail and concentration analysis

A convex strategy may legitimately depend on tails, but tail dependence must be understood. Report results after removing top 1%, 5%, and 10% trades; top days; and top clusters. Compare tail frequency across folds and regimes. Distinguish a coherent rare-payoff process from one accidental outlier.

## Drawdown and sequence risk

Backtest order matters. Compute chronological drawdown, loss streaks, time under water, recovery, and block-bootstrap capital paths. Candidate rows from the same event are never concatenated into a fake tradable equity curve. Portfolio simulation chooses one policy per event before constructing a curve.

## Calibration-linked economics

For model-driven decisions, group predictions into probability or expected-R bins. For each bin report predicted value, observed outcome, count, cluster count, net R, drawdown, and coverage. A score that ranks well but is poorly calibrated may still be useful for ranking but must not drive proportional risk.

## Report hierarchy

Every official report has:

1. identity and artifact hashes;
2. data and cluster coverage;
3. base statistics;
4. distribution and drawdown;
5. conditional tables;
6. baselines and uplift;
7. uncertainty;
8. anti-overfit results;
9. fragility/stress;
10. execution assumptions;
11. limitations and promotion status.

## Statistical anti-patterns

Reject reports that:

- show only win rate;
- select the best target without counting trials;
- mix no-fill and filled outcomes inconsistently;
- average candidate rows as if simultaneously tradable;
- use final-day/session information as context;
- omit costs;
- hide failed years or folds;
- remove losing anomalies without a predeclared data rule;
- optimize on the same interval called OOS;
- report p-values without dependence correction.

## Implementation

`statistics.py` provides the standard summary and grouped reports. `anti_overfit.py` provides cluster/block bootstrap, permutation, FDR, Deflated Sharpe, PBO, reality check, best-trade removal, and cost/delay stress. These are reference implementations designed for auditability. High-stakes promotion may add more rigorous libraries or independent replication, but the artifact and contract semantics remain unchanged.
