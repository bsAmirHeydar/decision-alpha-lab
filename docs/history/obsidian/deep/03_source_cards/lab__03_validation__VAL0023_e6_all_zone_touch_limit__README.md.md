
---
type: source_card
source_path: "lab/03_validation/VAL0023_e6_all_zone_touch_limit/README.md"
source_ext: ".md"
source_size: 9394
empty: false
generated_at: 2026-07-06
concepts: ["Convexity / Optionality", "Decision Node", "Execution / Risk", "MQL Native", "UI / React", "Validation / Audit", "Zone / RTV"]
entities: ["E0006", "M0001"]
---

# Source Card — README.md

## Source

[[lab/03_validation/VAL0023_e6_all_zone_touch_limit/README|lab/03_validation/VAL0023_e6_all_zone_touch_limit/README.md]]

## Summary

E0006 is a lightweight execution module that uses existing M0001 / execution modules instead of rebuilding structure logic. Source of truth for zones: M0001 live territory logic. Scan all confirmed structural nodes by default. No maximum trade-count cap by default. One managed pending limit order per live, non-hunted M0001 zone. New-bar only execution. No tick-by-tick recalculation. Stop loss is the far end of the zone. Take profit is fixed-R, default `20R`. LOW node / support zone: HIGH node / resistance zone: The sell-side SL and TP spread shift follows the requested execution rule. `InpMaxNodesScan=0` means all confirmed nodes are scanned. This is not a trade limit. The EA upserts each managed pending order: A stale pending order is deleted only if its managed node no longer appears as a valid live zone. New inputs: `0` means unlimited. Any positive value caps how many BUY LIMIT or SE

## Concepts

[[docs/obsidian_deep/02_concepts/Convexity____Optionality|Convexity / Optionality]], [[docs/obsidian_deep/02_concepts/Decision_Node|Decision Node]], [[docs/obsidian_deep/02_concepts/Execution____Risk|Execution / Risk]], [[docs/obsidian_deep/02_concepts/MQL_Native|MQL Native]], [[docs/obsidian_deep/02_concepts/UI____React|UI / React]], [[docs/obsidian_deep/02_concepts/Validation____Audit|Validation / Audit]], [[docs/obsidian_deep/02_concepts/Zone____RTV|Zone / RTV]]

## Entities

E0006, M0001

## Headings

- E0006 — All-Zone Touch Limit Fixed-R Executor
  - Contract
  - Direction
  - Important inputs
  - Order lifecycle
  - Compile target
  - Release 101 — per-side pending-order caps
  - Release 102 — open-position side blocking
  - Documentation added in Release 108
  - Release 109 modular kernel
  - Release 110 revisit secondary-node anchors

## Related Source Documents

- [[docs/debug/E0006/README|README.md]] — score `32`
- [[docs/debug/E0006/MODULE_KERNEL_README|MODULE_KERNEL_README.md]] — score `30`
- [[docs/debug/E0006/ENTRY_QUALIFICATION_README|ENTRY_QUALIFICATION_README.md]] — score `26`
- [[docs/debug/E0006/EXIT_AND_RISK_README|EXIT_AND_RISK_README.md]] — score `26`
- [[docs/debug/E0006/INPUT_REFERENCE_README|INPUT_REFERENCE_README.md]] — score `26`
- [[docs/debug/E0006/REVISIT_ONLY_README|REVISIT_ONLY_README.md]] — score `26`
- [[docs/execution/README|README.md]] — score `25`
- [[docs/ui/README|README.md]] — score `25`
- [[lab/03_validation/VAL0022_h6_reaction_box_zones/README|README.md]] — score `25`
- [[lab/04_execution/EXE0002_close_confirmed_market/README|README.md]] — score `25`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
