---
id: SAED-475071CBA5
title: "Prospective Challenge and Deterministic Promotion Gate"
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
  - anti-overfit
  - prospective
  - promotion
---

# Prospective Challenge and Deterministic Promotion Gate

## Freeze

Before prospective observations begin, freeze Context, candidate universe, model, preprocessing, calibration, threshold, Treatment, costs, risk limits and monitoring rules.

## No-Tuning Period

No retraining, threshold changes, cherry-picking, removal of bad events or Treatment substitution.

## Promotion Outcomes

- `PROMOTE`: all mandatory evidence and operational gates pass.
- `CHALLENGE`: promising but incomplete/uncertain; more frozen evidence required.
- `REJECT`: critical blocker or insufficient robust utility.

## Evidence

Expected/observed decisions, fills, costs, missed opportunities, duplicates, drift, incidents and deviations are retained immutably.
