
---
type: source_card
source_path: "docs/experience_capture/answers/EXT-06/answer_normalized_en.md"
source_ext: ".md"
source_size: 4334
empty: false
generated_at: 2026-07-06
concepts: ["Decision Node", "Execution / Risk", "Rally", "UI / React", "Validation / Audit", "Zone / RTV"]
entities: []
---

# Source Card — answer_normalized_en.md

## Source

[[docs/experience_capture/answers/EXT-06/answer_normalized_en|docs/experience_capture/answers/EXT-06/answer_normalized_en.md]]

## Summary

Node penetration is a hard invalidation event. If price passes even one point beyond the cycle-origin node, the validity of that node as an Extreme anchor is finished. This means there is no tolerance for penetration of the cycle-origin node. Suggested hard rule: Formal state: This is not a soft signal. It is a structural invalidation. For this specific rule, a small penetration is not treated as a valid stop-hunt that preserves the original node. The answer implies: Therefore, the system should not reinterpret a penetrated cycle-origin node as still valid just because price returned quickly. The answer does not allow a buffer for the cycle-origin node. There may be execution buffers for broker stop placement or spread handling, but the structural node validity itself is binary. Suggested distinction: So the structural record should mark the node invalid as soon as the node is crossed. T

## Concepts

[[docs/obsidian_deep/02_concepts/Decision_Node|Decision Node]], [[docs/obsidian_deep/02_concepts/Execution____Risk|Execution / Risk]], [[docs/obsidian_deep/02_concepts/Rally|Rally]], [[docs/obsidian_deep/02_concepts/UI____React|UI / React]], [[docs/obsidian_deep/02_concepts/Validation____Audit|Validation / Audit]], [[docs/obsidian_deep/02_concepts/Zone____RTV|Zone / RTV]]

## Entities

—

## Headings

- EXT-06 — Normalized Interpretation
  - Core Claim
  - Hard Rule
  - Small Penetration Is Not Treated as a Stop-Hunt
  - No Buffer Around the Cycle-Origin Node
  - Before Fill vs After Fill
  - Impact on Extreme
  - Relationship to EXT-01
  - Dataset Consequence
  - Execution Consequence
  - AI Relevance
  - Short Formal Statement

## Related Source Documents

- [[docs/experience_capture/questions/by_code/EXT-01|EXT-01.md]] — score `18`
- [[docs/experience_capture/questions/by_code/EXT-06|EXT-06.md]] — score `18`
- [[docs/ai_execution/AI_ALGORITHM_LAYER_MAP_FOR_EXTREME_ENGINE_FA|AI_ALGORITHM_LAYER_MAP_FOR_EXTREME_ENGINE_FA.md]] — score `12`
- [[docs/ai_execution/AI_NATIVE_EXECUTION_ROADMAP_FA|AI_NATIVE_EXECUTION_ROADMAP_FA.md]] — score `12`
- [[docs/ai_execution/AMIR_STRUCTURAL_EXPERIENCE_MAP_FA|AMIR_STRUCTURAL_EXPERIENCE_MAP_FA.md]] — score `12`
- [[docs/ai_execution/EXTREME_L2_NODE_CYCLE_LIMIT_ENTRY_FA|EXTREME_L2_NODE_CYCLE_LIMIT_ENTRY_FA.md]] — score `12`
- [[docs/debug/MARKET_LANGUAGE/README|README.md]] — score `12`
- [[docs/execution/H0005_R1_SIX_SLOT_TOUCH_LEDGER|H0005_R1_SIX_SLOT_TOUCH_LEDGER.md]] — score `12`
- [[docs/experience_capture/answers/BASE-02/answer_normalized_en|answer_normalized_en.md]] — score `12`
- [[docs/experience_capture/answers/BASE-04/answer_normalized_en|answer_normalized_en.md]] — score `12`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
