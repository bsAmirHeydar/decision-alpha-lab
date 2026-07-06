
---
type: source_card
source_path: "docs/experience_capture/answers/SCN-R02/notes_en.md"
source_ext: ".md"
source_size: 5101
empty: false
generated_at: 2026-07-06
concepts: ["AI Agent Layer", "Convexity / Optionality", "Execution / Risk", "Flag Counting", "Hook", "Python Brain", "UI / React", "Validation / Audit", "Zone / RTV"]
entities: []
---

# Source Card — notes_en.md

## Source

[[docs/experience_capture/answers/SCN-R02/notes_en|docs/experience_capture/answers/SCN-R02/notes_en.md]]

## Summary

This answer should be treated as: Zone generation should be recipe-based and trainable. The system should support many zone recipes, not one universal formula. Recommended architecture: Each zone must expose why it exists: This makes zone learning auditable. What exact formula defines F2 waist / midpoint? Should the F2 >= F1 constraint use price distance only? Should a zone created by F2 >= F1 require CycleHook ND, or can it stand alone? What exact price range defines the ND-to-origin zone? How should zone start from symmetry confluence be calculated? Should zone end behind Hook start use a fixed point, spread, or structural buffer? What exactly means the area itself is destroyed? Can a zone remain valid after partial penetration? Can multiple zones overlap and merge, or should they remain separate? Should each zone family have its own invalidation rules? Should zone training start globa

## Concepts

[[docs/obsidian_deep/02_concepts/AI_Agent_Layer|AI Agent Layer]], [[docs/obsidian_deep/02_concepts/Convexity____Optionality|Convexity / Optionality]], [[docs/obsidian_deep/02_concepts/Execution____Risk|Execution / Risk]], [[docs/obsidian_deep/02_concepts/Flag_Counting|Flag Counting]], [[docs/obsidian_deep/02_concepts/Hook|Hook]], [[docs/obsidian_deep/02_concepts/Python_Brain|Python Brain]], [[docs/obsidian_deep/02_concepts/UI____React|UI / React]], [[docs/obsidian_deep/02_concepts/Validation____Audit|Validation / Audit]], [[docs/obsidian_deep/02_concepts/Zone____RTV|Zone / RTV]]

## Entities

—

## Headings

- SCN-R02 — Notes and Open Questions
  - Classification
  - Core Hard Rules
  - Core Learnable Policies
  - Proposed Objects
  - Proposed Datasets
  - Proposed Fields
  - Proposed Labels
  - Proposed AI Modules
  - Architecture Consequence
  - Open Questions
  - Attachment Index

## Related Source Documents

- [[docs/architecture|architecture.md]] — score `20`
- [[docs/ai_execution/AI_ALGORITHM_LAYER_MAP_FOR_EXTREME_ENGINE_FA|AI_ALGORITHM_LAYER_MAP_FOR_EXTREME_ENGINE_FA.md]] — score `18`
- [[docs/ai_execution/AI_NATIVE_EXECUTION_ROADMAP_FA|AI_NATIVE_EXECUTION_ROADMAP_FA.md]] — score `18`
- [[docs/ai_execution/AMIR_STRUCTURAL_EXPERIENCE_MAP_FA|AMIR_STRUCTURAL_EXPERIENCE_MAP_FA.md]] — score `18`
- [[docs/flag_counting/FLAG_COUNTING_CURRENT_CANON|FLAG_COUNTING_CURRENT_CANON.md]] — score `18`
- [[docs/flag_counting/implementation_ladder_v1/15_MODULE_INTERFACE_CONTRACTS|15_MODULE_INTERFACE_CONTRACTS.md]] — score `18`
- [[docs/flag_counting/implementation_ladder_v1/16_IMPLEMENTATION_ORDER_AND_ACCEPTANCE_MATRIX|16_IMPLEMENTATION_ORDER_AND_ACCEPTANCE_MATRIX.md]] — score `18`
- [[docs/flag_counting/README|README.md]] — score `18`
- [[docs/nds_hook_architecture/06_build_phases|06_build_phases.md]] — score `18`
- [[mql5/Include/FlagCountingPhoenix/README_FlagCountingPhoenix|README_FlagCountingPhoenix.md]] — score `18`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
