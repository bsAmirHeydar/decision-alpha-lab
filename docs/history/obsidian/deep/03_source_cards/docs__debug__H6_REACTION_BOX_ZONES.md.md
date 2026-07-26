
---
type: source_card
source_path: "docs/debug/H6_REACTION_BOX_ZONES.md"
source_ext: ".md"
source_size: 14450
empty: false
generated_at: 2026-07-06
concepts: ["AI Agent Layer", "Convexity / Optionality", "Decision Node", "Execution / Risk", "Known-Time Causality", "UI / React", "Validation / Audit", "Zone / RTV"]
entities: ["M0001", "M0002", "M0006"]
---

# Source Card — H6_REACTION_BOX_ZONES.md

## Source

[[docs/debug/H6_REACTION_BOX_ZONES|docs/debug/H6_REACTION_BOX_ZONES.md]]

## Summary

Release 112 changes the official H6 chart visual from simple horizontal survivor lines to reaction-zone rectangles. Contract: Raw M0001 nodes only. No M0002 branch samples. Same-known-time events are never internally ordered. A reaction box starts from the known node time and ends at the first future touch. The vertical box spans from the node price to the touch extreme. For a high node, the touch extreme is the touch candle high; the expected reaction is downward. For a low node, the touch extreme is the touch candle low; the expected reaction is upward. After touch, reversal confirmation must happen on a later candle. This avoids hidden OHLC sequence assumptions inside the touch candle. Once reaction is confirmed, the box color is upgraded if price does not retouch the far edge of the zone for 20 / 50 / 100 candles. Default colors: H20 = red H50 = green H100 = purple Key report lines:

## Concepts

[[docs/obsidian_deep/02_concepts/AI_Agent_Layer|AI Agent Layer]], [[docs/obsidian_deep/02_concepts/Convexity____Optionality|Convexity / Optionality]], [[docs/obsidian_deep/02_concepts/Decision_Node|Decision Node]], [[docs/obsidian_deep/02_concepts/Execution____Risk|Execution / Risk]], [[docs/obsidian_deep/02_concepts/Known-Time_Causality|Known-Time Causality]], [[docs/obsidian_deep/02_concepts/UI____React|UI / React]], [[docs/obsidian_deep/02_concepts/Validation____Audit|Validation / Audit]], [[docs/obsidian_deep/02_concepts/Zone____RTV|Zone / RTV]]

## Entities

M0001, M0002, M0006

## Headings

- H6 Reaction Box Zones
  - Release 141 — node-capped projection

## Related Source Documents

- [[README|README.md]] — score `32`
- [[docs/execution/README|README.md]] — score `30`
- [[lab/04_execution/EXE0001_reversal_one_to_one/README|README.md]] — score `30`
- [[lab/03_validation/VAL0022_h6_reaction_box_zones/README|README.md]] — score `29`
- [[lab/04_execution/EXE0002_close_confirmed_market/README|README.md]] — score `28`
- [[docs/debug/E0008/README|README.md]] — score `27`
- [[lab/04_execution/EXE0003_continuation_close_hunt/README|README.md]] — score `26`
- [[lab/04_execution/EXE0004_continuation_heikin_ashi_flip/README|README.md]] — score `26`
- [[lab/05_validation/VAL0010_h4_atomic_no_sample_regime/README|README.md]] — score `26`
- [[lab/05_validation/VAL0011_main_atomic_no_sample_unification/README|README.md]] — score `26`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
