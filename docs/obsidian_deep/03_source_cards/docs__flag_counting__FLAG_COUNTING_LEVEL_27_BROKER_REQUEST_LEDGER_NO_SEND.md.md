
---
type: source_card
source_path: "docs/flag_counting/FLAG_COUNTING_LEVEL_27_BROKER_REQUEST_LEDGER_NO_SEND.md"
source_ext: ".md"
source_size: 4011
empty: false
generated_at: 2026-07-06
concepts: ["Decision Node", "Execution / Risk", "Flag Counting", "Hook", "Licensing", "MQL Native", "Python Brain", "UI / React", "Validation / Audit", "Zone / RTV"]
entities: []
---

# Source Card — FLAG_COUNTING_LEVEL_27_BROKER_REQUEST_LEDGER_NO_SEND.md

## Source

[[docs/flag_counting/FLAG_COUNTING_LEVEL_27_BROKER_REQUEST_LEDGER_NO_SEND|docs/flag_counting/FLAG_COUNTING_LEVEL_27_BROKER_REQUEST_LEDGER_NO_SEND.md]]

## Summary

Level 27 adds an append-only ledger for the broker-like request preview and validator result. Level 25 builds the dry-run preview. Level 26 validates the preview without sending anything. Level 27 records the request and validation state into a historical ledger. This is still not execution. It does not call `OrderSend`. It does not call `OrderCheck`. It does not use `CTrade`. It does not create a broker request. It does not create a position. It does not calculate volume or account risk. Level 27 does not modify: It remains: The first file is append-only. The second file is the latest snapshot. Each row records: The EA can recalculate the same request preview repeatedly. Level 27 builds a dedupe key from: If the same key repeats and duplicate skipping is enabled, the ledger does not append the same request again. It marks: Every output row explicitly includes: and: Level 20 answers: Lev

## Concepts

[[docs/obsidian_deep/02_concepts/Decision_Node|Decision Node]], [[docs/obsidian_deep/02_concepts/Execution____Risk|Execution / Risk]], [[docs/obsidian_deep/02_concepts/Flag_Counting|Flag Counting]], [[docs/obsidian_deep/02_concepts/Hook|Hook]], [[docs/obsidian_deep/02_concepts/Licensing|Licensing]], [[docs/obsidian_deep/02_concepts/MQL_Native|MQL Native]], [[docs/obsidian_deep/02_concepts/Python_Brain|Python Brain]], [[docs/obsidian_deep/02_concepts/UI____React|UI / React]], [[docs/obsidian_deep/02_concepts/Validation____Audit|Validation / Audit]], [[docs/obsidian_deep/02_concepts/Zone____RTV|Zone / RTV]]

## Entities

—

## Headings

- Flag Counting Level 27 — Broker Request Ledger / No Send
  - Purpose
  - Hard boundary
  - New outputs
  - New inputs
  - Ledger row content
  - Duplicate handling
  - Ledger statuses
  - No-send contract
  - Relationship to previous layers
  - Next correct layer

## Related Source Documents

- [[docs/flag_counting/FLAG_COUNTING_CURRENT_CANON|FLAG_COUNTING_CURRENT_CANON.md]] — score `21`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_CLEAN_ISOLATED_STATE_GATE|FLAG_COUNTING_LEVEL_19_CLEAN_ISOLATED_STATE_GATE.md]] — score `21`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19Z_COMPLETE_OBSERVATION_SUITE|FLAG_COUNTING_LEVEL_19Z_COMPLETE_OBSERVATION_SUITE.md]] — score `21`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_20_ENTRY_BRIDGE_XY_ANCHOR_JOIN|FLAG_COUNTING_LEVEL_20_ENTRY_BRIDGE_XY_ANCHOR_JOIN.md]] — score `21`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_21_PAPER_INTENT_NO_ORDER|FLAG_COUNTING_LEVEL_21_PAPER_INTENT_NO_ORDER.md]] — score `21`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_22_PAPER_LIFECYCLE_CLOSE_ONLY|FLAG_COUNTING_LEVEL_22_PAPER_LIFECYCLE_CLOSE_ONLY.md]] — score `21`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_23_PAPER_PERFORMANCE_CLOSE_ONLY|FLAG_COUNTING_LEVEL_23_PAPER_PERFORMANCE_CLOSE_ONLY.md]] — score `21`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_24_SAFETY_GATE_PRE_BROKER|FLAG_COUNTING_LEVEL_24_SAFETY_GATE_PRE_BROKER.md]] — score `21`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_25_BROKER_DRY_RUN_ONLY|FLAG_COUNTING_LEVEL_25_BROKER_DRY_RUN_ONLY.md]] — score `21`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_26_BROKER_VALIDATOR_NO_SEND|FLAG_COUNTING_LEVEL_26_BROKER_VALIDATOR_NO_SEND.md]] — score `21`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
