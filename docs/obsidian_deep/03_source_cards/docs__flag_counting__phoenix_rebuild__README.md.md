
---
type: source_card
source_path: "docs/flag_counting/phoenix_rebuild/README.md"
source_ext: ".md"
source_size: 1300
empty: false
generated_at: 2026-07-06
concepts: ["Decision Node", "Execution / Risk", "Flag Counting", "Hook", "UI / React", "Validation / Audit"]
entities: []
---

# Source Card — README.md

## Source

[[docs/flag_counting/phoenix_rebuild/README|docs/flag_counting/phoenix_rebuild/README.md]]

## Summary

This package replaces the failed patch-on-patch lineage with a clean engine. The old code must be removed before applying this patch. The design goal is not to hide complexity. The goal is to make every layer explicit: Node extraction. Hook/ND branch discovery. Two-leg body construction. Post-flag internal counting. F1/F2/F3 sequence orchestration. Renderer-only visualization. Audit-only diagnostics. The previous implementation failed for four root reasons: Audit events were rendered as chart structures. F1 roots were created from arbitrary two-leg windows instead of phase boundaries. F2/F3 ownership was not hard enough, so children could drift away from their parent context. Strict phase gates were applied before Hook/ND boundary extraction was strong enough, which made the chart empty. Phoenix fixes the thinking process by making each stage independently inspectable and by keeping fall

## Concepts

[[docs/obsidian_deep/02_concepts/Decision_Node|Decision Node]], [[docs/obsidian_deep/02_concepts/Execution____Risk|Execution / Risk]], [[docs/obsidian_deep/02_concepts/Flag_Counting|Flag Counting]], [[docs/obsidian_deep/02_concepts/Hook|Hook]], [[docs/obsidian_deep/02_concepts/UI____React|UI / React]], [[docs/obsidian_deep/02_concepts/Validation____Audit|Validation / Audit]]

## Entities

—

## Headings

- Flag Counting Phoenix Rebuild
  - Why the previous attempts failed
  - Apply policy

## Related Source Documents

- [[docs/flag_counting/phoenix_rebuild/PHOENIX_SEQUENCE_OWNERSHIP_REPAIR_V4|PHOENIX_SEQUENCE_OWNERSHIP_REPAIR_V4.md]] — score `13`
- [[docs/ai_execution/AI_ALGORITHM_LAYER_MAP_FOR_EXTREME_ENGINE_FA|AI_ALGORITHM_LAYER_MAP_FOR_EXTREME_ENGINE_FA.md]] — score `12`
- [[docs/ai_execution/AI_NATIVE_EXECUTION_ROADMAP_FA|AI_NATIVE_EXECUTION_ROADMAP_FA.md]] — score `12`
- [[docs/ai_execution/AMIR_STRUCTURAL_EXPERIENCE_MAP_FA|AMIR_STRUCTURAL_EXPERIENCE_MAP_FA.md]] — score `12`
- [[docs/debug/MARKET_LANGUAGE/README|README.md]] — score `12`
- [[docs/experience_capture/answers/BASE-01/answer_normalized_en|answer_normalized_en.md]] — score `12`
- [[docs/experience_capture/answers/BASE-02/answer_normalized_en|answer_normalized_en.md]] — score `12`
- [[docs/experience_capture/answers/BASE-04/answer_normalized_en|answer_normalized_en.md]] — score `12`
- [[docs/experience_capture/answers/BASE-05/answer_normalized_en|answer_normalized_en.md]] — score `12`
- [[docs/experience_capture/answers/BASE-06/answer_normalized_en|answer_normalized_en.md]] — score `12`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
