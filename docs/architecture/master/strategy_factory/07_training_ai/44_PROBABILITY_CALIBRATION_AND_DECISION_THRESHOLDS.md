---
type: strategy-factory-document
status: canonical
title: "Probability Calibration and Decision Thresholds"
tags:
  - strategy-factory
---

# Probability Calibration and Decision Thresholds

A probability is useful only when 0.7 means approximately 70% under comparable conditions and the threshold reflects economic utility.

## Calibration

Use train/validation-only Platt or isotonic calibration when sample size supports it. Report reliability tables, Brier score, expected calibration error, and fold variance. Recalibration is versioned.

## Thresholds

Thresholds maximize a declared utility that includes net R, drawdown, capacity, and false-positive cost. Do not select separately on the outer test. Use hysteresis or review zones to reduce unstable flip-flopping.

## Confidence versus risk

Confidence tier is an input to the independent risk gate, not direct leverage. Initial live risk remains capped until realized calibration and execution fidelity are demonstrated.

