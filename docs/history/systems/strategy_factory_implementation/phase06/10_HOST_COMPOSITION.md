---
title: "Host Composition"
phase: 06
status: canonical
---
# Host Composition

SF06_StrategyHost composes market services, the static registry, startup validator, generation compiler, result sink, runtime, metadata feature provider, and no-send boundary. The host contains no anatomy logic and can be replaced without changing the plugin.

## Invariants

- MQL5 owns event truth.
- All time fields are causal and explicit.
- Output is deterministic for an identical ordered input stream.
- Queue, memory, and processing work are bounded.
- No previous strategy is integrated in this phase.
- No execution authority exists.

## Acceptance Evidence

Evidence is stored in the Phase 06 QA report, test suite, schema registry, fixture manifest, local compile logs, and the generated JSONL ledger.
