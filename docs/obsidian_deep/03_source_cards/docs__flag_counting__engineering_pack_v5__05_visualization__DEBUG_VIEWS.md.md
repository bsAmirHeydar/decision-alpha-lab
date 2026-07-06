
---
type: source_card
source_path: "docs/flag_counting/engineering_pack_v5/05_visualization/DEBUG_VIEWS.md"
source_ext: ".md"
source_size: 2059
empty: false
generated_at: 2026-07-06
concepts: ["AI Agent Layer", "Convexity / Optionality", "Decision Node", "Flag Counting", "Hook", "Python Brain", "Validation / Audit"]
entities: []
---

# Source Card — DEBUG_VIEWS.md

## Source

[[docs/flag_counting/engineering_pack_v5/05_visualization/DEBUG_VIEWS|docs/flag_counting/engineering_pack_v5/05_visualization/DEBUG_VIEWS.md]]

## Summary

The user wants to see all structures. But all structures must still be inspectable. A single chart can show all emitted structures if rendering is disciplined, but debugging also needs panels and modes. Even if default draws all structures, modes help diagnose. Default: Panel should not replace chart drawings. It should summarize: A file/CSV/log view should include transitions: When a suspicious line appears, answer: Which object id owns it? Which chain owns it? Is it F1/F2/F3/ND? Where are Origin, Leg1, Waist, Leg2? Why is it alive? What would invalidate it? Was it emitted by logic engine or renderer? Does audit log contain its creation event? If any answer is missing, the bug is in logical emission or audit identity, not in line drawing. Rejected objects should be hidden by default. For debugging: When enabled, rejected objects must be visibly different and not confused with live struc

## Concepts

[[docs/obsidian_deep/02_concepts/AI_Agent_Layer|AI Agent Layer]], [[docs/obsidian_deep/02_concepts/Convexity____Optionality|Convexity / Optionality]], [[docs/obsidian_deep/02_concepts/Decision_Node|Decision Node]], [[docs/obsidian_deep/02_concepts/Flag_Counting|Flag Counting]], [[docs/obsidian_deep/02_concepts/Hook|Hook]], [[docs/obsidian_deep/02_concepts/Python_Brain|Python Brain]], [[docs/obsidian_deep/02_concepts/Validation____Audit|Validation / Audit]]

## Entities

—

## Headings

- Debug Views
  - Why Debug Views Are Needed
  - Recommended Inputs
  - View Modes
  - Status Panel
  - Audit Table
  - Visual Debug Checklist
  - Rejected View
  - ND Density Controls

## Related Source Documents

- [[docs/ai_execution/AI_ALGORITHM_LAYER_MAP_FOR_EXTREME_ENGINE_FA|AI_ALGORITHM_LAYER_MAP_FOR_EXTREME_ENGINE_FA.md]] — score `14`
- [[docs/ai_execution/AI_NATIVE_EXECUTION_ROADMAP_FA|AI_NATIVE_EXECUTION_ROADMAP_FA.md]] — score `14`
- [[docs/ai_execution/AMIR_STRUCTURAL_EXPERIENCE_MAP_FA|AMIR_STRUCTURAL_EXPERIENCE_MAP_FA.md]] — score `14`
- [[docs/flag_counting/FLAG_COUNTING_CURRENT_CANON|FLAG_COUNTING_CURRENT_CANON.md]] — score `14`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE11_ENTRY_BRIDGE_READINESS|FLAG_COUNTING_LEVEL_19_PHASE11_ENTRY_BRIDGE_READINESS.md]] — score `14`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE12_EXTREME_CANDIDATE_MAP|FLAG_COUNTING_LEVEL_19_PHASE12_EXTREME_CANDIDATE_MAP.md]] — score `14`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE4_HOOK_VIEW_PROJECTION|FLAG_COUNTING_LEVEL_19_PHASE4_HOOK_VIEW_PROJECTION.md]] — score `14`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE6_STATE_CONTRACT_STORAGE|FLAG_COUNTING_LEVEL_19_PHASE6_STATE_CONTRACT_STORAGE.md]] — score `14`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_STATE_GATE_IMPLEMENTATION_PLAN|FLAG_COUNTING_LEVEL_19_STATE_GATE_IMPLEMENTATION_PLAN.md]] — score `14`
- [[docs/flag_counting/implementation_ladder_v1/12_LEVEL_12_RENDERER_AND_LABEL_LAYOUT|12_LEVEL_12_RENDERER_AND_LABEL_LAYOUT.md]] — score `14`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
