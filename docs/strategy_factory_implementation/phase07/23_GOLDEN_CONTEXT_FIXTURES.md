---
title: "Golden Context Fixtures"
phase: 07
status: canonical
---
# Golden Context Fixtures

The reference event and feature graph form a golden context case. Approved expected feature order, graph hash, snapshot identity, frame identity and vector identity must be captured after local MQL5 compile and compared with Python.

## Invariants

- MQL5 owns runtime truth.
- Identical ordered inputs produce identical outputs.
- Known time is explicit and causal.
- Memory and work are bounded.
- No previous strategy is integrated.
- No execution authority exists.
