
---
type: source_card
source_path: "docs/evidence/m0001_relative_territory_volatility_rtv/9fec506c7ac3_M0001_relative_territory_volatility.md"
source_ext: ".md"
source_size: 9075
empty: false
generated_at: 2026-07-06
concepts: ["Decision Node", "Execution / Risk", "UI / React", "Validation / Audit", "Zone / RTV"]
entities: ["M0001"]
---

# Source Card — M0001_relative_territory_volatility.md

## Source

[[docs/evidence/m0001_relative_territory_volatility_rtv/9fec506c7ac3_M0001_relative_territory_volatility|docs/evidence/m0001_relative_territory_volatility_rtv/9fec506c7ac3_M0001_relative_territory_volatility.md]]

## Summary

Final Specification Frozen Design Document M0001 (Relative Territory Volatility) is a structural metric designed to quantify how price behaves when revisiting the territory of a structural node. The core question is: > Does price exhibit a different volatility regime when it returns to the vicinity of an important structural node? Instead of relying on classical volatility measures such as ATR or standard deviation, M0001 evaluates volatility through logarithmic candle movements within the context of structural node territories. OHLC data: time open high low close Nodes are supplied by: LRuleNodeDetector Only nodes satisfying: are considered. The entire metric is designed to behave exactly like a live market. At no point is future information allowed. Every decision must be made using only information available up to the current candle. Therefore: > Backtests and live execution follow id

## Concepts

[[docs/obsidian_deep/02_concepts/Decision_Node|Decision Node]], [[docs/obsidian_deep/02_concepts/Execution____Risk|Execution / Risk]], [[docs/obsidian_deep/02_concepts/UI____React|UI / React]], [[docs/obsidian_deep/02_concepts/Validation____Audit|Validation / Audit]], [[docs/obsidian_deep/02_concepts/Zone____RTV|Zone / RTV]]

## Entities

M0001

## Headings

- M0001 — Relative Territory Volatility (RTV)
  - Version
  - Status
- 1. Purpose
- 2. Inputs
  - 2.1 Market Data
  - 2.2 Structural Nodes
- 3. Design Philosophy
- 4. Live Market Simulation
- 5. Node States
  - TRACKING
  - ACTIVE EVENT

## Related Source Documents

- [[docs/architecture|architecture.md]] — score `15`
- [[docs/atomic_live_research_contract|atomic_live_research_contract.md]] — score `15`
- [[docs/debug/D0006_H5_LIVE_TOUCH_REPLAY_AUDIT|D0006_H5_LIVE_TOUCH_REPLAY_AUDIT.md]] — score `15`
- [[docs/debug/D0009_H5_ATOMIC_NO_SAMPLE_REPLAY_AUDIT|D0009_H5_ATOMIC_NO_SAMPLE_REPLAY_AUDIT.md]] — score `15`
- [[docs/debug/E0006/README|README.md]] — score `15`
- [[docs/debug/E0006_ALL_ZONE_TOUCH_LIMIT_README|E0006_ALL_ZONE_TOUCH_LIMIT_README.md]] — score `15`
- [[docs/debug/H6_BOX_ALGORITHM_README|H6_BOX_ALGORITHM_README.md]] — score `15`
- [[docs/debug/H6_REACTION_BOX_ZONES|H6_REACTION_BOX_ZONES.md]] — score `15`
- [[docs/execution/H0005_R1_SIX_SLOT_TOUCH_LEDGER|H0005_R1_SIX_SLOT_TOUCH_LEDGER.md]] — score `15`
- [[docs/M0001_MQL_INPUT_PARAMETER_BRIDGE|M0001_MQL_INPUT_PARAMETER_BRIDGE.md]] — score `15`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
