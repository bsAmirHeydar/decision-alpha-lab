
---
type: source_card
source_path: "docs/experience_capture/answers/RSK-R02/answer_normalized_en.md"
source_ext: ".md"
source_size: 7094
empty: false
generated_at: 2026-07-06
concepts: ["AI Agent Layer", "Convexity / Optionality", "Decision Node", "Execution / Risk", "Hook", "Rally", "UI / React", "Validation / Audit", "Zone / RTV"]
entities: []
---

# Source Card — answer_normalized_en.md

## Source

[[docs/experience_capture/answers/RSK-R02/answer_normalized_en|docs/experience_capture/answers/RSK-R02/answer_normalized_en.md]]

## Summary

Risk in NDS is account-percentage based, but it is not fixed. The base risk percentage should be adjusted by a setup-quality coefficient. Then position sizing must be calculated so that the true monetary cost, after stop distance and commission, equals the intended risk budget. Recommended canonical model: And the executable size must satisfy: This makes cost exact and auditable. The user clarifies that risk means: Therefore, the primary unit of risk budget should be: But this percentage should be modified by setup quality. Suggested fields: Setups have quality differences. The risk coefficient should reflect this. Possible interpretation: The coefficient should be trained from outcome data, not guessed permanently. Suggested model: This coefficient should be derived from the multi-level evaluation established in RSK-R01: The user defines cost operationally: To be precise, true cost shou

## Concepts

[[docs/obsidian_deep/02_concepts/AI_Agent_Layer|AI Agent Layer]], [[docs/obsidian_deep/02_concepts/Convexity____Optionality|Convexity / Optionality]], [[docs/obsidian_deep/02_concepts/Decision_Node|Decision Node]], [[docs/obsidian_deep/02_concepts/Execution____Risk|Execution / Risk]], [[docs/obsidian_deep/02_concepts/Hook|Hook]], [[docs/obsidian_deep/02_concepts/Rally|Rally]], [[docs/obsidian_deep/02_concepts/UI____React|UI / React]], [[docs/obsidian_deep/02_concepts/Validation____Audit|Validation / Audit]], [[docs/obsidian_deep/02_concepts/Zone____RTV|Zone / RTV]]

## Entities

—

## Headings

- RSK-R02 — Normalized Interpretation
  - Core Claim
  - Risk as Percent of Account
  - Setup Quality Risk Coefficient
  - True Cost
  - Position Sizing Consequence
  - High Reward Target
  - Cost-to-Potential
  - Optionality Is Multi-Level
  - Context Optionality
  - Zone Optionality
  - Entry Optionality

## Related Source Documents

- [[docs/architecture|architecture.md]] — score `20`
- [[docs/ai_execution/AI_ALGORITHM_LAYER_MAP_FOR_EXTREME_ENGINE_FA|AI_ALGORITHM_LAYER_MAP_FOR_EXTREME_ENGINE_FA.md]] — score `18`
- [[docs/ai_execution/AI_NATIVE_EXECUTION_ROADMAP_FA|AI_NATIVE_EXECUTION_ROADMAP_FA.md]] — score `18`
- [[docs/ai_execution/AMIR_STRUCTURAL_EXPERIENCE_MAP_FA|AMIR_STRUCTURAL_EXPERIENCE_MAP_FA.md]] — score `18`
- [[docs/ai_execution/EXTREME_L2_NODE_CYCLE_LIMIT_ENTRY_FA|EXTREME_L2_NODE_CYCLE_LIMIT_ENTRY_FA.md]] — score `18`
- [[docs/experience_capture/answers/EXT-01/answer_normalized_en|answer_normalized_en.md]] — score `18`
- [[docs/experience_capture/answers/EXT-08/notes_en|notes_en.md]] — score `18`
- [[docs/experience_capture/answers/NDS-R01/answer_normalized_en|answer_normalized_en.md]] — score `18`
- [[docs/flag_counting/FLAG_COUNTING_SEQUENCE_CONTRACT_V3|FLAG_COUNTING_SEQUENCE_CONTRACT_V3.md]] — score `18`
- [[docs/nds_hook_architecture/06_build_phases|06_build_phases.md]] — score `18`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
