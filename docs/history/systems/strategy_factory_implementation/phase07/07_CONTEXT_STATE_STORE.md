---
title: "Context State Store"
phase: 07
status: canonical
---
# Context State Store

The state store is bounded, typed and keyed by feature ID. Each entry records value, computation generation, expiry, dirty state and invalidation reason. Capacity overflow fails closed.

## Invariants

- MQL5 owns runtime truth.
- Identical ordered inputs produce identical outputs.
- Known time is explicit and causal.
- Memory and work are bounded.
- No previous strategy is integrated.
- No execution authority exists.
