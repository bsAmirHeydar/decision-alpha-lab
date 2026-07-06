
---
type: source_card
source_path: "mql5/Include/FlagCountingPhoenix/README_FlagCountingPhoenix.md"
source_ext: ".md"
source_size: 31761
empty: false
generated_at: 2026-07-06
concepts: ["AI Agent Layer", "Convexity / Optionality", "Decision Node", "Execution / Risk", "Flag Counting", "Hook", "Licensing", "MQL Native", "Python Brain", "UI / React", "Validation / Audit", "Zone / RTV"]
entities: []
---

# Source Card — README_FlagCountingPhoenix.md

## Source

[[mql5/Include/FlagCountingPhoenix/README_FlagCountingPhoenix|mql5/Include/FlagCountingPhoenix/README_FlagCountingPhoenix.md]]

## Summary

Phoenix must be implemented and audited from: That file is the source of truth. This README is an implementation index only. Phoenix is a clean rebuild of the Flag Counting engine. It intentionally does not include, reuse, or depend on any earlier `FlagCounting`, `FlagCountingVNext`, or `FlagCountingV6` implementation. Node logic is copied conceptually from the original project rule: a node is a candle high/low level that has at least `L` candles on both sides that do not reach that price. Equality is not a break. Equal highs/lows form one plateau node. Open, close, candle body, and candle color are ignored by the structural logic. A flag body is always `Origin -> Leg1 -> Waist -> Leg2`. F1, F2, and F3 share the same two-leg body shape; they differ in post-flag semantics. F2 and F3 use backfilled origins from the deepest adverse correction after their parent flag. Hook/ND is rendered and

## Concepts

[[docs/obsidian_deep/02_concepts/AI_Agent_Layer|AI Agent Layer]], [[docs/obsidian_deep/02_concepts/Convexity____Optionality|Convexity / Optionality]], [[docs/obsidian_deep/02_concepts/Decision_Node|Decision Node]], [[docs/obsidian_deep/02_concepts/Execution____Risk|Execution / Risk]], [[docs/obsidian_deep/02_concepts/Flag_Counting|Flag Counting]], [[docs/obsidian_deep/02_concepts/Hook|Hook]], [[docs/obsidian_deep/02_concepts/Licensing|Licensing]], [[docs/obsidian_deep/02_concepts/MQL_Native|MQL Native]], [[docs/obsidian_deep/02_concepts/Python_Brain|Python Brain]], [[docs/obsidian_deep/02_concepts/UI____React|UI / React]], [[docs/obsidian_deep/02_concepts/Validation____Audit|Validation / Audit]], [[docs/obsidian_deep/02_concepts/Zone____RTV|Zone / RTV]]

## Entities

—

## Headings

- FlagCounting Phoenix
  - Current canon
  - Core principles
  - Files
  - Level 01 candle stream
  - Level 02 node engine
  - Level 03 identity layer
  - Level 04 Hook / ND context engine
  - Level 05 Flag Body engine
  - Level 11.5 Raw audit export
  - Expert
  - Recommended first run

## Related Source Documents

- [[docs/flag_counting/FLAG_COUNTING_CURRENT_CANON|FLAG_COUNTING_CURRENT_CANON.md]] — score `32`
- [[docs/flag_counting/README|README.md]] — score `32`
- [[docs/flag_counting/implementation_ladder_v1/README|README.md]] — score `28`
- [[docs/debug/MARKET_LANGUAGE/README|README.md]] — score `26`
- [[docs/debug/E0008/README|README.md]] — score `24`
- [[docs/experience_capture/questions/README|README.md]] — score `24`
- [[lab/03_experiments/EXP0016_astro_meta_learner/README|README.md]] — score `24`
- [[lab/03_experiments/EXP_flag_counting/README|README.md]] — score `24`
- [[README|README.md]] — score `24`
- [[docs/nds_hook_architecture/README|README.md]] — score `24`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
