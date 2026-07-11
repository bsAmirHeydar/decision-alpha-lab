---
title: "Schema Registry"
phase: 07
status: canonical
---
# Schema Registry

Phase 07 adds schemas for feature descriptors, graph manifests, context frames, vector schemas and fixed vectors. Schema versions are explicit and runtime generations pin hashes.

## Invariants

- MQL5 owns runtime truth.
- Identical ordered inputs produce identical outputs.
- Known time is explicit and causal.
- Memory and work are bounded.
- No previous strategy is integrated.
- No execution authority exists.
