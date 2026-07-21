---
title: "EXP Flag Counting — Sequence Contract V4"
type: document_card
generated_by: alpha_lab_obsidian_builder
generated_at: 2026-07-06
source_path: "docs/releases/legacy_migration/general/0d840c62852d_README_FLAG_COUNTING_SEQUENCE_CONTRACT_V4.md"
source_ext: ".md"
category: "experiment"
source_size_bytes: "1169"
concepts:
  - "F-Counting"
  - "Hook"
  - "MQL Native"
  - "NDS Anatomy"
---


# EXP Flag Counting — Sequence Contract V4

**Source:** [[docs/releases/legacy_migration/general/0d840c62852d_README_FLAG_COUNTING_SEQUENCE_CONTRACT_V4|docs/releases/legacy_migration/general/0d840c62852d_README_FLAG_COUNTING_SEQUENCE_CONTRACT_V4.md]]

**Category:** `experiment`  
**Status:** ok  
**Size:** `1169` bytes

## خلاصه

Sequence Contract V4 remains the active semantic contract, but it is subordinate to the current canon: Use V4 for the F1/F2/F3 and Hook/ND semantic rules after reading the current canon. Active implementation path: Important V4 rules retained by the current canon: Nodes come from the existing project node logic. L is the existing left/right candle clearance definition. The algorithm uses high/low nodes only. Equality does not count as break. F1 starts from a phase boundary unless fail-open diagnostic recovery is explicitly used. F2 starts only after F1 confirmation and uses strict-window backfill. F3 starts only after F2 confirmation and uses strict-window backfill. F2 is size-compared to F1

## Headings

- EXP Flag Counting — Sequence Contract V4

## Concepts

- [[docs/obsidian/04_concepts/F-Counting|F-Counting]]
- [[docs/obsidian/04_concepts/Hook|Hook]]
- [[docs/obsidian/04_concepts/MQL_Native|MQL Native]]
- [[docs/evidence/nds_anatomy/6a11c75733b2_NDS_Anatomy|NDS Anatomy]]

## Related documents

- [[docs/flag_counting/FLAG_COUNTING_CURRENT_CANON|Flag Counting Current Canon]] — `flag_counting_docs`
- [[docs/flag_counting/FLAG_COUNTING_SEQUENCE_CONTRACT_V4|Flag Counting Sequence Contract V4]] — `flag_counting_docs`
- [[lab/03_experiments/EXP_flag_counting/README|EXP Flag Counting]] — `experiment`
- [[docs/flag_counting/implementation_ladder_v1/README|Phoenix Flag Counting Implementation Ladder V1]] — `flag_counting_docs`
- [[docs/flag_counting/README|Flag Counting Documentation]] — `flag_counting_docs`
- [[lab/03_experiments/EXP_flag_counting/validation_cases/README|Phoenix Flag Counting Validation Cases]] — `experiment`
- [[docs/ai_execution/README|AI Execution Docs]] — `ai_execution_docs`
- [[docs/debug/E0008/README|E0008 — MTF Purple Extreme Executor]] — `debug_docs`
- [[docs/debug/MARKET_LANGUAGE/README|DAL Market Language — Nodes, Cycles, Hooks, Rallies, Flags, 123 Flags, and Open 1/2s]] — `debug_docs`
- [[docs/experience_capture/questions/README|Quant Lab Experience Capture Questionnaire]] — `experience_capture_docs`
- [[docs/experience_capture/questions/remaining_v2/sections/03_entry_families/README|Entry Families Beyond Extreme]] — `experience_capture_docs`
- [[docs/flag_counting/engineering_pack_v5/01_concepts/README|01 Concepts README]] — `flag_counting_docs`

## Recommended Obsidian use

- این card را به نوت‌های concept، hypothesis، experiment یا ADR مربوط link کن.
- اگر این سند source of truth است، در MOC مربوطه بالاتر از اسناد legacy قرارش بده.
- اگر این سند report/validation است، نتیجه نهایی آن را به registry مربوط sync کن.
