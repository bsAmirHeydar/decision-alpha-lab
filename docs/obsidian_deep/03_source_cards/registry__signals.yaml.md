
---
type: source_card
source_path: "registry/signals.yaml"
source_ext: ".yaml"
source_size: 619
empty: false
generated_at: 2026-07-06
concepts: ["Execution / Risk", "UI / React", "Validation / Audit", "Zone / RTV"]
entities: []
---

# Source Card — signals.yaml

## Source

[registry/signals.yaml](../../registry/signals.yaml)

## Summary

signals: id: SIG_REVERSAL_REACTION family: reversal description: Reaction from a live-visible structural zone after a known reversal regime. required_entry_contract: zone_touch_or_close_confirmed_touch required_risk_contract: zone_edge_or_structural_invalidation status: research_candidate id: SIG_CONTINUATION_PATH family: continuation description: Path after structural break under known continuation regime. required_entry_contract: close_break_intrabar_break_or_donchian_break required_risk_contract: atr_structural_fixed_or_trailing_stop status: research_candidate

## Concepts

[[docs/obsidian_deep/02_concepts/Execution____Risk|Execution / Risk]], [[docs/obsidian_deep/02_concepts/UI____React|UI / React]], [[docs/obsidian_deep/02_concepts/Validation____Audit|Validation / Audit]], [[docs/obsidian_deep/02_concepts/Zone____RTV|Zone / RTV]]

## Entities

—

## Headings

- —

## Related Source Documents

- [[docs/ai_execution/AI_ALGORITHM_LAYER_MAP_FOR_EXTREME_ENGINE_FA|AI_ALGORITHM_LAYER_MAP_FOR_EXTREME_ENGINE_FA.md]] — score `8`
- [[docs/ai_execution/AI_NATIVE_EXECUTION_ROADMAP_FA|AI_NATIVE_EXECUTION_ROADMAP_FA.md]] — score `8`
- [[docs/ai_execution/AMIR_STRUCTURAL_EXPERIENCE_MAP_FA|AMIR_STRUCTURAL_EXPERIENCE_MAP_FA.md]] — score `8`
- [[docs/ai_execution/EXTREME_L2_NODE_CYCLE_LIMIT_ENTRY_FA|EXTREME_L2_NODE_CYCLE_LIMIT_ENTRY_FA.md]] — score `8`
- [[docs/architecture|architecture.md]] — score `8`
- [[docs/articles/reversal_vs_continuation_execution|reversal_vs_continuation_execution.md]] — score `8`
- [[docs/atomic_live_research_contract|atomic_live_research_contract.md]] — score `8`
- [[docs/debug/D0006_H5_LIVE_TOUCH_REPLAY_AUDIT|D0006_H5_LIVE_TOUCH_REPLAY_AUDIT.md]] — score `8`
- [[docs/debug/D0009_H5_ATOMIC_NO_SAMPLE_REPLAY_AUDIT|D0009_H5_ATOMIC_NO_SAMPLE_REPLAY_AUDIT.md]] — score `8`
- [[docs/debug/E0006/README|README.md]] — score `8`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
