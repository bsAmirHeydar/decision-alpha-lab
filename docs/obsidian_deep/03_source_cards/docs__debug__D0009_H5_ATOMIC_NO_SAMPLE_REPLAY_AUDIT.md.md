
---
type: source_card
source_path: "docs/debug/D0009_H5_ATOMIC_NO_SAMPLE_REPLAY_AUDIT.md"
source_ext: ".md"
source_size: 2409
empty: false
generated_at: 2026-07-06
concepts: ["Atomic No-Sample", "Decision Node", "Execution / Risk", "Licensing", "UI / React", "Validation / Audit", "Zone / RTV"]
entities: ["D0009", "M0001"]
---

# Source Card — D0009_H5_ATOMIC_NO_SAMPLE_REPLAY_AUDIT.md

## Source

[[docs/debug/D0009_H5_ATOMIC_NO_SAMPLE_REPLAY_AUDIT|docs/debug/D0009_H5_ATOMIC_NO_SAMPLE_REPLAY_AUDIT.md]]

## Summary

D0009 is the strict H5 validator for the "do not build samples first" contract. It never calls `DAL_M0002CollectBranchSamples` and never creates `DALM0002BranchSample` arrays. The replay path is: Earlier H5 reports were useful structural/path research, but they could still inherit sample/order bias: branch samples were built first; samples were sorted by outcome/exit/entry order; multiple events known on the same candle could become a fake sequence; continuation R was normalized by a structural denominator even when no trading stop existed. D0009 removes that layer for validation. Regime state is derived directly from raw M0001 events that are already knowable by the current replay candle. For every replay step, D0009 loads only the bars available up to that closed candle. It computes M0001 nodes and raw M0001 events on that prefix only. For each closed/touch-confirmed raw event, D0009 c

## Concepts

[[docs/obsidian_deep/02_concepts/Atomic_No-Sample|Atomic No-Sample]], [[docs/obsidian_deep/02_concepts/Decision_Node|Decision Node]], [[docs/obsidian_deep/02_concepts/Execution____Risk|Execution / Risk]], [[docs/obsidian_deep/02_concepts/Licensing|Licensing]], [[docs/obsidian_deep/02_concepts/UI____React|UI / React]], [[docs/obsidian_deep/02_concepts/Validation____Audit|Validation / Audit]], [[docs/obsidian_deep/02_concepts/Zone____RTV|Zone / RTV]]

## Entities

D0009, M0001

## Headings

- D0009 H5 Atomic No-Sample Replay Audit
  - Why this exists
  - Regime construction
  - Entry model
  - Risk/R measurement
  - Key log lines

## Related Source Documents

- [[lab/05_validation/VAL_M0001_MQL_NATIVE/report|report.md]] — score `21`
- [[lab/03_experiments/EXP0003_mql_native_m0002/report|report.md]] — score `19`
- [[README|README.md]] — score `19`
- [[lab/09_execution/mql5/README|README.md]] — score `18`
- [[docs/debug/D0006_H5_LIVE_TOUCH_REPLAY_AUDIT|D0006_H5_LIVE_TOUCH_REPLAY_AUDIT.md]] — score `18`
- [[docs/architecture|architecture.md]] — score `17`
- [[docs/atomic_live_research_contract|atomic_live_research_contract.md]] — score `17`
- [[docs/mql_native/H0003_CONTINUATION_INERTIA_MEMORY_CLUSTERING|H0003_CONTINUATION_INERTIA_MEMORY_CLUSTERING.md]] — score `17`
- [[lab/03_experiments/EXP0002_mql_native_m0001/report|report.md]] — score `17`
- [[papers/001_atomic_live_regime_framework|001_atomic_live_regime_framework.md]] — score `17`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
