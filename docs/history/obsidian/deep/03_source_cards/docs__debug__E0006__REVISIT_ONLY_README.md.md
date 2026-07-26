
---
type: source_card
source_path: "docs/debug/E0006/REVISIT_ONLY_README.md"
source_ext: ".md"
source_size: 3889
empty: false
generated_at: 2026-07-06
concepts: ["Decision Node", "Execution / Risk", "UI / React", "Zone / RTV"]
entities: ["E0006", "M0001"]
---

# Source Card — REVISIT_ONLY_README.md

## Source

[[docs/debug/E0006/REVISIT_ONLY_README|docs/debug/E0006/REVISIT_ONLY_README.md]]

## Summary

The revisit-only mode is designed for experiments where the first touch of a zone is not traded. The zone must first survive a non-hunted touch cycle, then become tradeable only on a later revisit, and only if both the f… When `InpOnlyTradeRevisitZones=false`, E0006 behaves like the standard entry-qualification mode. When `InpOnlyTradeRevisitZones=true`, first-touch entries are skipped and the origin must prove a prior non-hunted touch event. `InpRevisitMinInternalHunts=0` means reuse the standard threshold: A revisit-only trade requires this lifecycle: For a LOW origin: The logic is: For a HIGH origin: The logic is: The first cycle is the proof that the zone was approached with the same structural pressure standard before the first touch. If the first cycle did not hunt enough same-side internal nodes, then the later revisit is not considered a valid continuation of the same structural

## Concepts

[[docs/obsidian_deep/02_concepts/Decision_Node|Decision Node]], [[docs/obsidian_deep/02_concepts/Execution____Risk|Execution / Risk]], [[docs/obsidian_deep/02_concepts/UI____React|UI / React]], [[docs/obsidian_deep/02_concepts/Zone____RTV|Zone / RTV]]

## Entities

E0006, M0001

## Headings

- E0006 — Revisit-Only Entry Logic
  - Inputs
  - Required sequence
  - LOW origin / BUY revisit
  - HIGH origin / SELL revisit
  - Why the first cycle must qualify
  - What counts as a prior touch
  - Important implication
  - Recommended test setup

## Related Source Documents

- [[docs/debug/E0006/ENTRY_QUALIFICATION_README|ENTRY_QUALIFICATION_README.md]] — score `19`
- [[docs/debug/E0006/EXIT_AND_RISK_README|EXIT_AND_RISK_README.md]] — score `19`
- [[docs/debug/E0006/INPUT_REFERENCE_README|INPUT_REFERENCE_README.md]] — score `19`
- [[docs/debug/E0006/MODULE_KERNEL_README|MODULE_KERNEL_README.md]] — score `19`
- [[docs/debug/E0006/README|README.md]] — score `19`
- [[docs/debug/E0006_ALL_ZONE_TOUCH_LIMIT_README|E0006_ALL_ZONE_TOUCH_LIMIT_README.md]] — score `18`
- [[lab/03_validation/VAL0023_e6_all_zone_touch_limit/README|README.md]] — score `18`
- [[docs/debug/E0006/REVISIT_SECONDARY_NODE_ANCHORS_README|REVISIT_SECONDARY_NODE_ANCHORS_README.md]] — score `14`
- [[docs/architecture|architecture.md]] — score `13`
- [[docs/atomic_live_research_contract|atomic_live_research_contract.md]] — score `13`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
