
---
type: source_card
source_path: "docs/nds_hook_architecture/33_phase23_grouped_semicircle_compile_fix.md"
source_ext: ".md"
source_size: 719
empty: false
generated_at: 2026-07-06
concepts: ["Hook", "MQL Native"]
entities: []
---

# Source Card — 33_phase23_grouped_semicircle_compile_fix.md

## Source

[[docs/nds_hook_architecture/33_phase23_grouped_semicircle_compile_fix|docs/nds_hook_architecture/33_phase23_grouped_semicircle_compile_fix.md]]

## Summary

MetaEditor reported that `FP_HookP02CreateArcBetweenPoints` was undeclared and also rejected local reference variables such as: Adds the missing `FP_HookP02CreateArcBetweenPoints` helper before `FP_HookP02CreateCycleArc`. Replaces invalid local reference aliases with value copies: No visual semantics changed. The grouped Hook semicircle remains: one arc per Hook-origin group start at origin end at directional group extreme dim gray envelope arc

## Concepts

[[docs/obsidian_deep/02_concepts/Hook|Hook]], [[docs/obsidian_deep/02_concepts/MQL_Native|MQL Native]]

## Entities

—

## Headings

- Phase 23 Compile Fix — Grouped Semicircle Visual Helper
  - Issue
  - Fix
  - Behavior

## Related Source Documents

- [[lab/03_experiments/EXP0002_mql_native_m0001/report|report.md]] — score `10`
- [[lab/03_experiments/EXP0003_mql_native_m0002/report|report.md]] — score `10`
- [[lab/03_experiments/EXP0004_mql_native_m0004/report|report.md]] — score `10`
- [[lab/05_validation/VAL_M0001_MQL_NATIVE/report|report.md]] — score `10`
- [[lab/03_experiments/EXP0000_sample/report|report.md]] — score `8`
- [[lab/03_experiments/EXP0001_structural_highs_lows_importance/report|report.md]] — score `8`
- [[lab/05_validation/VAL001/report|report.md]] — score `8`
- [[docs/nds_hook_architecture/07_mql5_integration_contract|07_mql5_integration_contract.md]] — score `5`
- [[docs/nds_hook_architecture/08_phase01_node_source_adapter_implementation|08_phase01_node_source_adapter_implementation.md]] — score `5`
- [[docs/nds_hook_architecture/09_phase02_cyclehook_sequence_builder_implementation|09_phase02_cyclehook_sequence_builder_implementation.md]] — score `5`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
