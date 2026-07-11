---
type: strategy-factory-document
status: canonical
title: "Null, Placebo, and Random Baselines"
tags:
  - strategy-factory
---

# Null, Placebo, and Random Baselines

A strategy must beat alternatives that preserve the easy structure of the data while removing the claimed information.

## Core nulls

Session-matched random entry, confirmation-only entry, anatomy-time shuffle within day, role randomization, direction randomization, reference-time shift, placebo symbol pair, matched random zones, and no-divergence events.

## Preserve nuisance structure

Randomization should retain session, volatility, holding period, costs, and sample count so the null is not artificially weak. A strategy that only beats fully random timestamps may simply exploit intraday seasonality.

## Interpretation

Failure to beat a matched null kills the claimed mechanism even if raw expectancy is positive. The positive result may still be a generic execution effect and can be moved into a simpler strategy family.

