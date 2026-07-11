---
title: "Immutable Feature Snapshot"
phase: 07
status: canonical
---
# Immutable Feature Snapshot

The output snapshot uses the Phase 01 canonical contract. Features are added in topological order, duplicate IDs are impossible and snapshot identity is deterministic. Once emitted, the snapshot is append-only evidence.

## Invariants

- MQL5 owns runtime truth.
- Identical ordered inputs produce identical outputs.
- Known time is explicit and causal.
- Memory and work are bounded.
- No previous strategy is integrated.
- No execution authority exists.
