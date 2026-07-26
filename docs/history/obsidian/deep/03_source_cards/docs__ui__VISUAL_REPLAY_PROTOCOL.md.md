
---
type: source_card
source_path: "docs/ui/VISUAL_REPLAY_PROTOCOL.md"
source_ext: ".md"
source_size: 5693
empty: false
generated_at: 2026-07-06
concepts: ["AI Agent Layer", "Decision Node", "Execution / Risk", "UI / React", "Validation / Audit", "Zone / RTV"]
entities: ["M0001"]
---

# Source Card — VISUAL_REPLAY_PROTOCOL.md

## Source

[[docs/ui/VISUAL_REPLAY_PROTOCOL|docs/ui/VISUAL_REPLAY_PROTOCOL.md]]

## Summary

The Visual Replay Protocol defines how the UI replays market candles and overlays research artifacts on top of them. The goal is to make every test visually inspectable as if it were running live. The replay view is controlled by one object: A replay session contains: Valid replay states: The chart must advance by candle index, not wall-clock time. The current replay candle is the latest candle visible to the simulated system. No visual object may appear before its `visible_from_index`. L-rule nodes must become visible only after confirmation. Metric events must become visible only when their event lifecycle reaches the current replay index. Historical completed events may remain visible when the cursor moves forward. Moving the cursor backward must restore the visual state that would have been known at that point. The first UI implementation must include: Speed presets: Every overlay mu

## Concepts

[[docs/obsidian_deep/02_concepts/AI_Agent_Layer|AI Agent Layer]], [[docs/obsidian_deep/02_concepts/Decision_Node|Decision Node]], [[docs/obsidian_deep/02_concepts/Execution____Risk|Execution / Risk]], [[docs/obsidian_deep/02_concepts/UI____React|UI / React]], [[docs/obsidian_deep/02_concepts/Validation____Audit|Validation / Audit]], [[docs/obsidian_deep/02_concepts/Zone____RTV|Zone / RTV]]

## Entities

M0001

## Headings

- Visual Replay Protocol
  - Purpose
  - Central Concept
  - Replay Status
  - Timeline Rules
  - Core Replay Controls
  - Chart Layout
  - Visual Layers
  - Selection Model
  - Hover Model
  - Candle Replay Semantics
  - M0001 Replay Behavior

## Related Source Documents

- [[lab/05_validation/VAL_M0001_MQL_NATIVE/report|report.md]] — score `21`
- [[lab/03_experiments/EXP0003_mql_native_m0002/report|report.md]] — score `19`
- [[docs/ui/ROADMAP|ROADMAP.md]] — score `18`
- [[docs/ui/VISUALIZATION_API|VISUALIZATION_API.md]] — score `18`
- [[docs/architecture|architecture.md]] — score `17`
- [[docs/atomic_live_research_contract|atomic_live_research_contract.md]] — score `17`
- [[docs/debug/H6_REACTION_BOX_ZONES|H6_REACTION_BOX_ZONES.md]] — score `17`
- [[docs/execution/H0005_R1_SIX_SLOT_TOUCH_LEDGER|H0005_R1_SIX_SLOT_TOUCH_LEDGER.md]] — score `17`
- [[docs/MQL_LIVE_ALL_IN_ONE_APPLY|MQL_LIVE_ALL_IN_ONE_APPLY.md]] — score `17`
- [[docs/mql_live_visual_lab_debug_packages|mql_live_visual_lab_debug_packages.md]] — score `17`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
