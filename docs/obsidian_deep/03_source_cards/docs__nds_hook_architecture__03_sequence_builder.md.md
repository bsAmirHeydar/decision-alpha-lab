
---
type: source_card
source_path: "docs/nds_hook_architecture/03_sequence_builder.md"
source_ext: ".md"
source_size: 2081
empty: false
generated_at: 2026-07-06
concepts: ["Decision Node", "Execution / Risk", "Hook", "UI / React", "Validation / Audit", "Zone / RTV"]
entities: []
---

# Source Card — 03_sequence_builder.md

## Source

[[docs/nds_hook_architecture/03_sequence_builder|docs/nds_hook_architecture/03_sequence_builder.md]]

## Summary

Build Hook / CycleHook sequences from NDS nodes. Every eligible node can start a CycleHook sequence, subject to the starter reuse rule. A node can be the starter of a sequence once. A node may appear in later positions of other sequences, but it should not repeatedly start new sequences after already serving as a starter. Positive sequence: Each new accepted X node must be lower than the previous accepted X node. Negative sequence: Each new accepted X node must be higher than the previous accepted X node. The system should allow multiple alive sequences at the same time. Each sequence keeps its own identity. Suggested object: If a sequence produces more than the allowed number of nodes, increase L until the maximum accepted node count is within the target range. Existing captured principle: Default target: The system should support two views: Used for: The origin remains fixed. Used for:

## Concepts

[[docs/obsidian_deep/02_concepts/Decision_Node|Decision Node]], [[docs/obsidian_deep/02_concepts/Execution____Risk|Execution / Risk]], [[docs/obsidian_deep/02_concepts/Hook|Hook]], [[docs/obsidian_deep/02_concepts/UI____React|UI / React]], [[docs/obsidian_deep/02_concepts/Validation____Audit|Validation / Audit]], [[docs/obsidian_deep/02_concepts/Zone____RTV|Zone / RTV]]

## Entities

—

## Headings

- 03 — Sequence Builder
  - Objective
  - Starter Rule
  - Positive Sequence Rule
  - Negative Sequence Rule
  - Multi-Sequence Rule
  - Max Nodes Rule
  - Fixed-Origin vs Recalculated-Origin Views
    - Fixed-Origin View
    - Recalculated-Origin View
  - Sequence Fields
  - Sequence Audit

## Related Source Documents

- [[docs/architecture|architecture.md]] — score `18`
- [[docs/ui/ARCHITECTURE|ARCHITECTURE.md]] — score `18`
- [[docs/nds_hook_architecture/06_build_phases|06_build_phases.md]] — score `13`
- [[docs/nds_hook_architecture/13_phase06_xy_closure_quality_score_implementation|13_phase06_xy_closure_quality_score_implementation.md]] — score `13`
- [[docs/ai_execution/AI_ALGORITHM_LAYER_MAP_FOR_EXTREME_ENGINE_FA|AI_ALGORITHM_LAYER_MAP_FOR_EXTREME_ENGINE_FA.md]] — score `12`
- [[docs/ai_execution/AI_NATIVE_EXECUTION_ROADMAP_FA|AI_NATIVE_EXECUTION_ROADMAP_FA.md]] — score `12`
- [[docs/ai_execution/AMIR_STRUCTURAL_EXPERIENCE_MAP_FA|AMIR_STRUCTURAL_EXPERIENCE_MAP_FA.md]] — score `12`
- [[docs/ai_execution/EXTREME_L2_NODE_CYCLE_LIMIT_ENTRY_FA|EXTREME_L2_NODE_CYCLE_LIMIT_ENTRY_FA.md]] — score `12`
- [[docs/debug/MARKET_LANGUAGE/README|README.md]] — score `12`
- [[docs/experience_capture/answers/BASE-02/answer_normalized_en|answer_normalized_en.md]] — score `12`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
