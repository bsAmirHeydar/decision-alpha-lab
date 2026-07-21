
---
type: source_card
source_path: "docs/debug/H6_NODE_SURVIVAL_MAP.md"
source_ext: ".md"
source_size: 1445
empty: false
generated_at: 2026-07-06
concepts: ["Atomic No-Sample", "Decision Node", "Execution / Risk", "Known-Time Causality", "Validation / Audit"]
entities: ["H0006", "M0001", "M0002"]
---

# Source Card — H6_NODE_SURVIVAL_MAP.md

## Source

[[docs/debug/H6_NODE_SURVIVAL_MAP|docs/debug/H6_NODE_SURVIVAL_MAP.md]]

## Summary

This release redefines H0006 as a chart-facing no-sample node survival map. A raw M0001 node becomes an edge-candidate level if, after its known-time candle, the market does not break that node price within the configured survival horizons. Default horizons: 20 candles: red 50 candles: green 100 candles: purple Contract: raw M0001 nodes only no M0002 branch samples no branch sample ordering no internal ordering among nodes known on the same candle node survival is measured only after known-time chart objects are deleted and redrawn using the `DAL_H6_NODE_` prefix Break definition: high node breaks when a later candle high reaches `node_price + break_buffer` low node breaks when a later candle low reaches `node_price - break_buffer` Touch definition is reported separately: high node touched when high reaches `node_price - touch_buffer` low node touched when low reaches `node_price + touch

## Concepts

[[docs/obsidian_deep/02_concepts/Atomic_No-Sample|Atomic No-Sample]], [[docs/obsidian_deep/02_concepts/Decision_Node|Decision Node]], [[docs/obsidian_deep/02_concepts/Execution____Risk|Execution / Risk]], [[docs/obsidian_deep/02_concepts/Known-Time_Causality|Known-Time Causality]], [[docs/obsidian_deep/02_concepts/Validation____Audit|Validation / Audit]]

## Entities

H0006, M0001, M0002

## Headings

- H6 Node Survival Map

## Related Source Documents

- [[lab/03_experiments/EXP0003_mql_native_m0002/report|report.md]] — score `24`
- [[docs/debug/H6_CANDLE_STREAM_FAST|H6_CANDLE_STREAM_FAST.md]] — score `22`
- [[docs/architecture|architecture.md]] — score `20`
- [[docs/evidence/h0004_branch_regime_memory/45fad849057f_H0004_branch_regime_memory_atomic|H0004_branch_regime_memory_atomic.md]] — score `20`
- [[README|README.md]] — score `20`
- [[docs/debug/H6_FAST_ACCURATE_OPTIONALITY|H6_FAST_ACCURATE_OPTIONALITY.md]] — score `19`
- [[docs/evidence/h0006_node_survival_edge_map/067470759816_H0006_reversal_explosive_optionality|H0006_reversal_explosive_optionality.md]] — score `19`
- [[docs/debug/D0010_H4_ATOMIC_NO_SAMPLE_REGIME_AUDIT|D0010_H4_ATOMIC_NO_SAMPLE_REGIME_AUDIT.md]] — score `19`
- [[docs/debug/H4_ATOMIC_FULL_STRESS_CONTEXT|H4_ATOMIC_FULL_STRESS_CONTEXT.md]] — score `19`
- [[docs/debug/H4_FAST_ATOMIC_MAIN_REPORT|H4_FAST_ATOMIC_MAIN_REPORT.md]] — score `19`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
