
---
type: source_card
source_path: "docs/flag_counting/phoenix_rebuild/hook_nd_branching/HOOK_ND_IMPLEMENTATION_CHECKLIST_V1.md"
source_ext: ".md"
source_size: 3760
empty: false
generated_at: 2026-07-06
concepts: ["AI Agent Layer", "Convexity / Optionality", "Decision Node", "Execution / Risk", "Flag Counting", "Hook", "UI / React", "Validation / Audit"]
entities: []
---

# Source Card — HOOK_ND_IMPLEMENTATION_CHECKLIST_V1.md

## Source

[[docs/flag_counting/phoenix_rebuild/hook_nd_branching/HOOK_ND_IMPLEMENTATION_CHECKLIST_V1|docs/flag_counting/phoenix_rebuild/hook_nd_branching/HOOK_ND_IMPLEMENTATION_CHECKLIST_V1.md]]

## Summary

Use this checklist before modifying the Phoenix code. [ ] Use project L definition. [ ] Use candle high/low only. [ ] Preserve equal high/low plateau behavior. [ ] Treat equality as non-break. [ ] Support optional pending active node. [ ] Expose node id, time, price, kind, L, confirmed status. [ ] Add HookContext model. [ ] Add HookBranch model. [ ] Store boundary node id. [ ] Store active / resolve node id. [ ] Store counted same-side node ids. [ ] Store branch count. [ ] Store retracement ratio. [ ] Store adaptive L iteration count. [ ] Store ND qualification status. [ ] Store pending-node usage. [ ] Low-side Hook finds first older low strictly lower than active low. [ ] High-side Hook finds first older high strictly higher than active high. [ ] Boundary node is not counted as internal `1`. [ ] No bounded Hook is emitted if no boundary exists, unless audit mode requires unbounded diagn

## Concepts

[[docs/obsidian_deep/02_concepts/AI_Agent_Layer|AI Agent Layer]], [[docs/obsidian_deep/02_concepts/Convexity____Optionality|Convexity / Optionality]], [[docs/obsidian_deep/02_concepts/Decision_Node|Decision Node]], [[docs/obsidian_deep/02_concepts/Execution____Risk|Execution / Risk]], [[docs/obsidian_deep/02_concepts/Flag_Counting|Flag Counting]], [[docs/obsidian_deep/02_concepts/Hook|Hook]], [[docs/obsidian_deep/02_concepts/UI____React|UI / React]], [[docs/obsidian_deep/02_concepts/Validation____Audit|Validation / Audit]]

## Entities

—

## Headings

- Hook / ND Implementation Checklist V1
  - 1. Node engine prerequisites
  - 2. Hook engine data model
  - 3. Hook origin boundary
  - 4. Branch extraction
  - 5. Adaptive L
  - 6. ND qualification
  - 7. Hook / F1 integration
  - 8. Renderer
  - 9. Test scenarios
  - 10. Rejection checks

## Related Source Documents

- [[docs/flag_counting/phoenix_rebuild/hook_nd_branching/HOOK_ND_BRANCH_SEQUENCE_CONTRACT_V1|HOOK_ND_BRANCH_SEQUENCE_CONTRACT_V1.md]] — score `17`
- [[docs/ai_execution/AI_ALGORITHM_LAYER_MAP_FOR_EXTREME_ENGINE_FA|AI_ALGORITHM_LAYER_MAP_FOR_EXTREME_ENGINE_FA.md]] — score `16`
- [[docs/ai_execution/AI_NATIVE_EXECUTION_ROADMAP_FA|AI_NATIVE_EXECUTION_ROADMAP_FA.md]] — score `16`
- [[docs/ai_execution/AMIR_STRUCTURAL_EXPERIENCE_MAP_FA|AMIR_STRUCTURAL_EXPERIENCE_MAP_FA.md]] — score `16`
- [[docs/experience_capture/answers/EXT-01/answer_normalized_en|answer_normalized_en.md]] — score `16`
- [[docs/experience_capture/answers/NDS-R01/answer_normalized_en|answer_normalized_en.md]] — score `16`
- [[docs/flag_counting/FLAG_COUNTING_CURRENT_CANON|FLAG_COUNTING_CURRENT_CANON.md]] — score `16`
- [[docs/flag_counting/FLAG_COUNTING_IMPLEMENTATION_CHECKLIST_V4|FLAG_COUNTING_IMPLEMENTATION_CHECKLIST_V4.md]] — score `16`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE4_HOOK_VIEW_PROJECTION|FLAG_COUNTING_LEVEL_19_PHASE4_HOOK_VIEW_PROJECTION.md]] — score `16`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE6_STATE_CONTRACT_STORAGE|FLAG_COUNTING_LEVEL_19_PHASE6_STATE_CONTRACT_STORAGE.md]] — score `16`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
