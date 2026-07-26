
---
type: source_card
source_path: "docs/experience_capture/answers/BASE-04/notes_en.md"
source_ext: ".md"
source_size: 2809
empty: false
generated_at: 2026-07-06
concepts: ["AI Agent Layer", "Decision Node", "Execution / Risk", "Hook", "MQL Native", "Market Anatomy", "Python Brain", "Rally", "UI / React"]
entities: []
---

# Source Card — notes_en.md

## Source

[[docs/experience_capture/answers/BASE-04/notes_en|docs/experience_capture/answers/BASE-04/notes_en.md]]

## Summary

This experience should be treated as: Every future dataset, model, feature, label, and execution reason must pass an ontology filter. The system must not allow external concepts to enter silently. Gate states: Every future dataset should include a feature manifest. Each feature should declare: Future datasets should include an NDS ontology manifest: Possible columns: Are spread, commission, and slippage allowed as execution-cost fields even though they are not market-anatomy concepts? Is raw price allowed only as geometry, or can it become a feature directly? Are volume/tick-volume fields forbidden by default? Can session information ever be allowed if it is used only for execution permission rather than signal logic? Can statistical diagnostics be used for evaluation even if they are not part of the trading ontology? If an external concept resembles an NDS concept, should it be rejected

## Concepts

[[docs/obsidian_deep/02_concepts/AI_Agent_Layer|AI Agent Layer]], [[docs/obsidian_deep/02_concepts/Decision_Node|Decision Node]], [[docs/obsidian_deep/02_concepts/Execution____Risk|Execution / Risk]], [[docs/obsidian_deep/02_concepts/Hook|Hook]], [[docs/obsidian_deep/02_concepts/MQL_Native|MQL Native]], [[docs/obsidian_deep/02_concepts/Market_Anatomy|Market Anatomy]], [[docs/obsidian_deep/02_concepts/Python_Brain|Python Brain]], [[docs/obsidian_deep/02_concepts/Rally|Rally]], [[docs/obsidian_deep/02_concepts/UI____React|UI / React]]

## Entities

—

## Headings

- BASE-04 — Notes and Open Questions
  - Classification
  - Main Design Consequence
  - Proposed Ontology Gate
  - Proposed Feature Manifest Requirement
  - Proposed Forbidden Feature Families
  - Proposed Allowed Feature Families
  - Proposed Dataset Consequence
  - Proposed AI Modules
  - Open Questions
  - Architecture Consequence

## Related Source Documents

- [[docs/architecture|architecture.md]] — score `20`
- [[docs/ai_execution/AI_NATIVE_EXECUTION_ROADMAP_FA|AI_NATIVE_EXECUTION_ROADMAP_FA.md]] — score `18`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE2_CLOSED_BAR_TRACKER|FLAG_COUNTING_LEVEL_19_PHASE2_CLOSED_BAR_TRACKER.md]] — score `18`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE4_HOOK_VIEW_PROJECTION|FLAG_COUNTING_LEVEL_19_PHASE4_HOOK_VIEW_PROJECTION.md]] — score `18`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_STATE_GATE_DASHBOARD_SPEC|FLAG_COUNTING_LEVEL_19_STATE_GATE_DASHBOARD_SPEC.md]] — score `18`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_STATE_GATE_IMPLEMENTATION_PLAN|FLAG_COUNTING_LEVEL_19_STATE_GATE_IMPLEMENTATION_PLAN.md]] — score `18`
- [[docs/nds_hook_architecture/14_phase07_visual_profile_orchestrator_implementation|14_phase07_visual_profile_orchestrator_implementation.md]] — score `18`
- [[docs/experience_capture/answers/BASE-04/answer_normalized_en|answer_normalized_en.md]] — score `17`
- [[docs/experience_capture/answers/BASE-06/answer_normalized_en|answer_normalized_en.md]] — score `16`
- [[docs/experience_capture/answers/NDS-R01/answer_normalized_en|answer_normalized_en.md]] — score `16`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
