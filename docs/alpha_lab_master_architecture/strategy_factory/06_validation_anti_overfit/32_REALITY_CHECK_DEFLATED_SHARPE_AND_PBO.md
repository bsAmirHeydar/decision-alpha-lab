---
type: strategy-factory-document
status: canonical
title: "Reality Check, Deflated Sharpe, and Probability of Backtest Overfitting"
tags:
  - strategy-factory
---

# Reality Check, Deflated Sharpe, and Probability of Backtest Overfitting

Selection-aware metrics test whether the best result is better than what a broad search would produce by luck.

## White-style reality check

Bootstrap the maximum performance across candidate strategies under a centered null. This addresses the fact that the reported winner was selected from many alternatives.

## Deflated Sharpe

Compare observed Sharpe with the expected maximum Sharpe given the number and dispersion of trials, while accounting approximately for skew and kurtosis. Report the probability, not merely the adjusted number.

## PBO

Combinatorial symmetric cross-validation selects the in-sample winner and observes its out-of-sample rank. A high probability of below-median OOS rank means the research process is choosing noise.

## Limits

These tests depend on trial accounting and dependence assumptions. They do not rescue bad data or leakage. They are gates alongside, not substitutes for, causal validation.

