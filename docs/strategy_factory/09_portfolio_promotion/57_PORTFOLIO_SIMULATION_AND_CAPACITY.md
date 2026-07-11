---
type: strategy-factory-document
status: canonical
title: "Portfolio Simulation, Capacity, and Capital Path"
tags:
  - strategy-factory
---

# Portfolio Simulation, Capacity, and Capital Path

Strategy-level alpha can disappear when combined through correlated exposure, limited liquidity, and capital constraints.

## Simulation

Replay candidate decisions across strategies in timestamp order with aggregate risk limits, one-thesis clustering, margin, priority, and realistic fills. Measure portfolio drawdown, concentration, turnover, and missed opportunities.

## Capacity

Estimate spread/slippage response to size, available depth, broker limits, session liquidity, and fill probability. Capacity is strategy- and time-dependent. A high-R small-capacity edge may remain valuable but cannot support explosive scaling alone.

## Capital path stress

Monte Carlo or block bootstrap cluster returns, include cost uncertainty and strategy downtime, and test survival under adverse sequences. Use conservative risk-of-ruin and drawdown tolerances.

