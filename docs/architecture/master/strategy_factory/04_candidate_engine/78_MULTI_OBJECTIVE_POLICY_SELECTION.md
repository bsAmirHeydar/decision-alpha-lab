---
type: strategy-factory-document
status: canonical
title: "Multi-Objective Policy Selection"
tags:
  - strategy-factory
---

# Multi-Objective Policy Selection

The best candidate is rarely the one with the highest mean R alone. Selection must account for uncertainty, drawdown, fill, tail capture, costs, and operational complexity.

## Objectives

Expected net R, lower confidence bound, profit factor, drawdown, MAE, fill rate, latency sensitivity, turnover, capacity, tail share, calibration, and policy stability. Define hard constraints first, then rank feasible candidates.

## Pareto frontier

Retain candidates that are not dominated across selected objectives. A market entry may have lower average R but higher fill and robustness; a limit may offer better R but low capacity. The decision depends on portfolio role.

## Utility functions

Utility weights are versioned and chosen before the outer test. Robust alternatives include minimum OOS fold utility, lower-bound expectancy, or constrained optimization rather than a single mean. Do not tune utility weights to select the historical winner.

## Model use

A candidate ranker can estimate multiple outcomes and apply the same frozen utility. The risk gate remains separate. The selected policy distribution is monitored for abrupt changes and concentration.

