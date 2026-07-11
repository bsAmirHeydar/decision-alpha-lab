---
type: strategy-factory-document
status: canonical
title: "Exit and Position-Management Policy Catalog"
tags:
  - strategy-factory
---

# Exit and Position-Management Policy Catalog

Exit policies separate entry edge from management edge and prevent discretionary hindsight.

## Core families

Fixed R provides a clean baseline. Explicit structural targets test market anatomy. Time exits test cycle or session information. Trailing structures, partial-plus-runner, break-even, and regime-change exits are separate policies with their own state machines.

## Decomposition

First test entry/stop with simple exits. Then test management as an incremental layer. Report base position and runner separately. Break-even is not free: it alters stop probability, transaction costs, and tail capture.

## Path dependence

Multi-stage exits require event-by-event path replay, not final-bar labels. The outcome engine records every transition, partial fill, stop modification, and close reason. Management decisions use only information known at the transition time.

