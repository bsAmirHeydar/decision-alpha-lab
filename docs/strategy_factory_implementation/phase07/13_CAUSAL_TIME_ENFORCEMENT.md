---
title: "Causal Time Enforcement"
phase: 07
status: canonical
---
# Causal Time Enforcement

Every feature carries known_time. The context engine validates known_time <= snapshot_time. Event time, known time and confirmation time remain distinct. Future-derived features are rejected before they can enter research or execution.

## Invariants

- MQL5 owns runtime truth.
- Identical ordered inputs produce identical outputs.
- Known time is explicit and causal.
- Memory and work are bounded.
- No previous strategy is integrated.
- No execution authority exists.
