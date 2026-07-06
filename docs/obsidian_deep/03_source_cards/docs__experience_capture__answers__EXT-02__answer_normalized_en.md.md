
---
type: source_card
source_path: "docs/experience_capture/answers/EXT-02/answer_normalized_en.md"
source_ext: ".md"
source_size: 4481
empty: false
generated_at: 2026-07-06
concepts: ["Convexity / Optionality", "Decision Node", "Execution / Risk", "Flag Counting", "Hook", "Market Anatomy", "Rally", "UI / React", "Zone / RTV"]
entities: []
---

# Source Card — answer_normalized_en.md

## Source

[[docs/experience_capture/answers/EXT-02/answer_normalized_en|docs/experience_capture/answers/EXT-02/answer_normalized_en.md]]

## Summary

Extreme does not generate the directional thesis. Extreme does not generate the scenario. Extreme is the lower-timeframe entry mechanism used after the higher-level NDS analysis has already defined: The anchor node for Extreme belongs to NDS node logic, not RTV. RTV must not be used as a source for `extreme_anchor_node_id`. RTV is explicitly outside NDS. Therefore: This reinforces BASE-04 and BASE-06: The NDS process is layered. The system first analyzes the market using: The system then decides: Only after direction and region are defined does the system move to a lower timeframe and search for an Extreme entry. This means Extreme is not the whole strategy. Extreme is an execution/refinement entry family. The anchor node should come from NDS-native node logic. The answer does not yet define one exact engine name, but it clearly excludes RTV and implies that the anchor node must be produ

## Concepts

[[docs/obsidian_deep/02_concepts/Convexity____Optionality|Convexity / Optionality]], [[docs/obsidian_deep/02_concepts/Decision_Node|Decision Node]], [[docs/obsidian_deep/02_concepts/Execution____Risk|Execution / Risk]], [[docs/obsidian_deep/02_concepts/Flag_Counting|Flag Counting]], [[docs/obsidian_deep/02_concepts/Hook|Hook]], [[docs/obsidian_deep/02_concepts/Market_Anatomy|Market Anatomy]], [[docs/obsidian_deep/02_concepts/Rally|Rally]], [[docs/obsidian_deep/02_concepts/UI____React|UI / React]], [[docs/obsidian_deep/02_concepts/Zone____RTV|Zone / RTV]]

## Entities

—

## Headings

- EXT-02 — Normalized Interpretation
  - Core Claim
  - RTV Is Excluded
  - Extreme Is an Entry Mechanism, Not the Scenario Engine
    - Layer 1 — Multi-layer NDS analysis
    - Layer 2 — Direction and region decision
    - Layer 3 — Lower-timeframe entry refinement
  - Anchor Node Source
  - L2 Default Logic
  - Flexibility Requirement
  - Relationship Between Direction, Region, and Extreme
  - AI Relevance

## Related Source Documents

- [[docs/ai_execution/AI_NATIVE_EXECUTION_ROADMAP_FA|AI_NATIVE_EXECUTION_ROADMAP_FA.md]] — score `18`
- [[docs/experience_capture/answers/DST-R03/answer_normalized_en|answer_normalized_en.md]] — score `18`
- [[docs/experience_capture/answers/NDS-R01/answer_normalized_en|answer_normalized_en.md]] — score `18`
- [[lab/03_experiments/EXP_flag_counting/docs/README_FLAG_OPTIONALITY_XY_STATE_PHILOSOPHY|README_FLAG_OPTIONALITY_XY_STATE_PHILOSOPHY.md]] — score `18`
- [[lab/03_experiments/EXP_flag_counting/docs/README_FLAG_REVERSE_EXTREME_FRACTAL_ENTRY_PHILOSOPHY|README_FLAG_REVERSE_EXTREME_FRACTAL_ENTRY_PHILOSOPHY.md]] — score `18`
- [[docs/ai_execution/AI_ALGORITHM_LAYER_MAP_FOR_EXTREME_ENGINE_FA|AI_ALGORITHM_LAYER_MAP_FOR_EXTREME_ENGINE_FA.md]] — score `16`
- [[docs/ai_execution/AMIR_STRUCTURAL_EXPERIENCE_MAP_FA|AMIR_STRUCTURAL_EXPERIENCE_MAP_FA.md]] — score `16`
- [[docs/experience_capture/answers/EXT-01/answer_normalized_en|answer_normalized_en.md]] — score `16`
- [[docs/experience_capture/answers/NDS-R01/question_en|question_en.md]] — score `16`
- [[docs/experience_capture/answers/SCN-R01/answer_normalized_en|answer_normalized_en.md]] — score `16`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
