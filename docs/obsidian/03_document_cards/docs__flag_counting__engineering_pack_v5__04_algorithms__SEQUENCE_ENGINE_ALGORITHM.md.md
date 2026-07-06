---
title: "Sequence Engine Algorithm"
type: document_card
generated_by: alpha_lab_obsidian_builder
generated_at: 2026-07-06
source_path: "docs/flag_counting/engineering_pack_v5/04_algorithms/SEQUENCE_ENGINE_ALGORITHM.md"
source_ext: ".md"
category: "flag_counting_docs"
source_size_bytes: "2407"
concepts:
  - "F-Counting"
  - "Hook"
  - "NDS Anatomy"
  - "Validation"
---


# Sequence Engine Algorithm

**Source:** [[docs/flag_counting/engineering_pack_v5/04_algorithms/SEQUENCE_ENGINE_ALGORITHM|docs/flag_counting/engineering_pack_v5/04_algorithms/SEQUENCE_ENGINE_ALGORITHM.md]]

**Category:** `flag_counting_docs`  
**Status:** ok  
**Size:** `2407` bytes

## خلاصه

Own the F1 -> F2 -> F3 chain. Prevent sliding-window behavior. A new F1 may start only from: ND/Hook terminal extreme; opposite sequence end; confirmed opposite F1 that locks previous F3; explicitly emitted phase boundary. If there is already an active F1/F2 in same direction/context, do not start another same-direction F1 unless phase boundary rules permit it. 1. Receive phase boundary. 2. Start F1 origin from boundary extreme. 3. Build F1 body. 4. Display only after body complete. 5. Track post-F1 context. 6. If Waist passed before confirmation, reject F1 candidate. 7. If valid internal 1/2 exists and Leg2 is passed again, confirm F1. 8. Authorize F2 and backfill origin from post-F1 contex

## Headings

- Sequence Engine Algorithm
-   Purpose
-   Chain States
-   Phase Boundary Detection
-   F1 Flow
-   F2 Flow
-   F3 Flow
-   Parent/Child Death Rule
-   Active Opposite Direction
-   Chain Emissions

## Concepts

- [[docs/obsidian/04_concepts/F-Counting|F-Counting]]
- [[docs/obsidian/04_concepts/Hook|Hook]]
- [[docs/obsidian/04_concepts/NDS_Anatomy|NDS Anatomy]]
- [[docs/obsidian/04_concepts/Validation|Validation]]

## Related documents

- [[docs/flag_counting/engineering_pack_v5/04_algorithms/DEDUP_AUDIT_ALGORITHM|Dedup and Audit Algorithm]] — `flag_counting_docs`
- [[docs/flag_counting/engineering_pack_v5/04_algorithms/F1_F2_F3_ALGORITHMS|F1 / F2 / F3 Algorithms]] — `flag_counting_docs`
- [[docs/flag_counting/engineering_pack_v5/04_algorithms/MODULE_ARCHITECTURE|Module Architecture]] — `flag_counting_docs`
- [[docs/flag_counting/engineering_pack_v5/04_algorithms/NODE_ENGINE_ALGORITHM|Node Engine Algorithm]] — `flag_counting_docs`
- [[docs/flag_counting/engineering_pack_v5/04_algorithms/README|04 Algorithms README]] — `flag_counting_docs`
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
