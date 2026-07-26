---
id: SAED-5845D1FB2A
title: "Task 1 — Eligibility and Trade/Skip Meta-Label"
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
  - classification
---

# Task 1 — Eligibility and Trade/Skip Meta-Label

## Question

Does this Context/candidate combination clear a declared net utility hurdle after costs and uncertainty?

## Baselines

Never trade, always trade fixed policy, unconditional base rate, Context-only rule, single-feature thresholds and Manual policy.

## Metrics

Log loss, Brier score, calibration, coverage, net R at threshold, selective expectancy, false-positive cost, missed-tail cost and cluster-level uplift.

## Threshold

Selected on training/validation using declared utility and guardrails. The outer test evaluates the entire threshold-selection procedure.
