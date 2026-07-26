---
title: "Performance and Memory Bounds"
phase: 07
status: canonical
---
# Performance and Memory Bounds

The registry, dependency count, context state and vector length are bounded. No file reads, JSON parsing, training, dataframe allocation or unbounded candidate enumeration occurs in the context build path. Telemetry records build microseconds.

## Invariants

- MQL5 owns runtime truth.
- Identical ordered inputs produce identical outputs.
- Known time is explicit and causal.
- Memory and work are bounded.
- No previous strategy is integrated.
- No execution authority exists.
