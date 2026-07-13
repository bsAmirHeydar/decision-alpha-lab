---
id: SAED-2E4E9AE3DB
title: "Monitoring and Assumption Contract"
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
  - monitoring
  - assumptions
---

# Monitoring and Assumption Contract

## Monitored Assumptions

Context frequency/lifecycle, feature distribution, regime mix, prediction/calibration, selected profile/entry distribution, abstention, fill, spread/slippage, trail capture, tail behavior, capacity, latency and parity.

## Health Actions

```text
Healthy → Watch → Reduced → Quarantined → Retired
```

## Drift Response

Drift does not trigger silent online retraining. It triggers de-risk, diagnostic packet, new experiment, protected validation, challenger and explicit promotion.

## Profile-Specific Alerts

P1/P5 hit-rate/calibration decay; P2/P3 tail participation and losing streaks; P3/P4 trail capture/giveback; P4 trend-regime scarcity and capital occupancy.
