
---
type: source_card
source_path: "docs/research_lessons_and_failure_modes.md"
source_ext: ".md"
source_size: 4184
empty: false
generated_at: 2026-07-06
concepts: ["AI Agent Layer", "Atomic No-Sample", "Decision Node", "Execution / Risk", "Known-Time Causality", "UI / React", "Validation / Audit"]
entities: ["D0009", "D0010", "H0004", "H0005"]
---

# Source Card — research_lessons_and_failure_modes.md

## Source

[[docs/research_lessons_and_failure_modes|docs/research_lessons_and_failure_modes.md]]

## Summary

This document records the most important lessons learned during the H0004 and H0005 development process. Completed branch samples are useful for discovery. They are not automatically valid as live decision objects. The problem is not merely that a sample is convenient. The problem is that a sample usually exists after a full event has completed. If the report then uses that object to infer what would have been known earlier, it may… Rule: > If a report claims live validity, it must prove that every label and decision was knowable before the entry it explains. A major failure mode was discovered in H0004: several highs/lows or branch labels may become known on the same candle. A classic sequence can sort them by outcome index, entry index, or ID and accidentally create a fake… Example: Candle 1000: reversal label becomes known. Candle 1000: continuation label becomes known. This is not: r

## Concepts

[[docs/obsidian_deep/02_concepts/AI_Agent_Layer|AI Agent Layer]], [[docs/obsidian_deep/02_concepts/Atomic_No-Sample|Atomic No-Sample]], [[docs/obsidian_deep/02_concepts/Decision_Node|Decision Node]], [[docs/obsidian_deep/02_concepts/Execution____Risk|Execution / Risk]], [[docs/obsidian_deep/02_concepts/Known-Time_Causality|Known-Time Causality]], [[docs/obsidian_deep/02_concepts/UI____React|UI / React]], [[docs/obsidian_deep/02_concepts/Validation____Audit|Validation / Audit]]

## Entities

D0009, D0010, H0004, H0005

## Headings

- Research Lessons and Failure Modes
  - Lesson 1 — Samples are not live decisions
  - Lesson 2 — Same-candle labels are simultaneous
  - Lesson 3 — Classic H4 overstated regime memory
  - Lesson 4 — Continuation PF without a stop is not trading PF
  - Lesson 5 — Reversal and continuation are different species
  - Lesson 6 — Debug validators must be promoted into main reports
  - Lesson 7 — Random baselines must be matched to the claim
  - Lesson 8 — A good report can still be non-tradable

## Related Source Documents

- [[lab/09_execution/mql5/README|README.md]] — score `30`
- [[docs/evidence/h0004_branch_regime_memory/45fad849057f_H0004_branch_regime_memory_atomic|H0004_branch_regime_memory_atomic.md]] — score `24`
- [[README|README.md]] — score `24`
- [[docs/debug/D0010_H4_ATOMIC_NO_SAMPLE_REGIME_AUDIT|D0010_H4_ATOMIC_NO_SAMPLE_REGIME_AUDIT.md]] — score `22`
- [[docs/mql_native/H0007_FLAG_COUNTING_F1_START_STRUCTURE|H0007_FLAG_COUNTING_F1_START_STRUCTURE.md]] — score `22`
- [[docs/reports/2026-06-20_h4_h5_gold_m10_report|2026-06-20_h4_h5_gold_m10_report.md]] — score `22`
- [[lab/03_validation/VAL0010_h4_atomic_no_sample_regime/README|README.md]] — score `20`
- [[lab/05_validation/VAL0010_h4_atomic_no_sample_regime/README|README.md]] — score `20`
- [[docs/debug/D0007_H5_CAUSAL_LIVE_REPLAY_AUDIT|D0007_H5_CAUSAL_LIVE_REPLAY_AUDIT.md]] — score `20`
- [[docs/mql_native/H0005_CONTEXTUAL_BRANCH_REGIME_STATE|H0005_CONTEXTUAL_BRANCH_REGIME_STATE.md]] — score `20`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
