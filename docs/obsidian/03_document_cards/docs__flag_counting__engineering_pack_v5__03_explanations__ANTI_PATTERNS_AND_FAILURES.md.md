---
title: "Anti-Patterns and Failure Modes"
type: document_card
generated_by: alpha_lab_obsidian_builder
generated_at: 2026-07-06
source_path: "docs/flag_counting/engineering_pack_v5/03_explanations/ANTI_PATTERNS_AND_FAILURES.md"
source_ext: ".md"
category: "flag_counting_docs"
source_size_bytes: "2739"
concepts:
  - "AI Agent Layer"
  - "F-Counting"
  - "Hook"
  - "NDS Anatomy"
  - "Validation"
---


# Anti-Patterns and Failure Modes

**Source:** [[docs/flag_counting/engineering_pack_v5/03_explanations/ANTI_PATTERNS_AND_FAILURES|docs/flag_counting/engineering_pack_v5/03_explanations/ANTI_PATTERNS_AND_FAILURES.md]]

**Category:** `flag_counting_docs`  
**Status:** ok  
**Size:** `2739` bytes

## خلاصه

This file lists mistakes that previously produced wrong charts. Wrong: Why wrong: no phase boundary; no ownership; can start in middle of move; creates orphan lines; restarts F1 even while chain should search for F2/F3. Correct: Wrong: Correct: Wrong: Correct: Wrong: Correct: Wrong: Correct: Wrong: Correct: Wrong: Correct: Wrong: Correct: Wrong: Correct: Wrong: Correct research label: Wrong: Result: chart becomes empty and cannot debug stage logic. Correct: Wrong: Correct:

## Headings

- Anti-Patterns and Failure Modes
-   Failure 1: Sliding-Window F1
-   Failure 2: First Correction Used as Waist
-   Failure 3: Killing Parent When Child Dies
-   Failure 4: Abandoning F2 Search
-   Failure 5: Rejecting F2/F3 Too Early
-   Failure 6: Using Close Logic
-   Failure 7: Equality as Break
-   Failure 8: Renderer Invents Lines
-   Failure 9: Broken Curve Approximation
-   Failure 10: Untraceable Labels
-   Failure 11: Hiding All Live Roots

## Concepts

- [[docs/obsidian/04_concepts/AI_Agent_Layer|AI Agent Layer]]
- [[docs/obsidian/04_concepts/F-Counting|F-Counting]]
- [[docs/obsidian/04_concepts/Hook|Hook]]
- [[docs/evidence/nds_anatomy/6a11c75733b2_NDS_Anatomy|NDS Anatomy]]
- [[docs/obsidian/04_concepts/Validation|Validation]]

## Related documents

- [[docs/flag_counting/engineering_pack_v5/03_explanations/FLAG_COUNTING_EXPLAINED|Flag Counting Explained]] — `flag_counting_docs`
- [[docs/flag_counting/engineering_pack_v5/03_explanations/F1_F2_F3_EXPLAINED|F1 / F2 / F3 Explained]] — `flag_counting_docs`
- [[docs/ai_execution/AI_ALGORITHM_LAYER_MAP_FOR_EXTREME_ENGINE_FA|AI Algorithm Layer Map for Extreme Engine — نقشه الگوریتم‌های هوش مصنوعی برای اکستریم L2]] — `ai_execution_docs`
- [[docs/ai_execution/AI_NATIVE_EXECUTION_ROADMAP_FA|AI Native Execution Roadmap — نقشه راه هوش مصنوعی، بک‌تست و پل اگزکیوت]] — `ai_execution_docs`
- [[docs/ai_execution/AMIR_STRUCTURAL_EXPERIENCE_MAP_FA|Amir Structural Experience Map — نقشه تجربه‌های ساختاری امیر]] — `ai_execution_docs`
- [[docs/ai_execution/EXPERIENCE_CAPTURE_LOG_TEMPLATE_FA|Experience Capture Log Template — قالب ثبت تجربه‌های امیر]] — `ai_execution_docs`
- [[docs/debug/MARKET_LANGUAGE/README|DAL Market Language — Nodes, Cycles, Hooks, Rallies, Flags, 123 Flags, and Open 1/2s]] — `debug_docs`
- [[docs/experience_capture/answers/BASE-01/answer_normalized_en|BASE-01 — Normalized Interpretation]] — `experience_capture_docs`
- [[docs/experience_capture/answers/BASE-04/answer_normalized_en|BASE-04 — Normalized Interpretation]] — `experience_capture_docs`
- [[docs/experience_capture/answers/BASE-06/answer_normalized_en|BASE-06 — Normalized Interpretation]] — `experience_capture_docs`
- [[docs/experience_capture/answers/EXT-01/answer_normalized_en|EXT-01 — Normalized Interpretation]] — `experience_capture_docs`
- [[docs/experience_capture/answers/NDS-R01/answer_normalized_en|NDS-R01 — Normalized Interpretation]] — `experience_capture_docs`

## Recommended Obsidian use

- این card را به نوت‌های concept، hypothesis، experiment یا ADR مربوط link کن.
- اگر این سند source of truth است، در MOC مربوطه بالاتر از اسناد legacy قرارش بده.
- اگر این سند report/validation است، نتیجه نهایی آن را به registry مربوط sync کن.
