---
title: "Phase 08 Handoff"
phase: 07
status: canonical
---
# Phase 08 Handoff

Phase 08 builds the candidate policy registry and deterministic candidate matrix. It consumes AnatomyEvent, FeatureSnapshot, ContextFrame and FixedFeatureVector. Candidate creation must not modify context truth.

## Invariants

- MQL5 owns runtime truth.
- Identical ordered inputs produce identical outputs.
- Known time is explicit and causal.
- Memory and work are bounded.
- No previous strategy is integrated.
- No execution authority exists.
