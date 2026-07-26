
---
type: source_card
source_path: "lab/03_validation/VAL0025_e8_mtf_purple_extreme/README.md"
source_ext: ".md"
source_size: 1682
empty: false
generated_at: 2026-07-06
concepts: ["Decision Node", "Execution / Risk", "UI / React", "Validation / Audit", "Zone / RTV"]
entities: ["E0008", "VAL0025"]
---

# Source Card — README.md

## Source

[[lab/03_validation/VAL0025_e8_mtf_purple_extreme/README|lab/03_validation/VAL0025_e8_mtf_purple_extreme/README.md]]

## Summary

Find whether multi-timeframe context can filter purple/source zones into tiny-stop high-R candidates. A good candidate should show: Do not judge this by number of trades. The desired outcome is a small number of very asymmetric plans. Recommended first run: The EA should now rebuild: H1/H4/M15 context only when those timeframes print a new candle. Execution map only once per M1 candle. Nothing structural on every tick.

## Concepts

[[docs/obsidian_deep/02_concepts/Decision_Node|Decision Node]], [[docs/obsidian_deep/02_concepts/Execution____Risk|Execution / Risk]], [[docs/obsidian_deep/02_concepts/UI____React|UI / React]], [[docs/obsidian_deep/02_concepts/Validation____Audit|Validation / Audit]], [[docs/obsidian_deep/02_concepts/Zone____RTV|Zone / RTV]]

## Entities

E0008, VAL0025

## Headings

- VAL0025 — E0008 MTF Purple Extreme Validation
  - Goal
  - Main settings
  - Test matrix
    - A. No-future mode
    - B. Oracle purple mode
    - C. Micro tiny-stop mode
  - What to inspect in the log
  - Important
  - Release 101 performance settings

## Related Source Documents

- [[docs/debug/E0008/README|README.md]] — score `13`
- [[docs/ai_execution/AI_ALGORITHM_LAYER_MAP_FOR_EXTREME_ENGINE_FA|AI_ALGORITHM_LAYER_MAP_FOR_EXTREME_ENGINE_FA.md]] — score `10`
- [[docs/ai_execution/AI_NATIVE_EXECUTION_ROADMAP_FA|AI_NATIVE_EXECUTION_ROADMAP_FA.md]] — score `10`
- [[docs/ai_execution/AMIR_STRUCTURAL_EXPERIENCE_MAP_FA|AMIR_STRUCTURAL_EXPERIENCE_MAP_FA.md]] — score `10`
- [[docs/ai_execution/EXTREME_L2_NODE_CYCLE_LIMIT_ENTRY_FA|EXTREME_L2_NODE_CYCLE_LIMIT_ENTRY_FA.md]] — score `10`
- [[docs/architecture|architecture.md]] — score `10`
- [[docs/atomic_live_research_contract|atomic_live_research_contract.md]] — score `10`
- [[docs/debug/D0006_H5_LIVE_TOUCH_REPLAY_AUDIT|D0006_H5_LIVE_TOUCH_REPLAY_AUDIT.md]] — score `10`
- [[docs/debug/D0009_H5_ATOMIC_NO_SAMPLE_REPLAY_AUDIT|D0009_H5_ATOMIC_NO_SAMPLE_REPLAY_AUDIT.md]] — score `10`
- [[docs/debug/E0006/README|README.md]] — score `10`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
