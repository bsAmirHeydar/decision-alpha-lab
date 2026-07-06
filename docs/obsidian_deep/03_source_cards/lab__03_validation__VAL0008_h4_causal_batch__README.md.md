
---
type: source_card
source_path: "lab/03_validation/VAL0008_h4_causal_batch/README.md"
source_ext: ".md"
source_size: 825
empty: false
generated_at: 2026-07-06
concepts: ["AI Agent Layer", "Execution / Risk", "Known-Time Causality", "MQL Native", "Validation / Audit"]
entities: ["H0004", "VAL0008"]
---

# Source Card — README.md

## Source

[[lab/03_validation/VAL0008_h4_causal_batch/README|lab/03_validation/VAL0008_h4_causal_batch/README.md]]

## Summary

Goal: validate H0004 branch-regime memory using the candle on which each regime label becomes knowable, not an arbitrary sample order inside the same candle. Procedure: Run `M0004_BranchRegimeClustering.mq5` after this release. Compare the classic H4 output against the new `DAL_M0004_FINAL_CAUSAL_*` lines. Treat mixed same-candle reversal/continuation batches as ambiguous rather than as a sequential regime transition. Decision rule: If `removedFakeTransitionPct` is small and causal metrics stay close to classic metrics, H4 is robust to the batch correction. If `removedFakeTransitionPct` is high or `DAL_M0004_FINAL_CAUSAL_VS_CLASSIC` says `classic_sequence_materially_changed_by_causal_batching`, the old H4 result must not be used for live regime inference.

## Concepts

[[docs/obsidian_deep/02_concepts/AI_Agent_Layer|AI Agent Layer]], [[docs/obsidian_deep/02_concepts/Execution____Risk|Execution / Risk]], [[docs/obsidian_deep/02_concepts/Known-Time_Causality|Known-Time Causality]], [[docs/obsidian_deep/02_concepts/MQL_Native|MQL Native]], [[docs/obsidian_deep/02_concepts/Validation____Audit|Validation / Audit]]

## Entities

H0004, VAL0008

## Headings

- VAL0008 — H4 Causal Batch Validation

## Related Source Documents

- [[docs/mql_native/H0007_FLAG_COUNTING_F1_START_STRUCTURE|H0007_FLAG_COUNTING_F1_START_STRUCTURE.md]] — score `15`
- [[README|README.md]] — score `15`
- [[docs/articles/structural_regime_memory_without_samples|structural_regime_memory_without_samples.md]] — score `13`
- [[docs/debug/D0007_H5_CAUSAL_LIVE_REPLAY_AUDIT|D0007_H5_CAUSAL_LIVE_REPLAY_AUDIT.md]] — score `13`
- [[docs/debug/D0008_H4_CAUSAL_BATCH_REPORT|D0008_H4_CAUSAL_BATCH_REPORT.md]] — score `13`
- [[docs/debug/H6_STANDALONE_OPTIONALITY_EDGE_MAP|H6_STANDALONE_OPTIONALITY_EDGE_MAP.md]] — score `13`
- [[docs/mql_native/MODULE_MAP|MODULE_MAP.md]] — score `13`
- [[docs/reports/2026-06-20_h4_h5_gold_m10_report|2026-06-20_h4_h5_gold_m10_report.md]] — score `13`
- [[docs/research_lessons_and_failure_modes|research_lessons_and_failure_modes.md]] — score `13`
- [[lab/02_hypotheses/H0004_branch_regime_memory_atomic|H0004_branch_regime_memory_atomic.md]] — score `13`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
