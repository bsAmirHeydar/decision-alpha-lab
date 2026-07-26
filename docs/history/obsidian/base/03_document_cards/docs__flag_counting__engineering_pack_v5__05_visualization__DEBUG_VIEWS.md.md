---
title: "Debug Views"
type: document_card
generated_by: alpha_lab_obsidian_builder
generated_at: 2026-07-06
source_path: "docs/flag_counting/engineering_pack_v5/05_visualization/DEBUG_VIEWS.md"
source_ext: ".md"
category: "flag_counting_docs"
source_size_bytes: "2059"
concepts:
  - "AI Agent Layer"
  - "Convexity"
  - "F-Counting"
  - "Hook"
  - "NDS Anatomy"
  - "Validation"
---


# Debug Views

**Source:** [[docs/flag_counting/engineering_pack_v5/05_visualization/DEBUG_VIEWS|docs/flag_counting/engineering_pack_v5/05_visualization/DEBUG_VIEWS.md]]

**Category:** `flag_counting_docs`  
**Status:** ok  
**Size:** `2059` bytes

## خلاصه

The user wants to see all structures. But all structures must still be inspectable. A single chart can show all emitted structures if rendering is disciplined, but debugging also needs panels and modes. Even if default draws all structures, modes help diagnose. Default: Panel should not replace chart drawings. It should summarize: A file/CSV/log view should include transitions: When a suspicious line appears, answer: 1. Which object id owns it? 2. Which chain owns it? 3. Is it F1/F2/F3/ND? 4. Where are Origin, Leg1, Waist, Leg2? 5. Why is it alive? 6. What would invalidate it? 7. Was it emitted by logic engine or renderer? 8. Does audit log contain its creation event? If any answer is missin

## Headings

- Debug Views
-   Why Debug Views Are Needed
-   Recommended Inputs
-   View Modes
-   Status Panel
-   Audit Table
-   Visual Debug Checklist
-   Rejected View
-   ND Density Controls

## Concepts

- [[docs/obsidian/04_concepts/AI_Agent_Layer|AI Agent Layer]]
- [[docs/obsidian/04_concepts/Convexity|Convexity]]
- [[docs/obsidian/04_concepts/F-Counting|F-Counting]]
- [[docs/obsidian/04_concepts/Hook|Hook]]
- [[docs/evidence/nds_anatomy/6a11c75733b2_NDS_Anatomy|NDS Anatomy]]
- [[docs/obsidian/04_concepts/Validation|Validation]]

## Related documents

- [[docs/flag_counting/engineering_pack_v5/05_visualization/OBJECT_NAMING_AND_LAYERS|Object Naming and Layers]] — `flag_counting_docs`
- [[docs/ai_execution/AI_ALGORITHM_LAYER_MAP_FOR_EXTREME_ENGINE_FA|AI Algorithm Layer Map for Extreme Engine — نقشه الگوریتم‌های هوش مصنوعی برای اکستریم L2]] — `ai_execution_docs`
- [[docs/ai_execution/AI_NATIVE_EXECUTION_ROADMAP_FA|AI Native Execution Roadmap — نقشه راه هوش مصنوعی، بک‌تست و پل اگزکیوت]] — `ai_execution_docs`
- [[docs/ai_execution/AMIR_STRUCTURAL_EXPERIENCE_MAP_FA|Amir Structural Experience Map — نقشه تجربه‌های ساختاری امیر]] — `ai_execution_docs`
- [[docs/ai_execution/EXPERIENCE_CAPTURE_LOG_TEMPLATE_FA|Experience Capture Log Template — قالب ثبت تجربه‌های امیر]] — `ai_execution_docs`
- [[docs/experience_capture/answers/EXT-01/answer_normalized_en|EXT-01 — Normalized Interpretation]] — `experience_capture_docs`
- [[docs/experience_capture/answers/NDS-R01/answer_normalized_en|NDS-R01 — Normalized Interpretation]] — `experience_capture_docs`
- [[docs/experience_capture/answers/SCN-R02/notes_en|SCN-R02 — Notes and Open Questions]] — `experience_capture_docs`
- [[docs/experience_capture/questions/README|Quant Lab Experience Capture Questionnaire]] — `experience_capture_docs`
- [[docs/flag_counting/FLAG_COUNTING_CONCEPT_SPEC_V3|Flag Counting Concept Specification v3]] — `flag_counting_docs`
- [[docs/flag_counting/FLAG_COUNTING_CURRENT_CANON|Flag Counting Current Canon]] — `flag_counting_docs`
- [[docs/flag_counting/FLAG_COUNTING_IMPLEMENTATION_CHECKLIST_V4|Flag Counting Implementation Checklist V4]] — `flag_counting_docs`

## Recommended Obsidian use

- این card را به نوت‌های concept، hypothesis، experiment یا ADR مربوط link کن.
- اگر این سند source of truth است، در MOC مربوطه بالاتر از اسناد legacy قرارش بده.
- اگر این سند report/validation است، نتیجه نهایی آن را به registry مربوط sync کن.
