---
title: "Feature Descriptor Contract"
phase: 07
status: canonical
---
# Feature Descriptor Contract

Every output has one owner, one version, one explicit type, one update scope, one required/optional policy, one freshness budget and a bounded dependency list. Duplicate ownership, implicit dependencies and self-dependencies are rejected at startup.

## Invariants

- MQL5 owns runtime truth.
- Identical ordered inputs produce identical outputs.
- Known time is explicit and causal.
- Memory and work are bounded.
- No previous strategy is integrated.
- No execution authority exists.
