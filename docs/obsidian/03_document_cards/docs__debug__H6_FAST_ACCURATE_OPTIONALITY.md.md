---
title: "H6 Fast Accurate Optionality Report"
type: document_card
generated_by: alpha_lab_obsidian_builder
generated_at: 2026-07-06
source_path: "docs/debug/H6_FAST_ACCURATE_OPTIONALITY.md"
source_ext: ".md"
category: "debug_docs"
source_size_bytes: "1701"
entities:
  - "H0006"
  - "M0001"
concepts:
  - "Atomic No-Sample"
  - "Convexity"
  - "Execution"
  - "Known-Time Causality"
  - "NDS Anatomy"
  - "Validation"
---


# H6 Fast Accurate Optionality Report

**Source:** [[docs/debug/H6_FAST_ACCURATE_OPTIONALITY|docs/debug/H6_FAST_ACCURATE_OPTIONALITY.md]]

**Category:** `debug_docs`  
**Status:** ok  
**Size:** `1701` bytes

## خلاصه

This release makes the standalone H0006 optionality report faster and more execution-realistic without returning to samples. H6 remains atomic and no-sample: `sampleCalls=0` `branchSamplesBuilt=0` `m0002Calls=0` sequence is built from raw M0001 known-time batches events that become known on the same candle are simultaneous, not sequential The default H6 entry anchor is now `NEXT_OPEN`. Previously, future optionality used the known candle close as the anchor. The new default measures future excursion from the next candle open, which is closer to what could be acted on after the regime batch becomes knowable. Set `InpH6EntryAnchorMode=0` to compare against the old known-close anchor. H6 stress

## Headings

- H6 Fast Accurate Optionality Report
-   Contract
-   Accuracy change
-   Speed controls
-   New audit line

## Entities

`H0006`, `M0001`

## Concepts

- [[docs/obsidian/04_concepts/Atomic_No-Sample|Atomic No-Sample]]
- [[docs/obsidian/04_concepts/Convexity|Convexity]]
- [[docs/obsidian/04_concepts/Execution|Execution]]
- [[docs/obsidian/04_concepts/Known-Time_Causality|Known-Time Causality]]
- [[docs/obsidian/04_concepts/NDS_Anatomy|NDS Anatomy]]
- [[docs/obsidian/04_concepts/Validation|Validation]]

## Related documents

- [[docs/debug/H6_NODE_SURVIVAL_MAP|H6 Node Survival Map]] — `debug_docs`
- [[docs/debug/H6_CANDLE_STREAM_FAST|H6 Candle-Stream Fast Optionality]] — `debug_docs`
- [[docs/mql_native/H0007_FLAG_COUNTING_F1_START_STRUCTURE|H0007 — Flag Counting / F1 Start Structure]] — `mql_native_docs`
- [[lab/03_experiments/EXP0002_mql_native_m0001/report|EXP0002 — MQL-native M0001 Runtime]] — `experiment`
- [[docs/debug/H6_REACTION_BOX_ZONES|H6 Reaction Box Zones]] — `debug_docs`
- [[docs/debug/MAIN_ATOMIC_NO_SAMPLE_UNIFICATION|Main Atomic No-Sample Unification for H4/H5]] — `debug_docs`
- [[lab/02_hypotheses/H0006_reversal_explosive_optionality|H0006 — Node Survival Edge Map]] — `hypothesis`
- [[lab/02_hypotheses/H0004_branch_regime_memory_atomic|H0004 — Branch Regime Memory]] — `hypothesis`
- [[lab/02_hypotheses/H0005_directional_memory_atomic|H0005 — Directional Memory and Execution]] — `hypothesis`
- [[lab/03_experiments/EXP0003_mql_native_m0002/report|EXP0003 — M0002 Reversal/Continuation Exit Volatility]] — `experiment`
- [[lab/05_validation/VAL_M0001_MQL_NATIVE/report|VAL_M0001_MQL_NATIVE]] — `validation`
- [[docs/debug/D0009_H5_ATOMIC_NO_SAMPLE_REPLAY_AUDIT|D0009 H5 Atomic No-Sample Replay Audit]] — `debug_docs`

## Recommended Obsidian use

- این card را به نوت‌های concept، hypothesis، experiment یا ADR مربوط link کن.
- اگر این سند source of truth است، در MOC مربوطه بالاتر از اسناد legacy قرارش بده.
- اگر این سند report/validation است، نتیجه نهایی آن را به registry مربوط sync کن.
