---
title: "Phoenix Flag Counting Implementation Ladder V1"
type: document_card
generated_by: alpha_lab_obsidian_builder
generated_at: 2026-07-06
source_path: "docs/flag_counting/implementation_ladder_v1/03_LEVEL_03_NODE_IDENTITY_AND_SCALE.md"
source_ext: ".md"
category: "flag_counting_docs"
source_size_bytes: "4451"
concepts:
  - "F-Counting"
  - "Hook"
  - "MQL Native"
  - "NDS Anatomy"
  - "Structural Nodes"
  - "Validation"
---


# Phoenix Flag Counting Implementation Ladder V1

**Source:** [[docs/flag_counting/implementation_ladder_v1/03_LEVEL_03_NODE_IDENTITY_AND_SCALE|docs/flag_counting/implementation_ladder_v1/03_LEVEL_03_NODE_IDENTITY_AND_SCALE.md]]

**Category:** `flag_counting_docs`  
**Status:** ok  
**Size:** `4451` bytes

## خلاصه

This document is part of the implementation ladder for the Phoenix Flag Counting engine. Lower layers become frozen foundations before higher layers depend on them. Level 03 makes identity explicit before Hook/ND, F1/F2/F3 lifecycle, ownership, and renderer work. Phoenix must never decide visibility from only `node_id`, `event_id`, or chart object names. This layer separates: Wiring consumers: `FP_Node`, `FP_HookBranch`, and `FP_FlagEvent` carry Level 03 fields: For `FP_Node`, `source_L` is represented by the existing `L` field. Structural node identity: Visual node identity: This allows audit to keep multiple L versions while the main chart can collapse visually identical structures determi

## Headings

- Phoenix Flag Counting Implementation Ladder V1
- Level 03 — Node Identity and Scale
-   Purpose
-   Owned source modules
-   Identity fields
-   Node identity
-   Event identity
-   Canonical winner policy
-   Audit contract
-   Forbidden behavior
-   Acceptance tests
-     Test 01 — Same visible body across L

## Concepts

- [[docs/obsidian/04_concepts/F-Counting|F-Counting]]
- [[docs/obsidian/04_concepts/Hook|Hook]]
- [[docs/obsidian/04_concepts/MQL_Native|MQL Native]]
- [[docs/evidence/nds_anatomy/6a11c75733b2_NDS_Anatomy|NDS Anatomy]]
- [[docs/obsidian/04_concepts/Structural_Nodes|Structural Nodes]]
- [[docs/obsidian/04_concepts/Validation|Validation]]

## Related documents

- [[docs/flag_counting/implementation_ladder_v1/02_LEVEL_02_NODE_ENGINE|Phoenix Flag Counting Implementation Ladder V1]] — `flag_counting_docs`
- [[docs/evidence/exp0002_mql_native_m0001_runtime/319a21879dae_report|EXP0002 — MQL-native M0001 Runtime]] — `experiment`
- [[lab/03_experiments/EXP0003_mql_native_m0002/report|EXP0003 — M0002 Reversal/Continuation Exit Volatility]] — `experiment`
- [[lab/03_experiments/EXP0004_mql_native_m0004/report|EXP0004 — MQL-native M0004 Branch Regime Clustering]] — `experiment`
- [[docs/evidence/val_m0001_mql_native/454e81f9f0b3_report|VAL_M0001_MQL_NATIVE]] — `validation`
- [[docs/flag_counting/implementation_ladder_v1/00_GOVERNANCE_AND_FREEZE_PROTOCOL|Phoenix Flag Counting Implementation Ladder V1]] — `flag_counting_docs`
- [[docs/flag_counting/implementation_ladder_v1/01_LEVEL_01_CANDLE_STREAM_AND_TIMEBASE|Phoenix Flag Counting Implementation Ladder V1]] — `flag_counting_docs`
- [[docs/flag_counting/implementation_ladder_v1/04_LEVEL_04_HOOK_ND_CONTEXT_ENGINE|Phoenix Flag Counting Implementation Ladder V1]] — `flag_counting_docs`
- [[docs/flag_counting/implementation_ladder_v1/05_LEVEL_05_FLAG_BODY_ENGINE|Phoenix Flag Counting Implementation Ladder V1]] — `flag_counting_docs`
- [[docs/flag_counting/implementation_ladder_v1/07_LEVEL_07_F1_LIFECYCLE_ENGINE|Phoenix Flag Counting Implementation Ladder V1]] — `flag_counting_docs`
- [[docs/flag_counting/implementation_ladder_v1/08_LEVEL_08_F2_LIFECYCLE_ENGINE|Phoenix Flag Counting Implementation Ladder V1]] — `flag_counting_docs`
- [[docs/flag_counting/implementation_ladder_v1/10_LEVEL_10_SEQUENCE_OWNERSHIP_AND_PHASES|Phoenix Flag Counting Implementation Ladder V1]] — `flag_counting_docs`

## Recommended Obsidian use

- این card را به نوت‌های concept، hypothesis، experiment یا ADR مربوط link کن.
- اگر این سند source of truth است، در MOC مربوطه بالاتر از اسناد legacy قرارش بده.
- اگر این سند report/validation است، نتیجه نهایی آن را به registry مربوط sync کن.
