---
title: "Node and L Definition"
type: document_card
generated_by: alpha_lab_obsidian_builder
generated_at: 2026-07-06
source_path: "docs/flag_counting/engineering_pack_v5/02_definitions/NODE_AND_L_DEFINITION.md"
source_ext: ".md"
category: "flag_counting_docs"
source_size_bytes: "3288"
concepts:
  - "Convexity"
  - "F-Counting"
  - "NDS Anatomy"
---


# Node and L Definition

**Source:** [[docs/flag_counting/engineering_pack_v5/02_definitions/NODE_AND_L_DEFINITION|docs/flag_counting/engineering_pack_v5/02_definitions/NODE_AND_L_DEFINITION.md]]

**Category:** `flag_counting_docs`  
**Status:** ok  
**Size:** `3288` bytes

## خلاصه

The Flag Counting engine must reuse the existing project node module. Do not rewrite node logic locally inside Flag Counting unless the local implementation is a byte-for-byte or behavior-identical adapter of the project node logic. The structural inputs are: The following are not structural inputs: L is the minimum clearance count on both sides of a candidate high/low price. For a High node candidate at price `P`: For a Low node candidate at price `P`: Equality is special and must follow existing project plateau handling. Equal highs/lows are treated as one plateau-style node. High plateau: Low plateau: Important: equal-price bars inside or beside the plateau do not count as extra clearance

## Headings

- Node and L Definition
-   Source of Truth
-   Raw Inputs
-   L Definition
-   Equal Highs and Equal Lows
-   Node Stability
-   Node Identity
-   Strict Pass Logic
-   Tolerance
-   Node Views
-   Implementation Warning

## Concepts

- [[docs/obsidian/04_concepts/Convexity|Convexity]]
- [[docs/obsidian/04_concepts/F-Counting|F-Counting]]
- [[docs/evidence/nds_anatomy/6a11c75733b2_NDS_Anatomy|NDS Anatomy]]

## Related documents

- [[docs/flag_counting/engineering_pack_v5/02_definitions/F_LEVELS_DEFINITION|F-Level Definitions]] — `flag_counting_docs`
- [[docs/flag_counting/engineering_pack_v5/02_definitions/FLAG_BODY_DEFINITION|Flag Body Definition]] — `flag_counting_docs`
- [[docs/flag_counting/engineering_pack_v5/02_definitions/ND_HOOK_DEFINITION|ND / Hook Definition]] — `flag_counting_docs`
- [[docs/flag_counting/engineering_pack_v5/02_definitions/SEQUENCE_IDENTITY_DEFINITION|Sequence Identity Definition]] — `flag_counting_docs`
- [[docs/ai_execution/AI_ALGORITHM_LAYER_MAP_FOR_EXTREME_ENGINE_FA|AI Algorithm Layer Map for Extreme Engine — نقشه الگوریتم‌های هوش مصنوعی برای اکستریم L2]] — `ai_execution_docs`
- [[docs/ai_execution/AI_NATIVE_EXECUTION_ROADMAP_FA|AI Native Execution Roadmap — نقشه راه هوش مصنوعی، بک‌تست و پل اگزکیوت]] — `ai_execution_docs`
- [[docs/ai_execution/AMIR_STRUCTURAL_EXPERIENCE_MAP_FA|Amir Structural Experience Map — نقشه تجربه‌های ساختاری امیر]] — `ai_execution_docs`
- [[docs/ai_execution/EXPERIENCE_CAPTURE_LOG_TEMPLATE_FA|Experience Capture Log Template — قالب ثبت تجربه‌های امیر]] — `ai_execution_docs`
- [[docs/debug/E0008/README|E0008 — MTF Purple Extreme Executor]] — `debug_docs`
- [[docs/experience_capture/answers/DST-R01/notes_en|DST-R01 — Notes and Open Questions]] — `experience_capture_docs`
- [[docs/experience_capture/answers/DST-R01/question_en|DST-R01 — Destination Taxonomy and Open One-Two]] — `experience_capture_docs`
- [[docs/experience_capture/answers/DST-R03/answer_normalized_en|DST-R03 — Normalized Interpretation]] — `experience_capture_docs`

## Recommended Obsidian use

- این card را به نوت‌های concept، hypothesis، experiment یا ADR مربوط link کن.
- اگر این سند source of truth است، در MOC مربوطه بالاتر از اسناد legacy قرارش بده.
- اگر این سند report/validation است، نتیجه نهایی آن را به registry مربوط sync کن.
