---
id: SAED-216AC6C29B
title: "Manual, AI, and Hybrid Policy Architecture"
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
  - hybrid
---

# Manual, AI, and Hybrid Policy Architecture

## Manual Baseline

Every Context family has an executable manual policy, even if it always skips. It provides a transparent champion and attribution baseline.

## AI Challenger

The model can filter, rank or choose among declared Treatments. It cannot expand action support at runtime.

## Hybrid Graph

Examples:

- human eligibility + AI Treatment ranking;
- deterministic stop + AI exit selection;
- AI trade/skip + fixed manual Treatment;
- regime router + specialist policies;
- manual fallback on OOD.

## Authority

Kill switch and hard risk dominate operator, manual and model decisions according to the frozen authority matrix.
