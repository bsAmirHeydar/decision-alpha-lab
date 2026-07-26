
---
type: source_card
source_path: "docs/debug/D0008_H4_CAUSAL_BATCH_REPORT.md"
source_ext: ".md"
source_size: 1630
empty: false
generated_at: 2026-07-06
concepts: ["AI Agent Layer", "Execution / Risk", "Known-Time Causality", "UI / React", "Validation / Audit"]
entities: ["D0008", "H0004"]
---

# Source Card — D0008_H4_CAUSAL_BATCH_REPORT.md

## Source

[[docs/debug/D0008_H4_CAUSAL_BATCH_REPORT|docs/debug/D0008_H4_CAUSAL_BATCH_REPORT.md]]

## Summary

This release fixes the main H0004 live-validity ambiguity: multiple branch samples can become knowable on the same candle. The classic H0004 report sorts samples by `outcome_index`, then by `entry_index`, then by `id`. T… The new causal batch layer groups samples by their knowable candle: `known_index = outcome_index` when available else `exit_index` else `entry_index` All samples with the same `known_index` are treated as simultaneous. A batch with only reversal labels is a reversal batch. A batch with only continuation labels is a continuation batch. A batch containing both reversal… The classic report is still printed for continuity, but the new `DAL_M0004_FINAL_CAUSAL_*` lines are the live-style sequence diagnostics that should be used before trusting H0004 as a regime-memory signal. Important new log lines: `DAL_M0004_FINAL_CAUSAL_BATCH_AUDIT` `DAL_M0004_FINAL_CAUSAL_BATCH_SUMMARY`

## Concepts

[[docs/obsidian_deep/02_concepts/AI_Agent_Layer|AI Agent Layer]], [[docs/obsidian_deep/02_concepts/Execution____Risk|Execution / Risk]], [[docs/obsidian_deep/02_concepts/Known-Time_Causality|Known-Time Causality]], [[docs/obsidian_deep/02_concepts/UI____React|UI / React]], [[docs/obsidian_deep/02_concepts/Validation____Audit|Validation / Audit]]

## Entities

D0008, H0004

## Headings

- D0008 / H0004 Causal Known-Candle Batch Report

## Related Source Documents

- [[lab/03_experiments/EXP0004_mql_native_m0004/report|report.md]] — score `16`
- [[docs/articles/structural_regime_memory_without_samples|structural_regime_memory_without_samples.md]] — score `15`
- [[docs/mql_native/H0007_FLAG_COUNTING_F1_START_STRUCTURE|H0007_FLAG_COUNTING_F1_START_STRUCTURE.md]] — score `15`
- [[docs/reports/2026-06-20_h4_h5_gold_m10_report|2026-06-20_h4_h5_gold_m10_report.md]] — score `15`
- [[docs/research_lessons_and_failure_modes|research_lessons_and_failure_modes.md]] — score `15`
- [[docs/evidence/h0004_branch_regime_memory/45fad849057f_H0004_branch_regime_memory_atomic|H0004_branch_regime_memory_atomic.md]] — score `15`
- [[README|README.md]] — score `15`
- [[docs/debug/D0007_H5_CAUSAL_LIVE_REPLAY_AUDIT|D0007_H5_CAUSAL_LIVE_REPLAY_AUDIT.md]] — score `14`
- [[docs/debug/D0010_H4_ATOMIC_NO_SAMPLE_REGIME_AUDIT|D0010_H4_ATOMIC_NO_SAMPLE_REGIME_AUDIT.md]] — score `14`
- [[docs/debug/H6_STANDALONE_OPTIONALITY_EDGE_MAP|H6_STANDALONE_OPTIONALITY_EDGE_MAP.md]] — score `14`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
