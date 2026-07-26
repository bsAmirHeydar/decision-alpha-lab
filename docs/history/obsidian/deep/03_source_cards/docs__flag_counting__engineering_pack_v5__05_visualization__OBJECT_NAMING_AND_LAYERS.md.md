
---
type: source_card
source_path: "docs/flag_counting/engineering_pack_v5/05_visualization/OBJECT_NAMING_AND_LAYERS.md"
source_ext: ".md"
source_size: 1478
empty: false
generated_at: 2026-07-06
concepts: ["AI Agent Layer", "Decision Node", "Execution / Risk", "Flag Counting", "Hook", "UI / React", "Validation / Audit"]
entities: []
---

# Source Card — OBJECT_NAMING_AND_LAYERS.md

## Source

[[docs/flag_counting/engineering_pack_v5/05_visualization/OBJECT_NAMING_AND_LAYERS|docs/flag_counting/engineering_pack_v5/05_visualization/OBJECT_NAMING_AND_LAYERS.md]]

## Summary

Chart objects must be deletable, refreshable, and traceable. Never create anonymous trendlines. Use one prefix for all Flag Counting objects: Recommended draw order: historical/locked F3 extension background arcs; ND/Hook arcs; flag body lines; origin markers; internal numbers; F labels; panel/status objects. Default: Avoid scale-based thickness by default. Use deterministic shade from sequence id: Use shade inside semantic color family. Renderer receives current render object ids. On refresh: build set of desired object names; update/create desired objects; delete old FCN_ objects not desired unless locked persistence requires retention; never delete non-FCN objects. Locked F3 objects should remain if: Default true. Every object should include a description string containing: This allows chart audit without reading logs every time.

## Concepts

[[docs/obsidian_deep/02_concepts/AI_Agent_Layer|AI Agent Layer]], [[docs/obsidian_deep/02_concepts/Decision_Node|Decision Node]], [[docs/obsidian_deep/02_concepts/Execution____Risk|Execution / Risk]], [[docs/obsidian_deep/02_concepts/Flag_Counting|Flag Counting]], [[docs/obsidian_deep/02_concepts/Hook|Hook]], [[docs/obsidian_deep/02_concepts/UI____React|UI / React]], [[docs/obsidian_deep/02_concepts/Validation____Audit|Validation / Audit]]

## Entities

—

## Headings

- Object Naming and Layers
  - Naming Goals
  - Prefix
  - Suggested Names
  - Layer Order
  - Width
  - Shades
  - Stale Object Cleanup
  - Locked Persistence
  - Tooltip / Description

## Related Source Documents

- [[docs/ai_execution/AI_ALGORITHM_LAYER_MAP_FOR_EXTREME_ENGINE_FA|AI_ALGORITHM_LAYER_MAP_FOR_EXTREME_ENGINE_FA.md]] — score `14`
- [[docs/ai_execution/AI_NATIVE_EXECUTION_ROADMAP_FA|AI_NATIVE_EXECUTION_ROADMAP_FA.md]] — score `14`
- [[docs/ai_execution/AMIR_STRUCTURAL_EXPERIENCE_MAP_FA|AMIR_STRUCTURAL_EXPERIENCE_MAP_FA.md]] — score `14`
- [[docs/debug/MARKET_LANGUAGE/README|README.md]] — score `14`
- [[docs/experience_capture/answers/BASE-01/answer_normalized_en|answer_normalized_en.md]] — score `14`
- [[docs/experience_capture/answers/BASE-04/answer_normalized_en|answer_normalized_en.md]] — score `14`
- [[docs/experience_capture/answers/BASE-06/answer_normalized_en|answer_normalized_en.md]] — score `14`
- [[docs/experience_capture/answers/EXT-01/answer_normalized_en|answer_normalized_en.md]] — score `14`
- [[docs/experience_capture/answers/NDS-R01/answer_normalized_en|answer_normalized_en.md]] — score `14`
- [[docs/experience_capture/answers/NDS-R01/notes_en|notes_en.md]] — score `14`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
