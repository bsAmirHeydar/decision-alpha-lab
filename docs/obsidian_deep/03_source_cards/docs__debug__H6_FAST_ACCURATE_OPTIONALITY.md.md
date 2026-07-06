
---
type: source_card
source_path: "docs/debug/H6_FAST_ACCURATE_OPTIONALITY.md"
source_ext: ".md"
source_size: 1701
empty: false
generated_at: 2026-07-06
concepts: ["Atomic No-Sample", "Convexity / Optionality", "Execution / Risk", "Known-Time Causality", "UI / React", "Validation / Audit"]
entities: ["H0006", "M0001"]
---

# Source Card — H6_FAST_ACCURATE_OPTIONALITY.md

## Source

[[docs/debug/H6_FAST_ACCURATE_OPTIONALITY|docs/debug/H6_FAST_ACCURATE_OPTIONALITY.md]]

## Summary

This release makes the standalone H0006 optionality report faster and more execution-realistic without returning to samples. H6 remains atomic and no-sample: `sampleCalls=0` `branchSamplesBuilt=0` `m0002Calls=0` sequence is built from raw M0001 known-time batches events that become known on the same candle are simultaneous, not sequential The default H6 entry anchor is now `NEXT_OPEN`. Previously, future optionality used the known candle close as the anchor. The new default measures future excursion from the next candle open, which is closer to what could be acted on after the regime batch becomes know… Set `InpH6EntryAnchorMode=0` to compare against the old known-close anchor. H6 stress and edge maps now have levels: `InpH6StressMode=0`: no optionality stress. `InpH6StressMode=1`: fast null using mean absolute excursion and hit-rate above Tail2. No per-iteration quantile sorting. `InpH6

## Concepts

[[docs/obsidian_deep/02_concepts/Atomic_No-Sample|Atomic No-Sample]], [[docs/obsidian_deep/02_concepts/Convexity____Optionality|Convexity / Optionality]], [[docs/obsidian_deep/02_concepts/Execution____Risk|Execution / Risk]], [[docs/obsidian_deep/02_concepts/Known-Time_Causality|Known-Time Causality]], [[docs/obsidian_deep/02_concepts/UI____React|UI / React]], [[docs/obsidian_deep/02_concepts/Validation____Audit|Validation / Audit]]

## Entities

H0006, M0001

## Headings

- H6 Fast Accurate Optionality Report
  - Contract
  - Accuracy change
  - Speed controls
  - New audit line

## Related Source Documents

- [[docs/debug/H6_CANDLE_STREAM_FAST|H6_CANDLE_STREAM_FAST.md]] — score `21`
- [[docs/mql_native/H0007_FLAG_COUNTING_F1_START_STRUCTURE|H0007_FLAG_COUNTING_F1_START_STRUCTURE.md]] — score `20`
- [[docs/debug/H6_NODE_SURVIVAL_MAP|H6_NODE_SURVIVAL_MAP.md]] — score `19`
- [[lab/03_validation/VAL0017_h6_fast_accurate/README|README.md]] — score `17`
- [[lab/02_hypotheses/H0004_branch_regime_memory_atomic|H0004_branch_regime_memory_atomic.md]] — score `17`
- [[lab/02_hypotheses/H0005_directional_memory_atomic|H0005_directional_memory_atomic.md]] — score `17`
- [[lab/03_experiments/EXP0002_mql_native_m0001/report|report.md]] — score `17`
- [[lab/03_experiments/EXP0003_mql_native_m0002/report|report.md]] — score `17`
- [[lab/05_validation/VAL_M0001_MQL_NATIVE/report|report.md]] — score `17`
- [[docs/debug/H6_STANDALONE_OPTIONALITY_EDGE_MAP|H6_STANDALONE_OPTIONALITY_EDGE_MAP.md]] — score `16`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
