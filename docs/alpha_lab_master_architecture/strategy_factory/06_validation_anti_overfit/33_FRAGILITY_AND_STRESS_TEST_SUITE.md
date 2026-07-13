---
type: strategy-factory-document
status: canonical
title: "Fragility and Stress-Test Suite"
tags:
  - strategy-factory
---

# Fragility and Stress-Test Suite

A deployable edge should degrade gradually under realistic perturbations rather than disappear when one perfect assumption changes.

## Mandatory stresses

Cost multipliers, delayed entries, worse fill side, stop/target ambiguity, missing best trades, removed best days, parameter perturbation, time-boundary shifts, feed gaps, wider spreads, lower fill rates, and skipped signals.

## Parameter topology

Evaluate neighborhoods, not only the optimum. Broad plateaus are preferred over sharp peaks. A parameter chosen at an isolated maximum requires stronger confirmation and smaller risk.

## Failure report

For each stress, report the first point where expectancy, lower confidence bound, or drawdown breaches requirements. This defines operational tolerances and live kill thresholds.

