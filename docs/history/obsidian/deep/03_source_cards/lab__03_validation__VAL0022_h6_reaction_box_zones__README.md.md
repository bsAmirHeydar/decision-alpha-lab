
---
type: source_card
source_path: "lab/03_validation/VAL0022_h6_reaction_box_zones/README.md"
source_ext: ".md"
source_size: 13920
empty: false
generated_at: 2026-07-06
concepts: ["AI Agent Layer", "Convexity / Optionality", "Decision Node", "Execution / Risk", "Known-Time Causality", "UI / React", "Validation / Audit", "Zone / RTV"]
entities: ["M0001", "VAL0022"]
---

# Source Card — README.md

## Source

[[lab/03_validation/VAL0022_h6_reaction_box_zones/README|lab/03_validation/VAL0022_h6_reaction_box_zones/README.md]]

## Summary

Goal: validate the H6 chart object logic where a node touch that confirms reversal creates a rectangle from node origin to touch location. Validation checklist: `sampleCalls=0`, `branchSamplesBuilt=0`, `m0002Calls=0` remain unchanged. `DAL_H0006_REACTION_BOX_AUDIT` is printed. Boxes are drawn when `InpH6DrawReactionBoxes=true`. Horizontal lines are not drawn when `InpH6DrawNodeLines=false`. Red, green, and purple counts correspond to 20, 50, and 100 candles of post-confirmation survival without zone-end retouch. Increasing `InpH6ReactionAwayBufferPoints` reduces confirmed reaction count. Increasing `InpH6ReactionZoneEndBufferPoints` makes the invalidation stricter and may reduce survival. Recommended fast test: `InpH6UseAllAvailableBars=false` `InpH6FastDefaultClosedBars=50000` `InpH6DrawReactionBoxes=true` `InpH6DrawNodeLines=false` `InpH6ReactionMaxChartObjects=150` Release 113 visual

## Concepts

[[docs/obsidian_deep/02_concepts/AI_Agent_Layer|AI Agent Layer]], [[docs/obsidian_deep/02_concepts/Convexity____Optionality|Convexity / Optionality]], [[docs/obsidian_deep/02_concepts/Decision_Node|Decision Node]], [[docs/obsidian_deep/02_concepts/Execution____Risk|Execution / Risk]], [[docs/obsidian_deep/02_concepts/Known-Time_Causality|Known-Time Causality]], [[docs/obsidian_deep/02_concepts/UI____React|UI / React]], [[docs/obsidian_deep/02_concepts/Validation____Audit|Validation / Audit]], [[docs/obsidian_deep/02_concepts/Zone____RTV|Zone / RTV]]

## Entities

M0001, VAL0022

## Headings

- VAL0022 — H6 Reaction Box Zones
  - Release 141 zone projection test

## Related Source Documents

- [[docs/debug/E0008/README|README.md]] — score `27`
- [[README|README.md]] — score `27`
- [[docs/debug/E0006/README|README.md]] — score `25`
- [[docs/execution/README|README.md]] — score `25`
- [[lab/03_validation/VAL0023_e6_all_zone_touch_limit/README|README.md]] — score `25`
- [[lab/04_execution/EXE0001_reversal_one_to_one/README|README.md]] — score `25`
- [[docs/debug/H6_BOX_ALGORITHM_README|H6_BOX_ALGORITHM_README.md]] — score `23`
- [[docs/ui/README|README.md]] — score `23`
- [[lab/04_execution/EXE0002_close_confirmed_market/README|README.md]] — score `23`
- [[docs/flag_counting/README|README.md]] — score `22`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
