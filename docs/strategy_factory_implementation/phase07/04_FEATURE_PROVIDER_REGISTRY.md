---
title: "Feature Provider Registry"
phase: 07
status: canonical
---
# Feature Provider Registry

The registry is static for a runtime generation. Nodes are registered before startup, validated, compiled and then treated as immutable. Runtime discovery and dynamic imports are prohibited in the fast path.

## Invariants

- MQL5 owns runtime truth.
- Identical ordered inputs produce identical outputs.
- Known time is explicit and causal.
- Memory and work are bounded.
- No previous strategy is integrated.
- No execution authority exists.
