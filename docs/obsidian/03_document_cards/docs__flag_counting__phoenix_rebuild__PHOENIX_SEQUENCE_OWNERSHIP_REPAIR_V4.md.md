---
title: "Phoenix Sequence Ownership Repair V4"
type: document_card
generated_by: alpha_lab_obsidian_builder
generated_at: 2026-07-06
source_path: "docs/flag_counting/phoenix_rebuild/PHOENIX_SEQUENCE_OWNERSHIP_REPAIR_V4.md"
source_ext: ".md"
category: "flag_counting_docs"
source_size_bytes: "3078"
concepts:
  - "AI Agent Layer"
  - "Convexity"
  - "Execution"
  - "F-Counting"
  - "Hook"
  - "NDS Anatomy"
  - "Validation"
---


# Phoenix Sequence Ownership Repair V4

**Source:** [[docs/flag_counting/phoenix_rebuild/PHOENIX_SEQUENCE_OWNERSHIP_REPAIR_V4|docs/flag_counting/phoenix_rebuild/PHOENIX_SEQUENCE_OWNERSHIP_REPAIR_V4.md]]

**Category:** `flag_counting_docs`  
**Status:** ok  
**Size:** `3078` bytes

## خلاصه

The previous Phoenix repairs improved individual components, but they still left the main chart as a candidate enumeration layer. Hook/ND roots, raw fail-open roots, and multiple L-scales could all emit independent F1 roots in the middle of the same directional phase. This violated the sequence contract: Within one active directional phase, a later same-direction F1 is not allowed to become a new main-chart chain merely because a local Hook/ND or a lower-L body exists. The active chain is still doing work. The engine was doing the following: 1. Build Hook-derived roots. 2. Optionally build fail-open roots. 3. Build F1/F2/F3 chains from every root. 4. Try to clean the chart with duplicate-bod

## Headings

- Phoenix Sequence Ownership Repair V4
-   Failure that this patch addresses
-   Root cause
-   Correct contract
-   Implemented repair
-   Label discipline
-   What this patch does not change

## Concepts

- [[docs/obsidian/04_concepts/AI_Agent_Layer|AI Agent Layer]]
- [[docs/obsidian/04_concepts/Convexity|Convexity]]
- [[docs/obsidian/04_concepts/Execution|Execution]]
- [[docs/obsidian/04_concepts/F-Counting|F-Counting]]
- [[docs/obsidian/04_concepts/Hook|Hook]]
- [[docs/obsidian/04_concepts/NDS_Anatomy|NDS Anatomy]]
- [[docs/obsidian/04_concepts/Validation|Validation]]

## Related documents

- [[docs/flag_counting/phoenix_rebuild/PHOENIX_MAIN_CHART_CONTRACT_REPAIR_V3|Phoenix Main-Chart Contract Repair V3]] — `flag_counting_docs`
- [[docs/ai_execution/AI_ALGORITHM_LAYER_MAP_FOR_EXTREME_ENGINE_FA|AI Algorithm Layer Map for Extreme Engine — نقشه الگوریتم‌های هوش مصنوعی برای اکستریم L2]] — `ai_execution_docs`
- [[docs/ai_execution/AI_NATIVE_EXECUTION_ROADMAP_FA|AI Native Execution Roadmap — نقشه راه هوش مصنوعی، بک‌تست و پل اگزکیوت]] — `ai_execution_docs`
- [[docs/ai_execution/AMIR_STRUCTURAL_EXPERIENCE_MAP_FA|Amir Structural Experience Map — نقشه تجربه‌های ساختاری امیر]] — `ai_execution_docs`
- [[docs/ai_execution/EXPERIENCE_CAPTURE_LOG_TEMPLATE_FA|Experience Capture Log Template — قالب ثبت تجربه‌های امیر]] — `ai_execution_docs`
- [[docs/experience_capture/answers/EXT-01/answer_normalized_en|EXT-01 — Normalized Interpretation]] — `experience_capture_docs`
- [[docs/experience_capture/answers/NDS-R01/answer_normalized_en|NDS-R01 — Normalized Interpretation]] — `experience_capture_docs`
- [[docs/experience_capture/answers/SCN-R02/notes_en|SCN-R02 — Notes and Open Questions]] — `experience_capture_docs`
- [[docs/experience_capture/questions/README|Quant Lab Experience Capture Questionnaire]] — `experience_capture_docs`
- [[docs/flag_counting/FLAG_COUNTING_CURRENT_CANON|Flag Counting Current Canon]] — `flag_counting_docs`
- [[docs/flag_counting/FLAG_COUNTING_IMPLEMENTATION_CHECKLIST_V4|Flag Counting Implementation Checklist V4]] — `flag_counting_docs`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE11_ENTRY_BRIDGE_READINESS|Flag Counting Level 19 — Phase 11 Entry Bridge Readiness]] — `flag_counting_docs`

## Recommended Obsidian use

- این card را به نوت‌های concept، hypothesis، experiment یا ADR مربوط link کن.
- اگر این سند source of truth است، در MOC مربوطه بالاتر از اسناد legacy قرارش بده.
- اگر این سند report/validation است، نتیجه نهایی آن را به registry مربوط sync کن.
