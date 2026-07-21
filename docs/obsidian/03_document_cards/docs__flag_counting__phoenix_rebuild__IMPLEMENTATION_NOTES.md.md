---
title: "Phoenix Implementation Notes"
type: document_card
generated_by: alpha_lab_obsidian_builder
generated_at: 2026-07-06
source_path: "docs/flag_counting/phoenix_rebuild/IMPLEMENTATION_NOTES.md"
source_ext: ".md"
category: "flag_counting_docs"
source_size_bytes: "11956"
concepts:
  - "AI Agent Layer"
  - "F-Counting"
  - "Hook"
  - "Licensing"
  - "NDS Anatomy"
  - "Structural Nodes"
  - "Validation"
---


# Phoenix Implementation Notes

**Source:** [[docs/flag_counting/phoenix_rebuild/IMPLEMENTATION_NOTES|docs/flag_counting/phoenix_rebuild/IMPLEMENTATION_NOTES.md]]

**Category:** `flag_counting_docs`  
**Status:** ok  
**Size:** `11956` bytes

## خلاصه

`FP_NodeEngine` owns node extraction. No sequence code should inspect raw candle open/close/body. `FP_HookEngine` owns hook/ND branches and F1 phase-boundary origins. `FP_FlagBodyEngine` owns the invariant two-leg body. `FP_InternalCountEngine` owns post-flag 1/2/3/4 counting. `FP_SequenceEngine` owns F1 -> F2 -> F3 state transitions and parent-child ownership. `FP_Renderer` owns only drawing. `FP_Audit` owns diagnostic logs. Phoenix defaults to: This is deliberate. It keeps the chart inspectable while Hook/ND coverage is being verified. Once Hook/ND boundary coverage is strong, fail-open can be disabled. The current HookEngine builds readable 3/4-node alternating branches at each L. It is e

## Headings

- Phoenix Implementation Notes
-   Module boundaries
-   Deliberate fail-open setting
-   Known engineering tradeoffs
-   Semantic cleanup notes
-   Hook / ND branch-sequence code repair
-   Readable stacked labels patch
-   Renderer Patch: Candle-Index Arc Sampling
-   Phoenix Hook/ND Display Repair — Cycle Boundary Without Downstream Origin Mutation
-   2026-06-28 - Root repair: bounded Hook contexts and flag visibility recovery
-     1. Hook / ND is now rebuilt from bounded contexts
-     2. Hook visual start and F1 semantic start are separated

## Concepts

- [[docs/obsidian/04_concepts/AI_Agent_Layer|AI Agent Layer]]
- [[docs/obsidian/04_concepts/F-Counting|F-Counting]]
- [[docs/obsidian/04_concepts/Hook|Hook]]
- [[docs/obsidian/04_concepts/Licensing|Licensing]]
- [[docs/evidence/nds_anatomy/6a11c75733b2_NDS_Anatomy|NDS Anatomy]]
- [[docs/obsidian/04_concepts/Structural_Nodes|Structural Nodes]]
- [[docs/obsidian/04_concepts/Validation|Validation]]

## Related documents

- [[docs/flag_counting/phoenix_rebuild/hook_nd_branching/HOOK_ND_BRANCH_SEQUENCE_CONTRACT_V1|Hook / ND Branch-Sequence Contract V1]] — `flag_counting_docs`
- [[docs/flag_counting/phoenix_rebuild/hook_nd_branching/HOOK_ND_BRANCH_ALGORITHM_V1|Hook / ND Branch Algorithm V1]] — `flag_counting_docs`
- [[docs/ai_execution/AI_ALGORITHM_LAYER_MAP_FOR_EXTREME_ENGINE_FA|AI Algorithm Layer Map for Extreme Engine — نقشه الگوریتم‌های هوش مصنوعی برای اکستریم L2]] — `ai_execution_docs`
- [[docs/debug/MARKET_LANGUAGE/README|DAL Market Language — Nodes, Cycles, Hooks, Rallies, Flags, 123 Flags, and Open 1/2s]] — `debug_docs`
- [[docs/flag_counting/FLAG_COUNTING_CURRENT_CANON|Flag Counting Current Canon]] — `flag_counting_docs`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_CLEAN_ISOLATED_STATE_GATE|Flag Counting Level 19 — Clean Isolated State Gate]] — `flag_counting_docs`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19D_TRANSITION_EVENT_LEDGER|Flag Counting Level 19D — Closed-Bar Transition Event Ledger]] — `flag_counting_docs`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19Z_COMPLETE_OBSERVATION_SUITE|Flag Counting Level 19Z — Complete Observation Suite]] — `flag_counting_docs`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_20_ENTRY_BRIDGE_XY_ANCHOR_JOIN|Flag Counting Level 20 — Entry Bridge / X-Y Anchor Join]] — `flag_counting_docs`
- [[docs/flag_counting/README|Flag Counting Documentation]] — `flag_counting_docs`
- [[docs/flag_counting/phoenix_rebuild/PHOENIX_MAIN_CHART_CONTRACT_REPAIR_V3|Phoenix Main-Chart Contract Repair V3]] — `flag_counting_docs`
- [[docs/flag_counting/phoenix_rebuild/PHOENIX_ROOT_CONTRACT_REPAIR_V2|Phoenix Root Contract Repair V2]] — `flag_counting_docs`

## Recommended Obsidian use

- این card را به نوت‌های concept، hypothesis، experiment یا ADR مربوط link کن.
- اگر این سند source of truth است، در MOC مربوطه بالاتر از اسناد legacy قرارش بده.
- اگر این سند report/validation است، نتیجه نهایی آن را به registry مربوط sync کن.
