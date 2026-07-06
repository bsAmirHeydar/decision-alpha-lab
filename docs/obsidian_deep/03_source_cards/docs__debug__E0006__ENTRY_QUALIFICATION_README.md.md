
---
type: source_card
source_path: "docs/debug/E0006/ENTRY_QUALIFICATION_README.md"
source_ext: ".md"
source_size: 3944
empty: false
generated_at: 2026-07-06
concepts: ["Decision Node", "Execution / Risk", "UI / React", "Zone / RTV"]
entities: ["E0006", "M0001"]
---

# Source Card — ENTRY_QUALIFICATION_README.md

## Source

[[docs/debug/E0006/ENTRY_QUALIFICATION_README|docs/debug/E0006/ENTRY_QUALIFICATION_README.md]]

## Summary

This document describes how E0006 decides whether a structural zone is allowed to receive a limit order. The entry decision is not simply “every zone gets an order.” The current executor can require the path after the origin node to prove that enough same-side internal nodes were hunted before the origin zone becomes tradea… E0006 uses two L values. The origin node is the anchor of the trade. The internal nodes are the evidence that price has created and hunted enough same-side liquidity before the order is allowed. Inputs: With this setup, a zone is not eligible until at least three same-side internal nodes have been hunted after the origin node. For a LOW origin, E0006 is considering a BUY LIMIT. The same-side internal nodes are internal LOW nodes. A LOW origin zone becomes eligible only when: Example with threshold 3: The order is still placed at the configured zone edge, not at the i

## Concepts

[[docs/obsidian_deep/02_concepts/Decision_Node|Decision Node]], [[docs/obsidian_deep/02_concepts/Execution____Risk|Execution / Risk]], [[docs/obsidian_deep/02_concepts/UI____React|UI / React]], [[docs/obsidian_deep/02_concepts/Zone____RTV|Zone / RTV]]

## Entities

E0006, M0001

## Headings

- E0006 — Entry Qualification Logic
  - Origin versus internal nodes
  - Standard same-side hunt filter
  - LOW origin / BUY logic
  - HIGH origin / SELL logic
  - Hunt definition
  - Decision window
  - Same-side toggle
  - Interaction with pending caps
  - Fast test settings

## Related Source Documents

- [[docs/debug/E0006/EXIT_AND_RISK_README|EXIT_AND_RISK_README.md]] — score `19`
- [[docs/debug/E0006/INPUT_REFERENCE_README|INPUT_REFERENCE_README.md]] — score `19`
- [[docs/debug/E0006/MODULE_KERNEL_README|MODULE_KERNEL_README.md]] — score `19`
- [[docs/debug/E0006/README|README.md]] — score `19`
- [[docs/debug/E0006/REVISIT_ONLY_README|REVISIT_ONLY_README.md]] — score `19`
- [[docs/debug/E0006_ALL_ZONE_TOUCH_LIMIT_README|E0006_ALL_ZONE_TOUCH_LIMIT_README.md]] — score `18`
- [[lab/03_validation/VAL0023_e6_all_zone_touch_limit/README|README.md]] — score `18`
- [[docs/debug/E0006/REVISIT_SECONDARY_NODE_ANCHORS_README|REVISIT_SECONDARY_NODE_ANCHORS_README.md]] — score `14`
- [[docs/architecture|architecture.md]] — score `13`
- [[docs/atomic_live_research_contract|atomic_live_research_contract.md]] — score `13`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
