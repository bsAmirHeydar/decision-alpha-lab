
---
type: source_card
source_path: "docs/debug/E0006/INPUT_REFERENCE_README.md"
source_ext: ".md"
source_size: 4794
empty: false
generated_at: 2026-07-06
concepts: ["Decision Node", "Execution / Risk", "UI / React", "Zone / RTV"]
entities: ["E0006", "M0001"]
---

# Source Card — INPUT_REFERENCE_README.md

## Source

[[docs/debug/E0006/INPUT_REFERENCE_README|docs/debug/E0006/INPUT_REFERENCE_README.md]]

## Summary

This file groups the current E0006 inputs by purpose. `InpSymbol=""` means current chart symbol. `InpTimeframe=PERIOD_CURRENT` means current chart timeframe. `InpOriginNodeL` controls the main nodes whose zones can receive limit orders. `InpInternalNodeL` controls the smaller nodes used for internal hunt qualification and internal opposite-node exits. `InpZoneRatio` is passed to the M0001 live territory logic. When enabled, LOW origins require hunted internal LOW nodes and HIGH origins require hunted internal HIGH nodes. When enabled, E0006 skips first-touch entries and only trades zones with a prior non-hunted M0001 touch cycle. Both first cycle and current revisit cycle can be required to pass the internal hunt threshold. `InpRevisitMinInternalHunts=0` reuses `InpMinInternalHuntsForZone`. The magic number and managed comment prefix protect the EA from modifying unrelated orders. `InpRe

## Concepts

[[docs/obsidian_deep/02_concepts/Decision_Node|Decision Node]], [[docs/obsidian_deep/02_concepts/Execution____Risk|Execution / Risk]], [[docs/obsidian_deep/02_concepts/UI____React|UI / React]], [[docs/obsidian_deep/02_concepts/Zone____RTV|Zone / RTV]]

## Entities

E0006, M0001

## Headings

- E0006 — Input Reference
  - Symbol and bar source
  - Structural scales
  - Entry qualification
  - Revisit-only mode
  - Order sizing and identity
  - Reward and exit
  - Stop and spread handling
  - Pending and position caps
  - Sync and session
  - Useful presets
  - Revisit entry and stop anchors

## Related Source Documents

- [[docs/debug/E0006/ENTRY_QUALIFICATION_README|ENTRY_QUALIFICATION_README.md]] — score `19`
- [[docs/debug/E0006/EXIT_AND_RISK_README|EXIT_AND_RISK_README.md]] — score `19`
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
