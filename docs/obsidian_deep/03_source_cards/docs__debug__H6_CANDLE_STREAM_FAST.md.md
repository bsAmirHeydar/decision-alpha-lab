
---
type: source_card
source_path: "docs/debug/H6_CANDLE_STREAM_FAST.md"
source_ext: ".md"
source_size: 1374
empty: false
generated_at: 2026-07-06
concepts: ["Atomic No-Sample", "Convexity / Optionality", "Known-Time Causality", "UI / React", "Validation / Audit"]
entities: ["H0006", "M0001", "M0002"]
---

# Source Card — H6_CANDLE_STREAM_FAST.md

## Source

[[docs/debug/H6_CANDLE_STREAM_FAST|docs/debug/H6_CANDLE_STREAM_FAST.md]]

## Summary

Release 108 changes the standalone H0006 report from a heavy batch/edge-map workflow into a fast forward candle-stream workflow by default. Still atomic and no-sample. Still uses raw M0001 known-time batches. Still treats same-known-time events as simultaneous. Mixed reversal/continuation batches remain ambiguous and are skipped from pure H6 measurements. The H6 measurement starts only after the batch is known. Default engine: `CANDLE_FORWARD_STREAM`. For each pure known-time batch at bar `k`, H6 opens an observation at `k+1` using `NEXT_OPEN` by default. Then the engine walks candles forward once, updates active observations with each bar's high/low, and closes them… This avoids repeated horizon scans for optionality and avoids strict prefix rebuilds. It is candle-forward/live-style measurement, not M0002 sample replay. Daily default inputs are intentionally light: stress off edge map o

## Concepts

[[docs/obsidian_deep/02_concepts/Atomic_No-Sample|Atomic No-Sample]], [[docs/obsidian_deep/02_concepts/Convexity____Optionality|Convexity / Optionality]], [[docs/obsidian_deep/02_concepts/Known-Time_Causality|Known-Time Causality]], [[docs/obsidian_deep/02_concepts/UI____React|UI / React]], [[docs/obsidian_deep/02_concepts/Validation____Audit|Validation / Audit]]

## Entities

H0006, M0001, M0002

## Headings

- H6 Candle-Stream Fast Optionality
  - Contract
  - Engine
  - Speed defaults
  - Key audit fields

## Related Source Documents

- [[docs/debug/H6_NODE_SURVIVAL_MAP|H6_NODE_SURVIVAL_MAP.md]] — score `22`
- [[docs/debug/H6_FAST_ACCURATE_OPTIONALITY|H6_FAST_ACCURATE_OPTIONALITY.md]] — score `21`
- [[lab/02_hypotheses/H0004_branch_regime_memory_atomic|H0004_branch_regime_memory_atomic.md]] — score `20`
- [[lab/03_experiments/EXP0003_mql_native_m0002/report|report.md]] — score `20`
- [[docs/debug/D0010_H4_ATOMIC_NO_SAMPLE_REGIME_AUDIT|D0010_H4_ATOMIC_NO_SAMPLE_REGIME_AUDIT.md]] — score `19`
- [[docs/debug/H4_FAST_ATOMIC_MAIN_REPORT|H4_FAST_ATOMIC_MAIN_REPORT.md]] — score `19`
- [[docs/debug/H6_REACTION_BOX_ZONES|H6_REACTION_BOX_ZONES.md]] — score `19`
- [[docs/debug/MAIN_ATOMIC_NO_SAMPLE_UNIFICATION|MAIN_ATOMIC_NO_SAMPLE_UNIFICATION.md]] — score `19`
- [[docs/mql_native/H0007_FLAG_COUNTING_F1_START_STRUCTURE|H0007_FLAG_COUNTING_F1_START_STRUCTURE.md]] — score `18`
- [[docs/architecture|architecture.md]] — score `18`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
