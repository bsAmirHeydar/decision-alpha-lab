
---
type: source_card
source_path: "docs/evidence/h0004_branch_regime_memory/45fad849057f_H0004_branch_regime_memory_atomic.md"
source_ext: ".md"
source_size: 2301
empty: false
generated_at: 2026-07-06
concepts: ["AI Agent Layer", "Atomic No-Sample", "Convexity / Optionality", "Decision Node", "Execution / Risk", "Known-Time Causality", "UI / React", "Validation / Audit"]
entities: ["H0004", "H0005", "M0001", "M0002"]
---

# Source Card — H0004_branch_regime_memory_atomic.md

## Source

[[docs/evidence/h0004_branch_regime_memory/45fad849057f_H0004_branch_regime_memory_atomic|docs/evidence/h0004_branch_regime_memory/45fad849057f_H0004_branch_regime_memory_atomic.md]]

## Summary

Do reversal and continuation branch regimes display persistence beyond random ordering when measured by the time at which the regime became knowable? The classic formulation used M0002 branch samples and sorted completed labels into a chronological sequence. This was useful for exploration, but it had a serious live-validity risk: several labels could become known on… The official H0004 formulation is atomic and no-sample: replay closed candles, build structural nodes and raw M0001 events from the prefix, collect events that become knowable at the current candle/time, group them into one known-time batch, classify the batch as reversal, continuation, or ambiguous, compute transitions only between different known-time batches. After enforcing known-time batching, reversal and continuation labels do not persist beyond what is expected from random label order under appropriate null models.

## Concepts

[[docs/obsidian_deep/02_concepts/AI_Agent_Layer|AI Agent Layer]], [[docs/obsidian_deep/02_concepts/Atomic_No-Sample|Atomic No-Sample]], [[docs/obsidian_deep/02_concepts/Convexity____Optionality|Convexity / Optionality]], [[docs/obsidian_deep/02_concepts/Decision_Node|Decision Node]], [[docs/obsidian_deep/02_concepts/Execution____Risk|Execution / Risk]], [[docs/obsidian_deep/02_concepts/Known-Time_Causality|Known-Time Causality]], [[docs/obsidian_deep/02_concepts/UI____React|UI / React]], [[docs/obsidian_deep/02_concepts/Validation____Audit|Validation / Audit]]

## Entities

H0004, H0005, M0001, M0002

## Headings

- H0004 — Branch Regime Memory
  - Research question
  - Old formulation
  - Current formulation
  - Null hypothesis
  - Alternative hypothesis
  - Key failure mode addressed
  - Evidence required
  - Interpretation

## Related Source Documents

- [[README|README.md]] — score `34`
- [[docs/reports/2026-06-20_h4_h5_gold_m10_report|2026-06-20_h4_h5_gold_m10_report.md]] — score `32`
- [[lab/05_validation/VAL0011_main_atomic_no_sample_unification/README|README.md]] — score `30`
- [[docs/mql_native/H0007_FLAG_COUNTING_F1_START_STRUCTURE|H0007_FLAG_COUNTING_F1_START_STRUCTURE.md]] — score `29`
- [[docs/debug/D0010_H4_ATOMIC_NO_SAMPLE_REGIME_AUDIT|D0010_H4_ATOMIC_NO_SAMPLE_REGIME_AUDIT.md]] — score `27`
- [[docs/mql_native/MODULE_MAP|MODULE_MAP.md]] — score `27`
- [[lab/02_hypotheses/H0005_contextual_branch_regime_state|H0005_contextual_branch_regime_state.md]] — score `27`
- [[docs/execution/H0005_R1_SIX_SLOT_TOUCH_LEDGER|H0005_R1_SIX_SLOT_TOUCH_LEDGER.md]] — score `27`
- [[docs/evidence/h0004_branch_regime_clustering/9b519b63fc23_H0004_branch_regime_clustering|H0004_branch_regime_clustering.md]] — score `26`
- [[docs/articles/structural_regime_memory_without_samples|structural_regime_memory_without_samples.md]] — score `25`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
