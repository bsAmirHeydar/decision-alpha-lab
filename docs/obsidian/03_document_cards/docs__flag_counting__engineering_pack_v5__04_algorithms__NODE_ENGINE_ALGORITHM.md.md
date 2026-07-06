---
title: "Node Engine Algorithm"
type: document_card
generated_by: alpha_lab_obsidian_builder
generated_at: 2026-07-06
source_path: "docs/flag_counting/engineering_pack_v5/04_algorithms/NODE_ENGINE_ALGORITHM.md"
source_ext: ".md"
category: "flag_counting_docs"
source_size_bytes: "1783"
concepts:
  - "Execution"
  - "F-Counting"
  - "Hook"
  - "NDS Anatomy"
  - "Validation"
---


# Node Engine Algorithm

**Source:** [[docs/flag_counting/engineering_pack_v5/04_algorithms/NODE_ENGINE_ALGORITHM|docs/flag_counting/engineering_pack_v5/04_algorithms/NODE_ENGINE_ALGORITHM.md]]

**Category:** `flag_counting_docs`  
**Status:** ok  
**Size:** `1783` bytes

## خلاصه

Use existing project node logic. Flag Counting should call it as a dependency. Recommended adapter: Node fields: For candidate high plateau at price P: 1. Merge equal highs into one candidate. 2. Do not count equal adjacent highs as clearance. 3. Require at least L candles left with high < P. 4. Require at least L candles right with high < P. 5. Emit high node. For candidate low plateau at price P: 1. Merge equal lows into one candidate. 2. Do not count equal adjacent lows as clearance. 3. Require at least L candles left with low > P. 4. Require at least L candles right with low > P. 5. Emit low node. Nodes should be sorted by: The engine may request several L values. Example: Hook readabili

## Headings

- Node Engine Algorithm
-   Source
-   Required Interface
-   Extraction Semantics
-   Ordering
-   Multi-L Views
-   No Expiration
-   Break Function
-   Adapter Tests

## Concepts

- [[docs/obsidian/04_concepts/Execution|Execution]]
- [[docs/obsidian/04_concepts/F-Counting|F-Counting]]
- [[docs/obsidian/04_concepts/Hook|Hook]]
- [[docs/obsidian/04_concepts/NDS_Anatomy|NDS Anatomy]]
- [[docs/obsidian/04_concepts/Validation|Validation]]

## Related documents

- [[docs/flag_counting/engineering_pack_v5/04_algorithms/MODULE_ARCHITECTURE|Module Architecture]] — `flag_counting_docs`
- [[docs/flag_counting/engineering_pack_v5/04_algorithms/README|04 Algorithms README]] — `flag_counting_docs`
- [[docs/flag_counting/engineering_pack_v5/04_algorithms/DEDUP_AUDIT_ALGORITHM|Dedup and Audit Algorithm]] — `flag_counting_docs`
- [[docs/flag_counting/engineering_pack_v5/04_algorithms/F1_F2_F3_ALGORITHMS|F1 / F2 / F3 Algorithms]] — `flag_counting_docs`
- [[docs/flag_counting/engineering_pack_v5/04_algorithms/PSEUDOCODE_REFERENCE|Pseudocode Reference]] — `flag_counting_docs`
- [[docs/flag_counting/engineering_pack_v5/04_algorithms/SEQUENCE_ENGINE_ALGORITHM|Sequence Engine Algorithm]] — `flag_counting_docs`
- [[docs/ai_execution/AI_ALGORITHM_LAYER_MAP_FOR_EXTREME_ENGINE_FA|AI Algorithm Layer Map for Extreme Engine — نقشه الگوریتم‌های هوش مصنوعی برای اکستریم L2]] — `ai_execution_docs`
- [[docs/ai_execution/AI_NATIVE_EXECUTION_ROADMAP_FA|AI Native Execution Roadmap — نقشه راه هوش مصنوعی، بک‌تست و پل اگزکیوت]] — `ai_execution_docs`
- [[docs/ai_execution/AMIR_STRUCTURAL_EXPERIENCE_MAP_FA|Amir Structural Experience Map — نقشه تجربه‌های ساختاری امیر]] — `ai_execution_docs`
- [[docs/ai_execution/EXPERIENCE_CAPTURE_LOG_TEMPLATE_FA|Experience Capture Log Template — قالب ثبت تجربه‌های امیر]] — `ai_execution_docs`
- [[docs/debug/MARKET_LANGUAGE/README|DAL Market Language — Nodes, Cycles, Hooks, Rallies, Flags, 123 Flags, and Open 1/2s]] — `debug_docs`
- [[docs/experience_capture/answers/BASE-01/answer_normalized_en|BASE-01 — Normalized Interpretation]] — `experience_capture_docs`

## Recommended Obsidian use

- این card را به نوت‌های concept، hypothesis، experiment یا ADR مربوط link کن.
- اگر این سند source of truth است، در MOC مربوطه بالاتر از اسناد legacy قرارش بده.
- اگر این سند report/validation است، نتیجه نهایی آن را به registry مربوط sync کن.
