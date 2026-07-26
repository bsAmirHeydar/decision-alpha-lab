
---
type: source_card
source_path: "docs/flag_counting/phoenix_rebuild/hook_nd_branching/HOOK_ND_VISUALIZATION_AND_LABEL_LAYOUT_V1.md"
source_ext: ".md"
source_size: 6246
empty: false
generated_at: 2026-07-06
concepts: ["AI Agent Layer", "Decision Node", "Flag Counting", "Hook", "Path Smoothness", "UI / React", "Validation / Audit"]
entities: []
---

# Source Card — HOOK_ND_VISUALIZATION_AND_LABEL_LAYOUT_V1.md

## Source

[[docs/flag_counting/phoenix_rebuild/hook_nd_branching/HOOK_ND_VISUALIZATION_AND_LABEL_LAYOUT_V1|docs/flag_counting/phoenix_rebuild/hook_nd_branching/HOOK_ND_VISUALIZATION_AND_LABEL_LAYOUT_V1.md]]

## Summary

This document defines how Hook / ND structures and Flag Counting labels must be rendered on the chart. The main visual failures observed so far were: labels overlap and become unreadable; ND labels are drawn for raw/developing structures that are not true ND; multiple branch states are dumped directly on the main chart; Hook arcs do not clearly show which branch or Hook context they belong to. This contract separates semantic rendering from debug rendering. The renderer must not create Hook, ND, F1, F2, or F3 structures. It only draws events emitted by the engine. Semantic view is the default chart view. It should show: confirmed and active structures; meaningful developing structures; ND branches only when they satisfy the ND contract; clean labels. Audit view can show: raw branches; developing 1-node and 2-node Hook branches; below-threshold Hooks; superseded states; detailed node ids.

## Concepts

[[docs/obsidian_deep/02_concepts/AI_Agent_Layer|AI Agent Layer]], [[docs/obsidian_deep/02_concepts/Decision_Node|Decision Node]], [[docs/obsidian_deep/02_concepts/Flag_Counting|Flag Counting]], [[docs/obsidian_deep/02_concepts/Hook|Hook]], [[docs/obsidian_deep/02_concepts/Path_Smoothness|Path Smoothness]], [[docs/obsidian_deep/02_concepts/UI____React|UI / React]], [[docs/obsidian_deep/02_concepts/Validation____Audit|Validation / Audit]]

## Entities

—

## Headings

- Hook / ND Visualization and Label Layout V1
  - 1. Purpose
  - 2. Rendering principles
    - 2.1 Renderer is not a detector
    - 2.2 Semantic view versus audit view
  - 3. Hook / ND visual objects
    - 3.1 Hook arc
    - 3.2 ND label
    - 3.3 Branch number labels
    - 3.4 Developing branches
  - 4. Label layout contract
    - 4.1 Labels must be stacked

## Related Source Documents

- [[docs/principles|principles.md]] — score `16`
- [[docs/ai_execution/AI_NATIVE_EXECUTION_ROADMAP_FA|AI_NATIVE_EXECUTION_ROADMAP_FA.md]] — score `14`
- [[docs/flag_counting/engineering_pack_v5/01_concepts/CONCEPT_TAXONOMY|CONCEPT_TAXONOMY.md]] — score `14`
- [[docs/flag_counting/FLAG_COUNTING_ALGORITHM_BLUEPRINT|FLAG_COUNTING_ALGORITHM_BLUEPRINT.md]] — score `14`
- [[docs/flag_counting/FLAG_COUNTING_CONCEPT_SPEC_V2|FLAG_COUNTING_CONCEPT_SPEC_V2.md]] — score `14`
- [[docs/flag_counting/FLAG_COUNTING_CONCEPT_SPEC_V3|FLAG_COUNTING_CONCEPT_SPEC_V3.md]] — score `14`
- [[docs/flag_counting/FLAG_COUNTING_IMPLEMENTATION_CHECKLIST_V3|FLAG_COUNTING_IMPLEMENTATION_CHECKLIST_V3.md]] — score `14`
- [[docs/flag_counting/FLAG_COUNTING_SEQUENCE_CONTRACT_V2|FLAG_COUNTING_SEQUENCE_CONTRACT_V2.md]] — score `14`
- [[docs/flag_counting/FLAG_COUNTING_SEQUENCE_CONTRACT_V3|FLAG_COUNTING_SEQUENCE_CONTRACT_V3.md]] — score `14`
- [[docs/flag_counting/FLAG_COUNTING_SEQUENCE_CONTRACT_V4|FLAG_COUNTING_SEQUENCE_CONTRACT_V4.md]] — score `14`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
