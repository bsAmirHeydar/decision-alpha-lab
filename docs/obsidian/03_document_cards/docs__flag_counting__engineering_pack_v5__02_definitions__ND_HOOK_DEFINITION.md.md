---
title: "ND / Hook Definition"
type: document_card
generated_by: alpha_lab_obsidian_builder
generated_at: 2026-07-06
source_path: "docs/flag_counting/engineering_pack_v5/02_definitions/ND_HOOK_DEFINITION.md"
source_ext: ".md"
category: "flag_counting_docs"
source_size_bytes: "2947"
concepts:
  - "AI Agent Layer"
  - "Execution"
  - "F-Counting"
  - "Hook"
  - "NDS Anatomy"
---


# ND / Hook Definition

**Source:** [[docs/flag_counting/engineering_pack_v5/02_definitions/ND_HOOK_DEFINITION|docs/flag_counting/engineering_pack_v5/02_definitions/ND_HOOK_DEFINITION.md]]

**Category:** `flag_counting_docs`  
**Status:** ok  
**Size:** `2947` bytes

## خلاصه

ND and Hook are one phase family in this contract. They describe multi-node correction/cycle behavior using high/low nodes only. ND/Hook is not based on candle close. ND/Hook can appear: after a flag body as post-flag correction; inside a larger active sequence; as a phase before F1; in overlapping contexts if separate logical contexts emit them. All ND/Hook structures are displayed by default. An input may restrict display to open sequence contexts: ND/Hook numbering uses adverse-side nodes. Bullish context: Bearish context: Two numbered adverse-side nodes are internal 1/2 only. They are not ND. Three or four numbered adverse-side nodes form ND/Hook if other requirements pass. These should

## Headings

- ND / Hook Definition
-   General Definition
-   Scope
-   Numbered Nodes
-   Two Nodes
-   Three or Four Nodes
-   More Than Four Nodes
-   Branching
-   ND 50% Cycle Rule
-   ND Rendering
-   ND and F Overlap

## Concepts

- [[docs/obsidian/04_concepts/AI_Agent_Layer|AI Agent Layer]]
- [[docs/obsidian/04_concepts/Execution|Execution]]
- [[docs/obsidian/04_concepts/F-Counting|F-Counting]]
- [[docs/obsidian/04_concepts/Hook|Hook]]
- [[docs/obsidian/04_concepts/NDS_Anatomy|NDS Anatomy]]

## Related documents

- [[docs/flag_counting/engineering_pack_v5/02_definitions/SEQUENCE_IDENTITY_DEFINITION|Sequence Identity Definition]] — `flag_counting_docs`
- [[docs/ai_execution/AI_ALGORITHM_LAYER_MAP_FOR_EXTREME_ENGINE_FA|AI Algorithm Layer Map for Extreme Engine — نقشه الگوریتم‌های هوش مصنوعی برای اکستریم L2]] — `ai_execution_docs`
- [[docs/ai_execution/AI_NATIVE_EXECUTION_ROADMAP_FA|AI Native Execution Roadmap — نقشه راه هوش مصنوعی، بک‌تست و پل اگزکیوت]] — `ai_execution_docs`
- [[docs/ai_execution/AMIR_STRUCTURAL_EXPERIENCE_MAP_FA|Amir Structural Experience Map — نقشه تجربه‌های ساختاری امیر]] — `ai_execution_docs`
- [[docs/ai_execution/EXPERIENCE_CAPTURE_LOG_TEMPLATE_FA|Experience Capture Log Template — قالب ثبت تجربه‌های امیر]] — `ai_execution_docs`
- [[docs/ai_execution/README|AI Execution Docs]] — `ai_execution_docs`
- [[docs/debug/E0008/README|E0008 — MTF Purple Extreme Executor]] — `debug_docs`
- [[docs/debug/MARKET_LANGUAGE/README|DAL Market Language — Nodes, Cycles, Hooks, Rallies, Flags, 123 Flags, and Open 1/2s]] — `debug_docs`
- [[docs/experience_capture/answers/BASE-01/answer_normalized_en|BASE-01 — Normalized Interpretation]] — `experience_capture_docs`
- [[docs/experience_capture/answers/BASE-04/answer_normalized_en|BASE-04 — Normalized Interpretation]] — `experience_capture_docs`
- [[docs/experience_capture/answers/BASE-06/answer_normalized_en|BASE-06 — Normalized Interpretation]] — `experience_capture_docs`
- [[docs/experience_capture/answers/DST-R01/notes_en|DST-R01 — Notes and Open Questions]] — `experience_capture_docs`

## Recommended Obsidian use

- این card را به نوت‌های concept، hypothesis، experiment یا ADR مربوط link کن.
- اگر این سند source of truth است، در MOC مربوطه بالاتر از اسناد legacy قرارش بده.
- اگر این سند report/validation است، نتیجه نهایی آن را به registry مربوط sync کن.
