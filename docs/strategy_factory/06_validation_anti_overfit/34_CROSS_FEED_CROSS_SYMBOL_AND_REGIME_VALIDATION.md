---
type: strategy-factory-document
status: canonical
title: "Cross-Feed, Cross-Symbol, and Regime Validation"
tags:
  - strategy-factory
---

# Cross-Feed, Cross-Symbol, and Regime Validation

A real market effect should not depend entirely on one broker's synthetic pricing, one symbol alias, or one favorable regime unless that dependency is the explicit thesis.

## Feed hierarchy

Use a canonical market feed where possible and a broker-realistic feed for execution. Reconcile timestamps, sessions, missing bars, contract rolls, and symbol specifications. Divergence research especially requires synchronized sources.

## Transfer tests

Test related symbols, alternate brokers, nearby futures contracts, and different years. Do not expect identical magnitude, but require directionally coherent behavior or a documented mechanism for specificity.

## Regime map

Break down trend, volatility, liquidity, crisis, and low-volume regimes. A regime-specific strategy is valid if the regime classifier is causal and the dependence is stable; it should not be presented as universal.

