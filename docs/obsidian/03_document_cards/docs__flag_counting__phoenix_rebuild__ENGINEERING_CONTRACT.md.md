---
title: "Engineering Contract: Phoenix Flag Counting"
type: document_card
generated_by: alpha_lab_obsidian_builder
generated_at: 2026-07-06
source_path: "docs/flag_counting/phoenix_rebuild/ENGINEERING_CONTRACT.md"
source_ext: ".md"
category: "flag_counting_docs"
source_size_bytes: "2479"
concepts:
  - "F-Counting"
  - "Hook"
  - "NDS Anatomy"
  - "Validation"
---


# Engineering Contract: Phoenix Flag Counting

**Source:** [[docs/flag_counting/phoenix_rebuild/ENGINEERING_CONTRACT|docs/flag_counting/phoenix_rebuild/ENGINEERING_CONTRACT.md]]

**Category:** `flag_counting_docs`  
**Status:** ok  
**Size:** `2479` bytes

## خلاصه

A node is extracted from high/low data only. `L` is the number of candles on each side that must not reach the node price. Equal highs/lows are collapsed into one plateau node. The anchor time is the last equal touch of the plateau. Equality is never a break. For a bullish boundary, price must move strictly below the boundary to break it. For a bearish boundary, price must move strictly above the boundary to break it. A flag body is the invariant object: Bullish: Origin is a low node. Leg1 is the highest high before the correction. Waist is the deepest correction low after Leg1 that does not break Origin. Leg2 is the high that breaks Leg1. Bearish is symmetric. F1 is displayed after the two-

## Headings

- Engineering Contract: Phoenix Flag Counting
-   Node contract
-   Flag body contract
-   F1 contract
-   F2 contract
-   F3 contract
-   Hook/ND contract
-   Renderer contract

## Concepts

- [[docs/obsidian/04_concepts/F-Counting|F-Counting]]
- [[docs/obsidian/04_concepts/Hook|Hook]]
- [[docs/obsidian/04_concepts/NDS_Anatomy|NDS Anatomy]]
- [[docs/obsidian/04_concepts/Validation|Validation]]

## Related documents

- [[docs/flag_counting/phoenix_rebuild/IMPLEMENTATION_NOTES|Phoenix Implementation Notes]] — `flag_counting_docs`
- [[docs/flag_counting/phoenix_rebuild/PHOENIX_MAIN_CHART_CONTRACT_REPAIR_V3|Phoenix Main-Chart Contract Repair V3]] — `flag_counting_docs`
- [[docs/flag_counting/phoenix_rebuild/PHOENIX_ROOT_CONTRACT_REPAIR_V2|Phoenix Root Contract Repair V2]] — `flag_counting_docs`
- [[docs/flag_counting/phoenix_rebuild/PHOENIX_SEQUENCE_OWNERSHIP_REPAIR_V4|Phoenix Sequence Ownership Repair V4]] — `flag_counting_docs`
- [[docs/flag_counting/phoenix_rebuild/README|Flag Counting Phoenix Rebuild]] — `flag_counting_docs`
- [[docs/ai_execution/AI_ALGORITHM_LAYER_MAP_FOR_EXTREME_ENGINE_FA|AI Algorithm Layer Map for Extreme Engine — نقشه الگوریتم‌های هوش مصنوعی برای اکستریم L2]] — `ai_execution_docs`
- [[docs/ai_execution/AI_NATIVE_EXECUTION_ROADMAP_FA|AI Native Execution Roadmap — نقشه راه هوش مصنوعی، بک‌تست و پل اگزکیوت]] — `ai_execution_docs`
- [[docs/ai_execution/AMIR_STRUCTURAL_EXPERIENCE_MAP_FA|Amir Structural Experience Map — نقشه تجربه‌های ساختاری امیر]] — `ai_execution_docs`
- [[docs/ai_execution/EXPERIENCE_CAPTURE_LOG_TEMPLATE_FA|Experience Capture Log Template — قالب ثبت تجربه‌های امیر]] — `ai_execution_docs`
- [[docs/debug/MARKET_LANGUAGE/README|DAL Market Language — Nodes, Cycles, Hooks, Rallies, Flags, 123 Flags, and Open 1/2s]] — `debug_docs`
- [[docs/experience_capture/answers/BASE-01/answer_normalized_en|BASE-01 — Normalized Interpretation]] — `experience_capture_docs`
- [[docs/experience_capture/answers/BASE-02/answer_normalized_en|BASE-02 — Normalized Interpretation]] — `experience_capture_docs`

## Recommended Obsidian use

- این card را به نوت‌های concept، hypothesis، experiment یا ADR مربوط link کن.
- اگر این سند source of truth است، در MOC مربوطه بالاتر از اسناد legacy قرارش بده.
- اگر این سند report/validation است، نتیجه نهایی آن را به registry مربوط sync کن.
