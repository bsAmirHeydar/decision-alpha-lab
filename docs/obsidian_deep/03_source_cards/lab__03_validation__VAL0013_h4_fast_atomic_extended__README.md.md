
---
type: source_card
source_path: "lab/03_validation/VAL0013_h4_fast_atomic_extended/README.md"
source_ext: ".md"
source_size: 582
empty: false
generated_at: 2026-07-06
concepts: ["Known-Time Causality", "Validation / Audit"]
entities: ["M0001", "M0002", "VAL0013"]
---

# Source Card — README.md

## Source

[[lab/03_validation/VAL0013_h4_fast_atomic_extended/README|lab/03_validation/VAL0013_h4_fast_atomic_extended/README.md]]

## Summary

Purpose: restore rich H4 reporting without returning to the old sample-based report or the heavy strict prefix replay. Contract: No M0002 branch samples. No outcome-sorted sample sequence. Raw M0001 events are grouped by known candle/time. Same-known-time events are simultaneous. Mixed reversal/continuation batches are ambiguous and skipped. M0001 is computed once in the main fast mode. Use `InpAtomicPrintExtendedReport=true` to print lightweight lag decay, run-length transition, and block profile diagnostics.

## Concepts

[[docs/obsidian_deep/02_concepts/Known-Time_Causality|Known-Time Causality]], [[docs/obsidian_deep/02_concepts/Validation____Audit|Validation / Audit]]

## Entities

M0001, M0002, VAL0013

## Headings

- VAL0013 — H4 Fast Atomic Extended Diagnostics

## Related Source Documents

- [[lab/03_experiments/EXP0003_mql_native_m0002/report|report.md]] — score `20`
- [[lab/03_experiments/EXP0002_mql_native_m0001/report|report.md]] — score `17`
- [[lab/05_validation/VAL_M0001_MQL_NATIVE/report|report.md]] — score `15`
- [[docs/architecture|architecture.md]] — score `14`
- [[docs/articles/structural_regime_memory_without_samples|structural_regime_memory_without_samples.md]] — score `14`
- [[docs/debug/D0010_H4_ATOMIC_NO_SAMPLE_REGIME_AUDIT|D0010_H4_ATOMIC_NO_SAMPLE_REGIME_AUDIT.md]] — score `14`
- [[docs/debug/H4_ATOMIC_FULL_STRESS_CONTEXT|H4_ATOMIC_FULL_STRESS_CONTEXT.md]] — score `14`
- [[docs/debug/H4_FAST_ATOMIC_MAIN_REPORT|H4_FAST_ATOMIC_MAIN_REPORT.md]] — score `14`
- [[docs/debug/H6_CANDLE_STREAM_FAST|H6_CANDLE_STREAM_FAST.md]] — score `14`
- [[docs/debug/H6_NODE_SURVIVAL_MAP|H6_NODE_SURVIVAL_MAP.md]] — score `14`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
