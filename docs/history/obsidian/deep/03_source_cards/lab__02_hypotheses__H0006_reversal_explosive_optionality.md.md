
---
type: source_card
source_path: "docs/evidence/h0006_node_survival_edge_map/067470759816_H0006_reversal_explosive_optionality.md"
source_ext: ".md"
source_size: 715
empty: false
generated_at: 2026-07-06
concepts: ["Convexity / Optionality", "Decision Node", "Execution / Risk"]
entities: ["H0006", "M0001", "M0002"]
---

# Source Card — H0006_reversal_explosive_optionality.md

## Source

[[docs/evidence/h0006_node_survival_edge_map/067470759816_H0006_reversal_explosive_optionality|docs/evidence/h0006_node_survival_edge_map/067470759816_H0006_reversal_explosive_optionality.md]]

## Summary

The current H0006 framing is not a win-rate hypothesis. It asks whether raw structural nodes that remain unbroken after a fixed number of candles become more edge-like decision levels. The operational definition is: raw M0001 node is known at candle `k` from candle `k+1` forward, monitor whether price breaks the node price if it is not broken after 20 candles, mark it red if it is not broken after 50 candles, mark it green if it is not broken after 100 candles, mark it purple This converts H6 from a generic optionality report into a chart-updating node survival map. No M0002 samples are allowed. Nodes known on the same candle are simultaneous, not ordered.

## Concepts

[[docs/obsidian_deep/02_concepts/Convexity____Optionality|Convexity / Optionality]], [[docs/obsidian_deep/02_concepts/Decision_Node|Decision Node]], [[docs/obsidian_deep/02_concepts/Execution____Risk|Execution / Risk]]

## Entities

H0006, M0001, M0002

## Headings

- H0006 — Node Survival Edge Map

## Related Source Documents

- [[lab/03_experiments/EXP0003_mql_native_m0002/report|report.md]] — score `22`
- [[docs/debug/H6_NODE_SURVIVAL_MAP|H6_NODE_SURVIVAL_MAP.md]] — score `19`
- [[docs/debug/H6_CANDLE_STREAM_FAST|H6_CANDLE_STREAM_FAST.md]] — score `17`
- [[docs/evidence/h0004_branch_regime_memory/45fad849057f_H0004_branch_regime_memory_atomic|H0004_branch_regime_memory_atomic.md]] — score `17`
- [[docs/mql_native/H0007_FLAG_COUNTING_F1_START_STRUCTURE|H0007_FLAG_COUNTING_F1_START_STRUCTURE.md]] — score `16`
- [[docs/debug/H6_REACTION_BOX_ZONES|H6_REACTION_BOX_ZONES.md]] — score `16`
- [[docs/execution/E0002_CLOSE_CONFIRMED_MARKET|E0002_CLOSE_CONFIRMED_MARKET.md]] — score `16`
- [[docs/execution/E0003_CONTINUATION_CLOSE_HUNT|E0003_CONTINUATION_CLOSE_HUNT.md]] — score `16`
- [[docs/execution/E0004_CONTINUATION_HEIKIN_ASHI_FLIP|E0004_CONTINUATION_HEIKIN_ASHI_FLIP.md]] — score `16`
- [[docs/execution/E0005_CONTINUATION_CLOSE_BREAK_FIXED_R|E0005_CONTINUATION_CLOSE_BREAK_FIXED_R.md]] — score `16`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
