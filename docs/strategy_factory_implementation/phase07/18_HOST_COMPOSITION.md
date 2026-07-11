---
title: "Host Composition"
phase: 07
status: canonical
---
# Host Composition

SF07_StrategyHost composes the Phase 03 market bundle, Phase 06 reference anatomy, Phase 05 generation, Phase 07 context engine, JSONL sink and no-send boundary. The host contains no legacy strategy logic.

## Invariants

- MQL5 owns runtime truth.
- Identical ordered inputs produce identical outputs.
- Known time is explicit and causal.
- Memory and work are bounded.
- No previous strategy is integrated.
- No execution authority exists.
