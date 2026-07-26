---
title: "M0007 — F1 Flag Counting MQL5 Module"
type: document_card
generated_by: alpha_lab_obsidian_builder
generated_at: 2026-07-06
source_path: "mql5/Include/M0007/README_M0007_FlagCountingF1.md"
source_ext: ".md"
category: "mql5_docs"
source_size_bytes: "7920"
entities:
  - "M0007"
concepts:
  - "AI Agent Layer"
  - "Execution"
  - "F-Counting"
  - "MQL Native"
  - "NDS Anatomy"
  - "Validation"
---


# M0007 — F1 Flag Counting MQL5 Module

**Source:** [[mql5/Include/M0007/README_M0007_FlagCountingF1|mql5/Include/M0007/README_M0007_FlagCountingF1.md]]

**Category:** `mql5_docs`  
**Status:** ok  
**Size:** `7920` bytes

## خلاصه

M0007 counts and draws F1 flag structures on chart for visual/audit research. The detector now uses the actual four-node F1 origin logic. Bullish F1: A bullish F1 is accepted only when: Bearish F1: A bearish F1 is accepted only when: This fixes the earlier schematic problem where the chart origin was synthetic or taken from the wrong side of the structure. The renderer draws only the clean F1 grammar: No horizontal guide levels, no vertical audit lines, and no internal N/R labels are drawn by default. Important inputs: M0007 is visual/audit-only. It does not place orders. The renderer must not invent the origin. `Start` is now a first-class detector node and is stored in every `M0007_F1Event

## Headings

- M0007 — F1 Flag Counting MQL5 Module
-   Correct F1 topology
-   Visual contract
-   Files
-   Inputs
-   Scope
-   2026-06 fix — real origin plus post-leg-2 internal 1/2
-   Confirmation contract update
-   Strict confirmation after internal 1/2
-   Live forming / confirmed rendering contract
-   Incremental chart object contract
-   Renderer hotfix: no default `Text` labels

## Entities

`M0007`

## Concepts

- [[docs/obsidian/04_concepts/AI_Agent_Layer|AI Agent Layer]]
- [[docs/obsidian/04_concepts/Execution|Execution]]
- [[docs/obsidian/04_concepts/F-Counting|F-Counting]]
- [[docs/obsidian/04_concepts/MQL_Native|MQL Native]]
- [[docs/evidence/nds_anatomy/6a11c75733b2_NDS_Anatomy|NDS Anatomy]]
- [[docs/obsidian/04_concepts/Validation|Validation]]

## Related documents

- [[docs/flag_counting/README|Flag Counting Documentation]] — `flag_counting_docs`
- [[lab/03_experiments/EXP_flag_counting/README|EXP Flag Counting]] — `experiment`
- [[docs/debug/MARKET_LANGUAGE/README|DAL Market Language — Nodes, Cycles, Hooks, Rallies, Flags, 123 Flags, and Open 1/2s]] — `debug_docs`
- [[docs/flag_counting/implementation_ladder_v1/README|Phoenix Flag Counting Implementation Ladder V1]] — `flag_counting_docs`
- [[docs/flag_counting/FLAG_COUNTING_CURRENT_CANON|Flag Counting Current Canon]] — `flag_counting_docs`
- [[docs/flag_counting/implementation_ladder_v1/16_IMPLEMENTATION_ORDER_AND_ACCEPTANCE_MATRIX|Phoenix Flag Counting Implementation Ladder V1]] — `flag_counting_docs`
- [[docs/mql_native/H0007_FLAG_COUNTING_F1_START_STRUCTURE|H0007 — Flag Counting / F1 Start Structure]] — `mql_native_docs`
- [[docs/experience_capture/questions/README|Quant Lab Experience Capture Questionnaire]] — `experience_capture_docs`
- [[docs/flag_counting/engineering_pack_v5/README|Flag Counting Engineering Pack V5]] — `flag_counting_docs`
- [[lab/03_experiments/EXP0013_astro_feature_store/README|EXP0013 - Astro Feature Store]] — `experiment`
- [[lab/03_experiments/EXP0016_astro_meta_learner/README|EXP0016 Astro Meta Learner]] — `experiment`
- [[lab/03_validation/VAL0008_h4_causal_batch/README|VAL0008 — H4 Causal Batch Validation]] — `validation`

## Recommended Obsidian use

- این card را به نوت‌های concept، hypothesis، experiment یا ADR مربوط link کن.
- اگر این سند source of truth است، در MOC مربوطه بالاتر از اسناد legacy قرارش بده.
- اگر این سند report/validation است، نتیجه نهایی آن را به registry مربوط sync کن.
