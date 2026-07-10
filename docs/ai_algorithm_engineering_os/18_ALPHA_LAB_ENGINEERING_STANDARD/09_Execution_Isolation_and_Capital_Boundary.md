---
id: AIEOS2-33AED95304B1
title: "Execution Isolation and Capital Boundary"
type: standard
status: active
domain: alpha-lab-standard
version: 2.0.0
created: 2026-07-10
updated: 2026-07-10
tags:
  - ai-engineering
  - alpha-lab
  - alpha-lab-standard
---
# Execution Isolation and Capital Boundary

Execution receives approved intents through a versioned contract. It enforces risk, idempotency, broker validation, and reconciliation. It cannot infer new signals, alter model thresholds, or reinterpret domain state.

Research mode, paper mode, and live mode are distinct configurations with explicit guards and logs.
