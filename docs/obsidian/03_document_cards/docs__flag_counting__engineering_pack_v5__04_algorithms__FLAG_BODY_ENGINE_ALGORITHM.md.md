---
title: "Flag Body Engine Algorithm"
type: document_card
generated_by: alpha_lab_obsidian_builder
generated_at: 2026-07-06
source_path: "docs/flag_counting/engineering_pack_v5/04_algorithms/FLAG_BODY_ENGINE_ALGORITHM.md"
source_ext: ".md"
category: "flag_counting_docs"
source_size_bytes: "2240"
concepts:
  - "F-Counting"
  - "NDS Anatomy"
---


# Flag Body Engine Algorithm

**Source:** [[docs/flag_counting/engineering_pack_v5/04_algorithms/FLAG_BODY_ENGINE_ALGORITHM|docs/flag_counting/engineering_pack_v5/04_algorithms/FLAG_BODY_ENGINE_ALGORITHM.md]]

**Category:** `flag_counting_docs`  
**Status:** ok  
**Size:** `2240` bytes

## خلاصه

Build two-leg body candidates from owned context. Do not assign F-level confirmation here. This module only builds body geometry. Initialize: Process nodes chronologically. Track highest high after origin. When a low correction appears after at least one high: If low correction passes origin: Update waist while deeper lows appear: If low passes origin: If high passes leg1: Symmetric. Track lowest low after origin. When a high correction appears after at least one low: If high correction passes origin: Update waist while higher highs appear: If high passes origin: If low passes leg1: For F1 before valid post-body 1/2 exists: Bullish: Bearish: For F2/F3 candidates that need size/qualification:

## Headings

- Flag Body Engine Algorithm
-   Purpose
-   Inputs
-   Bullish Body Builder
-     SEEK_LEG1
-     SEEK_LEG2
-   Bearish Body Builder
-     SEEK_LEG1
-     SEEK_LEG2
-   Leg2 Extension
-   Output
-   Main Failure Guard

## Concepts

- [[docs/obsidian/04_concepts/F-Counting|F-Counting]]
- [[docs/evidence/nds_anatomy/6a11c75733b2_NDS_Anatomy|NDS Anatomy]]

## Related documents

- [[docs/flag_counting/engineering_pack_v5/04_algorithms/DEDUP_AUDIT_ALGORITHM|Dedup and Audit Algorithm]] — `flag_counting_docs`
- [[docs/flag_counting/engineering_pack_v5/04_algorithms/F1_F2_F3_ALGORITHMS|F1 / F2 / F3 Algorithms]] — `flag_counting_docs`
- [[docs/flag_counting/engineering_pack_v5/04_algorithms/HOOK_BRANCH_ENGINE_ALGORITHM|Hook Branch Engine Algorithm]] — `flag_counting_docs`
- [[docs/flag_counting/engineering_pack_v5/04_algorithms/MODULE_ARCHITECTURE|Module Architecture]] — `flag_counting_docs`
- [[docs/flag_counting/engineering_pack_v5/04_algorithms/NODE_ENGINE_ALGORITHM|Node Engine Algorithm]] — `flag_counting_docs`
- [[docs/flag_counting/engineering_pack_v5/04_algorithms/PSEUDOCODE_REFERENCE|Pseudocode Reference]] — `flag_counting_docs`
- [[docs/flag_counting/engineering_pack_v5/04_algorithms/README|04 Algorithms README]] — `flag_counting_docs`
- [[docs/flag_counting/engineering_pack_v5/04_algorithms/SEQUENCE_ENGINE_ALGORITHM|Sequence Engine Algorithm]] — `flag_counting_docs`
- [[docs/ai_execution/AI_ALGORITHM_LAYER_MAP_FOR_EXTREME_ENGINE_FA|AI Algorithm Layer Map for Extreme Engine — نقشه الگوریتم‌های هوش مصنوعی برای اکستریم L2]] — `ai_execution_docs`
- [[docs/ai_execution/AI_NATIVE_EXECUTION_ROADMAP_FA|AI Native Execution Roadmap — نقشه راه هوش مصنوعی، بک‌تست و پل اگزکیوت]] — `ai_execution_docs`
- [[docs/ai_execution/AMIR_STRUCTURAL_EXPERIENCE_MAP_FA|Amir Structural Experience Map — نقشه تجربه‌های ساختاری امیر]] — `ai_execution_docs`
- [[docs/ai_execution/EXPERIENCE_CAPTURE_LOG_TEMPLATE_FA|Experience Capture Log Template — قالب ثبت تجربه‌های امیر]] — `ai_execution_docs`

## Recommended Obsidian use

- این card را به نوت‌های concept، hypothesis، experiment یا ADR مربوط link کن.
- اگر این سند source of truth است، در MOC مربوطه بالاتر از اسناد legacy قرارش بده.
- اگر این سند report/validation است، نتیجه نهایی آن را به registry مربوط sync کن.
