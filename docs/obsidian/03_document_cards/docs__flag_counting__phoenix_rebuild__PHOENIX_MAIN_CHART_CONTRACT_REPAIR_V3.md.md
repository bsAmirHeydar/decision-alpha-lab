---
title: "Phoenix Main-Chart Contract Repair V3"
type: document_card
generated_by: alpha_lab_obsidian_builder
generated_at: 2026-07-06
source_path: "docs/flag_counting/phoenix_rebuild/PHOENIX_MAIN_CHART_CONTRACT_REPAIR_V3.md"
source_ext: ".md"
category: "flag_counting_docs"
source_size_bytes: "2513"
concepts:
  - "AI Agent Layer"
  - "Convexity"
  - "F-Counting"
  - "Hook"
  - "NDS Anatomy"
  - "Validation"
---


# Phoenix Main-Chart Contract Repair V3

**Source:** [[docs/flag_counting/phoenix_rebuild/PHOENIX_MAIN_CHART_CONTRACT_REPAIR_V3|docs/flag_counting/phoenix_rebuild/PHOENIX_MAIN_CHART_CONTRACT_REPAIR_V3.md]]

**Category:** `flag_counting_docs`  
**Status:** ok  
**Size:** `2513` bytes

## خلاصه

This repair re-separates the Phoenix engine into three hard layers: 1. **Structure layer**: F1/F2/F3 two-leg flag bodies are the primary chart structures. 2. **Context layer**: Hook/ND is a phase-boundary/context source. It must never erase valid flag structures. 3. **Presentation layer**: the main chart renders canonical visible structures only; audit labels remain optional. Hook/ND cannot be the only source of F roots. Hook-derived roots are built first, but raw-origin fail-open roots are also inspected when fail-open is enabled. Duplicate visual bodies are hidden after detection, not before the engine has a chance to recover valid F structures. F2 can only be emitted from a confirmed F1.

## Headings

- Phoenix Main-Chart Contract Repair V3
-   Red lines enforced
-   Main chart defaults
-   Audit mode
-   Canonicalization

## Concepts

- [[docs/obsidian/04_concepts/AI_Agent_Layer|AI Agent Layer]]
- [[docs/obsidian/04_concepts/Convexity|Convexity]]
- [[docs/obsidian/04_concepts/F-Counting|F-Counting]]
- [[docs/obsidian/04_concepts/Hook|Hook]]
- [[docs/obsidian/04_concepts/NDS_Anatomy|NDS Anatomy]]
- [[docs/obsidian/04_concepts/Validation|Validation]]

## Related documents

- [[docs/flag_counting/phoenix_rebuild/PHOENIX_SEQUENCE_OWNERSHIP_REPAIR_V4|Phoenix Sequence Ownership Repair V4]] — `flag_counting_docs`
- [[docs/flag_counting/phoenix_rebuild/IMPLEMENTATION_NOTES|Phoenix Implementation Notes]] — `flag_counting_docs`
- [[docs/flag_counting/phoenix_rebuild/PHOENIX_ROOT_CONTRACT_REPAIR_V2|Phoenix Root Contract Repair V2]] — `flag_counting_docs`
- [[docs/ai_execution/AI_ALGORITHM_LAYER_MAP_FOR_EXTREME_ENGINE_FA|AI Algorithm Layer Map for Extreme Engine — نقشه الگوریتم‌های هوش مصنوعی برای اکستریم L2]] — `ai_execution_docs`
- [[docs/ai_execution/AI_NATIVE_EXECUTION_ROADMAP_FA|AI Native Execution Roadmap — نقشه راه هوش مصنوعی، بک‌تست و پل اگزکیوت]] — `ai_execution_docs`
- [[docs/ai_execution/AMIR_STRUCTURAL_EXPERIENCE_MAP_FA|Amir Structural Experience Map — نقشه تجربه‌های ساختاری امیر]] — `ai_execution_docs`
- [[docs/ai_execution/EXPERIENCE_CAPTURE_LOG_TEMPLATE_FA|Experience Capture Log Template — قالب ثبت تجربه‌های امیر]] — `ai_execution_docs`
- [[docs/experience_capture/answers/EXT-01/answer_normalized_en|EXT-01 — Normalized Interpretation]] — `experience_capture_docs`
- [[docs/experience_capture/answers/NDS-R01/answer_normalized_en|NDS-R01 — Normalized Interpretation]] — `experience_capture_docs`
- [[docs/experience_capture/answers/SCN-R02/notes_en|SCN-R02 — Notes and Open Questions]] — `experience_capture_docs`
- [[docs/experience_capture/questions/README|Quant Lab Experience Capture Questionnaire]] — `experience_capture_docs`
- [[docs/flag_counting/engineering_pack_v5/05_visualization/DEBUG_VIEWS|Debug Views]] — `flag_counting_docs`

## Recommended Obsidian use

- این card را به نوت‌های concept، hypothesis، experiment یا ADR مربوط link کن.
- اگر این سند source of truth است، در MOC مربوطه بالاتر از اسناد legacy قرارش بده.
- اگر این سند report/validation است، نتیجه نهایی آن را به registry مربوط sync کن.
