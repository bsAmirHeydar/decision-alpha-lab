---
title: "Hook / ND Branch Algorithm V1"
type: document_card
generated_by: alpha_lab_obsidian_builder
generated_at: 2026-07-06
source_path: "docs/flag_counting/phoenix_rebuild/hook_nd_branching/HOOK_ND_BRANCH_ALGORITHM_V1.md"
source_ext: ".md"
category: "flag_counting_docs"
source_size_bytes: "11740"
concepts:
  - "AI Agent Layer"
  - "Convexity"
  - "F-Counting"
  - "Hook"
  - "NDS Anatomy"
  - "Rally"
  - "Validation"
---


# Hook / ND Branch Algorithm V1

**Source:** [[docs/flag_counting/phoenix_rebuild/hook_nd_branching/HOOK_ND_BRANCH_ALGORITHM_V1|docs/flag_counting/phoenix_rebuild/hook_nd_branching/HOOK_ND_BRANCH_ALGORITHM_V1.md]]

**Category:** `flag_counting_docs`  
**Status:** ok  
**Size:** `11740` bytes

## خلاصه

This document converts the Hook / ND branch-sequence contract into a deterministic implementation algorithm. The goal is to produce a list of Hook containers. Each Hook container can contain many branch sequences. Each branch sequence contains one to four counted same-side nodes after adaptive L normalization. A Hook qualifies as ND only when at least one branch has exactly three or four counted nodes and passes the retracement rule. For each symbol, timeframe, direction side, and L: Node engine output must include: The high-side implementation is the mirror of low-side implementation. Important: increasing L requires rebuilding nodes and branches. Do not just remove extra branch nodes. For

## Headings

- Hook / ND Branch Algorithm V1
-   1. Goal
-   2. Inputs
-   3. Direction mapping
-     3.1 Low-side Hook
-     3.2 High-side Hook
-   4. Main adaptive loop
-   5. Building Hook contexts at one L
-   6. Finding the origin boundary
-     6.1 Low-side Hook
-     6.2 High-side Hook
-   7. Branch extraction model

## Concepts

- [[docs/obsidian/04_concepts/AI_Agent_Layer|AI Agent Layer]]
- [[docs/obsidian/04_concepts/Convexity|Convexity]]
- [[docs/obsidian/04_concepts/F-Counting|F-Counting]]
- [[docs/obsidian/04_concepts/Hook|Hook]]
- [[docs/obsidian/04_concepts/NDS_Anatomy|NDS Anatomy]]
- [[docs/obsidian/04_concepts/Rally|Rally]]
- [[docs/obsidian/04_concepts/Validation|Validation]]

## Related documents

- [[docs/flag_counting/phoenix_rebuild/hook_nd_branching/HOOK_ND_BRANCH_SEQUENCE_CONTRACT_V1|Hook / ND Branch-Sequence Contract V1]] — `flag_counting_docs`
- [[docs/experience_capture/questions/remaining_v3_split/index_en|Remaining Questions v3 Split Index]] — `experience_capture_docs`
- [[docs/flag_counting/phoenix_rebuild/hook_nd_branching/HOOK_ND_IMPLEMENTATION_CHECKLIST_V1|Hook / ND Implementation Checklist V1]] — `flag_counting_docs`
- [[docs/ai_execution/AI_ALGORITHM_LAYER_MAP_FOR_EXTREME_ENGINE_FA|AI Algorithm Layer Map for Extreme Engine — نقشه الگوریتم‌های هوش مصنوعی برای اکستریم L2]] — `ai_execution_docs`
- [[docs/ai_execution/AI_NATIVE_EXECUTION_ROADMAP_FA|AI Native Execution Roadmap — نقشه راه هوش مصنوعی، بک‌تست و پل اگزکیوت]] — `ai_execution_docs`
- [[docs/ai_execution/AMIR_STRUCTURAL_EXPERIENCE_MAP_FA|Amir Structural Experience Map — نقشه تجربه‌های ساختاری امیر]] — `ai_execution_docs`
- [[docs/ai_execution/EXPERIENCE_CAPTURE_LOG_TEMPLATE_FA|Experience Capture Log Template — قالب ثبت تجربه‌های امیر]] — `ai_execution_docs`
- [[docs/experience_capture/answers/EXT-01/answer_normalized_en|EXT-01 — Normalized Interpretation]] — `experience_capture_docs`
- [[docs/experience_capture/answers/NDS-R01/answer_normalized_en|NDS-R01 — Normalized Interpretation]] — `experience_capture_docs`
- [[docs/experience_capture/questions/README|Quant Lab Experience Capture Questionnaire]] — `experience_capture_docs`
- [[docs/flag_counting/FLAG_COUNTING_CONCEPT_SPEC_V3|Flag Counting Concept Specification v3]] — `flag_counting_docs`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE11_ENTRY_BRIDGE_READINESS|Flag Counting Level 19 — Phase 11 Entry Bridge Readiness]] — `flag_counting_docs`

## Recommended Obsidian use

- این card را به نوت‌های concept، hypothesis، experiment یا ADR مربوط link کن.
- اگر این سند source of truth است، در MOC مربوطه بالاتر از اسناد legacy قرارش بده.
- اگر این سند report/validation است، نتیجه نهایی آن را به registry مربوط sync کن.
