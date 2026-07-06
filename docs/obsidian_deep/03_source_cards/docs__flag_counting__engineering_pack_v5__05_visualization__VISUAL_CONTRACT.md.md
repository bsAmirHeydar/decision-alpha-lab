
---
type: source_card
source_path: "docs/flag_counting/engineering_pack_v5/05_visualization/VISUAL_CONTRACT.md"
source_ext: ".md"
source_size: 2051
empty: false
generated_at: 2026-07-06
concepts: ["AI Agent Layer", "Decision Node", "Flag Counting", "Hook", "Path Smoothness", "UI / React"]
entities: []
---

# Source Card — VISUAL_CONTRACT.md

## Source

[[docs/flag_counting/engineering_pack_v5/05_visualization/VISUAL_CONTRACT|docs/flag_counting/engineering_pack_v5/05_visualization/VISUAL_CONTRACT.md]]

## Summary

Renderer receives render model objects: It does not receive raw bars to infer structures. A flag body uses two visual pieces: All flag lines are thin by default. Do not make larger scale lines thick by default. Use label and shade, not width. The curve must not look like broken angular trendlines. Implementation options: polyline sampled from quadratic Bezier through Waist; arc-like curve with enough sample points; platform curve object if available and stable. Minimum visual rule: The curve does not need to follow every candle. It must show body logic. ND/Hook uses gray arc/semicircle. Do not draw the 50% line by default. Show `O` by default during research. Input: Research default uses detailed labels: `Q` can be sequence/chain id. `H` can be hook id. Use semantic color families: Within a semantic family, use shade variation for different sequence ids. Do not use huge line width differ

## Concepts

[[docs/obsidian_deep/02_concepts/AI_Agent_Layer|AI Agent Layer]], [[docs/obsidian_deep/02_concepts/Decision_Node|Decision Node]], [[docs/obsidian_deep/02_concepts/Flag_Counting|Flag Counting]], [[docs/obsidian_deep/02_concepts/Hook|Hook]], [[docs/obsidian_deep/02_concepts/Path_Smoothness|Path Smoothness]], [[docs/obsidian_deep/02_concepts/UI____React|UI / React]]

## Entities

—

## Headings

- Visual Contract
  - Rendering Inputs
  - Flag Body Rendering
  - Smooth Arc Requirement
  - ND / Hook Rendering
  - Origin Marker
  - Labels
  - Colors
  - Main Chart Defaults
  - Fidelity Rule

## Related Source Documents

- [[docs/ai_execution/AI_NATIVE_EXECUTION_ROADMAP_FA|AI_NATIVE_EXECUTION_ROADMAP_FA.md]] — score `12`
- [[docs/flag_counting/engineering_pack_v5/01_concepts/CONCEPT_TAXONOMY|CONCEPT_TAXONOMY.md]] — score `12`
- [[docs/flag_counting/FLAG_COUNTING_ALGORITHM_BLUEPRINT|FLAG_COUNTING_ALGORITHM_BLUEPRINT.md]] — score `12`
- [[docs/flag_counting/FLAG_COUNTING_CONCEPT_SPEC_V2|FLAG_COUNTING_CONCEPT_SPEC_V2.md]] — score `12`
- [[docs/flag_counting/FLAG_COUNTING_CONCEPT_SPEC_V3|FLAG_COUNTING_CONCEPT_SPEC_V3.md]] — score `12`
- [[docs/flag_counting/FLAG_COUNTING_IMPLEMENTATION_CHECKLIST_V3|FLAG_COUNTING_IMPLEMENTATION_CHECKLIST_V3.md]] — score `12`
- [[docs/flag_counting/FLAG_COUNTING_SEQUENCE_CONTRACT_V2|FLAG_COUNTING_SEQUENCE_CONTRACT_V2.md]] — score `12`
- [[docs/flag_counting/FLAG_COUNTING_SEQUENCE_CONTRACT_V3|FLAG_COUNTING_SEQUENCE_CONTRACT_V3.md]] — score `12`
- [[docs/flag_counting/FLAG_COUNTING_SEQUENCE_CONTRACT_V4|FLAG_COUNTING_SEQUENCE_CONTRACT_V4.md]] — score `12`
- [[docs/flag_counting/FLAG_COUNTING_V6_IMPLEMENTATION_NOTES|FLAG_COUNTING_V6_IMPLEMENTATION_NOTES.md]] — score `12`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
