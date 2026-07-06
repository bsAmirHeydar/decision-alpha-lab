
---
type: source_card
source_path: "docs/flag_counting/FLAG_COUNTING_IMPLEMENTATION_CHECKLIST_V4.md"
source_ext: ".md"
source_size: 5397
empty: false
generated_at: 2026-07-06
concepts: ["AI Agent Layer", "Convexity / Optionality", "Decision Node", "Execution / Risk", "Flag Counting", "Hook", "UI / React", "Validation / Audit"]
entities: []
---

# Source Card — FLAG_COUNTING_IMPLEMENTATION_CHECKLIST_V4.md

## Source

[[docs/flag_counting/FLAG_COUNTING_IMPLEMENTATION_CHECKLIST_V4|docs/flag_counting/FLAG_COUNTING_IMPLEMENTATION_CHECKLIST_V4.md]]

## Summary

<!-- CURRENT CANON NOTICE This file is retained as historical/context documentation. For current Phoenix implementation decisions, use: docs/flag_counting/FLAG_COUNTING_CURRENT_CANON.md If this file conflicts with the current canon, the current canon wins. --> Use this checklist before modifying code. [ ] Reuse the existing project node engine. [ ] Do not redefine L inside FlagCounting. [ ] L means minimum left/right candles that do not reach the candidate high/low price. [ ] Equal highs/lows are merged as one plateau node according to existing logic. [ ] Equality does not count as break. [ ] Nodes do not expire after confirmation. Each node must expose: [ ] time [ ] price [ ] type: high/low [ ] L [ ] stable node id [ ] plateau/merged identity if applicable Each flag event must expose: [ ] sequence id [ ] parent sequence id [ ] direction [ ] F level [ ] status [ ] origin node [ ] leg1 no

## Concepts

[[docs/obsidian_deep/02_concepts/AI_Agent_Layer|AI Agent Layer]], [[docs/obsidian_deep/02_concepts/Convexity____Optionality|Convexity / Optionality]], [[docs/obsidian_deep/02_concepts/Decision_Node|Decision Node]], [[docs/obsidian_deep/02_concepts/Execution____Risk|Execution / Risk]], [[docs/obsidian_deep/02_concepts/Flag_Counting|Flag Counting]], [[docs/obsidian_deep/02_concepts/Hook|Hook]], [[docs/obsidian_deep/02_concepts/UI____React|UI / React]], [[docs/obsidian_deep/02_concepts/Validation____Audit|Validation / Audit]]

## Entities

—

## Headings

- Flag Counting Implementation Checklist V4
  - 1. Node Engine
  - 2. Data Model
  - 3. F1 Checklist
  - 4. F2 Checklist
  - 5. F3 Checklist
  - 6. Hook/ND Checklist
  - 7. Boundary Checklist
  - 8. Display Checklist
  - 9. Anti-Regression Tests

## Related Source Documents

- [[docs/flag_counting/FLAG_COUNTING_CURRENT_CANON|FLAG_COUNTING_CURRENT_CANON.md]] — score `25`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE4_HOOK_VIEW_PROJECTION|FLAG_COUNTING_LEVEL_19_PHASE4_HOOK_VIEW_PROJECTION.md]] — score `17`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE6_STATE_CONTRACT_STORAGE|FLAG_COUNTING_LEVEL_19_PHASE6_STATE_CONTRACT_STORAGE.md]] — score `17`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_STATE_GATE_IMPLEMENTATION_PLAN|FLAG_COUNTING_LEVEL_19_STATE_GATE_IMPLEMENTATION_PLAN.md]] — score `17`
- [[docs/flag_counting/FLAG_COUNTING_SEQUENCE_CONTRACT_V2|FLAG_COUNTING_SEQUENCE_CONTRACT_V2.md]] — score `17`
- [[docs/flag_counting/FLAG_COUNTING_SEQUENCE_CONTRACT_V3|FLAG_COUNTING_SEQUENCE_CONTRACT_V3.md]] — score `17`
- [[docs/flag_counting/FLAG_COUNTING_SEQUENCE_CONTRACT_V4|FLAG_COUNTING_SEQUENCE_CONTRACT_V4.md]] — score `17`
- [[docs/flag_counting/IMPLEMENTATION_LADDER_V1_INDEX|IMPLEMENTATION_LADDER_V1_INDEX.md]] — score `17`
- [[docs/flag_counting/README|README.md]] — score `17`
- [[docs/ai_execution/AI_ALGORITHM_LAYER_MAP_FOR_EXTREME_ENGINE_FA|AI_ALGORITHM_LAYER_MAP_FOR_EXTREME_ENGINE_FA.md]] — score `16`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
