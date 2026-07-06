
---
type: source_card
source_path: "docs/flag_counting/phoenix_rebuild/IMPLEMENTATION_NOTES.md"
source_ext: ".md"
source_size: 11956
empty: false
generated_at: 2026-07-06
concepts: ["AI Agent Layer", "Decision Node", "Flag Counting", "Hook", "Licensing", "UI / React", "Validation / Audit"]
entities: []
---

# Source Card — IMPLEMENTATION_NOTES.md

## Source

[[docs/flag_counting/phoenix_rebuild/IMPLEMENTATION_NOTES|docs/flag_counting/phoenix_rebuild/IMPLEMENTATION_NOTES.md]]

## Summary

`FP_NodeEngine` owns node extraction. No sequence code should inspect raw candle open/close/body. `FP_HookEngine` owns hook/ND branches and F1 phase-boundary origins. `FP_FlagBodyEngine` owns the invariant two-leg body. `FP_InternalCountEngine` owns post-flag 1/2/3/4 counting. `FP_SequenceEngine` owns F1 -> F2 -> F3 state transitions and parent-child ownership. `FP_Renderer` owns only drawing. `FP_Audit` owns diagnostic logs. Phoenix defaults to: This is deliberate. It keeps the chart inspectable while Hook/ND coverage is being verified. Once Hook/ND boundary coverage is strong, fail-open can be disabled. The current HookEngine builds readable 3/4-node alternating branches at each L. It is explicitly isolated so the branch algorithm can be upgraded without touching the sequence engine. The current InternalCountEngine keeps one strict adverse-side branch per event. It is also isolated so

## Concepts

[[docs/obsidian_deep/02_concepts/AI_Agent_Layer|AI Agent Layer]], [[docs/obsidian_deep/02_concepts/Decision_Node|Decision Node]], [[docs/obsidian_deep/02_concepts/Flag_Counting|Flag Counting]], [[docs/obsidian_deep/02_concepts/Hook|Hook]], [[docs/obsidian_deep/02_concepts/Licensing|Licensing]], [[docs/obsidian_deep/02_concepts/UI____React|UI / React]], [[docs/obsidian_deep/02_concepts/Validation____Audit|Validation / Audit]]

## Entities

—

## Headings

- Phoenix Implementation Notes
  - Module boundaries
  - Deliberate fail-open setting
  - Known engineering tradeoffs
  - Semantic cleanup notes
  - Hook / ND branch-sequence code repair
  - Readable stacked labels patch
  - Renderer Patch: Candle-Index Arc Sampling
  - Phoenix Hook/ND Display Repair — Cycle Boundary Without Downstream Origin Mutation
  - 2026-06-28 - Root repair: bounded Hook contexts and flag visibility recovery
    - 1. Hook / ND is now rebuilt from bounded contexts
    - 2. Hook visual start and F1 semantic start are separated

## Related Source Documents

- [[docs/flag_counting/phoenix_rebuild/hook_nd_branching/HOOK_ND_BRANCH_ALGORITHM_V1|HOOK_ND_BRANCH_ALGORITHM_V1.md]] — score `20`
- [[docs/flag_counting/phoenix_rebuild/hook_nd_branching/HOOK_ND_BRANCH_SEQUENCE_CONTRACT_V1|HOOK_ND_BRANCH_SEQUENCE_CONTRACT_V1.md]] — score `20`
- [[docs/ai_execution/AI_ALGORITHM_LAYER_MAP_FOR_EXTREME_ENGINE_FA|AI_ALGORITHM_LAYER_MAP_FOR_EXTREME_ENGINE_FA.md]] — score `14`
- [[docs/ai_execution/AMIR_STRUCTURAL_EXPERIENCE_MAP_FA|AMIR_STRUCTURAL_EXPERIENCE_MAP_FA.md]] — score `14`
- [[docs/debug/MARKET_LANGUAGE/README|README.md]] — score `14`
- [[docs/flag_counting/FLAG_COUNTING_CURRENT_CANON|FLAG_COUNTING_CURRENT_CANON.md]] — score `14`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_CLEAN_ISOLATED_STATE_GATE|FLAG_COUNTING_LEVEL_19_CLEAN_ISOLATED_STATE_GATE.md]] — score `14`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE13_MTF_ALIGNMENT_MAP|FLAG_COUNTING_LEVEL_19_PHASE13_MTF_ALIGNMENT_MAP.md]] — score `14`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE14_ENTRY_GEOMETRY_READINESS|FLAG_COUNTING_LEVEL_19_PHASE14_ENTRY_GEOMETRY_READINESS.md]] — score `14`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE22_PAPER_FILTER_DIAGNOSTICS|FLAG_COUNTING_LEVEL_19_PHASE22_PAPER_FILTER_DIAGNOSTICS.md]] — score `14`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
