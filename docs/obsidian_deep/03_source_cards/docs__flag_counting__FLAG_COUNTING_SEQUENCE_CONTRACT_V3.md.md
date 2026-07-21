
---
type: source_card
source_path: "docs/flag_counting/FLAG_COUNTING_SEQUENCE_CONTRACT_V3.md"
source_ext: ".md"
source_size: 27376
empty: false
generated_at: 2026-07-06
concepts: ["AI Agent Layer", "Convexity / Optionality", "Decision Node", "Execution / Risk", "Flag Counting", "Hook", "Path Smoothness", "Rally", "UI / React", "Validation / Audit", "Zone / RTV"]
entities: []
---

# Source Card — FLAG_COUNTING_SEQUENCE_CONTRACT_V3.md

## Source

[[docs/flag_counting/FLAG_COUNTING_SEQUENCE_CONTRACT_V3|docs/flag_counting/FLAG_COUNTING_SEQUENCE_CONTRACT_V3.md]]

## Summary

<!-- CURRENT CANON NOTICE This file is retained as historical/context documentation. For current Phoenix implementation decisions, use: docs/flag_counting/FLAG_COUNTING_CURRENT_CANON.md If this file conflicts with the current canon, the current canon wins. --> Status: implementation contract, English canonical version. This document replaces the previous loose flag-counting descriptions. It defines the deterministic sequence logic for `F1 -> F2 -> F3`, ND/Hook detection, adaptive node compression, invalidation, confirmation, rendering… The goal is not to scan arbitrary four-node windows and draw them. The goal is to preserve every raw high/low observation, build scale-aware views from those observations, and assign every meaningful movement to a cohere… The entire Flag Counting model works on swing high and swing low geometry. The following values are not part of F or ND definitions: can

## Concepts

[[docs/obsidian_deep/02_concepts/AI_Agent_Layer|AI Agent Layer]], [[docs/obsidian_deep/02_concepts/Convexity____Optionality|Convexity / Optionality]], [[docs/obsidian_deep/02_concepts/Decision_Node|Decision Node]], [[docs/obsidian_deep/02_concepts/Execution____Risk|Execution / Risk]], [[docs/obsidian_deep/02_concepts/Flag_Counting|Flag Counting]], [[docs/obsidian_deep/02_concepts/Hook|Hook]], [[docs/obsidian_deep/02_concepts/Path_Smoothness|Path Smoothness]], [[docs/obsidian_deep/02_concepts/Rally|Rally]], [[docs/obsidian_deep/02_concepts/UI____React|UI / React]], [[docs/obsidian_deep/02_concepts/Validation____Audit|Validation / Audit]], [[docs/obsidian_deep/02_concepts/Zone____RTV|Zone / RTV]]

## Entities

—

## Headings

- Flag Counting Sequence Contract V3
  - 1. Core Philosophy
    - 1.1 The engine is high/low based
    - 1.2 All raw highs and lows are preserved
    - 1.3 A flag is always a two-leg body
    - 1.4 The sequence is ordered
    - 1.5 No idle movement
  - 2. Node Model
    - 2.1 Raw node
    - 2.2 Scaled node view
    - 2.3 Adaptive compression
    - 2.4 The start node of an ND cycle

## Related Source Documents

- [[docs/flag_counting/FLAG_COUNTING_CURRENT_CANON|FLAG_COUNTING_CURRENT_CANON.md]] — score `27`
- [[docs/ai_execution/AI_NATIVE_EXECUTION_ROADMAP_FA|AI_NATIVE_EXECUTION_ROADMAP_FA.md]] — score `22`
- [[docs/releases/legacy_migration/general/0b9f38e7e2fd_README_FLAG_OPTIONALITY_XY_STATE_PHILOSOPHY|README_FLAG_OPTIONALITY_XY_STATE_PHILOSOPHY.md]] — score `22`
- [[docs/flag_counting/FLAG_COUNTING_SEQUENCE_CONTRACT_V2|FLAG_COUNTING_SEQUENCE_CONTRACT_V2.md]] — score `21`
- [[docs/flag_counting/FLAG_COUNTING_SEQUENCE_CONTRACT_V4|FLAG_COUNTING_SEQUENCE_CONTRACT_V4.md]] — score `21`
- [[docs/ai_execution/AI_ALGORITHM_LAYER_MAP_FOR_EXTREME_ENGINE_FA|AI_ALGORITHM_LAYER_MAP_FOR_EXTREME_ENGINE_FA.md]] — score `20`
- [[docs/ai_execution/AMIR_STRUCTURAL_EXPERIENCE_MAP_FA|AMIR_STRUCTURAL_EXPERIENCE_MAP_FA.md]] — score `20`
- [[docs/experience_capture/answers/EXT-01/answer_normalized_en|answer_normalized_en.md]] — score `20`
- [[docs/experience_capture/answers/NDS-R01/answer_normalized_en|answer_normalized_en.md]] — score `20`
- [[docs/mql_native/H0007_FLAG_COUNTING_F1_START_STRUCTURE|H0007_FLAG_COUNTING_F1_START_STRUCTURE.md]] — score `20`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
