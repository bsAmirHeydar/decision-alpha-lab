---
title: "VAL0018 — H6 Candle-Stream Fast Optionality"
type: document_card
generated_by: alpha_lab_obsidian_builder
generated_at: 2026-07-06
source_path: "lab/03_validation/VAL0018_h6_candle_stream_fast/README.md"
source_ext: ".md"
category: "validation"
source_size_bytes: "706"
entities:
  - "H0006"
  - "VAL0018"
concepts:
  - "Convexity"
  - "Execution"
  - "Validation"
---


# VAL0018 — H6 Candle-Stream Fast Optionality

**Source:** [[lab/03_validation/VAL0018_h6_candle_stream_fast/README|lab/03_validation/VAL0018_h6_candle_stream_fast/README.md]]

**Category:** `validation`  
**Status:** ok  
**Size:** `706` bytes

## خلاصه

Purpose: validate H0006 optionality using a faster forward candle-stream measurement. Recommended first run: `InpH6CandleStreamMode=true` `InpStressH6Optionality=false` `InpPrintH6EdgeMap=false` `InpH6ReportSlowHorizon=false` `InpH6RequireFullHorizon=true` `InpH6EntryAnchorMode=1` Expected audit: `sampleCalls=0` `branchSamplesBuilt=0` `m0002Calls=0` `h6Engine=CANDLE_FORWARD_STREAM` `measurement=candle_forward_stream_no_prefix_rebuild_no_sample` Escalation run for publication: enable slow horizon set stress mode to 1 first only use stress mode 2 and full edge map after the fast report identifies candidate conditions

## Headings

- VAL0018 — H6 Candle-Stream Fast Optionality

## Entities

`H0006`, `VAL0018`

## Concepts

- [[docs/obsidian/04_concepts/Convexity|Convexity]]
- [[docs/obsidian/04_concepts/Execution|Execution]]
- [[docs/obsidian/04_concepts/Validation|Validation]]

## Related documents

- [[lab/03_validation/VAL0017_h6_fast_accurate/README|VAL0017 — H6 Fast Accurate Optionality]] — `validation`
- [[lab/03_validation/VAL0015_h4_deep_h6_optionality/README|VAL0015 — H4 Deep Atomic + H6 Optionality Report]] — `validation`
- [[lab/03_validation/VAL0016_h6_standalone_optionality/README|VAL0016 — H6 standalone optionality edge map]] — `validation`
- [[docs/debug/E0006/README|E0006 — Structural Execution Layer Overview]] — `debug_docs`
- [[docs/experience_capture/questions/README|Quant Lab Experience Capture Questionnaire]] — `experience_capture_docs`
- [[docs/flag_counting/implementation_ladder_v1/README|Phoenix Flag Counting Implementation Ladder V1]] — `flag_counting_docs`
- [[docs/flag_counting/README|Flag Counting Documentation]] — `flag_counting_docs`
- [[docs/nds_hook_architecture/README|NDS Hook Architecture — Design Pack]] — `nds_hook_architecture_docs`
- [[lab/03_experiments/EXP0014_ICT/README|EXP0014 — ICT Sweep / FVG / IFVG / CISD Execution Lab]] — `experiment`
- [[lab/03_experiments/EXP0016_astro_meta_learner/README|EXP0016 Astro Meta Learner]] — `experiment`
- [[lab/03_validation/VAL0022_h6_reaction_box_zones/README|VAL0022 — H6 Reaction Box Zones]] — `validation`
- [[lab/03_validation/VAL0023_e6_all_zone_touch_limit/README|E0006 — All-Zone Touch Limit Fixed-R Executor]] — `validation`

## Recommended Obsidian use

- این card را به نوت‌های concept، hypothesis، experiment یا ADR مربوط link کن.
- اگر این سند source of truth است، در MOC مربوطه بالاتر از اسناد legacy قرارش بده.
- اگر این سند report/validation است، نتیجه نهایی آن را به registry مربوط sync کن.
