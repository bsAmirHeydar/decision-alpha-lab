
---
type: source_card
source_path: "docs/nds_hook_architecture/27_phase19_label_semantics_directional_clarity.md"
source_ext: ".md"
source_size: 1119
empty: false
generated_at: 2026-07-06
concepts: ["AI Agent Layer", "Decision Node", "Hook", "Market Anatomy", "UI / React"]
entities: []
---

# Source Card — 27_phase19_label_semantics_directional_clarity.md

## Source

[[docs/nds_hook_architecture/27_phase19_label_semantics_directional_clarity|docs/nds_hook_architecture/27_phase19_label_semantics_directional_clarity.md]]

## Summary

Align the minimal Hook view with the intended Hook reading semantics: Sequence counting should be `1, 2, 3, 4` as the meaningful internal Hook sequence. The chart should not start numbering from `0` in minimal mode. The origin remains the structural start anchor, but it is left unlabeled in the minimal numeric view. Positive Hook reading is based on **valleys**. Negative Hook reading is based on **peaks**. A new label mode was added: Behavior: origin: no numeric label X1: `1` X2: `2` X3: `3` X4: `4` This mode is now the default for the minimal all-hooks view and the default Phase 02 node-label input. The Phase 02 sequence builder already uses directional node typing as follows: `POSITIVE` Hook sequences use `VALLEY` nodes `NEGATIVE` Hook sequences use `PEAK` nodes This patch documents that expectation explicitly so the minimal rendering semantics match the intended Hook anatomy.

## Concepts

[[docs/obsidian_deep/02_concepts/AI_Agent_Layer|AI Agent Layer]], [[docs/obsidian_deep/02_concepts/Decision_Node|Decision Node]], [[docs/obsidian_deep/02_concepts/Hook|Hook]], [[docs/obsidian_deep/02_concepts/Market_Anatomy|Market Anatomy]], [[docs/obsidian_deep/02_concepts/UI____React|UI / React]]

## Entities

—

## Headings

- Phase 19 — Label Semantics and Directional Clarity
  - Goal
  - What changed
    - Node label mode
    - Directional semantics

## Related Source Documents

- [[docs/nds_hook_architecture/14_phase07_visual_profile_orchestrator_implementation|14_phase07_visual_profile_orchestrator_implementation.md]] — score `11`
- [[docs/ai_execution/AI_NATIVE_EXECUTION_ROADMAP_FA|AI_NATIVE_EXECUTION_ROADMAP_FA.md]] — score `10`
- [[docs/debug/MARKET_LANGUAGE/README|README.md]] — score `10`
- [[docs/experience_capture/answers/BASE-04/answer_normalized_en|answer_normalized_en.md]] — score `10`
- [[docs/experience_capture/answers/BASE-04/notes_en|notes_en.md]] — score `10`
- [[docs/experience_capture/answers/BASE-06/answer_normalized_en|answer_normalized_en.md]] — score `10`
- [[docs/experience_capture/answers/DST-R03/notes_en|notes_en.md]] — score `10`
- [[docs/experience_capture/answers/ENT-R01/notes_en|notes_en.md]] — score `10`
- [[docs/experience_capture/answers/NDS-R01/answer_normalized_en|answer_normalized_en.md]] — score `10`
- [[docs/experience_capture/answers/SCN-R01/answer_normalized_en|answer_normalized_en.md]] — score `10`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
