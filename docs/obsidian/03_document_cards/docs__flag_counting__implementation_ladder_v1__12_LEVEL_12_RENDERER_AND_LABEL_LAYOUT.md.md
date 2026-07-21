---
title: "Level 12 — Renderer / Labels / Visual Layer"
type: document_card
generated_by: alpha_lab_obsidian_builder
generated_at: 2026-07-06
source_path: "docs/flag_counting/implementation_ladder_v1/12_LEVEL_12_RENDERER_AND_LABEL_LAYOUT.md"
source_ext: ".md"
category: "flag_counting_docs"
source_size_bytes: "6166"
concepts:
  - "AI Agent Layer"
  - "Convexity"
  - "Execution"
  - "F-Counting"
  - "Hook"
  - "MQL Native"
  - "NDS Anatomy"
  - "Validation"
---


# Level 12 — Renderer / Labels / Visual Layer

**Source:** [[docs/flag_counting/implementation_ladder_v1/12_LEVEL_12_RENDERER_AND_LABEL_LAYOUT|docs/flag_counting/implementation_ladder_v1/12_LEVEL_12_RENDERER_AND_LABEL_LAYOUT.md]]

**Category:** `flag_counting_docs`  
**Status:** ok  
**Size:** `6166` bytes

## خلاصه

Level 12 turns the final Level 11 canonical stream into MetaTrader chart objects. It is a **visual product only**. It cannot create structure, delete structure, confirm structure, lock structure, change ownership, repair hidden reasons, or decide parent/child truth. Those decisions already belong to Levels 01 through 11. The renderer is allowed to do only these things: Export must be able to run even when renderer is visually disabled. Renderer output is never the source of truth. Renderer consumes: Renderer assumes: Renderer returns: `FP_RenderReport` counts: The report is folded into `FP_DetectResult` so `FP_SUMMARY` exposes render counts. Object names are derived from canonical identity b

## Headings

- Level 12 — Renderer / Labels / Visual Layer
-   Purpose
-   Owned source modules
-   Execution order
-   Input contract
-   Output contract
-   Object naming contract
-   Visibility contract
-   Curve contract
-     Flag body
-     Hook / ND
-   Label contract

## Concepts

- [[docs/obsidian/04_concepts/AI_Agent_Layer|AI Agent Layer]]
- [[docs/obsidian/04_concepts/Convexity|Convexity]]
- [[docs/obsidian/04_concepts/Execution|Execution]]
- [[docs/obsidian/04_concepts/F-Counting|F-Counting]]
- [[docs/obsidian/04_concepts/Hook|Hook]]
- [[docs/obsidian/04_concepts/MQL_Native|MQL Native]]
- [[docs/evidence/nds_anatomy/6a11c75733b2_NDS_Anatomy|NDS Anatomy]]
- [[docs/obsidian/04_concepts/Validation|Validation]]

## Related documents

- [[docs/flag_counting/implementation_ladder_v1/11_LEVEL_11_CANONICALIZATION_AND_AUDIT|Phoenix Flag Counting Implementation Ladder V1]] — `flag_counting_docs`
- [[docs/flag_counting/implementation_ladder_v1/15_MODULE_INTERFACE_CONTRACTS|Phoenix Flag Counting Implementation Ladder V1]] — `flag_counting_docs`
- [[docs/flag_counting/implementation_ladder_v1/16_IMPLEMENTATION_ORDER_AND_ACCEPTANCE_MATRIX|Phoenix Flag Counting Implementation Ladder V1]] — `flag_counting_docs`
- [[docs/flag_counting/implementation_ladder_v1/README|Phoenix Flag Counting Implementation Ladder V1]] — `flag_counting_docs`
- [[docs/flag_counting/implementation_ladder_v1/00_GOVERNANCE_AND_FREEZE_PROTOCOL|Phoenix Flag Counting Implementation Ladder V1]] — `flag_counting_docs`
- [[docs/flag_counting/implementation_ladder_v1/04_LEVEL_04_HOOK_ND_CONTEXT_ENGINE|Phoenix Flag Counting Implementation Ladder V1]] — `flag_counting_docs`
- [[docs/flag_counting/implementation_ladder_v1/10_LEVEL_10_SEQUENCE_OWNERSHIP_AND_PHASES|Phoenix Flag Counting Implementation Ladder V1]] — `flag_counting_docs`
- [[docs/flag_counting/implementation_ladder_v1/11_5_LEVEL_11_5_RAW_AUDIT_EXPORT|Level 11.5 — Raw Audit Export / Report Engine]] — `flag_counting_docs`
- [[docs/flag_counting/implementation_ladder_v1/14_LEVEL_14_RELEASE_ROLLBACK_AND_DEBUG_PROTOCOL|Phoenix Flag Counting Implementation Ladder V1]] — `flag_counting_docs`
- [[docs/ai_execution/AI_NATIVE_EXECUTION_ROADMAP_FA|AI Native Execution Roadmap — نقشه راه هوش مصنوعی، بک‌تست و پل اگزکیوت]] — `ai_execution_docs`
- [[docs/experience_capture/answers/NDS-R01/answer_normalized_en|NDS-R01 — Normalized Interpretation]] — `experience_capture_docs`
- [[docs/flag_counting/FLAG_COUNTING_CURRENT_CANON|Flag Counting Current Canon]] — `flag_counting_docs`

## Recommended Obsidian use

- این card را به نوت‌های concept، hypothesis، experiment یا ADR مربوط link کن.
- اگر این سند source of truth است، در MOC مربوطه بالاتر از اسناد legacy قرارش بده.
- اگر این سند report/validation است، نتیجه نهایی آن را به registry مربوط sync کن.
