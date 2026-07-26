
---
type: source_card
source_path: "docs/experience_capture/questions/remaining_v3_split/DATA-R01/question_en.md"
source_ext: ".md"
source_size: 1108
empty: false
generated_at: 2026-07-06
concepts: ["Convexity / Optionality", "Decision Node", "Execution / Risk", "Hook", "Python Brain", "UI / React", "Zone / RTV"]
entities: []
---

# Source Card — question_en.md

## Source

[[docs/experience_capture/questions/remaining_v3_split/DATA-R01/question_en|docs/experience_capture/questions/remaining_v3_split/DATA-R01/question_en.md]]

## Summary

چون rule engine، AI، backtest، shadow، paper و execution باید همه از یک زبان مشترک استفاده کنند. این زبان همان state packet استاندارد NDS است. در هر لحظه، Node state باید چه فیلدهایی داشته باشد؟ CycleHook state شامل چه چیزهایی باشد؟ Sequence state، X/Y closure و Hook type چطور ذخیره شوند؟ Context/position چطور وارد packet شود؟ Zone candidates چطور ثبت شوند؟ Scenario threads چطور ثبت شوند؟ Entry extremes و ExecutionIntentها چطور وصل شوند؟ Destinations و optionality چطور ذخیره شوند؟ Risk state و pending orders چطور وارد packet شوند؟ Parent-child fractal relations چطور استاندارد شوند؟ خیر. پاسخ متنی کافی است. `canonical_state_packet_v1.csv` `nds_state_schema_v1.csv` `state_packet_versioning_v1.csv`

## Concepts

[[docs/obsidian_deep/02_concepts/Convexity____Optionality|Convexity / Optionality]], [[docs/obsidian_deep/02_concepts/Decision_Node|Decision Node]], [[docs/obsidian_deep/02_concepts/Execution____Risk|Execution / Risk]], [[docs/obsidian_deep/02_concepts/Hook|Hook]], [[docs/obsidian_deep/02_concepts/Python_Brain|Python Brain]], [[docs/obsidian_deep/02_concepts/UI____React|UI / React]], [[docs/obsidian_deep/02_concepts/Zone____RTV|Zone / RTV]]

## Entities

—

## Headings

- DATA-R01 — Canonical State Packet v1
  - Purpose
  - Required Clarifications
  - Image Requirement
  - Expected Derived Outputs

## Related Source Documents

- [[docs/ai_execution/AI_ALGORITHM_LAYER_MAP_FOR_EXTREME_ENGINE_FA|AI_ALGORITHM_LAYER_MAP_FOR_EXTREME_ENGINE_FA.md]] — score `14`
- [[docs/ai_execution/AI_NATIVE_EXECUTION_ROADMAP_FA|AI_NATIVE_EXECUTION_ROADMAP_FA.md]] — score `14`
- [[docs/ai_execution/AMIR_STRUCTURAL_EXPERIENCE_MAP_FA|AMIR_STRUCTURAL_EXPERIENCE_MAP_FA.md]] — score `14`
- [[docs/ai_execution/EXTREME_L2_NODE_CYCLE_LIMIT_ENTRY_FA|EXTREME_L2_NODE_CYCLE_LIMIT_ENTRY_FA.md]] — score `14`
- [[docs/experience_capture/answers/ENT-R01/notes_en|notes_en.md]] — score `14`
- [[docs/experience_capture/answers/EXT-08/notes_en|notes_en.md]] — score `14`
- [[docs/experience_capture/questions/remaining_v2/by_code/DATA-R01|DATA-R01.md]] — score `14`
- [[docs/flag_counting/FLAG_COUNTING_CURRENT_CANON|FLAG_COUNTING_CURRENT_CANON.md]] — score `14`
- [[docs/flag_counting/implementation_ladder_v1/15_MODULE_INTERFACE_CONTRACTS|15_MODULE_INTERFACE_CONTRACTS.md]] — score `14`
- [[docs/flag_counting/implementation_ladder_v1/16_IMPLEMENTATION_ORDER_AND_ACCEPTANCE_MATRIX|16_IMPLEMENTATION_ORDER_AND_ACCEPTANCE_MATRIX.md]] — score `14`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
