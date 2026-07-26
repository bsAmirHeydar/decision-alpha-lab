---
id: SAED-540837CC29
title: "Capital and Portfolio Handoff"
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
  - portfolio
  - capital
---

# Capital and Portfolio Handoff

## Output to Portfolio

The Setup AI system publishes an opportunity candidate containing expected utility/distribution, uncertainty, novelty, requested risk tier, capacity, holding horizon, Context/cluster identities and promotion/calibration evidence.

## Boundary

The model does not calculate final lot size or guarantee allocation. Capital and Portfolio apply independent limits, dependence, concentration, capacity and reservation rules.

## Profile Implications

- P1/P4 consume more risk time and capacity.
- P2/P3 may create clustered small losses and rare tail dependence.
- P5 is execution-sensitive and may require tighter capacity/latency constraints.

Portfolio denial is a valid final action.
