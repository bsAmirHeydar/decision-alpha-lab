---
title: "Flag Counting MQL5 Implementation"
type: document_card
generated_by: alpha_lab_obsidian_builder
generated_at: 2026-07-06
source_path: "docs/mql_native/FLAG_COUNTING_MQL5_IMPLEMENTATION.md"
source_ext: ".md"
category: "mql_native_docs"
source_size_bytes: "4317"
concepts:
  - "AI Agent Layer"
  - "Convexity"
  - "F-Counting"
  - "Hook"
  - "MQL Native"
  - "NDS Anatomy"
  - "Validation"
---


# Flag Counting MQL5 Implementation

**Source:** [[docs/mql_native/FLAG_COUNTING_MQL5_IMPLEMENTATION|docs/mql_native/FLAG_COUNTING_MQL5_IMPLEMENTATION.md]]

**Category:** `mql_native_docs`  
**Status:** ok  
**Size:** `4317` bytes

## خلاصه

Active expert: Reusable modules: The current detector is intended to be a multi-sequence counting engine, not a loose overlay scanner. Each `FC_FlagEvent` should carry enough information to audit: F1 is the root body. F1 validity: F1 lifecycle: Continuation levels inherit direction from the parent and start from the parent internal `2`. Continuation lifecycle: Continuation levels may break their own waist. A waist-break branch is interpreted as: After F1, the sequence waits for F2. After F2, it waits for F3. The child can be delayed or very large. The parent remains visible/live while the child is not yet complete. `InpContinuationCoreSearchMaxNodes = 0` means no small-window cap; search con

## Headings

- Flag Counting MQL5 Implementation
-   Architecture
-   Data contract
-   F1 implementation contract
-   F2/F3 implementation contract
-   Mandatory but live continuation
-   Fractal multi-sequence layer
-   Renderer
-   ND / Hook layer
-   Compile note
-   Visibility safety contract

## Concepts

- [[docs/obsidian/04_concepts/AI_Agent_Layer|AI Agent Layer]]
- [[docs/obsidian/04_concepts/Convexity|Convexity]]
- [[docs/obsidian/04_concepts/F-Counting|F-Counting]]
- [[docs/obsidian/04_concepts/Hook|Hook]]
- [[docs/obsidian/04_concepts/MQL_Native|MQL Native]]
- [[docs/evidence/nds_anatomy/6a11c75733b2_NDS_Anatomy|NDS Anatomy]]
- [[docs/obsidian/04_concepts/Validation|Validation]]

## Related documents

- [[docs/mql_native/H0007_FLAG_COUNTING_F1_START_STRUCTURE|H0007 — Flag Counting / F1 Start Structure]] — `mql_native_docs`
- [[docs/architecture|System Architecture]] — `core_docs`
- [[docs/ai_execution/AI_NATIVE_EXECUTION_ROADMAP_FA|AI Native Execution Roadmap — نقشه راه هوش مصنوعی، بک‌تست و پل اگزکیوت]] — `ai_execution_docs`
- [[docs/experience_capture/answers/NDS-R01/answer_normalized_en|NDS-R01 — Normalized Interpretation]] — `experience_capture_docs`
- [[docs/flag_counting/FLAG_COUNTING_CURRENT_CANON|Flag Counting Current Canon]] — `flag_counting_docs`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE11_ENTRY_BRIDGE_READINESS|Flag Counting Level 19 — Phase 11 Entry Bridge Readiness]] — `flag_counting_docs`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE12_EXTREME_CANDIDATE_MAP|Flag Counting Level 19 — Phase 12 Extreme Candidate Map]] — `flag_counting_docs`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE4_HOOK_VIEW_PROJECTION|Flag Counting Phoenix — Level 19 Phase 4 Hook View Projection]] — `flag_counting_docs`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_STATE_GATE_IMPLEMENTATION_PLAN|Flag Counting Level 19 — State Gate and Dashboard Implementation Plan]] — `flag_counting_docs`
- [[docs/flag_counting/FLAG_COUNTING_V6_IMPLEMENTATION_NOTES|Flag Counting V6 Implementation Notes]] — `flag_counting_docs`
- [[docs/flag_counting/implementation_ladder_v1/11_LEVEL_11_CANONICALIZATION_AND_AUDIT|Phoenix Flag Counting Implementation Ladder V1]] — `flag_counting_docs`
- [[docs/flag_counting/implementation_ladder_v1/12_LEVEL_12_RENDERER_AND_LABEL_LAYOUT|Level 12 — Renderer / Labels / Visual Layer]] — `flag_counting_docs`

## Recommended Obsidian use

- این card را به نوت‌های concept، hypothesis، experiment یا ADR مربوط link کن.
- اگر این سند source of truth است، در MOC مربوطه بالاتر از اسناد legacy قرارش بده.
- اگر این سند report/validation است، نتیجه نهایی آن را به registry مربوط sync کن.
