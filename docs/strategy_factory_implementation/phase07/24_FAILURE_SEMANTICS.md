---
title: "Failure Semantics"
phase: 07
status: canonical
---
# Failure Semantics

Startup failures include empty registry, duplicate owner, missing dependency, cycle, invalid vector schema and capacity violations. Runtime failures include future feature, type mismatch, invalid quality, computation failure and vector coercion failure. Strict mode fails closed.

## Invariants

- MQL5 owns runtime truth.
- Identical ordered inputs produce identical outputs.
- Known time is explicit and causal.
- Memory and work are bounded.
- No previous strategy is integrated.
- No execution authority exists.
