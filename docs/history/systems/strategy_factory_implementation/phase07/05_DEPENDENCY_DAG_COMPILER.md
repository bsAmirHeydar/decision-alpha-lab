---
title: "Dependency DAG Compiler"
phase: 07
status: canonical
---
# Dependency DAG Compiler

The compiler validates every dependency, rejects cycles and produces a deterministic topological order. Lexicographic tie-breaking makes the graph hash and snapshot ordering reproducible across identical builds.

## Invariants

- MQL5 owns runtime truth.
- Identical ordered inputs produce identical outputs.
- Known time is explicit and causal.
- Memory and work are bounded.
- No previous strategy is integrated.
- No execution authority exists.
