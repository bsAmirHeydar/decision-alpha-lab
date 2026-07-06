---
title: "Phoenix Flag Counting Implementation Ladder V1"
type: document_card
generated_by: alpha_lab_obsidian_builder
generated_at: 2026-07-06
source_path: "docs/flag_counting/implementation_ladder_v1/08_LEVEL_08_F2_LIFECYCLE_ENGINE.md"
source_ext: ".md"
category: "flag_counting_docs"
source_size_bytes: "6905"
concepts:
  - "F-Counting"
  - "Hook"
  - "MQL Native"
  - "NDS Anatomy"
  - "Validation"
---


# Phoenix Flag Counting Implementation Ladder V1

**Source:** [[docs/flag_counting/implementation_ladder_v1/08_LEVEL_08_F2_LIFECYCLE_ENGINE|docs/flag_counting/implementation_ladder_v1/08_LEVEL_08_F2_LIFECYCLE_ENGINE.md]]

**Category:** `flag_counting_docs`  
**Status:** ok  
**Size:** `6905` bytes

## خلاصه

This document is part of the implementation ladder for the Phoenix Flag Counting engine. The ladder is intentionally layered so that lower layers become frozen foundations before higher layers are allowed to depend on them. Global non-negotiables: All structural decisions use candle `high` and `low` only. `open`, `close`, candle body, candle color, volume, and indicators are not structural inputs. Equality is not a break. A level is broken only by a strict pass beyond it. The renderer is non-authoritative. It may only draw logical objects emitted by engines. Main-chart rendering and audit rendering are separate products. Every layer must expose enough audit fields to prove why an object exis

## Headings

- Phoenix Flag Counting Implementation Ladder V1
- Level 08 — F2 Lifecycle Engine
-   Purpose
-   Owned source modules
-   Parent authorization
-   F2 origin backfill
-   Body dependency
-   Size gate
-   Internal confirmation
-   Invalidation
-   F3 authorization
-   Required fields

## Concepts

- [[docs/obsidian/04_concepts/F-Counting|F-Counting]]
- [[docs/obsidian/04_concepts/Hook|Hook]]
- [[docs/obsidian/04_concepts/MQL_Native|MQL Native]]
- [[docs/obsidian/04_concepts/NDS_Anatomy|NDS Anatomy]]
- [[docs/obsidian/04_concepts/Validation|Validation]]

## Related documents

- [[lab/03_experiments/EXP0002_mql_native_m0001/report|EXP0002 — MQL-native M0001 Runtime]] — `experiment`
- [[lab/03_experiments/EXP0003_mql_native_m0002/report|EXP0003 — M0002 Reversal/Continuation Exit Volatility]] — `experiment`
- [[lab/03_experiments/EXP0004_mql_native_m0004/report|EXP0004 — MQL-native M0004 Branch Regime Clustering]] — `experiment`
- [[lab/05_validation/VAL_M0001_MQL_NATIVE/report|VAL_M0001_MQL_NATIVE]] — `validation`
- [[docs/flag_counting/implementation_ladder_v1/00_GOVERNANCE_AND_FREEZE_PROTOCOL|Phoenix Flag Counting Implementation Ladder V1]] — `flag_counting_docs`
- [[docs/flag_counting/implementation_ladder_v1/01_LEVEL_01_CANDLE_STREAM_AND_TIMEBASE|Phoenix Flag Counting Implementation Ladder V1]] — `flag_counting_docs`
- [[docs/flag_counting/implementation_ladder_v1/02_LEVEL_02_NODE_ENGINE|Phoenix Flag Counting Implementation Ladder V1]] — `flag_counting_docs`
- [[docs/flag_counting/implementation_ladder_v1/03_LEVEL_03_NODE_IDENTITY_AND_SCALE|Phoenix Flag Counting Implementation Ladder V1]] — `flag_counting_docs`
- [[docs/flag_counting/implementation_ladder_v1/04_LEVEL_04_HOOK_ND_CONTEXT_ENGINE|Phoenix Flag Counting Implementation Ladder V1]] — `flag_counting_docs`
- [[docs/flag_counting/implementation_ladder_v1/05_LEVEL_05_FLAG_BODY_ENGINE|Phoenix Flag Counting Implementation Ladder V1]] — `flag_counting_docs`
- [[docs/flag_counting/implementation_ladder_v1/07_LEVEL_07_F1_LIFECYCLE_ENGINE|Phoenix Flag Counting Implementation Ladder V1]] — `flag_counting_docs`
- [[docs/flag_counting/implementation_ladder_v1/10_LEVEL_10_SEQUENCE_OWNERSHIP_AND_PHASES|Phoenix Flag Counting Implementation Ladder V1]] — `flag_counting_docs`

## Recommended Obsidian use

- این card را به نوت‌های concept، hypothesis، experiment یا ADR مربوط link کن.
- اگر این سند source of truth است، در MOC مربوطه بالاتر از اسناد legacy قرارش بده.
- اگر این سند report/validation است، نتیجه نهایی آن را به registry مربوط sync کن.
