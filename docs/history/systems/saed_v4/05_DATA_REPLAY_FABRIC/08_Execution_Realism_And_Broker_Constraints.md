---
title: Execution Realism and Broker Constraints
status: canonical
version: 4.0.0
created: '2026-07-13'
updated: '2026-07-13'
tags:
- saed-v4
- gap-closure
- canonical
---

# Objective

Ensure treatment outcomes and runtime decisions respect executable bid/ask, spread, slippage, tick size, volume step, stop level, freeze level, margin, session, latency, reject and partial-fill mechanics.

# Contract

Each broker/economics profile is immutable and time-bounded. Unknown constraints are unsupported—not zero.

# Research controls

- Market entries use executable side prices.
- Limit/stop orders model trigger, queue/fill, expiry and adverse selection.
- Tight-stop profiles receive one-tick, one-bar, spread and feed stress.
- Capacity curves degrade fill and utility with size.
- Broker differences are transport tests, not nuisance averaging.

# Runtime controls

Hard preflight normalizes price/volume, validates margin/session/stops, and rejects incompatible requests before order authority.
