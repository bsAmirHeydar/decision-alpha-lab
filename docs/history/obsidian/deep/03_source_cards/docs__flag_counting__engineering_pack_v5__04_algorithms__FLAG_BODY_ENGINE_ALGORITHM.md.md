
---
type: source_card
source_path: "docs/flag_counting/engineering_pack_v5/04_algorithms/FLAG_BODY_ENGINE_ALGORITHM.md"
source_ext: ".md"
source_size: 2240
empty: false
generated_at: 2026-07-06
concepts: ["Decision Node", "Flag Counting", "UI / React"]
entities: []
---

# Source Card — FLAG_BODY_ENGINE_ALGORITHM.md

## Source

[[docs/flag_counting/engineering_pack_v5/04_algorithms/FLAG_BODY_ENGINE_ALGORITHM|docs/flag_counting/engineering_pack_v5/04_algorithms/FLAG_BODY_ENGINE_ALGORITHM.md]]

## Summary

Build two-leg body candidates from owned context. Do not assign F-level confirmation here. This module only builds body geometry. Initialize: Process nodes chronologically. Track highest high after origin. When a low correction appears after at least one high: If low correction passes origin: Update waist while deeper lows appear: If low passes origin: If high passes leg1: Symmetric. Track lowest low after origin. When a high correction appears after at least one low: If high correction passes origin: Update waist while higher highs appear: If high passes origin: If low passes leg1: For F1 before valid post-body 1/2 exists: Bullish: Bearish: For F2/F3 candidates that need size/qualification: A completed body candidate emits: Never create body from arbitrary 4-node window unless the origin came from an owned phase context.

## Concepts

[[docs/obsidian_deep/02_concepts/Decision_Node|Decision Node]], [[docs/obsidian_deep/02_concepts/Flag_Counting|Flag Counting]], [[docs/obsidian_deep/02_concepts/UI____React|UI / React]]

## Entities

—

## Headings

- Flag Body Engine Algorithm
  - Purpose
  - Inputs
  - Bullish Body Builder
    - SEEK_LEG1
    - SEEK_LEG2
  - Bearish Body Builder
    - SEEK_LEG1
    - SEEK_LEG2
  - Leg2 Extension
  - Output
  - Main Failure Guard

## Related Source Documents

- [[docs/flag_counting/engineering_pack_v5/04_algorithms/DEDUP_AUDIT_ALGORITHM|DEDUP_AUDIT_ALGORITHM.md]] — score `7`
- [[docs/flag_counting/engineering_pack_v5/04_algorithms/F1_F2_F3_ALGORITHMS|F1_F2_F3_ALGORITHMS.md]] — score `7`
- [[docs/flag_counting/engineering_pack_v5/04_algorithms/HOOK_BRANCH_ENGINE_ALGORITHM|HOOK_BRANCH_ENGINE_ALGORITHM.md]] — score `7`
- [[docs/flag_counting/engineering_pack_v5/04_algorithms/MODULE_ARCHITECTURE|MODULE_ARCHITECTURE.md]] — score `7`
- [[docs/flag_counting/engineering_pack_v5/04_algorithms/NODE_ENGINE_ALGORITHM|NODE_ENGINE_ALGORITHM.md]] — score `7`
- [[docs/flag_counting/engineering_pack_v5/04_algorithms/PSEUDOCODE_REFERENCE|PSEUDOCODE_REFERENCE.md]] — score `7`
- [[docs/flag_counting/engineering_pack_v5/04_algorithms/README|README.md]] — score `7`
- [[docs/ai_execution/AI_ALGORITHM_LAYER_MAP_FOR_EXTREME_ENGINE_FA|AI_ALGORITHM_LAYER_MAP_FOR_EXTREME_ENGINE_FA.md]] — score `6`
- [[docs/ai_execution/AI_NATIVE_EXECUTION_ROADMAP_FA|AI_NATIVE_EXECUTION_ROADMAP_FA.md]] — score `6`
- [[docs/ai_execution/AMIR_STRUCTURAL_EXPERIENCE_MAP_FA|AMIR_STRUCTURAL_EXPERIENCE_MAP_FA.md]] — score `6`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
