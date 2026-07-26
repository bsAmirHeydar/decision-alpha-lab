---
title: "Phase Charter"
phase: 07
status: canonical
---
# Phase Charter

Build the shared MQL5 context engine before any legacy anatomy is integrated. The phase owns feature descriptors, graph compilation, context state, immutable snapshots, fixed vectors, telemetry, fixtures and failure semantics. Candidate logic, model inference, risk and execution remain outside scope.

## Invariants

- MQL5 owns runtime truth.
- Identical ordered inputs produce identical outputs.
- Known time is explicit and causal.
- Memory and work are bounded.
- No previous strategy is integrated.
- No execution authority exists.
