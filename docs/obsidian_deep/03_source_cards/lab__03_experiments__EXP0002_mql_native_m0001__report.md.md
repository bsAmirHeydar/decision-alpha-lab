
---
type: source_card
source_path: "lab/03_experiments/EXP0002_mql_native_m0001/report.md"
source_ext: ".md"
source_size: 688
empty: false
generated_at: 2026-07-06
concepts: ["Decision Node", "Known-Time Causality", "MQL Native", "Python Brain", "Validation / Audit"]
entities: ["EXP0002", "M0001"]
---

# Source Card — report.md

## Source

[[lab/03_experiments/EXP0002_mql_native_m0001/report|lab/03_experiments/EXP0002_mql_native_m0001/report.md]]

## Summary

Move M0001 from a Python/MQL bridge into a pure MQL5 runtime while preserving the lab research workflow. A native MQL5 implementation will produce faster, clearer, and more live-safe visual validation than an external Python bridge because the detector, event engine, tester timeline, and chart objects live in the same runti… L-rule nodes appear only after `L` right-side candles exist. Markers point to the true pivot candle. Event construction starts only from `active_from_index`. No future candles are available to the engine. Visual redraw is synchronous with MT5 tester time.

## Concepts

[[docs/obsidian_deep/02_concepts/Decision_Node|Decision Node]], [[docs/obsidian_deep/02_concepts/Known-Time_Causality|Known-Time Causality]], [[docs/obsidian_deep/02_concepts/MQL_Native|MQL Native]], [[docs/obsidian_deep/02_concepts/Python_Brain|Python Brain]], [[docs/obsidian_deep/02_concepts/Validation____Audit|Validation / Audit]]

## Entities

EXP0002, M0001

## Headings

- EXP0002 — MQL-native M0001 Runtime
  - Objective
  - Hypothesis
  - Validation Target

## Related Source Documents

- [[docs/architecture|architecture.md]] — score `15`
- [[docs/debug/H4_FAST_ATOMIC_MAIN_REPORT|H4_FAST_ATOMIC_MAIN_REPORT.md]] — score `15`
- [metadata.yaml](../../lab/03_experiments/EXP0002_mql_native_m0001/metadata.yaml) — score `13`
- [[docs/debug/D0005_H5_NO_FUTURE_WALK_FORWARD_AUDIT|D0005_H5_NO_FUTURE_WALK_FORWARD_AUDIT.md]] — score `13`
- [[docs/debug/D0006_H5_LIVE_TOUCH_REPLAY_AUDIT|D0006_H5_LIVE_TOUCH_REPLAY_AUDIT.md]] — score `13`
- [[docs/M0001_EVENT_BRIDGE_ARCHITECTURE|M0001_EVENT_BRIDGE_ARCHITECTURE.md]] — score `13`
- [[docs/M0001_MQL_INPUT_PARAMETER_BRIDGE|M0001_MQL_INPUT_PARAMETER_BRIDGE.md]] — score `13`
- [[docs/M0001_SINGLE_SOURCE_LIVE_ARCHITECTURE|M0001_SINGLE_SOURCE_LIVE_ARCHITECTURE.md]] — score `13`
- [[docs/MQL_LIVE_ALL_IN_ONE_APPLY|MQL_LIVE_ALL_IN_ONE_APPLY.md]] — score `13`
- [[docs/mql_native/H0007_FLAG_COUNTING_F1_START_STRUCTURE|H0007_FLAG_COUNTING_F1_START_STRUCTURE.md]] — score `13`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
