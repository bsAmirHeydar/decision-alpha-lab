
---
type: source_card
source_path: "docs/flag_counting/FLAG_COUNTING_VISUALIZATION_SPEC.md"
source_ext: ".md"
source_size: 4810
empty: false
generated_at: 2026-07-06
concepts: ["AI Agent Layer", "Convexity / Optionality", "Decision Node", "Execution / Risk", "Flag Counting", "Hook", "Path Smoothness", "Validation / Audit"]
entities: []
---

# Source Card — FLAG_COUNTING_VISUALIZATION_SPEC.md

## Source

[[docs/flag_counting/FLAG_COUNTING_VISUALIZATION_SPEC|docs/flag_counting/FLAG_COUNTING_VISUALIZATION_SPEC.md]]

## Summary

<!-- CURRENT CANON NOTICE This file is retained as historical/context documentation. For current Phoenix implementation decisions, use: docs/flag_counting/FLAG_COUNTING_CURRENT_CANON.md If this file conflicts with the current canon, the current canon wins. --> This document defines the clean-all chart visualization for `FlagCountingVNext`. The renderer must allow all accepted F and ND sequences to remain visible, but it must avoid turning the chart into unreadable noise. The default visual contract is: all body lines use the same thin width; different sequences use shade variations inside the same direction/status color family; peak labels are placed above peaks; valley labels are placed below valleys; labels are stacked deterministically when several F/ND labels belong to the same visual cluster; the closest label to price is the dominant one: larger scale first, then higher F level, th

## Concepts

[[docs/obsidian_deep/02_concepts/AI_Agent_Layer|AI Agent Layer]], [[docs/obsidian_deep/02_concepts/Convexity____Optionality|Convexity / Optionality]], [[docs/obsidian_deep/02_concepts/Decision_Node|Decision Node]], [[docs/obsidian_deep/02_concepts/Execution____Risk|Execution / Risk]], [[docs/obsidian_deep/02_concepts/Flag_Counting|Flag Counting]], [[docs/obsidian_deep/02_concepts/Hook|Hook]], [[docs/obsidian_deep/02_concepts/Path_Smoothness|Path Smoothness]], [[docs/obsidian_deep/02_concepts/Validation____Audit|Validation / Audit]]

## Entities

—

## Headings

- Flag Counting Visualization Specification
  - Core display contract
  - Label stacking
  - ND labels
  - Curves
  - Line widths
  - ND / Hook Detection Contract
    - ND high/low-only contract
  - Origin identity and live-root display contract

## Related Source Documents

- [[docs/flag_counting/FLAG_COUNTING_CURRENT_CANON|FLAG_COUNTING_CURRENT_CANON.md]] — score `23`
- [[docs/flag_counting/FLAG_COUNTING_SEQUENCE_CONTRACT_V2|FLAG_COUNTING_SEQUENCE_CONTRACT_V2.md]] — score `17`
- [[docs/flag_counting/FLAG_COUNTING_SEQUENCE_CONTRACT_V3|FLAG_COUNTING_SEQUENCE_CONTRACT_V3.md]] — score `17`
- [[docs/flag_counting/FLAG_COUNTING_SEQUENCE_CONTRACT_V4|FLAG_COUNTING_SEQUENCE_CONTRACT_V4.md]] — score `17`
- [[docs/ai_execution/AI_NATIVE_EXECUTION_ROADMAP_FA|AI_NATIVE_EXECUTION_ROADMAP_FA.md]] — score `16`
- [[docs/mql_native/H0007_FLAG_COUNTING_F1_START_STRUCTURE|H0007_FLAG_COUNTING_F1_START_STRUCTURE.md]] — score `16`
- [[lab/03_experiments/EXP_flag_counting/docs/README_FLAG_OPTIONALITY_XY_STATE_PHILOSOPHY|README_FLAG_OPTIONALITY_XY_STATE_PHILOSOPHY.md]] — score `16`
- [[docs/flag_counting/FLAG_COUNTING_ALGORITHM_BLUEPRINT|FLAG_COUNTING_ALGORITHM_BLUEPRINT.md]] — score `15`
- [[docs/flag_counting/FLAG_COUNTING_CONCEPT_SPEC_V2|FLAG_COUNTING_CONCEPT_SPEC_V2.md]] — score `15`
- [[docs/flag_counting/FLAG_COUNTING_CONCEPT_SPEC_V3|FLAG_COUNTING_CONCEPT_SPEC_V3.md]] — score `15`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
