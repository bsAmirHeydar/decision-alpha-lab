
---
type: source_card
source_path: "docs/flag_counting/FLAG_COUNTING_LEVEL_24_SAFETY_GATE_PRE_BROKER.md"
source_ext: ".md"
source_size: 4360
empty: false
generated_at: 2026-07-06
concepts: ["Decision Node", "Execution / Risk", "Flag Counting", "Hook", "Licensing", "MQL Native", "Python Brain", "UI / React", "Validation / Audit", "Zone / RTV"]
entities: []
---

# Source Card — FLAG_COUNTING_LEVEL_24_SAFETY_GATE_PRE_BROKER.md

## Source

[[docs/flag_counting/FLAG_COUNTING_LEVEL_24_SAFETY_GATE_PRE_BROKER|docs/flag_counting/FLAG_COUNTING_LEVEL_24_SAFETY_GATE_PRE_BROKER.md]]

## Summary

Level 24 adds a pre-broker safety gate after the Level 23 close-only paper performance layer. This is still not execution. It does not send orders. It does not create broker requests. It does not calculate volume or account risk. The goal is to decide whether the system is allowed to move to a future dry-run broker layer. Level 24 does not modify: It remains: The safety gate evaluates: By default, real execution is disabled: Manual arm is also disabled: However, manual arm is not required by default at this layer: This keeps Level 24 usable as a diagnostic safety report without blocking all research runs. Performance gating is available but disabled by default: When enabled, Level 24 requires: The performance values come from Level 23 runtime counters. If: spread filtering is disabled. If it is positive, the current symbol spread must be less than or equal to the configured maximum. Allo

## Concepts

[[docs/obsidian_deep/02_concepts/Decision_Node|Decision Node]], [[docs/obsidian_deep/02_concepts/Execution____Risk|Execution / Risk]], [[docs/obsidian_deep/02_concepts/Flag_Counting|Flag Counting]], [[docs/obsidian_deep/02_concepts/Hook|Hook]], [[docs/obsidian_deep/02_concepts/Licensing|Licensing]], [[docs/obsidian_deep/02_concepts/MQL_Native|MQL Native]], [[docs/obsidian_deep/02_concepts/Python_Brain|Python Brain]], [[docs/obsidian_deep/02_concepts/UI____React|UI / React]], [[docs/obsidian_deep/02_concepts/Validation____Audit|Validation / Audit]], [[docs/obsidian_deep/02_concepts/Zone____RTV|Zone / RTV]]

## Entities

—

## Headings

- Flag Counting Level 24 — Safety Gate / Pre-Broker Guard
  - Purpose
  - Hard boundary
  - New output
  - New inputs
  - Checks
  - Default behavior
  - Performance gate
  - Spread gate
  - Allow lists
  - Gate statuses
  - Block reasons

## Related Source Documents

- [[docs/flag_counting/FLAG_COUNTING_CURRENT_CANON|FLAG_COUNTING_CURRENT_CANON.md]] — score `21`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_CLEAN_ISOLATED_STATE_GATE|FLAG_COUNTING_LEVEL_19_CLEAN_ISOLATED_STATE_GATE.md]] — score `21`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19Z_COMPLETE_OBSERVATION_SUITE|FLAG_COUNTING_LEVEL_19Z_COMPLETE_OBSERVATION_SUITE.md]] — score `21`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_20_ENTRY_BRIDGE_XY_ANCHOR_JOIN|FLAG_COUNTING_LEVEL_20_ENTRY_BRIDGE_XY_ANCHOR_JOIN.md]] — score `21`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_21_PAPER_INTENT_NO_ORDER|FLAG_COUNTING_LEVEL_21_PAPER_INTENT_NO_ORDER.md]] — score `21`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_22_PAPER_LIFECYCLE_CLOSE_ONLY|FLAG_COUNTING_LEVEL_22_PAPER_LIFECYCLE_CLOSE_ONLY.md]] — score `21`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_23_PAPER_PERFORMANCE_CLOSE_ONLY|FLAG_COUNTING_LEVEL_23_PAPER_PERFORMANCE_CLOSE_ONLY.md]] — score `21`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_25_BROKER_DRY_RUN_ONLY|FLAG_COUNTING_LEVEL_25_BROKER_DRY_RUN_ONLY.md]] — score `21`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_26_BROKER_VALIDATOR_NO_SEND|FLAG_COUNTING_LEVEL_26_BROKER_VALIDATOR_NO_SEND.md]] — score `21`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_27_BROKER_REQUEST_LEDGER_NO_SEND|FLAG_COUNTING_LEVEL_27_BROKER_REQUEST_LEDGER_NO_SEND.md]] — score `21`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
