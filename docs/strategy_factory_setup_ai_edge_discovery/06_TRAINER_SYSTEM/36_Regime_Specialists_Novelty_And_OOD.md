---
id: SAED-0C4F102054
title: "Regime Specialists, Novelty, and Out-of-Distribution Control"
type: architecture
status: canonical
domain: strategy-factory-setup-ai-edge-discovery
version: 1.0.0
created: 2026-07-13
updated: 2026-07-13
tags:
  - strategy-factory
  - setup-factory
  - ai-training
  - trainer
  - regime
  - ood
---

# Regime Specialists, Novelty, and Out-of-Distribution Control

## Regime Use

Regimes may route to specialists only when regime state is known at decision time and the routing process is included in validation.

## Novelty/OOD

Monitor feature support, categorical novelty, distance/density, ensemble disagreement, calibration cohorts and Context capability mismatches.

## Actions

- proceed with champion;
- use conservative baseline;
- reduce eligibility tier;
- abstain;
- quarantine if systemic.

## Anti-Overfit

Do not create many regime experts from the same data and report only the best. Regime definition and expert count are part of the trial universe.
