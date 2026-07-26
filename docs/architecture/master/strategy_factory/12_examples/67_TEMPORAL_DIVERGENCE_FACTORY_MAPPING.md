---
type: strategy-factory-document
status: canonical
title: "Example — Temporal Intermarket Divergence Mapping"
tags:
  - strategy-factory
---

# Example — Temporal Intermarket Divergence Mapping

This example maps EXP0017-style divergence into the generic factory without granting its ontology to the shared core.

## Event

Reference extreme, hunter/clean roles, cycle group, direction, divergence known time, close confirmation, signal expiry, pair identity, and market-event cluster.

## Features

Cycle position, reference age, divergence strength, leader/lagger, session, spread, volatility, distance to invalidation, related-market return, and confirmation displacement. Every feature is frozen at confirmation.

## Candidates

Market confirmation, first retracement, reference limit; structural or ATR-buffered stop; fixed R, current-cycle-end, or explicit opposing reference exit.

## Nulls

Confirmation-only, time-matched random, role randomization, pair placebo, time shift, and no-divergence baseline. Promotion depends on incremental uplift, not raw SMT win rate.

