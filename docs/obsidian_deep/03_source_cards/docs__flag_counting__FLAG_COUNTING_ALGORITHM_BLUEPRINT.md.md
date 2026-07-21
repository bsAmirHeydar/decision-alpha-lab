
---
type: source_card
source_path: "docs/flag_counting/FLAG_COUNTING_ALGORITHM_BLUEPRINT.md"
source_ext: ".md"
source_size: 7207
empty: false
generated_at: 2026-07-06
concepts: ["AI Agent Layer", "Decision Node", "Execution / Risk", "Flag Counting", "Hook", "Path Smoothness", "Rally", "UI / React", "Validation / Audit"]
entities: []
---

# Source Card — FLAG_COUNTING_ALGORITHM_BLUEPRINT.md

## Source

[[docs/flag_counting/FLAG_COUNTING_ALGORITHM_BLUEPRINT|docs/flag_counting/FLAG_COUNTING_ALGORITHM_BLUEPRINT.md]]

## Summary

This document converts the concept specification into implementation-level algorithms. Fields: `int index` `datetime time` `double price` `int kind` where `+1 = high`, `-1 = low` `int scale_l` `bool confirmed` A lightweight copy of a node used inside a sequence: `index` `time` `price` `kind` `scale_l` `valid` Fields: `sequence_id` `parent_id` `root_id` `scale_l` `direction` `level`: F1/F2/F3 `phase`: F or ND `status`: live/confirmed/invalidated/terminal `position`: building_leg1, building_waist, building_leg2, waiting_internal1, waiting_internal2, waiting_rebreak, confirmed, terminal_f3 `origin` `leg1` `waist` `leg2` `internal1` `internal2` `confirm` `invalid` `branch_type`: none, normal_internal12, waist_break, terminal_f3 `body_size` `parent_body_size` `created_at_index` `last_update_index` `extension_count` `reason` For every configured scale L: Detect raw swing highs and lows. Compre

## Concepts

[[docs/obsidian_deep/02_concepts/AI_Agent_Layer|AI Agent Layer]], [[docs/obsidian_deep/02_concepts/Decision_Node|Decision Node]], [[docs/obsidian_deep/02_concepts/Execution____Risk|Execution / Risk]], [[docs/obsidian_deep/02_concepts/Flag_Counting|Flag Counting]], [[docs/obsidian_deep/02_concepts/Hook|Hook]], [[docs/obsidian_deep/02_concepts/Path_Smoothness|Path Smoothness]], [[docs/obsidian_deep/02_concepts/Rally|Rally]], [[docs/obsidian_deep/02_concepts/UI____React|UI / React]], [[docs/obsidian_deep/02_concepts/Validation____Audit|Validation / Audit]]

## Entities

—

## Headings

- Flag Counting Algorithm Blueprint
  - 1. Data model
    - FC_Node
    - FC_Point
    - FC_Sequence
  - 2. Node engine
  - 3. F1 body construction
    - Bullish F1 body
    - Bearish F1 body
  - 4. F1 internal count
    - Bullish
    - Bearish

## Related Source Documents

- [[docs/flag_counting/FLAG_COUNTING_CONCEPT_SPEC_V2|FLAG_COUNTING_CONCEPT_SPEC_V2.md]] — score `19`
- [[docs/flag_counting/FLAG_COUNTING_SEQUENCE_CONTRACT_V2|FLAG_COUNTING_SEQUENCE_CONTRACT_V2.md]] — score `19`
- [[docs/flag_counting/FLAG_COUNTING_SEQUENCE_CONTRACT_V3|FLAG_COUNTING_SEQUENCE_CONTRACT_V3.md]] — score `19`
- [[docs/flag_counting/FLAG_COUNTING_SEQUENCE_CONTRACT_V4|FLAG_COUNTING_SEQUENCE_CONTRACT_V4.md]] — score `19`
- [[docs/ai_execution/AI_NATIVE_EXECUTION_ROADMAP_FA|AI_NATIVE_EXECUTION_ROADMAP_FA.md]] — score `18`
- [[docs/releases/legacy_migration/general/0b9f38e7e2fd_README_FLAG_OPTIONALITY_XY_STATE_PHILOSOPHY|README_FLAG_OPTIONALITY_XY_STATE_PHILOSOPHY.md]] — score `18`
- [[docs/flag_counting/FLAG_COUNTING_CONCEPT_SPEC_V3|FLAG_COUNTING_CONCEPT_SPEC_V3.md]] — score `17`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE13_MTF_ALIGNMENT_MAP|FLAG_COUNTING_LEVEL_19_PHASE13_MTF_ALIGNMENT_MAP.md]] — score `17`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE14_ENTRY_GEOMETRY_READINESS|FLAG_COUNTING_LEVEL_19_PHASE14_ENTRY_GEOMETRY_READINESS.md]] — score `17`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE28_CONTEXT_PERFORMANCE_MATRIX|FLAG_COUNTING_LEVEL_19_PHASE28_CONTEXT_PERFORMANCE_MATRIX.md]] — score `17`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
