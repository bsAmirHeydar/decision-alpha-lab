
---
type: source_card
source_path: "docs/debug/E0006/EXIT_AND_RISK_README.md"
source_ext: ".md"
source_size: 5995
empty: false
generated_at: 2026-07-06
concepts: ["Decision Node", "Execution / Risk", "UI / React", "Zone / RTV"]
entities: ["E0006", "M0001"]
---

# Source Card — EXIT_AND_RISK_README.md

## Source

[[docs/debug/E0006/EXIT_AND_RISK_README|docs/debug/E0006/EXIT_AND_RISK_README.md]]

## Summary

This document explains how E0006 places entries, anchors stops, handles spread, sizes risk, and manages take profit after a trade opens. E0006 uses limit orders on structural zones. For LOW origin zones: The BUY entry is shifted upward because a buy fills on Ask. This adjustment is intentionally preserved even when stop mode changes. For HIGH origin zones: The SELL entry remains at the lower edge of the high/supply zone. Inputs: E0006 now has two revisit entry anchors and three stop anchors. Origin-zone revisit entry: This keeps the order on the original M0001 zone when the node revisits. Secondary-node revisit entry: This is only meaningful when `InpOnlyTradeRevisitZones = true`. After the first non-hunted touch, E0006 finds the same-side internal node created inside that first touch cycle and uses that node's zone as the new entry z… BUY / LOW origin: SELL / HIGH origin: BUY / LOW orig

## Concepts

[[docs/obsidian_deep/02_concepts/Decision_Node|Decision Node]], [[docs/obsidian_deep/02_concepts/Execution____Risk|Execution / Risk]], [[docs/obsidian_deep/02_concepts/UI____React|UI / React]], [[docs/obsidian_deep/02_concepts/Zone____RTV|Zone / RTV]]

## Entities

E0006, M0001

## Headings

- E0006 — Exit, Stop, Spread, and Risk Logic
  - Entry prices
  - Stop anchor modes
    - Revisit entry anchors
    - Stop anchor 1: origin zone back
    - Stop anchor 2: origin node
    - Stop anchor 3: revisit secondary node
  - Risk distance
  - Fixed-R TP
  - Internal opposite-node TP manager
    - BUY position exit
    - SELL position exit

## Related Source Documents

- [[docs/debug/E0006/ENTRY_QUALIFICATION_README|ENTRY_QUALIFICATION_README.md]] — score `19`
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
