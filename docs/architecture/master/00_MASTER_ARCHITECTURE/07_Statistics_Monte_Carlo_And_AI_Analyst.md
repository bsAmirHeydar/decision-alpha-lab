---
id: ALMA-A9D20B8A85
title: "Statistics, Monte Carlo and AI Analyst"
type: architecture
status: canonical
domain: alpha-lab-master-architecture
version: 1.0.0
created: 2026-07-13
updated: 2026-07-13
tags:
  - alpha-lab
  - master-architecture
---
# Statistics, Monte Carlo and AI Analyst

## 1. Central Statistical Engine

All manual and AI setups enter one shared statistical engine. Strategy authors cannot choose easier tests for preferred ideas.

The standard pack reports:

- independent opportunity and cluster counts;
- base rate and incremental uplift;
- expectancy and net utility;
- win rate and payoff distribution;
- confidence intervals;
- drawdown depth, duration and recovery;
- tail loss and expected shortfall;
- MFE, MAE and holding time;
- calibration, discrimination and coverage;
- regime, symbol, session and time buckets;
- cost and execution sensitivity;
- concentration in best trades, periods or clusters.

## 2. Dependence-Aware Inference

Trade rows are not automatically independent. Treatment siblings from one opportunity, overlapping holding periods and regime clusters require cluster/block resampling, purge and embargo.

## 3. Monte Carlo Engines

The central Monte Carlo layer includes:

- opportunity-cluster bootstrap;
- block or stationary bootstrap;
- trade-order/path uncertainty;
- spread, slippage and latency simulation;
- missed and partial fills;
- gap and tail scenarios;
- model and parameter uncertainty;
- portfolio dependence and ruin probability.

Outputs include terminal wealth distribution, drawdown, time underwater, risk-limit breach, worst quantile paths and capital requirements.

## 4. Anti-Overfit Suite

Mandatory controls include:

- nested/purged walk-forward;
- multiple-testing correction;
- deflated performance;
- probability of backtest overfitting;
- reality-check or superior-predictive-ability tests;
- parameter-surface stability;
- feature and treatment ablation;
- best-trade/period/cluster removal;
- cross-feed, cross-symbol and regime tests;
- cost, delay and execution stress;
- prospective paper evidence.

## 5. Null and Placebo Generator

Every context declares matched nulls preserving nuisance variables such as session, volatility, direction balance, holding period and cost. The platform can remove the context signal, shift timestamps, shuffle direction, substitute irrelevant pairs or compare against simple unconditional policies.

The key question is not merely “did it make money?” but “did this context add information beyond matched baselines?”

## 6. AI Analyst

The analyst receives registered artifacts and produces structured claims:

- profit source;
- loss source;
- regime/context attribution;
- treatment and feature attribution;
- cost/execution attribution;
- alternative explanations;
- confidence;
- counter-evidence;
- proposed falsification experiment.

All numeric claims must link to machine-generated artifacts. Unsupported explanations are labeled speculation.

## 7. Final Decision

Statistics and analysis create evidence. A deterministic gate and authorized human governance decide promotion. Profit alone never overrides leakage, non-reproducibility or critical execution failure.
