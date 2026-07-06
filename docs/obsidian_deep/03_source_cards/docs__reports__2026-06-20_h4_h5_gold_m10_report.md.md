
---
type: source_card
source_path: "docs/reports/2026-06-20_h4_h5_gold_m10_report.md"
source_ext: ".md"
source_size: 3323
empty: false
generated_at: 2026-07-06
concepts: ["AI Agent Layer", "Atomic No-Sample", "Execution / Risk", "Known-Time Causality", "UI / React", "Validation / Audit", "Zone / RTV"]
entities: ["H0004", "H0005", "M0001", "M0002"]
---

# Source Card — 2026-06-20_h4_h5_gold_m10_report.md

## Source

[[docs/reports/2026-06-20_h4_h5_gold_m10_report|docs/reports/2026-06-20_h4_h5_gold_m10_report.md]]

## Summary

This report summarizes the project findings from the GOLD M10 H4/H5 logs and the subsequent code-audit discussion. Instrument: GOLD Timeframe: M10 Bars: approximately 21,370 M0001 events: approximately 3,197 Classic M0002 paired branch labels: approximately 2,484 The classic H4 sample sequence reported strong regime inertia: same-label transition rate: 72.82%, same lift over IID: 19.80 percentage points, lag-1 correlation: 0.4214. After causal known-candle batching: pure known-time batches: 1,807, ambiguous mixed-energy batches: 40, same-candle batch count: 441, causal same-label transition rate: 65.61%, causal same lift: 11.98 percentage points, causal lag-1 correlation: 0.2584. Interpretation: Same-candle sequencing was a real issue. The classic report overstated inertia. The causal effect remained meaningful after removing fake same-candle transitions. The correct next standard is ato

## Concepts

[[docs/obsidian_deep/02_concepts/AI_Agent_Layer|AI Agent Layer]], [[docs/obsidian_deep/02_concepts/Atomic_No-Sample|Atomic No-Sample]], [[docs/obsidian_deep/02_concepts/Execution____Risk|Execution / Risk]], [[docs/obsidian_deep/02_concepts/Known-Time_Causality|Known-Time Causality]], [[docs/obsidian_deep/02_concepts/UI____React|UI / React]], [[docs/obsidian_deep/02_concepts/Validation____Audit|Validation / Audit]], [[docs/obsidian_deep/02_concepts/Zone____RTV|Zone / RTV]]

## Entities

H0004, H0005, M0001, M0002

## Headings

- Report — H4/H5 GOLD M10 Review, 2026-06-20
  - Dataset context
  - H0004 classic vs causal-batch result
  - H0005 classic path result
    - Reversal
    - Continuation
  - Official conclusion
  - Decision impact
    - Reversal execution
    - Continuation execution

## Related Source Documents

- [[README|README.md]] — score `34`
- [[lab/02_hypotheses/H0004_branch_regime_memory_atomic|H0004_branch_regime_memory_atomic.md]] — score `32`
- [[lab/05_validation/VAL0011_main_atomic_no_sample_unification/README|README.md]] — score `30`
- [[docs/mql_native/H0007_FLAG_COUNTING_F1_START_STRUCTURE|H0007_FLAG_COUNTING_F1_START_STRUCTURE.md]] — score `27`
- [[lab/02_hypotheses/H0005_contextual_branch_regime_state|H0005_contextual_branch_regime_state.md]] — score `26`
- [[docs/articles/structural_regime_memory_without_samples|structural_regime_memory_without_samples.md]] — score `25`
- [[docs/debug/D0010_H4_ATOMIC_NO_SAMPLE_REGIME_AUDIT|D0010_H4_ATOMIC_NO_SAMPLE_REGIME_AUDIT.md]] — score `25`
- [[docs/mql_native/H0001_H0002_ALGORITHM_AND_HYPOTHESIS_README|H0001_H0002_ALGORITHM_AND_HYPOTHESIS_README.md]] — score `25`
- [[docs/mql_native/H0001_H0004_RESEARCH_LOCK|H0001_H0004_RESEARCH_LOCK.md]] — score `25`
- [[docs/mql_native/H0004_BRANCH_REGIME_CLUSTERING|H0004_BRANCH_REGIME_CLUSTERING.md]] — score `25`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
