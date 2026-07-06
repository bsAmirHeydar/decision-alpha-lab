---
title: "Status and Lifecycle Definition"
type: document_card
generated_by: alpha_lab_obsidian_builder
generated_at: 2026-07-06
source_path: "docs/flag_counting/engineering_pack_v5/02_definitions/STATUS_AND_LIFECYCLE_DEFINITION.md"
source_ext: ".md"
category: "flag_counting_docs"
source_size_bytes: "2603"
concepts:
  - "F-Counting"
  - "Hook"
  - "Validation"
---


# Status and Lifecycle Definition

**Source:** [[docs/flag_counting/engineering_pack_v5/02_definitions/STATUS_AND_LIFECYCLE_DEFINITION|docs/flag_counting/engineering_pack_v5/02_definitions/STATUS_AND_LIFECYCLE_DEFINITION.md]]

**Category:** `flag_counting_docs`  
**Status:** ok  
**Size:** `2603` bytes

## خلاصه

A partial structure that has not yet formed a complete body. F1 seed is hidden on main chart. F2/F3 seed may be displayed because it belongs to an existing confirmed parent context and helps debug stage progression. A possible body under construction. May have Origin/Leg1/Waist but no Leg2 yet. A complete two-leg body exists. For F1, this is the earliest display stage. The body exists and the engine is tracking post-flag internal numbering. This is where 1/2/3/4 and ND/Hook may appear. A child F object has a body but is waiting for size/scale qualification. F2 may wait for: F3 may wait for either OR condition: F1 or F2 only. F1 confirms after post-flag internal numbering and Leg2 re-pass wit

## Headings

- Status and Lifecycle Definition
-   Recommended Status Enum
-   SEED
-   BODY_CANDIDATE
-   LIVE_BODY
-   POST_FLAG_COUNTING
-   QUALIFYING
-   CONFIRMED
-   COMPLETED
-   EXTENDING
-   LOCKED
-   INVALIDATED

## Concepts

- [[docs/obsidian/04_concepts/F-Counting|F-Counting]]
- [[docs/obsidian/04_concepts/Hook|Hook]]
- [[docs/obsidian/04_concepts/Validation|Validation]]

## Related documents

- [[docs/flag_counting/engineering_pack_v5/02_definitions/F_LEVELS_DEFINITION|F-Level Definitions]] — `flag_counting_docs`
- [[docs/flag_counting/engineering_pack_v5/02_definitions/ND_HOOK_DEFINITION|ND / Hook Definition]] — `flag_counting_docs`
- [[docs/flag_counting/engineering_pack_v5/02_definitions/README|02 Definitions README]] — `flag_counting_docs`
- [[docs/flag_counting/engineering_pack_v5/02_definitions/SEQUENCE_IDENTITY_DEFINITION|Sequence Identity Definition]] — `flag_counting_docs`
- [[docs/ai_execution/AI_ALGORITHM_LAYER_MAP_FOR_EXTREME_ENGINE_FA|AI Algorithm Layer Map for Extreme Engine — نقشه الگوریتم‌های هوش مصنوعی برای اکستریم L2]] — `ai_execution_docs`
- [[docs/ai_execution/AI_NATIVE_EXECUTION_ROADMAP_FA|AI Native Execution Roadmap — نقشه راه هوش مصنوعی، بک‌تست و پل اگزکیوت]] — `ai_execution_docs`
- [[docs/ai_execution/AMIR_STRUCTURAL_EXPERIENCE_MAP_FA|Amir Structural Experience Map — نقشه تجربه‌های ساختاری امیر]] — `ai_execution_docs`
- [[docs/ai_execution/EXPERIENCE_CAPTURE_LOG_TEMPLATE_FA|Experience Capture Log Template — قالب ثبت تجربه‌های امیر]] — `ai_execution_docs`
- [[docs/debug/MARKET_LANGUAGE/README|DAL Market Language — Nodes, Cycles, Hooks, Rallies, Flags, 123 Flags, and Open 1/2s]] — `debug_docs`
- [[docs/experience_capture/answers/BASE-01/answer_normalized_en|BASE-01 — Normalized Interpretation]] — `experience_capture_docs`
- [[docs/experience_capture/answers/BASE-02/answer_normalized_en|BASE-02 — Normalized Interpretation]] — `experience_capture_docs`
- [[docs/experience_capture/answers/BASE-02/answer_raw_en|BASE-02 — Raw Answer]] — `experience_capture_docs`

## Recommended Obsidian use

- این card را به نوت‌های concept، hypothesis، experiment یا ADR مربوط link کن.
- اگر این سند source of truth است، در MOC مربوطه بالاتر از اسناد legacy قرارش بده.
- اگر این سند report/validation است، نتیجه نهایی آن را به registry مربوط sync کن.
