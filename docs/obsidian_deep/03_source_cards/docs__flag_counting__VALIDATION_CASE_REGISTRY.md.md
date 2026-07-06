
---
type: source_card
source_path: "docs/flag_counting/VALIDATION_CASE_REGISTRY.md"
source_ext: ".md"
source_size: 4892
empty: false
generated_at: 2026-07-06
concepts: ["AI Agent Layer", "Decision Node", "Execution / Risk", "Flag Counting", "Hook", "MQL Native", "Python Brain", "UI / React", "Validation / Audit", "Zone / RTV"]
entities: []
---

# Source Card — VALIDATION_CASE_REGISTRY.md

## Source

[[docs/flag_counting/VALIDATION_CASE_REGISTRY|docs/flag_counting/VALIDATION_CASE_REGISTRY.md]]

## Summary

Status: active validation registry for Phoenix. Source of truth: `docs/flag_counting/FLAG_COUNTING_CURRENT_CANON.md`. This registry turns validation from visual opinion into deterministic baselines. Broker-specific symbol names and exact historical availability differ. Therefore a case has two states: Do not invent expected counts. The first accepted run for a pinned broker/range creates the baseline; later patches compare against it. Recommended output location: Recommended files per case: Purpose: Required status before Level 02 freeze: `baselined`. Purpose: Required status before Level 04 freeze: `baselined`. Purpose: Required status before Level 05 freeze: `baselined`. Purpose: Required status before Level 07 freeze: `baselined`. Purpose: Required status before Level 08 freeze: `baselined`. Purpose: Required status before Level 09 freeze: `baselined`. Purpose: Required status before

## Concepts

[[docs/obsidian_deep/02_concepts/AI_Agent_Layer|AI Agent Layer]], [[docs/obsidian_deep/02_concepts/Decision_Node|Decision Node]], [[docs/obsidian_deep/02_concepts/Execution____Risk|Execution / Risk]], [[docs/obsidian_deep/02_concepts/Flag_Counting|Flag Counting]], [[docs/obsidian_deep/02_concepts/Hook|Hook]], [[docs/obsidian_deep/02_concepts/MQL_Native|MQL Native]], [[docs/obsidian_deep/02_concepts/Python_Brain|Python Brain]], [[docs/obsidian_deep/02_concepts/UI____React|UI / React]], [[docs/obsidian_deep/02_concepts/Validation____Audit|Validation / Audit]], [[docs/obsidian_deep/02_concepts/Zone____RTV|Zone / RTV]]

## Entities

—

## Headings

- Flag Counting Validation Case Registry
  - Purpose
  - Baseline file naming
  - Required fields per baseline
  - Mandatory baseline cases
    - FC-GC-001 — Node plateau and equality
    - FC-GC-002 — Hook/ND branch size
    - FC-GC-003 — Bullish and bearish flag body
    - FC-GC-004 — F1 internal confirmation
    - FC-GC-005 — F2 backfill and size qualification
    - FC-GC-006 — F3 OR completion and lock
    - FC-GC-007 — Sequence ownership and duplicate hiding

## Related Source Documents

- [[docs/flag_counting/FLAG_COUNTING_CURRENT_CANON|FLAG_COUNTING_CURRENT_CANON.md]] — score `29`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_CLEAN_ISOLATED_STATE_GATE|FLAG_COUNTING_LEVEL_19_CLEAN_ISOLATED_STATE_GATE.md]] — score `21`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19Z_COMPLETE_OBSERVATION_SUITE|FLAG_COUNTING_LEVEL_19Z_COMPLETE_OBSERVATION_SUITE.md]] — score `21`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_20_ENTRY_BRIDGE_XY_ANCHOR_JOIN|FLAG_COUNTING_LEVEL_20_ENTRY_BRIDGE_XY_ANCHOR_JOIN.md]] — score `21`
- [[docs/flag_counting/README|README.md]] — score `21`
- [[docs/ai_execution/AI_NATIVE_EXECUTION_ROADMAP_FA|AI_NATIVE_EXECUTION_ROADMAP_FA.md]] — score `20`
- [[docs/flag_counting/implementation_ladder_v1/15_MODULE_INTERFACE_CONTRACTS|15_MODULE_INTERFACE_CONTRACTS.md]] — score `20`
- [[docs/flag_counting/implementation_ladder_v1/16_IMPLEMENTATION_ORDER_AND_ACCEPTANCE_MATRIX|16_IMPLEMENTATION_ORDER_AND_ACCEPTANCE_MATRIX.md]] — score `20`
- [[docs/nds_hook_architecture/13_phase06_xy_closure_quality_score_implementation|13_phase06_xy_closure_quality_score_implementation.md]] — score `20`
- [[mql5/Include/FlagCountingPhoenix/README_FlagCountingPhoenix|README_FlagCountingPhoenix.md]] — score `20`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
