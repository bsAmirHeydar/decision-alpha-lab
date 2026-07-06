
---
type: source_card
source_path: "lab/04_analysis/ANL004_h4_causal_batch_vs_classic/README.md"
source_ext: ".md"
source_size: 790
empty: false
generated_at: 2026-07-06
concepts: ["Atomic No-Sample", "Known-Time Causality", "UI / React"]
entities: ["ANL004", "H0004"]
---

# Source Card — README.md

## Source

[[lab/04_analysis/ANL004_h4_causal_batch_vs_classic/README|lab/04_analysis/ANL004_h4_causal_batch_vs_classic/README.md]]

## Summary

How much did same-candle fake sequencing inflate H0004 regime memory? Causal batching reduced the reported memory but did not eliminate it. Classic sequence: samePct: 72.82%, sameLift: 19.80 percentage points, lag1Corr: 0.4214. Causal known-candle pure batches: samePct: 65.61%, sameLift: 11.98 percentage points, lag1Corr: 0.2584. The old report was too optimistic, but not entirely fake. Roughly speaking, part of the effect was sequencing artifact, and part remained after removing same-time ambiguity. Classic H4 should remain as a historical/debug reference only. Official H4 claims should use atomic no-sample known-time batches.

## Concepts

[[docs/obsidian_deep/02_concepts/Atomic_No-Sample|Atomic No-Sample]], [[docs/obsidian_deep/02_concepts/Known-Time_Causality|Known-Time Causality]], [[docs/obsidian_deep/02_concepts/UI____React|UI / React]]

## Entities

ANL004, H0004

## Headings

- ANL004 — H4 Classic vs Causal Batch Analysis
  - Question
  - Key finding
  - Interpretation
  - Research decision

## Related Source Documents

- [experiments.yaml](../../registry/experiments.yaml) — score `14`
- [[docs/debug/D0010_H4_ATOMIC_NO_SAMPLE_REGIME_AUDIT|D0010_H4_ATOMIC_NO_SAMPLE_REGIME_AUDIT.md]] — score `11`
- [[docs/debug/H6_STANDALONE_OPTIONALITY_EDGE_MAP|H6_STANDALONE_OPTIONALITY_EDGE_MAP.md]] — score `11`
- [[docs/reports/2026-06-20_h4_h5_gold_m10_report|2026-06-20_h4_h5_gold_m10_report.md]] — score `11`
- [[docs/research_lessons_and_failure_modes|research_lessons_and_failure_modes.md]] — score `11`
- [[lab/02_hypotheses/H0004_branch_regime_memory_atomic|H0004_branch_regime_memory_atomic.md]] — score `11`
- [[lab/03_validation/VAL0010_h4_atomic_no_sample_regime/README|README.md]] — score `11`
- [[lab/03_validation/VAL0012_h4_fast_atomic_main/README|README.md]] — score `11`
- [[lab/05_validation/VAL0010_h4_atomic_no_sample_regime/README|README.md]] — score `11`
- [[lab/05_validation/VAL0011_main_atomic_no_sample_unification/README|README.md]] — score `11`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
