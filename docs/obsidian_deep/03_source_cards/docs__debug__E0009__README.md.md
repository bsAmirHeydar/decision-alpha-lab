
---
type: source_card
source_path: "docs/debug/E0009/README.md"
source_ext: ".md"
source_size: 2214
empty: false
generated_at: 2026-07-06
concepts: ["Decision Node", "Execution / Risk", "Hook", "UI / React", "Zone / RTV"]
entities: ["E0009"]
---

# Source Card — README.md

## Source

[[docs/debug/E0009/README|docs/debug/E0009/README.md]]

## Summary

Release 112 aligns E0009 with the intended reversal logic. Default: Index convention: Macro scans backwards from live and finds the nearest valid same-type chain. This is reversal logic: rising highs define a sell-reversal context; falling lows define a buy-reversal context. Default: Setup does **not** scan older chains. It only checks the latest N highs and latest N lows. If `InpRequireSetupAgreesWithMacro=true`, macro and setup must point to the same trade direction. Default: `InpMaxHookCandidatesPerBar = 0` means scan all eligible hooks. Entry is a limit touch on the hook extreme: `InpRejectHuntedM1Hook=true` means consumed/hunted hooks are not allowed back into the game. Default: The filter is available but disabled by default. Default: Exit does not depend on entry time or entry price. The EA continuously syncs TP for open positions when the structural exit condition exists.

## Concepts

[[docs/obsidian_deep/02_concepts/Decision_Node|Decision Node]], [[docs/obsidian_deep/02_concepts/Execution____Risk|Execution / Risk]], [[docs/obsidian_deep/02_concepts/Hook|Hook]], [[docs/obsidian_deep/02_concepts/UI____React|UI / React]], [[docs/obsidian_deep/02_concepts/Zone____RTV|Zone / RTV]]

## Entities

E0009

## Headings

- E0009 — Reversal Macro / Latest Setup / Hook Executor
  - Layer 1 — Macro mode
  - Layer 2 — Middle setup
  - Layer 3 — M1 hook entry
  - Layer 4 — Micro filter
  - Layer 5 — Exit

## Related Source Documents

- [[lab/03_validation/VAL0026_e9_htf_123_m1_hook_reversal/README|README.md]] — score `13`
- [[docs/ai_execution/AI_ALGORITHM_LAYER_MAP_FOR_EXTREME_ENGINE_FA|AI_ALGORITHM_LAYER_MAP_FOR_EXTREME_ENGINE_FA.md]] — score `10`
- [[docs/ai_execution/AI_NATIVE_EXECUTION_ROADMAP_FA|AI_NATIVE_EXECUTION_ROADMAP_FA.md]] — score `10`
- [[docs/ai_execution/AMIR_STRUCTURAL_EXPERIENCE_MAP_FA|AMIR_STRUCTURAL_EXPERIENCE_MAP_FA.md]] — score `10`
- [[docs/ai_execution/EXTREME_L2_NODE_CYCLE_LIMIT_ENTRY_FA|EXTREME_L2_NODE_CYCLE_LIMIT_ENTRY_FA.md]] — score `10`
- [[docs/debug/E0007/README|README.md]] — score `10`
- [[docs/debug/E0008/README|README.md]] — score `10`
- [[docs/debug/MARKET_LANGUAGE/README|README.md]] — score `10`
- [[docs/experience_capture/answers/BASE-02/answer_normalized_en|answer_normalized_en.md]] — score `10`
- [[docs/experience_capture/answers/BASE-04/answer_normalized_en|answer_normalized_en.md]] — score `10`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
