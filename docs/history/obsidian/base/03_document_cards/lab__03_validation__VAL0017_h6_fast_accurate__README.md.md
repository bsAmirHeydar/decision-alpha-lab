---
title: "VAL0017 — H6 Fast Accurate Optionality"
type: document_card
generated_by: alpha_lab_obsidian_builder
generated_at: 2026-07-06
source_path: "lab/03_validation/VAL0017_h6_fast_accurate/README.md"
source_ext: ".md"
category: "validation"
source_size_bytes: "995"
entities:
  - "H0006"
  - "VAL0017"
concepts:
  - "AI Agent Layer"
  - "Atomic No-Sample"
  - "Convexity"
  - "Execution"
  - "Known-Time Causality"
  - "Validation"
---


# VAL0017 — H6 Fast Accurate Optionality

**Source:** [[lab/03_validation/VAL0017_h6_fast_accurate/README|lab/03_validation/VAL0017_h6_fast_accurate/README.md]]

**Category:** `validation`  
**Status:** ok  
**Size:** `995` bytes

## خلاصه

Goal: keep H0006 standalone and atomic/no-sample while reducing runtime and improving execution realism. 1. Default anchor is `NEXT_OPEN`, not the known candle close. 2. Stress can run in fast mode using mean excursion and Tail2 hit-rate instead of full quantile sorting. 3. Edge map can run in core mode instead of full bucket mode. 4. Fast/main/slow horizons can be enabled independently. `InpH6StressMode=1` `InpH6EdgeMapLevel=1` `InpH6ReportFastHorizon=true` `InpH6ReportMainHorizon=true` `InpH6ReportSlowHorizon=false` `InpH6EntryAnchorMode=1` `InpH6StressMode=2` `InpH6EdgeMapLevel=2` all horizons enabled `InpPermutationIterations=500` This validation does not ask whether reversal has a bette

## Headings

- VAL0017 — H6 Fast Accurate Optionality
-   What changed
-   Recommended quick run
-   Recommended final run
-   Interpretation

## Entities

`H0006`, `VAL0017`

## Concepts

- [[docs/obsidian/04_concepts/AI_Agent_Layer|AI Agent Layer]]
- [[docs/obsidian/04_concepts/Atomic_No-Sample|Atomic No-Sample]]
- [[docs/obsidian/04_concepts/Convexity|Convexity]]
- [[docs/obsidian/04_concepts/Execution|Execution]]
- [[docs/obsidian/04_concepts/Known-Time_Causality|Known-Time Causality]]
- [[docs/obsidian/04_concepts/Validation|Validation]]

## Related documents

- [[lab/03_validation/VAL0018_h6_candle_stream_fast/README|VAL0018 — H6 Candle-Stream Fast Optionality]] — `validation`
- [[lab/03_validation/VAL0015_h4_deep_h6_optionality/README|VAL0015 — H4 Deep Atomic + H6 Optionality Report]] — `validation`
- [[lab/03_validation/VAL0016_h6_standalone_optionality/README|VAL0016 — H6 standalone optionality edge map]] — `validation`
- [[lab/03_experiments/EXP0016_astro_meta_learner/README|EXP0016 Astro Meta Learner]] — `experiment`
- [[lab/03_validation/VAL0008_h4_causal_batch/README|VAL0008 — H4 Causal Batch Validation]] — `validation`
- [[lab/03_validation/VAL0022_h6_reaction_box_zones/README|VAL0022 — H6 Reaction Box Zones]] — `validation`
- [[README|Decision Alpha Lab]] — `readme`
- [[tools/astro_ml/README|Astro ML Tools]] — `tool_docs`
- [[docs/debug/E0008/README|E0008 — MTF Purple Extreme Executor]] — `debug_docs`
- [[docs/experience_capture/questions/README|Quant Lab Experience Capture Questionnaire]] — `experience_capture_docs`
- [[docs/flag_counting/implementation_ladder_v1/README|Phoenix Flag Counting Implementation Ladder V1]] — `flag_counting_docs`
- [[docs/flag_counting/README|Flag Counting Documentation]] — `flag_counting_docs`

## Recommended Obsidian use

- این card را به نوت‌های concept، hypothesis، experiment یا ADR مربوط link کن.
- اگر این سند source of truth است، در MOC مربوطه بالاتر از اسناد legacy قرارش بده.
- اگر این سند report/validation است، نتیجه نهایی آن را به registry مربوط sync کن.
