---
title: "VAL0008 — H4 Causal Batch Validation"
type: document_card
generated_by: alpha_lab_obsidian_builder
generated_at: 2026-07-06
source_path: "lab/03_validation/VAL0008_h4_causal_batch/README.md"
source_ext: ".md"
category: "validation"
source_size_bytes: "825"
entities:
  - "H0004"
  - "VAL0008"
concepts:
  - "AI Agent Layer"
  - "Atomic No-Sample"
  - "Execution"
  - "Known-Time Causality"
  - "MQL Native"
  - "NDS Anatomy"
  - "Validation"
---


# VAL0008 — H4 Causal Batch Validation

**Source:** [[lab/03_validation/VAL0008_h4_causal_batch/README|lab/03_validation/VAL0008_h4_causal_batch/README.md]]

**Category:** `validation`  
**Status:** ok  
**Size:** `825` bytes

## خلاصه

Goal: validate H0004 branch-regime memory using the candle on which each regime label becomes knowable, not an arbitrary sample order inside the same candle. Procedure: 1. Run `M0004_BranchRegimeClustering.mq5` after this release. 2. Compare the classic H4 output against the new `DAL_M0004_FINAL_CAUSAL_*` lines. 3. Treat mixed same-candle reversal/continuation batches as ambiguous rather than as a sequential regime transition. Decision rule: If `removedFakeTransitionPct` is small and causal metrics stay close to classic metrics, H4 is robust to the batch correction. If `removedFakeTransitionPct` is high or `DAL_M0004_FINAL_CAUSAL_VS_CLASSIC` says `classic_sequence_materially_changed_by_causa

## Headings

- VAL0008 — H4 Causal Batch Validation

## Entities

`H0004`, `VAL0008`

## Concepts

- [[docs/obsidian/04_concepts/AI_Agent_Layer|AI Agent Layer]]
- [[docs/obsidian/04_concepts/Atomic_No-Sample|Atomic No-Sample]]
- [[docs/obsidian/04_concepts/Execution|Execution]]
- [[docs/obsidian/04_concepts/Known-Time_Causality|Known-Time Causality]]
- [[docs/obsidian/04_concepts/MQL_Native|MQL Native]]
- [[docs/obsidian/04_concepts/NDS_Anatomy|NDS Anatomy]]
- [[docs/obsidian/04_concepts/Validation|Validation]]

## Related documents

- [[README|Decision Alpha Lab]] — `readme`
- [[lab/03_validation/VAL0010_h4_atomic_no_sample_regime/README|VAL0010 — H4 Atomic No-Sample Regime Replay]] — `validation`
- [[lab/05_validation/VAL0010_h4_atomic_no_sample_regime/README|VAL0010 — H4 Atomic No-Sample Regime Validation]] — `validation`
- [[lab/05_validation/VAL0011_main_atomic_no_sample_unification/README|VAL0011 — Main Atomic No-Sample Unification]] — `validation`
- [[lab/09_execution/mql5/README|MQL5 Execution and Validation Layer]] — `execution`
- [[lab/03_validation/VAL0014_h4_atomic_full_stress_context/README|VAL0014 — H4 Atomic Full Stress + Human Context]] — `validation`
- [[lab/03_validation/VAL0012_h4_fast_atomic_main/README|VAL0012 — H4 Fast Atomic Main Report]] — `validation`
- [[lab/04_analysis/ANL004_h4_causal_batch_vs_classic/README|ANL004 — H4 Classic vs Causal Batch Analysis]] — `analysis`
- [[lab/03_experiments/EXP0016_astro_meta_learner/README|EXP0016 Astro Meta Learner]] — `experiment`
- [[tools/astro_ml/README|Astro ML Tools]] — `tool_docs`
- [[lab/03_validation/VAL0016_h6_standalone_optionality/README|VAL0016 — H6 standalone optionality edge map]] — `validation`
- [[docs/flag_counting/implementation_ladder_v1/README|Phoenix Flag Counting Implementation Ladder V1]] — `flag_counting_docs`

## Recommended Obsidian use

- این card را به نوت‌های concept، hypothesis، experiment یا ADR مربوط link کن.
- اگر این سند source of truth است، در MOC مربوطه بالاتر از اسناد legacy قرارش بده.
- اگر این سند report/validation است، نتیجه نهایی آن را به registry مربوط sync کن.
