---
id: SAED-0F61FBACAA
title: "P4 — Wide-Survival Open-Target Trend Capture"
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
  - payoff-profile
  - p4
  - trend
---

# P4 — Wide-Survival Open-Target Trend Capture

## Mission

Keep the thesis alive through normal noise with a wide structural stop, then follow a genuine trend with an open target and trailing exit.

## Distinction from P3

P3 creates convexity mainly through a small initial loss. P4 creates participation through survival and trend persistence. P4 consumes more risk time and is more regime-dependent.

## Required Models

- trend persistence;
- remaining trend length;
- pullback-depth distribution;
- regime survival;
- time-to-regime-break;
- path smoothness;
- trail-width suitability;
- capital occupancy.

## Guardrails

- no unlimited holding without expiry/health rules;
- explicit chop/regime abstention;
- time-underwater and capacity limits;
- correlation/concentration stress;
- no use of wide stop to manufacture hit rate.
