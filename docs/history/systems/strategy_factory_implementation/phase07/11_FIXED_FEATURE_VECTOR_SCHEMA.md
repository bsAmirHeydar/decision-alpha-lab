---
title: "Fixed Feature Vector Schema"
phase: 07
status: canonical
---
# Fixed Feature Vector Schema

Models and candidate rankers require a fixed numeric order. The vector schema declares each feature, expected type, missing policy and default. Strings are excluded from numeric vectors. Schema mismatch fails startup or inference.

## Invariants

- MQL5 owns runtime truth.
- Identical ordered inputs produce identical outputs.
- Known time is explicit and causal.
- Memory and work are bounded.
- No previous strategy is integrated.
- No execution authority exists.
