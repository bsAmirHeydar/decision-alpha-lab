---
title: "Feature Freshness and TTL"
phase: 07
status: canonical
---
# Feature Freshness and TTL

Feature freshness is explicit. max_age_milliseconds is part of the descriptor. A stale required feature cannot silently become current. Zero TTL means event-bound validity in the Phase 07 reference flow.

## Invariants

- MQL5 owns runtime truth.
- Identical ordered inputs produce identical outputs.
- Known time is explicit and causal.
- Memory and work are bounded.
- No previous strategy is integrated.
- No execution authority exists.
