---
type: strategy-factory-document
status: canonical
title: "Cost, Fill, and Microstructure Model"
tags:
  - strategy-factory
---

# Cost, Fill, and Microstructure Model

Economic validity requires realistic bid/ask, commission, slippage, latency, fill probability, and broker constraints.

## Cost layers

Model spread by symbol and time, commission by volume, slippage by volatility and order type, financing/roll when relevant, exchange fees for futures, and reject/missed-fill behavior. Historical mid-price outcomes are diagnostic only.

## Stress scenarios

Every strategy is tested at normal, 1.5x, 2x, and severe cost; one-bar and multi-second delay; worse-side intrabar ambiguity; missed best fills; and broker minimum-stop rounding. Scalping strategies face stricter thresholds.

## Research/live reconciliation

Paper and live traces calculate realized cost in R and compare it with the research assumption. Persistent underestimation demotes the strategy or updates a new cost-model version followed by revalidation.

