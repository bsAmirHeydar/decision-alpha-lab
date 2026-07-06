
---
type: source_card
source_path: "docs/debug/E0008/README.md"
source_ext: ".md"
source_size: 5482
empty: false
generated_at: 2026-07-06
concepts: ["AI Agent Layer", "Convexity / Optionality", "Decision Node", "Execution / Risk", "Flag Counting", "Hook", "Known-Time Causality", "UI / React", "Zone / RTV"]
entities: ["E0007", "E0008", "M0001"]
---

# Source Card — README.md

## Source

[[docs/debug/E0008/README|docs/debug/E0008/README.md]]

## Summary

E0008 is the execution template that matches the user objective more directly than E0007: > We do not want every purple zone. > We want purple/source zones that sit inside the correct higher-timeframe context and give a tiny local stop with 50R/100R path potential. Default stack: The default `L=2` is intentional because the purple screenshots were generated with L=2. Each context timeframe builds M0001 node/zone events and searches for a source-like event: This is not yet a full human-grade hook engine, but it is the first testable proxy: No future survival label is required. Oracle/research mode: only zones that already survived 500 bars are used. This is for reverse engineering and must not be treated as live-valid. Uses the latest same-side execution-timeframe node after the local source. For BUY: For SELL: Uses the local context source zone directly. Finds a same-side node inside the

## Concepts

[[docs/obsidian_deep/02_concepts/AI_Agent_Layer|AI Agent Layer]], [[docs/obsidian_deep/02_concepts/Convexity____Optionality|Convexity / Optionality]], [[docs/obsidian_deep/02_concepts/Decision_Node|Decision Node]], [[docs/obsidian_deep/02_concepts/Execution____Risk|Execution / Risk]], [[docs/obsidian_deep/02_concepts/Flag_Counting|Flag Counting]], [[docs/obsidian_deep/02_concepts/Hook|Hook]], [[docs/obsidian_deep/02_concepts/Known-Time_Causality|Known-Time Causality]], [[docs/obsidian_deep/02_concepts/UI____React|UI / React]], [[docs/obsidian_deep/02_concepts/Zone____RTV|Zone / RTV]]

## Entities

E0007, E0008, M0001

## Headings

- E0008 — MTF Purple Extreme Executor
  - Architecture
  - What counts as context
  - Live mode vs oracle purple research
  - Entry modes
    - MICRO_NODE_REVISIT
    - LOCAL_SOURCE_REVISIT
    - LOCAL_SECONDARY_NODE
    - EARLY_LADDER_STEP
  - Stop modes
  - Target modes
  - Suggested tests

## Related Source Documents

- [[docs/architecture|architecture.md]] — score `25`
- [[docs/mql_native/H0007_FLAG_COUNTING_F1_START_STRUCTURE|H0007_FLAG_COUNTING_F1_START_STRUCTURE.md]] — score `23`
- [[docs/debug/H6_REACTION_BOX_ZONES|H6_REACTION_BOX_ZONES.md]] — score `19`
- [[lab/03_validation/VAL0022_h6_reaction_box_zones/README|README.md]] — score `19`
- [[lab/05_validation/VAL_M0001_MQL_NATIVE/report|report.md]] — score `19`
- [[docs/debug/E0007/README|README.md]] — score `17`
- [[docs/atomic_live_research_contract|atomic_live_research_contract.md]] — score `17`
- [[docs/execution/E0002_CLOSE_CONFIRMED_MARKET|E0002_CLOSE_CONFIRMED_MARKET.md]] — score `17`
- [[docs/execution/H0005_R1_SIX_SLOT_TOUCH_LEDGER|H0005_R1_SIX_SLOT_TOUCH_LEDGER.md]] — score `17`
- [[docs/execution/README|README.md]] — score `17`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
