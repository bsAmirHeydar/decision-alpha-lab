---
title: "Level 11.5 — Raw Audit Export / Report Engine"
type: document_card
generated_by: alpha_lab_obsidian_builder
generated_at: 2026-07-06
source_path: "docs/flag_counting/implementation_ladder_v1/11_5_LEVEL_11_5_RAW_AUDIT_EXPORT.md"
source_ext: ".md"
category: "flag_counting_docs"
source_size_bytes: "5216"
concepts:
  - "AI Agent Layer"
  - "Execution"
  - "F-Counting"
  - "Hook"
  - "MQL Native"
  - "NDS Anatomy"
  - "Validation"
---


# Level 11.5 — Raw Audit Export / Report Engine

**Source:** [[docs/flag_counting/implementation_ladder_v1/11_5_LEVEL_11_5_RAW_AUDIT_EXPORT|docs/flag_counting/implementation_ladder_v1/11_5_LEVEL_11_5_RAW_AUDIT_EXPORT.md]]

**Category:** `flag_counting_docs`  
**Status:** ok  
**Size:** `5216` bytes

## خلاصه

Level 11.5 makes the Phoenix engine auditable as data before Level 12 renderer/layout work. The chart is useful, but it is not proof. The export layer serializes the final Level 11 canonical stream into stable CSV files so hidden structures, losing candidates, parent links, lifecycle states, and canonical decisions can be inspected outside MetaTrader. Pipeline position: Level 11.5 is read-only. It may: It may not: Default output folder: Default overwrite mode: Validation mode may set: `events.csv` exports both visible and hidden events by default. Each row includes: This is intentionally wide. The goal is debugability, not compactness. `hooks.csv` exports both visible and hidden Hook/ND cont

## Headings

- Level 11.5 — Raw Audit Export / Report Engine
-   Purpose
-   Active files
-   Authority boundary
-   Inputs
-   Inputs added to EA
-   Output path
-   Event CSV contract
-   Hook CSV contract
-   Summary CSV contract
-   Manifest CSV contract
-   Sanity log

## Concepts

- [[docs/obsidian/04_concepts/AI_Agent_Layer|AI Agent Layer]]
- [[docs/obsidian/04_concepts/Execution|Execution]]
- [[docs/obsidian/04_concepts/F-Counting|F-Counting]]
- [[docs/obsidian/04_concepts/Hook|Hook]]
- [[docs/obsidian/04_concepts/MQL_Native|MQL Native]]
- [[docs/obsidian/04_concepts/NDS_Anatomy|NDS Anatomy]]
- [[docs/obsidian/04_concepts/Validation|Validation]]

## Related documents

- [[docs/flag_counting/implementation_ladder_v1/00_GOVERNANCE_AND_FREEZE_PROTOCOL|Phoenix Flag Counting Implementation Ladder V1]] — `flag_counting_docs`
- [[docs/flag_counting/implementation_ladder_v1/04_LEVEL_04_HOOK_ND_CONTEXT_ENGINE|Phoenix Flag Counting Implementation Ladder V1]] — `flag_counting_docs`
- [[docs/flag_counting/implementation_ladder_v1/10_LEVEL_10_SEQUENCE_OWNERSHIP_AND_PHASES|Phoenix Flag Counting Implementation Ladder V1]] — `flag_counting_docs`
- [[docs/flag_counting/implementation_ladder_v1/11_LEVEL_11_CANONICALIZATION_AND_AUDIT|Phoenix Flag Counting Implementation Ladder V1]] — `flag_counting_docs`
- [[docs/flag_counting/implementation_ladder_v1/12_LEVEL_12_RENDERER_AND_LABEL_LAYOUT|Level 12 — Renderer / Labels / Visual Layer]] — `flag_counting_docs`
- [[docs/flag_counting/implementation_ladder_v1/14_LEVEL_14_RELEASE_ROLLBACK_AND_DEBUG_PROTOCOL|Phoenix Flag Counting Implementation Ladder V1]] — `flag_counting_docs`
- [[docs/flag_counting/implementation_ladder_v1/15_MODULE_INTERFACE_CONTRACTS|Phoenix Flag Counting Implementation Ladder V1]] — `flag_counting_docs`
- [[docs/flag_counting/implementation_ladder_v1/16_IMPLEMENTATION_ORDER_AND_ACCEPTANCE_MATRIX|Phoenix Flag Counting Implementation Ladder V1]] — `flag_counting_docs`
- [[docs/flag_counting/implementation_ladder_v1/README|Phoenix Flag Counting Implementation Ladder V1]] — `flag_counting_docs`
- [[lab/03_experiments/EXP0004_mql_native_m0004/report|EXP0004 — MQL-native M0004 Branch Regime Clustering]] — `experiment`
- [[docs/flag_counting/implementation_ladder_v1/01_LEVEL_01_CANDLE_STREAM_AND_TIMEBASE|Phoenix Flag Counting Implementation Ladder V1]] — `flag_counting_docs`
- [[docs/flag_counting/implementation_ladder_v1/13_LEVEL_13_VALIDATION_MATRIX|Phoenix Flag Counting Implementation Ladder V1]] — `flag_counting_docs`

## Recommended Obsidian use

- این card را به نوت‌های concept، hypothesis، experiment یا ADR مربوط link کن.
- اگر این سند source of truth است، در MOC مربوطه بالاتر از اسناد legacy قرارش بده.
- اگر این سند report/validation است، نتیجه نهایی آن را به registry مربوط sync کن.
