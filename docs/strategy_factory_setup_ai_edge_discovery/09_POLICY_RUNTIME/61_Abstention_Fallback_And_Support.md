---
id: SAED-EB3D3C0532
title: "Abstention, Fallback, and Policy Support"
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
  - policy
  - fallback
---

# Abstention, Fallback, and Policy Support

## Support Audit

Before selecting a candidate, verify that the model was trained/calibrated on the Context/view/candidate combination and that runtime features are within declared support.

## Fallback Order

A typical order:

```text
Certified AI policy
→ simpler certified model
→ manual baseline
→ conservative skip
```

## Reasons

Stale Context, missing view, novelty, high uncertainty, small ranking margin, low expected utility, cost infeasibility, artifact mismatch, runtime degradation or portfolio conflict.

## Evidence

Every abstention/fallback is a decision event with reason, thresholds, support findings and selected authority path.
