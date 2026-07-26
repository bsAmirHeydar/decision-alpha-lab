
---
type: source_card
source_path: "docs/flag_counting/engineering_pack_v5/04_algorithms/README.md"
source_ext: ".md"
source_size: 770
empty: false
generated_at: 2026-07-06
concepts: ["Decision Node", "Execution / Risk", "Flag Counting", "Hook", "UI / React", "Validation / Audit"]
entities: []
---

# Source Card — README.md

## Source

[[docs/flag_counting/engineering_pack_v5/04_algorithms/README|docs/flag_counting/engineering_pack_v5/04_algorithms/README.md]]

## Summary

This package translates the contract into implementation modules. `MODULE_ARCHITECTURE.md` `NODE_ENGINE_ALGORITHM.md` `HOOK_BRANCH_ENGINE_ALGORITHM.md` `FLAG_BODY_ENGINE_ALGORITHM.md` `SEQUENCE_ENGINE_ALGORITHM.md` `F1_F2_F3_ALGORITHMS.md` `DEDUP_AUDIT_ALGORITHM.md` `PSEUDOCODE_REFERENCE.md` Do not patch one giant detector function. Implement modules in this order: Node adapter. Flag body builder. Post-flag context tracker. Hook branch engine. F1 state machine. F2 state machine with backfill. F3 state machine with extension/lock. Dedup/identity/audit. Renderer. If a module needs renderer information to decide logic, the architecture is wrong.

## Concepts

[[docs/obsidian_deep/02_concepts/Decision_Node|Decision Node]], [[docs/obsidian_deep/02_concepts/Execution____Risk|Execution / Risk]], [[docs/obsidian_deep/02_concepts/Flag_Counting|Flag Counting]], [[docs/obsidian_deep/02_concepts/Hook|Hook]], [[docs/obsidian_deep/02_concepts/UI____React|UI / React]], [[docs/obsidian_deep/02_concepts/Validation____Audit|Validation / Audit]]

## Entities

—

## Headings

- 04 Algorithms README
  - Files
  - Implementation Strategy
  - Rule

## Related Source Documents

- [[docs/flag_counting/engineering_pack_v5/04_algorithms/MODULE_ARCHITECTURE|MODULE_ARCHITECTURE.md]] — score `21`
- [[docs/flag_counting/engineering_pack_v5/04_algorithms/NODE_ENGINE_ALGORITHM|NODE_ENGINE_ALGORITHM.md]] — score `21`
- [[docs/debug/MARKET_LANGUAGE/README|README.md]] — score `20`
- [[docs/flag_counting/engineering_pack_v5/README|README.md]] — score `20`
- [[docs/flag_counting/implementation_ladder_v1/README|README.md]] — score `20`
- [[docs/flag_counting/phoenix_rebuild/README|README.md]] — score `20`
- [[docs/flag_counting/README|README.md]] — score `20`
- [[docs/nds_hook_architecture/README|README.md]] — score `20`
- [[lab/03_experiments/EXP_flag_counting/README|README.md]] — score `20`
- [[lab/03_experiments/EXP_flag_counting/validation_cases/README|README.md]] — score `20`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
