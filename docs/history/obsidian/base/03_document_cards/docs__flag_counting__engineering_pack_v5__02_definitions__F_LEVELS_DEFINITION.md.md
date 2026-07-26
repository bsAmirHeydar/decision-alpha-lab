---
title: "F-Level Definitions"
type: document_card
generated_by: alpha_lab_obsidian_builder
generated_at: 2026-07-06
source_path: "docs/flag_counting/engineering_pack_v5/02_definitions/F_LEVELS_DEFINITION.md"
source_ext: ".md"
category: "flag_counting_docs"
source_size_bytes: "4266"
concepts:
  - "F-Counting"
  - "Hook"
  - "NDS Anatomy"
  - "Validation"
---


# F-Level Definitions

**Source:** [[docs/flag_counting/engineering_pack_v5/02_definitions/F_LEVELS_DEFINITION|docs/flag_counting/engineering_pack_v5/02_definitions/F_LEVELS_DEFINITION.md]]

**Category:** `flag_counting_docs`  
**Status:** ok  
**Size:** `4266` bytes

## خلاصه

F1, F2, and F3 all use the same body geometry: Their differences are sequence role and post-body requirements. F1 is the first flag in a sequence. F1 must start from a valid phase boundary: terminal extreme of ND/Hook; end of opposite sequence; confirmed opposite F1 that locks previous F3 and starts a new opposite sequence; another explicitly owned phase boundary. F1 must not start from the middle of an active movement just because a local alternating window exists. F1 appears on chart after the probable two-leg body has been hit/completed. Before Leg2, it is only a seed and should not appear as F1 body on main chart. F1 confirms when: Bullish F1 confirms with: Bearish F1 confirms with: Befo

## Headings

- F-Level Definitions
-   Shared Body
-   F1 Definition
-     F1 Start
-     F1 Display
-     F1 Confirmation
-     F1 Invalidation
-   F2 Definition
-     F2 Authorization
-     F2 Origin
-     F2 Size
-     F2 Invalidation

## Concepts

- [[docs/obsidian/04_concepts/F-Counting|F-Counting]]
- [[docs/obsidian/04_concepts/Hook|Hook]]
- [[docs/evidence/nds_anatomy/6a11c75733b2_NDS_Anatomy|NDS Anatomy]]
- [[docs/obsidian/04_concepts/Validation|Validation]]

## Related documents

- [[docs/flag_counting/engineering_pack_v5/02_definitions/ND_HOOK_DEFINITION|ND / Hook Definition]] — `flag_counting_docs`
- [[docs/flag_counting/engineering_pack_v5/02_definitions/README|02 Definitions README]] — `flag_counting_docs`
- [[docs/flag_counting/engineering_pack_v5/02_definitions/SEQUENCE_IDENTITY_DEFINITION|Sequence Identity Definition]] — `flag_counting_docs`
- [[docs/flag_counting/engineering_pack_v5/02_definitions/STATUS_AND_LIFECYCLE_DEFINITION|Status and Lifecycle Definition]] — `flag_counting_docs`
- [[docs/ai_execution/AI_ALGORITHM_LAYER_MAP_FOR_EXTREME_ENGINE_FA|AI Algorithm Layer Map for Extreme Engine — نقشه الگوریتم‌های هوش مصنوعی برای اکستریم L2]] — `ai_execution_docs`
- [[docs/ai_execution/AI_NATIVE_EXECUTION_ROADMAP_FA|AI Native Execution Roadmap — نقشه راه هوش مصنوعی، بک‌تست و پل اگزکیوت]] — `ai_execution_docs`
- [[docs/ai_execution/AMIR_STRUCTURAL_EXPERIENCE_MAP_FA|Amir Structural Experience Map — نقشه تجربه‌های ساختاری امیر]] — `ai_execution_docs`
- [[docs/ai_execution/EXPERIENCE_CAPTURE_LOG_TEMPLATE_FA|Experience Capture Log Template — قالب ثبت تجربه‌های امیر]] — `ai_execution_docs`
- [[docs/debug/MARKET_LANGUAGE/README|DAL Market Language — Nodes, Cycles, Hooks, Rallies, Flags, 123 Flags, and Open 1/2s]] — `debug_docs`
- [[docs/experience_capture/answers/BASE-01/answer_normalized_en|BASE-01 — Normalized Interpretation]] — `experience_capture_docs`
- [[docs/experience_capture/answers/BASE-02/answer_normalized_en|BASE-02 — Normalized Interpretation]] — `experience_capture_docs`
- [[docs/experience_capture/answers/BASE-03/answer_normalized_en|BASE-03 — Normalized Interpretation]] — `experience_capture_docs`

## Recommended Obsidian use

- این card را به نوت‌های concept، hypothesis، experiment یا ADR مربوط link کن.
- اگر این سند source of truth است، در MOC مربوطه بالاتر از اسناد legacy قرارش بده.
- اگر این سند report/validation است، نتیجه نهایی آن را به registry مربوط sync کن.
