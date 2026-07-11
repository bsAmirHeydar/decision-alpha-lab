---
title: "Context Frame Identity"
phase: 07
status: canonical
---
# Context Frame Identity

A ContextFrame binds event ID, snapshot ID, graph hash, vector schema hash, vector ID, state generation, feature count, snapshot time and source hash. This prevents a model score from being detached from the exact context that produced it.

## Invariants

- MQL5 owns runtime truth.
- Identical ordered inputs produce identical outputs.
- Known time is explicit and causal.
- Memory and work are bounded.
- No previous strategy is integrated.
- No execution authority exists.
