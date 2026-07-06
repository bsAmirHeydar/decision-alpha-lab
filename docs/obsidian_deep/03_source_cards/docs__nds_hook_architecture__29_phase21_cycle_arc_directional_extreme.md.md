
---
type: source_card
source_path: "docs/nds_hook_architecture/29_phase21_cycle_arc_directional_extreme.md"
source_ext: ".md"
source_size: 1498
empty: false
generated_at: 2026-07-06
concepts: ["Hook", "Market Anatomy"]
entities: []
---

# Source Card — 29_phase21_cycle_arc_directional_extreme.md

## Source

[[docs/nds_hook_architecture/29_phase21_cycle_arc_directional_extreme|docs/nds_hook_architecture/29_phase21_cycle_arc_directional_extreme.md]]

## Summary

Make the cycle semicircle match the intended Hook anatomy: the cycle arc starts at the Hook origin the arc spans toward the semicircle crown the arc endpoint lands where the cycle actually saw its directional extreme for a positive Hook, that endpoint is the **lowest valley seen by the cycle** for a negative Hook, that endpoint is the **highest peak seen by the cycle** The cycle arc ended at the **last visible X** (`X1`, `X2`, `X3`, or `X4`). That was acceptable for generic debugging, but it did not match the intended interpretation of the Hook cycle. A new Phase 02 setting was added: Modes: `FP_HOOK_P02_CYCLE_ARC_END_LAST_VISIBLE_X` `FP_HOOK_P02_CYCLE_ARC_END_DIRECTIONAL_EXTREME` When `DIRECTIONAL_EXTREME` is active: **Positive** Hook: choose the lowest price among `X1..X4` **Negative** Hook: choose the highest price among `X1..X4` if two points have the same extreme price, prefer the l

## Concepts

[[docs/obsidian_deep/02_concepts/Hook|Hook]], [[docs/obsidian_deep/02_concepts/Market_Anatomy|Market Anatomy]]

## Entities

—

## Headings

- Phase 21 — Cycle Arc Ends at the Directional Extreme
  - Goal
  - Problem in previous versions
  - New arc endpoint mode
  - Directional extreme behavior
  - Minimal profile default

## Related Source Documents

- [[docs/nds_hook_architecture/14_phase07_visual_profile_orchestrator_implementation|14_phase07_visual_profile_orchestrator_implementation.md]] — score `5`
- [[docs/nds_hook_architecture/17_phase10_freeze_training_contract_implementation|17_phase10_freeze_training_contract_implementation.md]] — score `5`
- [[docs/nds_hook_architecture/27_phase19_label_semantics_directional_clarity|27_phase19_label_semantics_directional_clarity.md]] — score `5`
- [[docs/nds_hook_architecture/README|README.md]] — score `5`
- [[docs/ai_execution/AI_NATIVE_EXECUTION_ROADMAP_FA|AI_NATIVE_EXECUTION_ROADMAP_FA.md]] — score `4`
- [[docs/debug/MARKET_LANGUAGE/README|README.md]] — score `4`
- [[docs/experience_capture/answers/BASE-02/answer_normalized_en|answer_normalized_en.md]] — score `4`
- [[docs/experience_capture/answers/BASE-02/answer_raw_en|answer_raw_en.md]] — score `4`
- [[docs/experience_capture/answers/BASE-03/answer_normalized_en|answer_normalized_en.md]] — score `4`
- [[docs/experience_capture/answers/BASE-03/answer_raw_en|answer_raw_en.md]] — score `4`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
