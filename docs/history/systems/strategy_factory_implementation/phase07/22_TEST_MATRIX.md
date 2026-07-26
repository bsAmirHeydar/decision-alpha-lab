---
title: "Test Matrix"
phase: 07
status: canonical
---
# Test Matrix

Tests cover duplicate ownership, missing dependencies, cycle detection, deterministic ordering, state capacity, freshness, dirty flags, end-to-end snapshot build, vector order, type mismatch, deterministic IDs, MQL5 inventory, no live authority and no unsupported serialization calls.

## Invariants

- MQL5 owns runtime truth.
- Identical ordered inputs produce identical outputs.
- Known time is explicit and causal.
- Memory and work are bounded.
- No previous strategy is integrated.
- No execution authority exists.
