---
title: "F1 / F2 / F3 Algorithms"
type: document_card
generated_by: alpha_lab_obsidian_builder
generated_at: 2026-07-06
source_path: "docs/flag_counting/engineering_pack_v5/04_algorithms/F1_F2_F3_ALGORITHMS.md"
source_ext: ".md"
category: "flag_counting_docs"
source_size_bytes: "3979"
concepts:
  - "F-Counting"
  - "Hook"
  - "NDS Anatomy"
  - "Validation"
---


# F1 / F2 / F3 Algorithms

**Source:** [[docs/flag_counting/engineering_pack_v5/04_algorithms/F1_F2_F3_ALGORITHMS|docs/flag_counting/engineering_pack_v5/04_algorithms/F1_F2_F3_ALGORITHMS.md]]

**Category:** `flag_counting_docs`  
**Status:** ok  
**Size:** `3979` bytes

## خلاصه

After Leg2: Bullish deepest adverse: Bearish deepest adverse: If no valid internal 1/2 exists and price passes Leg2 again: Before confirmation: Only after F1 confirmed. Use FlagBodyBuilder from F2 origin. F2 seed may be shown. Then: If after F2 body the correction passes F2 Waist but not F2 Origin: Continue branch logic into 3/4 if present. Only after F2 confirmed. Backfill Origin into the F2 correction window, force Leg1 to the F2 confirmation node, then use normal FlagBodyBuilder rules for Waist and Leg2 after F2 confirmation. F3 seed/leg development may be shown, but incomplete bodies cannot be terminal. If `condA OR condB`: Else: After completion: For child flags F2 and F3, only the chil

## Headings

- F1 / F2 / F3 Algorithms
-   F1 Algorithm
-     Create F1
-     Show F1
-     Track Post-F1 Context
-     F1 Extension
-     F1 Invalidation
-     F1 Confirmation
-   F2 Algorithm
-     Authorize F2
-     Build F2
-     F2 Qualification

## Concepts

- [[docs/obsidian/04_concepts/F-Counting|F-Counting]]
- [[docs/obsidian/04_concepts/Hook|Hook]]
- [[docs/obsidian/04_concepts/NDS_Anatomy|NDS Anatomy]]
- [[docs/obsidian/04_concepts/Validation|Validation]]

## Related documents

- [[docs/flag_counting/engineering_pack_v5/04_algorithms/DEDUP_AUDIT_ALGORITHM|Dedup and Audit Algorithm]] — `flag_counting_docs`
- [[docs/flag_counting/engineering_pack_v5/04_algorithms/MODULE_ARCHITECTURE|Module Architecture]] — `flag_counting_docs`
- [[docs/flag_counting/engineering_pack_v5/04_algorithms/NODE_ENGINE_ALGORITHM|Node Engine Algorithm]] — `flag_counting_docs`
- [[docs/flag_counting/engineering_pack_v5/04_algorithms/README|04 Algorithms README]] — `flag_counting_docs`
- [[docs/flag_counting/engineering_pack_v5/04_algorithms/SEQUENCE_ENGINE_ALGORITHM|Sequence Engine Algorithm]] — `flag_counting_docs`
- [[docs/flag_counting/engineering_pack_v5/04_algorithms/HOOK_BRANCH_ENGINE_ALGORITHM|Hook Branch Engine Algorithm]] — `flag_counting_docs`
- [[docs/flag_counting/engineering_pack_v5/04_algorithms/PSEUDOCODE_REFERENCE|Pseudocode Reference]] — `flag_counting_docs`
- [[docs/ai_execution/AI_ALGORITHM_LAYER_MAP_FOR_EXTREME_ENGINE_FA|AI Algorithm Layer Map for Extreme Engine — نقشه الگوریتم‌های هوش مصنوعی برای اکستریم L2]] — `ai_execution_docs`
- [[docs/ai_execution/AI_NATIVE_EXECUTION_ROADMAP_FA|AI Native Execution Roadmap — نقشه راه هوش مصنوعی، بک‌تست و پل اگزکیوت]] — `ai_execution_docs`
- [[docs/ai_execution/AMIR_STRUCTURAL_EXPERIENCE_MAP_FA|Amir Structural Experience Map — نقشه تجربه‌های ساختاری امیر]] — `ai_execution_docs`
- [[docs/ai_execution/EXPERIENCE_CAPTURE_LOG_TEMPLATE_FA|Experience Capture Log Template — قالب ثبت تجربه‌های امیر]] — `ai_execution_docs`
- [[docs/debug/MARKET_LANGUAGE/README|DAL Market Language — Nodes, Cycles, Hooks, Rallies, Flags, 123 Flags, and Open 1/2s]] — `debug_docs`

## Recommended Obsidian use

- این card را به نوت‌های concept، hypothesis، experiment یا ADR مربوط link کن.
- اگر این سند source of truth است، در MOC مربوطه بالاتر از اسناد legacy قرارش بده.
- اگر این سند report/validation است، نتیجه نهایی آن را به registry مربوط sync کن.
