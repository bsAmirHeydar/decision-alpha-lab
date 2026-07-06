---
title: "Research Lessons and Failure Modes"
type: document_card
generated_by: alpha_lab_obsidian_builder
generated_at: 2026-07-06
source_path: "docs/research_lessons_and_failure_modes.md"
source_ext: ".md"
category: "core_docs"
source_size_bytes: "4184"
entities:
  - "D0009"
  - "D0010"
  - "H0004"
  - "H0005"
concepts:
  - "AI Agent Layer"
  - "Atomic No-Sample"
  - "Execution"
  - "Known-Time Causality"
  - "NDS Anatomy"
  - "Validation"
---


# Research Lessons and Failure Modes

**Source:** [[docs/research_lessons_and_failure_modes|docs/research_lessons_and_failure_modes.md]]

**Category:** `core_docs`  
**Status:** ok  
**Size:** `4184` bytes

## خلاصه

This document records the most important lessons learned during the H0004 and H0005 development process. Completed branch samples are useful for discovery. They are not automatically valid as live decision objects. The problem is not merely that a sample is convenient. The problem is that a sample usually exists after a full event has completed. If the report then uses that object to infer what would have been known earlier, it may accidentally import future knowledge. Rule: > If a report claims live validity, it must prove that every label and decision was knowable before the entry it explains. A major failure mode was discovered in H0004: several highs/lows or branch labels may become know

## Headings

- Research Lessons and Failure Modes
-   Lesson 1 — Samples are not live decisions
-   Lesson 2 — Same-candle labels are simultaneous
-   Lesson 3 — Classic H4 overstated regime memory
-   Lesson 4 — Continuation PF without a stop is not trading PF
-   Lesson 5 — Reversal and continuation are different species
-   Lesson 6 — Debug validators must be promoted into main reports
-   Lesson 7 — Random baselines must be matched to the claim
-   Lesson 8 — A good report can still be non-tradable

## Entities

`D0009`, `D0010`, `H0004`, `H0005`

## Concepts

- [[docs/obsidian/04_concepts/AI_Agent_Layer|AI Agent Layer]]
- [[docs/obsidian/04_concepts/Atomic_No-Sample|Atomic No-Sample]]
- [[docs/obsidian/04_concepts/Execution|Execution]]
- [[docs/obsidian/04_concepts/Known-Time_Causality|Known-Time Causality]]
- [[docs/obsidian/04_concepts/NDS_Anatomy|NDS Anatomy]]
- [[docs/obsidian/04_concepts/Validation|Validation]]

## Related documents

- [[lab/09_execution/mql5/README|MQL5 Execution and Validation Layer]] — `execution`
- [[docs/reports/2026-06-20_h4_h5_gold_m10_report|Report — H4/H5 GOLD M10 Review, 2026-06-20]] — `core_docs`
- [[lab/02_hypotheses/H0004_branch_regime_memory_atomic|H0004 — Branch Regime Memory]] — `hypothesis`
- [[README|Decision Alpha Lab]] — `readme`
- [[docs/debug/D0010_H4_ATOMIC_NO_SAMPLE_REGIME_AUDIT|D0010 — H4 Atomic No-Sample Regime Audit]] — `debug_docs`
- [[lab/03_validation/VAL0010_h4_atomic_no_sample_regime/README|VAL0010 — H4 Atomic No-Sample Regime Replay]] — `validation`
- [[lab/05_validation/VAL0010_h4_atomic_no_sample_regime/README|VAL0010 — H4 Atomic No-Sample Regime Validation]] — `validation`
- [[docs/debug/D0007_H5_CAUSAL_LIVE_REPLAY_AUDIT|D0007 — H5 Causal Live Replay Audit]] — `debug_docs`
- [[docs/mql_native/H0007_FLAG_COUNTING_F1_START_STRUCTURE|H0007 — Flag Counting / F1 Start Structure]] — `mql_native_docs`
- [[lab/05_validation/VAL0011_main_atomic_no_sample_unification/README|VAL0011 — Main Atomic No-Sample Unification]] — `validation`
- [[docs/mql_native/H0005_CONTEXTUAL_BRANCH_REGIME_STATE|H0005 — Contextual Branch Regime State]] — `mql_native_docs`
- [[docs/debug/D0008_H4_CAUSAL_BATCH_REPORT|D0008 / H0004 Causal Known-Candle Batch Report]] — `debug_docs`

## Recommended Obsidian use

- این card را به نوت‌های concept، hypothesis، experiment یا ADR مربوط link کن.
- اگر این سند source of truth است، در MOC مربوطه بالاتر از اسناد legacy قرارش بده.
- اگر این سند report/validation است، نتیجه نهایی آن را به registry مربوط sync کن.
