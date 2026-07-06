
---
type: source_card
source_path: "docs/debug/H4_FAST_ATOMIC_MAIN_REPORT.md"
source_ext: ".md"
source_size: 1649
empty: false
generated_at: 2026-07-06
concepts: ["Atomic No-Sample", "Decision Node", "Known-Time Causality", "MQL Native", "Python Brain", "UI / React", "Validation / Audit"]
entities: ["M0001", "M0002", "M0004"]
---

# Source Card — H4_FAST_ATOMIC_MAIN_REPORT.md

## Source

[[docs/debug/H4_FAST_ATOMIC_MAIN_REPORT|docs/debug/H4_FAST_ATOMIC_MAIN_REPORT.md]]

## Summary

M0004 build 1.07 keeps the official no-sample contract but removes the heavy strict prefix replay from the default main report path. The first atomic no-sample implementation was intentionally strict: for every replay candle it rebuilt the prefix bars, structural nodes, and M0001 events. That is useful as a validator, but it is too heavy for normal re… The main expert now defaults to: This mode runs M0001 once on the final closed-bar stream, classifies raw M0001 events by their knowable candle, groups all events with the same `known_time` into one simultaneous batch, and computes transitions only betw… It still does not build M0002 branch samples and it still does not treat same-candle regimes as sequential. For small debugging runs only: Strict mode keeps the old prefix-by-prefix validator behavior and may be slow on large histories. The main EA now exposes `InpAtomicReportMode` as an i

## Concepts

[[docs/obsidian_deep/02_concepts/Atomic_No-Sample|Atomic No-Sample]], [[docs/obsidian_deep/02_concepts/Decision_Node|Decision Node]], [[docs/obsidian_deep/02_concepts/Known-Time_Causality|Known-Time Causality]], [[docs/obsidian_deep/02_concepts/MQL_Native|MQL Native]], [[docs/obsidian_deep/02_concepts/Python_Brain|Python Brain]], [[docs/obsidian_deep/02_concepts/UI____React|UI / React]], [[docs/obsidian_deep/02_concepts/Validation____Audit|Validation / Audit]]

## Entities

M0001, M0002, M0004

## Headings

- H4 Fast Atomic Main Report
  - Why this was needed
  - New default
  - Strict mode
  - Compile sync note (release 1.01)

## Related Source Documents

- [[docs/architecture|architecture.md]] — score `29`
- [[docs/debug/D0010_H4_ATOMIC_NO_SAMPLE_REGIME_AUDIT|D0010_H4_ATOMIC_NO_SAMPLE_REGIME_AUDIT.md]] — score `26`
- [[docs/debug/MAIN_ATOMIC_NO_SAMPLE_UNIFICATION|MAIN_ATOMIC_NO_SAMPLE_UNIFICATION.md]] — score `26`
- [[docs/mql_native/MODULE_MAP|MODULE_MAP.md]] — score `25`
- [[lab/03_validation/VAL0012_h4_fast_atomic_main/README|README.md]] — score `25`
- [[lab/03_experiments/EXP0003_mql_native_m0002/report|report.md]] — score `24`
- [[lab/03_experiments/EXP0002_mql_native_m0001/report|report.md]] — score `23`
- [[lab/05_validation/VAL_M0001_MQL_NATIVE/report|report.md]] — score `23`
- [[README|README.md]] — score `22`
- [[docs/debug/D0005_H5_NO_FUTURE_WALK_FORWARD_AUDIT|D0005_H5_NO_FUTURE_WALK_FORWARD_AUDIT.md]] — score `21`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
