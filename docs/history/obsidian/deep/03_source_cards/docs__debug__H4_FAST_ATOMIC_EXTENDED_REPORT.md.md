
---
type: source_card
source_path: "docs/debug/H4_FAST_ATOMIC_EXTENDED_REPORT.md"
source_ext: ".md"
source_size: 825
empty: false
generated_at: 2026-07-06
concepts: ["Atomic No-Sample", "Known-Time Causality", "UI / React", "Validation / Audit"]
entities: []
---

# Source Card — H4_FAST_ATOMIC_EXTENDED_REPORT.md

## Source

[[docs/debug/H4_FAST_ATOMIC_EXTENDED_REPORT|docs/debug/H4_FAST_ATOMIC_EXTENDED_REPORT.md]]

## Summary

This update keeps the official H4 report no-sample and fast, while restoring useful diagnostics that were previously only visible in the legacy sample report. The report still uses `sampleCalls=0`, `branchSamplesBuilt=0`, `m0002Calls=0`, and `m0001ComputePasses=1`. It does not run strict prefix replay by default. New lightweight outputs: `DAL_D0010_ATOMIC_LAG_DECAY` `DAL_D0010_ATOMIC_RUN_LENGTH_TRANSITION` `DAL_D0010_ATOMIC_BLOCK_PROFILE_FAST` `DAL_D0010_ATOMIC_BLOCK_PROFILE_MAIN` `DAL_D0010_ATOMIC_BLOCK_PROFILE_SLOW` These diagnostics are computed over pure known-time batches, so events that become known on the same candle are never treated as sequential. Mixed reversal/continuation batches remain ambiguous and are skipped from trans…

## Concepts

[[docs/obsidian_deep/02_concepts/Atomic_No-Sample|Atomic No-Sample]], [[docs/obsidian_deep/02_concepts/Known-Time_Causality|Known-Time Causality]], [[docs/obsidian_deep/02_concepts/UI____React|UI / React]], [[docs/obsidian_deep/02_concepts/Validation____Audit|Validation / Audit]]

## Entities

—

## Headings

- H4 Fast Atomic Extended Report

## Related Source Documents

- [[lab/03_experiments/EXP0002_mql_native_m0001/report|report.md]] — score `12`
- [[lab/03_experiments/EXP0004_mql_native_m0004/report|report.md]] — score `12`
- [[lab/05_validation/VAL_M0001_MQL_NATIVE/report|report.md]] — score `12`
- [[lab/03_experiments/EXP0003_mql_native_m0002/report|report.md]] — score `10`
- [[lab/05_validation/VAL001/report|report.md]] — score `10`
- [[docs/debug/D0010_H4_ATOMIC_NO_SAMPLE_REGIME_AUDIT|D0010_H4_ATOMIC_NO_SAMPLE_REGIME_AUDIT.md]] — score `9`
- [[docs/debug/H4_DEEP_H6_OPTIONALITY_REPORT|H4_DEEP_H6_OPTIONALITY_REPORT.md]] — score `9`
- [[docs/debug/H4_FAST_ATOMIC_MAIN_REPORT|H4_FAST_ATOMIC_MAIN_REPORT.md]] — score `9`
- [[docs/debug/H6_CANDLE_STREAM_FAST|H6_CANDLE_STREAM_FAST.md]] — score `9`
- [[docs/debug/H6_FAST_ACCURATE_OPTIONALITY|H6_FAST_ACCURATE_OPTIONALITY.md]] — score `9`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
