
---
type: source_card
source_path: "docs/flag_counting/implementation_ladder_v1/15_MODULE_INTERFACE_CONTRACTS.md"
source_ext: ".md"
source_size: 25943
empty: false
generated_at: 2026-07-06
concepts: ["AI Agent Layer", "Convexity / Optionality", "Decision Node", "Execution / Risk", "Flag Counting", "Hook", "MQL Native", "Python Brain", "UI / React", "Validation / Audit", "Zone / RTV"]
entities: []
---

# Source Card — 15_MODULE_INTERFACE_CONTRACTS.md

## Source

[[docs/flag_counting/implementation_ladder_v1/15_MODULE_INTERFACE_CONTRACTS|docs/flag_counting/implementation_ladder_v1/15_MODULE_INTERFACE_CONTRACTS.md]]

## Summary

This document is part of the implementation ladder for the Phoenix Flag Counting engine. Global non-negotiables: All structural decisions use candle `high` and `low` only. `open`, `close`, candle body, candle color, volume, and indicators are not structural inputs. Equality is not a break. A level is broken only by a strict pass beyond it. The renderer is non-authoritative. It may only draw logical objects emitted by engines. Main-chart rendering and audit rendering are separate products. Every layer must expose enough audit fields to prove why an object exists. A higher layer may never silently repair a lower-layer defect. This document defines Phoenix module boundaries. Each module owns one layer of truth. No module may silently redo another module's work. The active interface source is aligned with the current Phoenix shared types in: Do not require older placeholder structs unless th

## Concepts

[[docs/obsidian_deep/02_concepts/AI_Agent_Layer|AI Agent Layer]], [[docs/obsidian_deep/02_concepts/Convexity____Optionality|Convexity / Optionality]], [[docs/obsidian_deep/02_concepts/Decision_Node|Decision Node]], [[docs/obsidian_deep/02_concepts/Execution____Risk|Execution / Risk]], [[docs/obsidian_deep/02_concepts/Flag_Counting|Flag Counting]], [[docs/obsidian_deep/02_concepts/Hook|Hook]], [[docs/obsidian_deep/02_concepts/MQL_Native|MQL Native]], [[docs/obsidian_deep/02_concepts/Python_Brain|Python Brain]], [[docs/obsidian_deep/02_concepts/UI____React|UI / React]], [[docs/obsidian_deep/02_concepts/Validation____Audit|Validation / Audit]], [[docs/obsidian_deep/02_concepts/Zone____RTV|Zone / RTV]]

## Entities

—

## Headings

- Phoenix Flag Counting Implementation Ladder V1
- Module Interface Contracts
  - Purpose
  - Active shared data structures
  - FP_Types.mqh
  - Level 02 node modules
  - Level 03 identity modules
  - Level 04 Hook/ND modules
  - FP_FlagBodyRules.mqh
  - FP_FlagBodyAudit.mqh
  - FP_FlagBodyEngine.mqh
  - FP_InternalCountRules.mqh / FP_InternalCountAudit.mqh / FP_InternalCountEngine.mqh

## Related Source Documents

- [[docs/flag_counting/implementation_ladder_v1/16_IMPLEMENTATION_ORDER_AND_ACCEPTANCE_MATRIX|16_IMPLEMENTATION_ORDER_AND_ACCEPTANCE_MATRIX.md]] — score `23`
- [[docs/ai_execution/AI_NATIVE_EXECUTION_ROADMAP_FA|AI_NATIVE_EXECUTION_ROADMAP_FA.md]] — score `22`
- [[docs/flag_counting/FLAG_COUNTING_CURRENT_CANON|FLAG_COUNTING_CURRENT_CANON.md]] — score `22`
- [[docs/flag_counting/README|README.md]] — score `22`
- [[mql5/Include/FlagCountingPhoenix/README_FlagCountingPhoenix|README_FlagCountingPhoenix.md]] — score `22`
- [[docs/flag_counting/implementation_ladder_v1/README|README.md]] — score `21`
- [[docs/ai_execution/AI_ALGORITHM_LAYER_MAP_FOR_EXTREME_ENGINE_FA|AI_ALGORITHM_LAYER_MAP_FOR_EXTREME_ENGINE_FA.md]] — score `20`
- [[docs/ai_execution/AMIR_STRUCTURAL_EXPERIENCE_MAP_FA|AMIR_STRUCTURAL_EXPERIENCE_MAP_FA.md]] — score `20`
- [[docs/experience_capture/answers/NDS-R01/answer_normalized_en|answer_normalized_en.md]] — score `20`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_CLEAN_ISOLATED_STATE_GATE|FLAG_COUNTING_LEVEL_19_CLEAN_ISOLATED_STATE_GATE.md]] — score `20`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
