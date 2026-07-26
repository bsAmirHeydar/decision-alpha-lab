---
title: "VAL0007 — H5 Causal Live Replay"
type: document_card
generated_by: alpha_lab_obsidian_builder
generated_at: 2026-07-06
source_path: "lab/03_validation/VAL0007_h5_causal_live_replay/README.md"
source_ext: ".md"
category: "validation"
source_size_bytes: "1387"
entities:
  - "H0005"
  - "VAL0007"
concepts:
  - "Execution"
  - "Known-Time Causality"
  - "NDS Anatomy"
  - "Structural Nodes"
  - "Validation"
---


# VAL0007 — H5 Causal Live Replay

**Source:** [[lab/03_validation/VAL0007_h5_causal_live_replay/README|lab/03_validation/VAL0007_h5_causal_live_replay/README.md]]

**Category:** `validation`  
**Status:** ok  
**Size:** `1387` bytes

## خلاصه

This validation replaces path-first H5 interpretation with live-style replay. When H0005 has a known regime state at candle `t`, and that state was knowable using only data up to `t`, do later zone touches or structural breaks produce positive post-entry movement? Old H5 reports can be useful for structural research, but they are not strict live execution proof. VAL0007 treats regime confirmation as a time-stamped event and processes all samples confirmed on the same candle as one batch. If multiple highs/lows are confirmed on the same candle, they do not form a chronological sequence. They are simultaneous. A mixed reversal/continuation batch is marked ambiguous by default. Reversal: regime

## Headings

- VAL0007 — H5 Causal Live Replay
-   Hypothesis under test
-   What is different from old H5 reports?
-   Simultaneous breaks
-   Entry definitions
-   Measurement

## Entities

`H0005`, `VAL0007`

## Concepts

- [[docs/obsidian/04_concepts/Execution|Execution]]
- [[docs/obsidian/04_concepts/Known-Time_Causality|Known-Time Causality]]
- [[docs/evidence/nds_anatomy/6a11c75733b2_NDS_Anatomy|NDS Anatomy]]
- [[docs/obsidian/04_concepts/Structural_Nodes|Structural Nodes]]
- [[docs/obsidian/04_concepts/Validation|Validation]]

## Related documents

- [[README|Decision Alpha Lab]] — `readme`
- [[lab/03_validation/VAL0006_h5_live_touch_replay/README|VAL0006 — H5 live-valid touch-entry replay]] — `validation`
- [[lab/05_validation/VAL0011_main_atomic_no_sample_unification/README|VAL0011 — Main Atomic No-Sample Unification]] — `validation`
- [[docs/execution/README|Decision Alpha Lab — Execution]] — `execution_docs`
- [[lab/03_validation/VAL0005_h5_no_future_walk_forward/README|VAL0005 — H5 No-Future Walk-Forward Validation]] — `validation`
- [[lab/04_execution/EXE0001_reversal_one_to_one/README|EXE0001 — H0005 Reversal Fixed-R Executor]] — `execution`
- [[lab/04_execution/EXE0002_close_confirmed_market/README|EXE0002 — Close-Confirmed Market After Touch]] — `execution`
- [[lab/04_execution/EXE0005_continuation_close_break_fixed_r/README|EXE0005 — Continuation Close-Break Fixed-R]] — `execution`
- [[lab/09_execution/mql5/README|MQL5 Execution and Validation Layer]] — `execution`
- [[lab/03_experiments/EXP0005_mql_native_directional_memory/README|EXP0005 — MQL-native H0005 directional memory]] — `experiment`
- [[lab/04_execution/EXE0004_continuation_heikin_ashi_flip/README|EXE0004 — Continuation Heikin Ashi Flip]] — `execution`
- [[lab/03_validation/VAL0022_h6_reaction_box_zones/README|VAL0022 — H6 Reaction Box Zones]] — `validation`

## Recommended Obsidian use

- این card را به نوت‌های concept، hypothesis، experiment یا ADR مربوط link کن.
- اگر این سند source of truth است، در MOC مربوطه بالاتر از اسناد legacy قرارش بده.
- اگر این سند report/validation است، نتیجه نهایی آن را به registry مربوط sync کن.
