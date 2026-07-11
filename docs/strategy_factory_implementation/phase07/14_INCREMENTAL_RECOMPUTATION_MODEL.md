---
title: "Incremental Recalculation Model"
phase: 07
status: canonical
---
# Incremental Recalculation Model

The engine supports STATIC, EVENT, TICK, NEW_BAR and TIMER scopes. Phase 07 exercises event-scoped nodes. Later providers may reuse fresh cached values and recompute only dirty descendants without changing contracts.

## Invariants

- MQL5 owns runtime truth.
- Identical ordered inputs produce identical outputs.
- Known time is explicit and causal.
- Memory and work are bounded.
- No previous strategy is integrated.
- No execution authority exists.
