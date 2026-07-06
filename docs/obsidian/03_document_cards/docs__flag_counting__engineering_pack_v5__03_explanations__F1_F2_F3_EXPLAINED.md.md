---
title: "F1 / F2 / F3 Explained"
type: document_card
generated_by: alpha_lab_obsidian_builder
generated_at: 2026-07-06
source_path: "docs/flag_counting/engineering_pack_v5/03_explanations/F1_F2_F3_EXPLAINED.md"
source_ext: ".md"
category: "flag_counting_docs"
source_size_bytes: "4184"
concepts:
  - "F-Counting"
  - "Hook"
  - "NDS Anatomy"
  - "Validation"
---


# F1 / F2 / F3 Explained

**Source:** [[docs/flag_counting/engineering_pack_v5/03_explanations/F1_F2_F3_EXPLAINED|docs/flag_counting/engineering_pack_v5/03_explanations/F1_F2_F3_EXPLAINED.md]]

**Category:** `flag_counting_docs`  
**Status:** ok  
**Size:** `4184` bytes

## خلاصه

F1, F2, and F3 all have the same body: The difference is not the shape. The difference is what the market must do after that body and where the object lives in the sequence. F1 is the first flag of a chain. It must not begin in the middle of movement. It begins after a legitimate boundary, such as ND/Hook or opposite-sequence end. After F1 body forms, it must not be trusted immediately. It must produce post-flag internal correction numbering. Bullish F1: F1 invalidation uses Waist because F1 is fragile after its first body. If the correction after body passes the flag's Waist before confirmation, the F1 candidate failed. Why Waist, not Origin? Because F1's role is to prove that the post-flag

## Headings

- F1 / F2 / F3 Explained
-   Shared Body, Different Role
-   F1 Explained
-   F1 Leg2 Extension
-   F2 Explained
-   F3 Explained
-   Why F3 Must Persist
-   Debug lock — child-start rule after parent confirmation

## Concepts

- [[docs/obsidian/04_concepts/F-Counting|F-Counting]]
- [[docs/obsidian/04_concepts/Hook|Hook]]
- [[docs/obsidian/04_concepts/NDS_Anatomy|NDS Anatomy]]
- [[docs/obsidian/04_concepts/Validation|Validation]]

## Related documents

- [[docs/flag_counting/engineering_pack_v5/03_explanations/ANTI_PATTERNS_AND_FAILURES|Anti-Patterns and Failure Modes]] — `flag_counting_docs`
- [[docs/flag_counting/engineering_pack_v5/03_explanations/FLAG_COUNTING_EXPLAINED|Flag Counting Explained]] — `flag_counting_docs`
- [[docs/flag_counting/engineering_pack_v5/03_explanations/BACKFILL_AND_CONTEXT_EXPLAINED|Backfill and Context Explained]] — `flag_counting_docs`
- [[docs/ai_execution/AI_ALGORITHM_LAYER_MAP_FOR_EXTREME_ENGINE_FA|AI Algorithm Layer Map for Extreme Engine — نقشه الگوریتم‌های هوش مصنوعی برای اکستریم L2]] — `ai_execution_docs`
- [[docs/ai_execution/AI_NATIVE_EXECUTION_ROADMAP_FA|AI Native Execution Roadmap — نقشه راه هوش مصنوعی، بک‌تست و پل اگزکیوت]] — `ai_execution_docs`
- [[docs/ai_execution/AMIR_STRUCTURAL_EXPERIENCE_MAP_FA|Amir Structural Experience Map — نقشه تجربه‌های ساختاری امیر]] — `ai_execution_docs`
- [[docs/ai_execution/EXPERIENCE_CAPTURE_LOG_TEMPLATE_FA|Experience Capture Log Template — قالب ثبت تجربه‌های امیر]] — `ai_execution_docs`
- [[docs/debug/MARKET_LANGUAGE/README|DAL Market Language — Nodes, Cycles, Hooks, Rallies, Flags, 123 Flags, and Open 1/2s]] — `debug_docs`
- [[docs/experience_capture/answers/BASE-01/answer_normalized_en|BASE-01 — Normalized Interpretation]] — `experience_capture_docs`
- [[docs/experience_capture/answers/BASE-02/answer_normalized_en|BASE-02 — Normalized Interpretation]] — `experience_capture_docs`
- [[docs/experience_capture/answers/BASE-03/answer_normalized_en|BASE-03 — Normalized Interpretation]] — `experience_capture_docs`
- [[docs/experience_capture/answers/BASE-04/answer_normalized_en|BASE-04 — Normalized Interpretation]] — `experience_capture_docs`

## Recommended Obsidian use

- این card را به نوت‌های concept، hypothesis، experiment یا ADR مربوط link کن.
- اگر این سند source of truth است، در MOC مربوطه بالاتر از اسناد legacy قرارش بده.
- اگر این سند report/validation است، نتیجه نهایی آن را به registry مربوط sync کن.
