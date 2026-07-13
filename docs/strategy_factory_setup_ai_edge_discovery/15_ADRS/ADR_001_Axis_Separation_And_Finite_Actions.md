---
id: SAED-B380FC0AD5
title: "ADR-001 — Separate Payoff Profile from Entry Mechanism and Keep Actions Finite"
type: adr
status: canonical
domain: strategy-factory-setup-ai-edge-discovery
version: 1.0.0
created: 2026-07-13
updated: 2026-07-13
tags:
  - strategy-factory
  - setup-factory
  - ai-training
  - adr
---

# ADR-001 — Separate Payoff Profile from Entry Mechanism and Keep Actions Finite

## Decision

Represent the user's styles as orthogonal, versioned axes and allow AI to select only from a finite Treatment universe.

## Rationale

This preserves interpretability, permits profile-specific objectives, enables controlled ablation, prevents arbitrary runtime actions and integrates with UCEE treatment/policy contracts.

## Rejected Alternatives

- one free-form “strategy generator”;
- treating Breakout/Market/Limit as complete strategies;
- predicting raw future prices and deriving undeclared orders;
- letting a model optimize stop/exit continuously without bounded registries.

## Consequences

More up-front registry work, but far stronger auditability, parity and false-discovery control.
