
---
type: source_card
source_path: "docs/flag_counting/engineering_pack_v5/04_algorithms/SEQUENCE_ENGINE_ALGORITHM.md"
source_ext: ".md"
source_size: 2407
empty: false
generated_at: 2026-07-06
concepts: ["Flag Counting", "Hook", "UI / React", "Validation / Audit"]
entities: []
---

# Source Card — SEQUENCE_ENGINE_ALGORITHM.md

## Source

[[docs/flag_counting/engineering_pack_v5/04_algorithms/SEQUENCE_ENGINE_ALGORITHM|docs/flag_counting/engineering_pack_v5/04_algorithms/SEQUENCE_ENGINE_ALGORITHM.md]]

## Summary

Own the F1 -> F2 -> F3 chain. Prevent sliding-window behavior. A new F1 may start only from: ND/Hook terminal extreme; opposite sequence end; confirmed opposite F1 that locks previous F3; explicitly emitted phase boundary. If there is already an active F1/F2 in same direction/context, do not start another same-direction F1 unless phase boundary rules permit it. Receive phase boundary. Start F1 origin from boundary extreme. Build F1 body. Display only after body complete. Track post-F1 context. If Waist passed before confirmation, reject F1 candidate. If valid internal 1/2 exists and Leg2 is passed again, confirm F1. Authorize F2 and backfill origin from post-F1 context. After F1 confirmation, use stored post-F1 deepest adverse correction as F2 origin. Build F2 body. Display seed/leg development for debugging. Wait for size >= F1 size; allow extension. Track post-F2 context. If F2 origin

## Concepts

[[docs/obsidian_deep/02_concepts/Flag_Counting|Flag Counting]], [[docs/obsidian_deep/02_concepts/Hook|Hook]], [[docs/obsidian_deep/02_concepts/UI____React|UI / React]], [[docs/obsidian_deep/02_concepts/Validation____Audit|Validation / Audit]]

## Entities

—

## Headings

- Sequence Engine Algorithm
  - Purpose
  - Chain States
  - Phase Boundary Detection
  - F1 Flow
  - F2 Flow
  - F3 Flow
  - Parent/Child Death Rule
  - Active Opposite Direction
  - Chain Emissions

## Related Source Documents

- [[docs/flag_counting/engineering_pack_v5/04_algorithms/DEDUP_AUDIT_ALGORITHM|DEDUP_AUDIT_ALGORITHM.md]] — score `9`
- [[docs/flag_counting/engineering_pack_v5/04_algorithms/F1_F2_F3_ALGORITHMS|F1_F2_F3_ALGORITHMS.md]] — score `9`
- [[docs/flag_counting/engineering_pack_v5/04_algorithms/MODULE_ARCHITECTURE|MODULE_ARCHITECTURE.md]] — score `9`
- [[docs/flag_counting/engineering_pack_v5/04_algorithms/NODE_ENGINE_ALGORITHM|NODE_ENGINE_ALGORITHM.md]] — score `9`
- [[docs/flag_counting/engineering_pack_v5/04_algorithms/README|README.md]] — score `9`
- [[docs/ai_execution/AI_ALGORITHM_LAYER_MAP_FOR_EXTREME_ENGINE_FA|AI_ALGORITHM_LAYER_MAP_FOR_EXTREME_ENGINE_FA.md]] — score `8`
- [[docs/ai_execution/AI_NATIVE_EXECUTION_ROADMAP_FA|AI_NATIVE_EXECUTION_ROADMAP_FA.md]] — score `8`
- [[docs/ai_execution/AMIR_STRUCTURAL_EXPERIENCE_MAP_FA|AMIR_STRUCTURAL_EXPERIENCE_MAP_FA.md]] — score `8`
- [[docs/ai_execution/EXPERIENCE_CAPTURE_LOG_TEMPLATE_FA|EXPERIENCE_CAPTURE_LOG_TEMPLATE_FA.md]] — score `8`
- [[docs/debug/MARKET_LANGUAGE/README|README.md]] — score `8`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
