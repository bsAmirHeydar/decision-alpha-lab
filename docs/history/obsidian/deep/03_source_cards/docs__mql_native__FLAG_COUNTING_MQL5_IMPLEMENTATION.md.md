
---
type: source_card
source_path: "docs/mql_native/FLAG_COUNTING_MQL5_IMPLEMENTATION.md"
source_ext: ".md"
source_size: 4317
empty: false
generated_at: 2026-07-06
concepts: ["AI Agent Layer", "Convexity / Optionality", "Decision Node", "Flag Counting", "Hook", "MQL Native", "Validation / Audit"]
entities: []
---

# Source Card — FLAG_COUNTING_MQL5_IMPLEMENTATION.md

## Source

[[docs/mql_native/FLAG_COUNTING_MQL5_IMPLEMENTATION|docs/mql_native/FLAG_COUNTING_MQL5_IMPLEMENTATION.md]]

## Summary

Active expert: Reusable modules: The current detector is intended to be a multi-sequence counting engine, not a loose overlay scanner. Each `FC_FlagEvent` should carry enough information to audit: F1 is the root body. F1 validity: F1 lifecycle: Continuation levels inherit direction from the parent and start from the parent internal `2`. Continuation lifecycle: Continuation levels may break their own waist. A waist-break branch is interpreted as: After F1, the sequence waits for F2. After F2, it waits for F3. The child can be delayed or very large. The parent remains visible/live while the child is not yet complete. `InpContinuationCoreSearchMaxNodes = 0` means no small-window cap; search continues until invalidation or the end of the node stream. The market can produce F-counting sequences at different scales in parallel. The detector supports this with: Every event receives `scale_L` an

## Concepts

[[docs/obsidian_deep/02_concepts/AI_Agent_Layer|AI Agent Layer]], [[docs/obsidian_deep/02_concepts/Convexity____Optionality|Convexity / Optionality]], [[docs/obsidian_deep/02_concepts/Decision_Node|Decision Node]], [[docs/obsidian_deep/02_concepts/Flag_Counting|Flag Counting]], [[docs/obsidian_deep/02_concepts/Hook|Hook]], [[docs/obsidian_deep/02_concepts/MQL_Native|MQL Native]], [[docs/obsidian_deep/02_concepts/Validation____Audit|Validation / Audit]]

## Entities

—

## Headings

- Flag Counting MQL5 Implementation
  - Architecture
  - Data contract
  - F1 implementation contract
  - F2/F3 implementation contract
  - Mandatory but live continuation
  - Fractal multi-sequence layer
  - Renderer
  - ND / Hook layer
  - Compile note
  - Visibility safety contract

## Related Source Documents

- [[docs/architecture|architecture.md]] — score `16`
- [[docs/mql_native/H0007_FLAG_COUNTING_F1_START_STRUCTURE|H0007_FLAG_COUNTING_F1_START_STRUCTURE.md]] — score `15`
- [[docs/ai_execution/AI_NATIVE_EXECUTION_ROADMAP_FA|AI_NATIVE_EXECUTION_ROADMAP_FA.md]] — score `14`
- [[docs/experience_capture/answers/NDS-R01/answer_normalized_en|answer_normalized_en.md]] — score `14`
- [[docs/flag_counting/FLAG_COUNTING_CURRENT_CANON|FLAG_COUNTING_CURRENT_CANON.md]] — score `14`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE11_ENTRY_BRIDGE_READINESS|FLAG_COUNTING_LEVEL_19_PHASE11_ENTRY_BRIDGE_READINESS.md]] — score `14`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE12_EXTREME_CANDIDATE_MAP|FLAG_COUNTING_LEVEL_19_PHASE12_EXTREME_CANDIDATE_MAP.md]] — score `14`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE4_HOOK_VIEW_PROJECTION|FLAG_COUNTING_LEVEL_19_PHASE4_HOOK_VIEW_PROJECTION.md]] — score `14`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_STATE_GATE_IMPLEMENTATION_PLAN|FLAG_COUNTING_LEVEL_19_STATE_GATE_IMPLEMENTATION_PLAN.md]] — score `14`
- [[docs/flag_counting/FLAG_COUNTING_V6_IMPLEMENTATION_NOTES|FLAG_COUNTING_V6_IMPLEMENTATION_NOTES.md]] — score `14`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
