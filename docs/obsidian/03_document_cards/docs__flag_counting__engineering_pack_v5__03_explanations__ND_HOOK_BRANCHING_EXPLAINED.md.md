---
title: "ND / Hook Branching Explained"
type: document_card
generated_by: alpha_lab_obsidian_builder
generated_at: 2026-07-06
source_path: "docs/flag_counting/engineering_pack_v5/03_explanations/ND_HOOK_BRANCHING_EXPLAINED.md"
source_ext: ".md"
category: "flag_counting_docs"
source_size_bytes: "2455"
concepts:
  - "AI Agent Layer"
  - "Execution"
  - "Hook"
  - "NDS Anatomy"
---


# ND / Hook Branching Explained

**Source:** [[docs/flag_counting/engineering_pack_v5/03_explanations/ND_HOOK_BRANCHING_EXPLAINED|docs/flag_counting/engineering_pack_v5/03_explanations/ND_HOOK_BRANCHING_EXPLAINED.md]]

**Category:** `flag_counting_docs`  
**Status:** ok  
**Size:** `2455` bytes

## خلاصه

Post-flag correction is not always a simple sequence: There can be multiple possible `1` nodes, and one later `2` can validate more than one earlier `1`. This is why hook logic cannot be a single linear counter. In a bullish post-flag correction, numbered nodes are lows. Imagine these lows appear: L1 can be a `1`. L2, being higher, can also be a new `1` in another branch. L3 passes below both L1 and L2. Therefore L3 can serve as `2` for both branches. L4 is higher again and can become a new `1` branch. The structure is not one counter. It is multiple hook branches. A practical way to count is from the latest adverse node backward. For bullish lows: 1. Start from a current low. 2. Move backwa

## Headings

- ND / Hook Branching Explained
-   Why Hook Counting Is Branchable
-   Bullish Example
-   End-Backward Counting
-   Why L Must Increase
-   ND Qualification
-   Why ND Can Overlap F
-   Why We Do Not Draw the 50% Line

## Concepts

- [[docs/obsidian/04_concepts/AI_Agent_Layer|AI Agent Layer]]
- [[docs/obsidian/04_concepts/Execution|Execution]]
- [[docs/obsidian/04_concepts/Hook|Hook]]
- [[docs/obsidian/04_concepts/NDS_Anatomy|NDS Anatomy]]

## Related documents

- [[docs/flag_counting/engineering_pack_v5/03_explanations/ANTI_PATTERNS_AND_FAILURES|Anti-Patterns and Failure Modes]] — `flag_counting_docs`
- [[docs/flag_counting/engineering_pack_v5/03_explanations/FLAG_COUNTING_EXPLAINED|Flag Counting Explained]] — `flag_counting_docs`
- [[docs/ai_execution/AI_ALGORITHM_LAYER_MAP_FOR_EXTREME_ENGINE_FA|AI Algorithm Layer Map for Extreme Engine — نقشه الگوریتم‌های هوش مصنوعی برای اکستریم L2]] — `ai_execution_docs`
- [[docs/ai_execution/AI_NATIVE_EXECUTION_ROADMAP_FA|AI Native Execution Roadmap — نقشه راه هوش مصنوعی، بک‌تست و پل اگزکیوت]] — `ai_execution_docs`
- [[docs/ai_execution/AMIR_STRUCTURAL_EXPERIENCE_MAP_FA|Amir Structural Experience Map — نقشه تجربه‌های ساختاری امیر]] — `ai_execution_docs`
- [[docs/ai_execution/EXPERIENCE_CAPTURE_LOG_TEMPLATE_FA|Experience Capture Log Template — قالب ثبت تجربه‌های امیر]] — `ai_execution_docs`
- [[docs/ai_execution/EXTREME_L2_NODE_CYCLE_LIMIT_ENTRY_FA|Extreme L2 Node Cycle Limit Entry — تعریف رسمی اکستریم، نود L2 و ورود لیمیت]] — `ai_execution_docs`
- [[docs/ai_execution/README|AI Execution Docs]] — `ai_execution_docs`
- [[docs/debug/E0007/README|E0007 — Purple Source Extreme Executor Template]] — `debug_docs`
- [[docs/debug/E0008/README|E0008 — MTF Purple Extreme Executor]] — `debug_docs`
- [[docs/debug/MARKET_LANGUAGE/README|DAL Market Language — Nodes, Cycles, Hooks, Rallies, Flags, 123 Flags, and Open 1/2s]] — `debug_docs`
- [[docs/experience_capture/answers/BASE-01/answer_normalized_en|BASE-01 — Normalized Interpretation]] — `experience_capture_docs`

## Recommended Obsidian use

- این card را به نوت‌های concept، hypothesis، experiment یا ADR مربوط link کن.
- اگر این سند source of truth است، در MOC مربوطه بالاتر از اسناد legacy قرارش بده.
- اگر این سند report/validation است، نتیجه نهایی آن را به registry مربوط sync کن.
