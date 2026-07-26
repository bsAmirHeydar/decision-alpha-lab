---
title: "Dirty Generation Propagation"
phase: 07
status: canonical
---
# Dirty Generation Propagation

Context state uses explicit generations and dirty flags. Event-scoped features are invalidated for every event. Future tick, bar and timer nodes can invalidate only affected descendants. Dirty propagation is dependency-driven rather than a full uncontrolled rebuild.

## Invariants

- MQL5 owns runtime truth.
- Identical ordered inputs produce identical outputs.
- Known time is explicit and causal.
- Memory and work are bounded.
- No previous strategy is integrated.
- No execution authority exists.
