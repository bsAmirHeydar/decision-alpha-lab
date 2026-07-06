
---
type: source_card
source_path: "docs/flag_counting/FLAG_COUNTING_LEVEL_23_PAPER_PERFORMANCE_CLOSE_ONLY.md"
source_ext: ".md"
source_size: 3196
empty: false
generated_at: 2026-07-06
concepts: ["Decision Node", "Execution / Risk", "Flag Counting", "Hook", "Licensing", "MQL Native", "Python Brain", "UI / React", "Validation / Audit", "Zone / RTV"]
entities: []
---

# Source Card — FLAG_COUNTING_LEVEL_23_PAPER_PERFORMANCE_CLOSE_ONLY.md

## Source

[[docs/flag_counting/FLAG_COUNTING_LEVEL_23_PAPER_PERFORMANCE_CLOSE_ONLY|docs/flag_counting/FLAG_COUNTING_LEVEL_23_PAPER_PERFORMANCE_CLOSE_ONLY.md]]

## Summary

Level 23 summarizes the close-only paper lifecycle produced by Level 22. Level 22 reconstructs a single paper lifecycle from the current paper intent. Level 23 converts that lifecycle into performance-style research metrics. This is still not execution. It does not send orders. It does not create broker requests. It does not calculate volume or account risk. Level 23 does not modify: It remains: The summary row includes: The EA can recalculate the same lifecycle many times on the same bar. Level 23 builds a sample key from: If the same sample repeats, it increments duplicate count and does not double-count performance. Level 23 uses the close-only realized R-like value from Level 22. The result is research-only. It is not account PnL. It is not broker PnL. It is not a real trade result. Level 20 answers: Level 21 answers: Level 22 answers: Level 23 answers: The next layer should be: Leve

## Concepts

[[docs/obsidian_deep/02_concepts/Decision_Node|Decision Node]], [[docs/obsidian_deep/02_concepts/Execution____Risk|Execution / Risk]], [[docs/obsidian_deep/02_concepts/Flag_Counting|Flag Counting]], [[docs/obsidian_deep/02_concepts/Hook|Hook]], [[docs/obsidian_deep/02_concepts/Licensing|Licensing]], [[docs/obsidian_deep/02_concepts/MQL_Native|MQL Native]], [[docs/obsidian_deep/02_concepts/Python_Brain|Python Brain]], [[docs/obsidian_deep/02_concepts/UI____React|UI / React]], [[docs/obsidian_deep/02_concepts/Validation____Audit|Validation / Audit]], [[docs/obsidian_deep/02_concepts/Zone____RTV|Zone / RTV]]

## Entities

—

## Headings

- Flag Counting Level 23 — Paper Performance Close-Only
  - Purpose
  - Hard boundary
  - New output
  - New inputs
  - What it measures
  - Outcome classes
  - Duplicate handling
  - R-like metrics
  - Relationship to earlier levels
  - Next correct layer

## Related Source Documents

- [[docs/flag_counting/FLAG_COUNTING_CURRENT_CANON|FLAG_COUNTING_CURRENT_CANON.md]] — score `21`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_CLEAN_ISOLATED_STATE_GATE|FLAG_COUNTING_LEVEL_19_CLEAN_ISOLATED_STATE_GATE.md]] — score `21`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19Z_COMPLETE_OBSERVATION_SUITE|FLAG_COUNTING_LEVEL_19Z_COMPLETE_OBSERVATION_SUITE.md]] — score `21`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_20_ENTRY_BRIDGE_XY_ANCHOR_JOIN|FLAG_COUNTING_LEVEL_20_ENTRY_BRIDGE_XY_ANCHOR_JOIN.md]] — score `21`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_21_PAPER_INTENT_NO_ORDER|FLAG_COUNTING_LEVEL_21_PAPER_INTENT_NO_ORDER.md]] — score `21`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_22_PAPER_LIFECYCLE_CLOSE_ONLY|FLAG_COUNTING_LEVEL_22_PAPER_LIFECYCLE_CLOSE_ONLY.md]] — score `21`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_24_SAFETY_GATE_PRE_BROKER|FLAG_COUNTING_LEVEL_24_SAFETY_GATE_PRE_BROKER.md]] — score `21`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_25_BROKER_DRY_RUN_ONLY|FLAG_COUNTING_LEVEL_25_BROKER_DRY_RUN_ONLY.md]] — score `21`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_26_BROKER_VALIDATOR_NO_SEND|FLAG_COUNTING_LEVEL_26_BROKER_VALIDATOR_NO_SEND.md]] — score `21`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_27_BROKER_REQUEST_LEDGER_NO_SEND|FLAG_COUNTING_LEVEL_27_BROKER_REQUEST_LEDGER_NO_SEND.md]] — score `21`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
