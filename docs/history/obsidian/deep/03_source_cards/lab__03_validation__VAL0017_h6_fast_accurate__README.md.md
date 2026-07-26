
---
type: source_card
source_path: "lab/03_validation/VAL0017_h6_fast_accurate/README.md"
source_ext: ".md"
source_size: 995
empty: false
generated_at: 2026-07-06
concepts: ["AI Agent Layer", "Atomic No-Sample", "Convexity / Optionality", "Execution / Risk", "Known-Time Causality", "UI / React", "Validation / Audit"]
entities: ["H0006", "VAL0017"]
---

# Source Card — README.md

## Source

[[lab/03_validation/VAL0017_h6_fast_accurate/README|lab/03_validation/VAL0017_h6_fast_accurate/README.md]]

## Summary

Goal: keep H0006 standalone and atomic/no-sample while reducing runtime and improving execution realism. Default anchor is `NEXT_OPEN`, not the known candle close. Stress can run in fast mode using mean excursion and Tail2 hit-rate instead of full quantile sorting. Edge map can run in core mode instead of full bucket mode. Fast/main/slow horizons can be enabled independently. `InpH6StressMode=1` `InpH6EdgeMapLevel=1` `InpH6ReportFastHorizon=true` `InpH6ReportMainHorizon=true` `InpH6ReportSlowHorizon=false` `InpH6EntryAnchorMode=1` `InpH6StressMode=2` `InpH6EdgeMapLevel=2` all horizons enabled `InpPermutationIterations=500` This validation does not ask whether reversal has a better win rate. It asks whether reversal known-time batches mark fatter optionality tails compared with continuation and with shuffled labels.

## Concepts

[[docs/obsidian_deep/02_concepts/AI_Agent_Layer|AI Agent Layer]], [[docs/obsidian_deep/02_concepts/Atomic_No-Sample|Atomic No-Sample]], [[docs/obsidian_deep/02_concepts/Convexity____Optionality|Convexity / Optionality]], [[docs/obsidian_deep/02_concepts/Execution____Risk|Execution / Risk]], [[docs/obsidian_deep/02_concepts/Known-Time_Causality|Known-Time Causality]], [[docs/obsidian_deep/02_concepts/UI____React|UI / React]], [[docs/obsidian_deep/02_concepts/Validation____Audit|Validation / Audit]]

## Entities

H0006, VAL0017

## Headings

- VAL0017 — H6 Fast Accurate Optionality
  - What changed
  - Recommended quick run
  - Recommended final run
  - Interpretation

## Related Source Documents

- [[docs/debug/H6_FAST_ACCURATE_OPTIONALITY|H6_FAST_ACCURATE_OPTIONALITY.md]] — score `17`
- [[docs/debug/H6_STANDALONE_OPTIONALITY_EDGE_MAP|H6_STANDALONE_OPTIONALITY_EDGE_MAP.md]] — score `17`
- [[docs/mql_native/H0007_FLAG_COUNTING_F1_START_STRUCTURE|H0007_FLAG_COUNTING_F1_START_STRUCTURE.md]] — score `17`
- [[lab/03_experiments/EXP0004_mql_native_m0004/report|report.md]] — score `16`
- [[docs/debug/H6_CANDLE_STREAM_FAST|H6_CANDLE_STREAM_FAST.md]] — score `15`
- [[docs/debug/H4_DEEP_H6_OPTIONALITY_REPORT|H4_DEEP_H6_OPTIONALITY_REPORT.md]] — score `14`
- [[docs/glossary|glossary.md]] — score `14`
- [[docs/principles|principles.md]] — score `14`
- [[docs/evidence/h0004_branch_regime_memory/45fad849057f_H0004_branch_regime_memory_atomic|H0004_branch_regime_memory_atomic.md]] — score `14`
- [[docs/evidence/h0005_directional_memory_execution/57d9666c6533_H0005_directional_memory_atomic|H0005_directional_memory_atomic.md]] — score `14`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
