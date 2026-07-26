
---
type: source_card
source_path: "docs/debug/E0006/REVISIT_SECONDARY_NODE_ANCHORS_README.md"
source_ext: ".md"
source_size: 3926
empty: false
generated_at: 2026-07-06
concepts: ["Decision Node", "Execution / Risk", "UI / React", "Zone / RTV"]
entities: ["E0006"]
---

# Source Card — REVISIT_SECONDARY_NODE_ANCHORS_README.md

## Source

[[docs/debug/E0006/REVISIT_SECONDARY_NODE_ANCHORS_README|docs/debug/E0006/REVISIT_SECONDARY_NODE_ANCHORS_README.md]]

## Summary

This document defines the third stop-anchor mode and the second revisit-entry mode added after the original E0006 execution design. In the first E0006 revisit model, the origin node stays the main execution anchor: The new model treats the first touch as a structural event that can create a smaller same-side node. On the next revisit, execution can be transferred from the large origin node to this smaller node. For a BUY example: For SELL, the logic is symmetric with HIGH nodes. Available revisit entry anchors: Available stop anchors: The secondary-node modes require `InpOnlyTradeRevisitZones = true` because there is no first-touch secondary node before the first touch exists. This is the original revisit behavior. For BUY: For SELL: The first non-hunted touch is only a qualification event. The later order still belongs to the origin zone. This is the new behavior. E0006 finds the same-s

## Concepts

[[docs/obsidian_deep/02_concepts/Decision_Node|Decision Node]], [[docs/obsidian_deep/02_concepts/Execution____Risk|Execution / Risk]], [[docs/obsidian_deep/02_concepts/UI____React|UI / React]], [[docs/obsidian_deep/02_concepts/Zone____RTV|Zone / RTV]]

## Entities

E0006

## Headings

- E0006 — Revisit Secondary-Node Entry and Stop Anchors
  - Why this mode exists
  - Inputs
  - Revisit entry mode 1 — origin zone
  - Revisit entry mode 2 — secondary-node zone
  - Stop mode 1 — origin zone back
  - Stop mode 2 — origin node
  - Stop mode 3 — revisit secondary node
  - Recommended secondary-node revisit experiment

## Related Source Documents

- [[docs/debug/E0006/ENTRY_QUALIFICATION_README|ENTRY_QUALIFICATION_README.md]] — score `14`
- [[docs/debug/E0006/EXIT_AND_RISK_README|EXIT_AND_RISK_README.md]] — score `14`
- [[docs/debug/E0006/INPUT_REFERENCE_README|INPUT_REFERENCE_README.md]] — score `14`
- [[docs/debug/E0006/MODULE_KERNEL_README|MODULE_KERNEL_README.md]] — score `14`
- [[docs/debug/E0006/README|README.md]] — score `14`
- [[docs/debug/E0006/REVISIT_ONLY_README|REVISIT_ONLY_README.md]] — score `14`
- [[docs/debug/E0006_ALL_ZONE_TOUCH_LIMIT_README|E0006_ALL_ZONE_TOUCH_LIMIT_README.md]] — score `13`
- [[lab/03_validation/VAL0023_e6_all_zone_touch_limit/README|README.md]] — score `13`
- [[docs/ai_execution/AI_ALGORITHM_LAYER_MAP_FOR_EXTREME_ENGINE_FA|AI_ALGORITHM_LAYER_MAP_FOR_EXTREME_ENGINE_FA.md]] — score `8`
- [[docs/ai_execution/AI_NATIVE_EXECUTION_ROADMAP_FA|AI_NATIVE_EXECUTION_ROADMAP_FA.md]] — score `8`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
