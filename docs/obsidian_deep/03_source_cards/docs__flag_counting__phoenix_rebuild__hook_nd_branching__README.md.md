
---
type: source_card
source_path: "docs/flag_counting/phoenix_rebuild/hook_nd_branching/README.md"
source_ext: ".md"
source_size: 1691
empty: false
generated_at: 2026-07-06
concepts: ["AI Agent Layer", "Decision Node", "Flag Counting", "Hook", "UI / React"]
entities: []
---

# Source Card — README.md

## Source

[[docs/flag_counting/phoenix_rebuild/hook_nd_branching/README|docs/flag_counting/phoenix_rebuild/hook_nd_branching/README.md]]

## Summary

This package defines the Hook / ND component used by the Flag Counting Phoenix engine. It is intentionally separated from the F1/F2/F3 sequence documents because Hook / ND is not a simple label or a single visual marker. It is a structural container that can hold multiple internal branch sequences. The purpose of this package is to remove ambiguity before implementation. The engine must not treat every three or four raw nodes as ND. A Hook / ND exists only when the branch-sequence rules defined here are satisfied. `HOOK_ND_BRANCH_SEQUENCE_CONTRACT_V1.md` Canonical conceptual and engineering contract for Hook / ND. `HOOK_ND_BRANCH_ALGORITHM_V1.md` Step-by-step deterministic algorithm for extracting Hook / ND branches. `HOOK_ND_VISUALIZATION_AND_LABEL_LAYOUT_V1.md` Rendering contract for Hook / ND arcs, branch labels, ND text, and clean stacked chart labels. `HOOK_ND_IMPLEMENTATION_CHECKLI

## Concepts

[[docs/obsidian_deep/02_concepts/AI_Agent_Layer|AI Agent Layer]], [[docs/obsidian_deep/02_concepts/Decision_Node|Decision Node]], [[docs/obsidian_deep/02_concepts/Flag_Counting|Flag Counting]], [[docs/obsidian_deep/02_concepts/Hook|Hook]], [[docs/obsidian_deep/02_concepts/UI____React|UI / React]]

## Entities

—

## Headings

- Hook / ND Branch-Sequence Documentation Pack
  - Files
  - Core idea

## Related Source Documents

- [[docs/flag_counting/phoenix_rebuild/hook_nd_branching/HOOK_ND_BRANCH_ALGORITHM_V1|HOOK_ND_BRANCH_ALGORITHM_V1.md]] — score `19`
- [[docs/flag_counting/phoenix_rebuild/hook_nd_branching/HOOK_ND_BRANCH_SEQUENCE_CONTRACT_V1|HOOK_ND_BRANCH_SEQUENCE_CONTRACT_V1.md]] — score `19`
- [[docs/flag_counting/phoenix_rebuild/hook_nd_branching/HOOK_ND_IMPLEMENTATION_CHECKLIST_V1|HOOK_ND_IMPLEMENTATION_CHECKLIST_V1.md]] — score `19`
- [[docs/flag_counting/phoenix_rebuild/hook_nd_branching/HOOK_ND_VISUALIZATION_AND_LABEL_LAYOUT_V1|HOOK_ND_VISUALIZATION_AND_LABEL_LAYOUT_V1.md]] — score `19`
- [[docs/ai_execution/AI_ALGORITHM_LAYER_MAP_FOR_EXTREME_ENGINE_FA|AI_ALGORITHM_LAYER_MAP_FOR_EXTREME_ENGINE_FA.md]] — score `10`
- [[docs/ai_execution/AI_NATIVE_EXECUTION_ROADMAP_FA|AI_NATIVE_EXECUTION_ROADMAP_FA.md]] — score `10`
- [[docs/ai_execution/AMIR_STRUCTURAL_EXPERIENCE_MAP_FA|AMIR_STRUCTURAL_EXPERIENCE_MAP_FA.md]] — score `10`
- [[docs/ai_execution/README|README.md]] — score `10`
- [[docs/debug/E0008/README|README.md]] — score `10`
- [[docs/debug/MARKET_LANGUAGE/README|README.md]] — score `10`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
