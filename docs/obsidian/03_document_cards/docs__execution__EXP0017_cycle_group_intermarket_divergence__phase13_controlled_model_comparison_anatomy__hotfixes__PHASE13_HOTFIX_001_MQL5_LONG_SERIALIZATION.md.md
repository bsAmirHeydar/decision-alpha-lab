---
type: document-card
project: EXP0017
phase: 13
status: implemented
source: docs/execution/EXP0017_cycle_group_intermarket_divergence/phase13_controlled_model_comparison_anatomy/hotfixes/PHASE13_HOTFIX_001_MQL5_LONG_SERIALIZATION.md
---

# Phase 13 Hotfix001 — MQL5 Long Serialization

Fixes the unsupported `LongToString` call in the Phase 13 MQL5 inventory writer by using `IntegerToString` for the long `size_bytes` field.

[[MQL5_Long_Values_Use_IntegerToString]]
