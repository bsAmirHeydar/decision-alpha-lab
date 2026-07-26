
---
type: source_card
source_path: "docs/flag_counting/implementation_ladder_v1/README.md"
source_ext: ".md"
source_size: 8090
empty: false
generated_at: 2026-07-06
concepts: ["AI Agent Layer", "Convexity / Optionality", "Decision Node", "Execution / Risk", "Flag Counting", "Hook", "MQL Native", "Python Brain", "UI / React", "Validation / Audit"]
entities: []
---

# Source Card — README.md

## Source

[[docs/flag_counting/implementation_ladder_v1/README|docs/flag_counting/implementation_ladder_v1/README.md]]

## Summary

This package defines a layered implementation plan for the Phoenix Flag Counting engine. It is subordinate to `docs/flag_counting/FLAG_COUNTING_CURRENT_CANON.md`, which is the active source of truth and conflict resolver… The solution is not another tactical patch. The solution is a strict implementation ladder. Each layer has: a responsibility boundary; source-file ownership; input and output contracts; forbidden dependencies; acceptance tests; freeze criteria; failure symptoms. A layer is not allowed to move upward until its acceptance tests pass. A higher layer is not allowed to compensate for a lower-layer bug. If a lower-layer bug appears, implementation returns to that layer, fixes it, upda… `00_GOVERNANCE_AND_FREEZE_PROTOCOL.md` — how the ladder must be used, committed, frozen, and rolled back. `01_LEVEL_01_CANDLE_STREAM_AND_TIMEBASE.md` — bar stream, candle indexing, and time-gap

## Concepts

[[docs/obsidian_deep/02_concepts/AI_Agent_Layer|AI Agent Layer]], [[docs/obsidian_deep/02_concepts/Convexity____Optionality|Convexity / Optionality]], [[docs/obsidian_deep/02_concepts/Decision_Node|Decision Node]], [[docs/obsidian_deep/02_concepts/Execution____Risk|Execution / Risk]], [[docs/obsidian_deep/02_concepts/Flag_Counting|Flag Counting]], [[docs/obsidian_deep/02_concepts/Hook|Hook]], [[docs/obsidian_deep/02_concepts/MQL_Native|MQL Native]], [[docs/obsidian_deep/02_concepts/Python_Brain|Python Brain]], [[docs/obsidian_deep/02_concepts/UI____React|UI / React]], [[docs/obsidian_deep/02_concepts/Validation____Audit|Validation / Audit]]

## Entities

—

## Headings

- Phoenix Flag Counting Implementation Ladder V1
  - Purpose
  - Directory
  - Source modules covered
  - Core rule
  - Implementation policy
  - Level 10 patch status
  - Level 11.5 patch status
  - Level 12 patch status
  - Level 13 patch status
  - Level 13 patch status
  - Level 14 patch status

## Related Source Documents

- [[docs/flag_counting/implementation_ladder_v1/15_MODULE_INTERFACE_CONTRACTS|15_MODULE_INTERFACE_CONTRACTS.md]] — score `29`
- [[docs/flag_counting/implementation_ladder_v1/16_IMPLEMENTATION_ORDER_AND_ACCEPTANCE_MATRIX|16_IMPLEMENTATION_ORDER_AND_ACCEPTANCE_MATRIX.md]] — score `29`
- [[docs/flag_counting/FLAG_COUNTING_CURRENT_CANON|FLAG_COUNTING_CURRENT_CANON.md]] — score `28`
- [[docs/flag_counting/implementation_ladder_v1/11_LEVEL_11_CANONICALIZATION_AND_AUDIT|11_LEVEL_11_CANONICALIZATION_AND_AUDIT.md]] — score `27`
- [[docs/flag_counting/implementation_ladder_v1/12_LEVEL_12_RENDERER_AND_LABEL_LAYOUT|12_LEVEL_12_RENDERER_AND_LABEL_LAYOUT.md]] — score `27`
- [[docs/flag_counting/implementation_ladder_v1/14_LEVEL_14_RELEASE_ROLLBACK_AND_DEBUG_PROTOCOL|14_LEVEL_14_RELEASE_ROLLBACK_AND_DEBUG_PROTOCOL.md]] — score `27`
- [[docs/flag_counting/implementation_ladder_v1/04_LEVEL_04_HOOK_ND_CONTEXT_ENGINE|04_LEVEL_04_HOOK_ND_CONTEXT_ENGINE.md]] — score `25`
- [[docs/flag_counting/implementation_ladder_v1/11_5_LEVEL_11_5_RAW_AUDIT_EXPORT|11_5_LEVEL_11_5_RAW_AUDIT_EXPORT.md]] — score `25`
- [[docs/flag_counting/implementation_ladder_v1/17_AMBIGUITIES_TO_RESOLVE_BEFORE_CODE|17_AMBIGUITIES_TO_RESOLVE_BEFORE_CODE.md]] — score `25`
- [[docs/flag_counting/implementation_ladder_v1/13_LEVEL_13_VALIDATION_MATRIX|13_LEVEL_13_VALIDATION_MATRIX.md]] — score `25`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
