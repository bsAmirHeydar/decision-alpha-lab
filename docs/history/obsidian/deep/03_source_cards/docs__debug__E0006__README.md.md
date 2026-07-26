
---
type: source_card
source_path: "docs/debug/E0006/README.md"
source_ext: ".md"
source_size: 5241
empty: false
generated_at: 2026-07-06
concepts: ["Convexity / Optionality", "Decision Node", "Execution / Risk", "MQL Native", "UI / React", "Validation / Audit", "Zone / RTV"]
entities: ["E0006", "M0001"]
---

# Source Card — README.md

## Source

[[docs/debug/E0006/README|docs/debug/E0006/README.md]]

## Summary

E0006 is the execution-facing layer of Decision Alpha Lab. It does **not** try to discover an alpha by itself and it does **not** redefine the structural market logic. Its job is to translate already-defined structural z… The module is intentionally built as a thin executor around the existing modules: M0001 supplies the live territory/zone semantics, touch/revisit events, node hunt state, and node invalidation logic. the L-rule structural node engine supplies confirmed origin nodes and confirmed internal nodes. the execution helpers supply spread-aware price normalization, order placement, stale-order deletion, and risk sizing. E0006 therefore has one main contract: E0006 runs once per new candle. It is not designed as a tick-by-tick scanner. On each sync: The newest-origin-first scan is deliberate. When a cap is active, newer structures win over older structures. E0006 separates the st

## Concepts

[[docs/obsidian_deep/02_concepts/Convexity____Optionality|Convexity / Optionality]], [[docs/obsidian_deep/02_concepts/Decision_Node|Decision Node]], [[docs/obsidian_deep/02_concepts/Execution____Risk|Execution / Risk]], [[docs/obsidian_deep/02_concepts/MQL_Native|MQL Native]], [[docs/obsidian_deep/02_concepts/UI____React|UI / React]], [[docs/obsidian_deep/02_concepts/Validation____Audit|Validation / Audit]], [[docs/obsidian_deep/02_concepts/Zone____RTV|Zone / RTV]]

## Entities

E0006, M0001

## Headings

- E0006 — Structural Execution Layer Overview
  - High-level cycle
  - Two structural scales
  - Origin zone
  - Internal game
  - Managed order identity
  - Main execution modes
  - Current recommended baseline
  - Compile target
  - Modular execution kernel

## Related Source Documents

- [[lab/03_validation/VAL0023_e6_all_zone_touch_limit/README|README.md]] — score `32`
- [[docs/debug/E0006/MODULE_KERNEL_README|MODULE_KERNEL_README.md]] — score `31`
- [[docs/execution/README|README.md]] — score `25`
- [[docs/ui/README|README.md]] — score `25`
- [[lab/03_validation/VAL0022_h6_reaction_box_zones/README|README.md]] — score `25`
- [[lab/04_execution/EXE0002_close_confirmed_market/README|README.md]] — score `25`
- [[README|README.md]] — score `25`
- [[docs/debug/E0006_ALL_ZONE_TOUCH_LIMIT_README|E0006_ALL_ZONE_TOUCH_LIMIT_README.md]] — score `24`
- [[docs/debug/E0008/README|README.md]] — score `23`
- [[lab/04_execution/EXE0001_reversal_one_to_one/README|README.md]] — score `23`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
