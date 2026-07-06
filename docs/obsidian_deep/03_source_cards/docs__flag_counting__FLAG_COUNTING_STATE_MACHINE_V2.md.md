
---
type: source_card
source_path: "docs/flag_counting/FLAG_COUNTING_STATE_MACHINE_V2.md"
source_ext: ".md"
source_size: 5549
empty: false
generated_at: 2026-07-06
concepts: ["Decision Node", "Execution / Risk", "Flag Counting", "UI / React", "Validation / Audit"]
entities: []
---

# Source Card — FLAG_COUNTING_STATE_MACHINE_V2.md

## Source

[[docs/flag_counting/FLAG_COUNTING_STATE_MACHINE_V2|docs/flag_counting/FLAG_COUNTING_STATE_MACHINE_V2.md]]

## Summary

<!-- CURRENT CANON NOTICE This file is retained as historical/context documentation. For current Phoenix implementation decisions, use: docs/flag_counting/FLAG_COUNTING_CURRENT_CANON.md If this file conflicts with the current canon, the current canon wins. --> This document defines a state-machine interpretation of the Flag Counting Sequence Contract V2. The purpose is to prevent the detector from behaving like a sliding-window pattern scanner. Do not create F1 from arbitrary four-node middle windows. The intervening node between internal 1 and internal 2 must not exceed the F1 flag endpoint. For bullish F1: For bearish F1: If F2 rejects: The exact definition of smallest opposite F1 remains open. Rejected states must be logged but not drawn on the main chart.

## Concepts

[[docs/obsidian_deep/02_concepts/Decision_Node|Decision Node]], [[docs/obsidian_deep/02_concepts/Execution____Risk|Execution / Risk]], [[docs/obsidian_deep/02_concepts/Flag_Counting|Flag Counting]], [[docs/obsidian_deep/02_concepts/UI____React|UI / React]], [[docs/obsidian_deep/02_concepts/Validation____Audit|Validation / Audit]]

## Entities

—

## Headings

- Flag Counting State Machine V2
  - 1. Top-level sequence states
  - 2. Shared event types
  - 3. WAIT_F1
    - Entry conditions
    - Valid transitions
    - Invalid transitions
  - 4. F1_CANDIDATE
    - Internal substates
    - Rules
    - Transitions
    - Important F1-specific rule

## Related Source Documents

- [[docs/flag_counting/FLAG_COUNTING_CURRENT_CANON|FLAG_COUNTING_CURRENT_CANON.md]] — score `19`
- [[docs/flag_counting/FLAG_COUNTING_ALGORITHM_BLUEPRINT|FLAG_COUNTING_ALGORITHM_BLUEPRINT.md]] — score `11`
- [[docs/flag_counting/FLAG_COUNTING_CONCEPT_SPEC_V2|FLAG_COUNTING_CONCEPT_SPEC_V2.md]] — score `11`
- [[docs/flag_counting/FLAG_COUNTING_IMPLEMENTATION_CHECKLIST_V2|FLAG_COUNTING_IMPLEMENTATION_CHECKLIST_V2.md]] — score `11`
- [[docs/flag_counting/FLAG_COUNTING_IMPLEMENTATION_CHECKLIST_V4|FLAG_COUNTING_IMPLEMENTATION_CHECKLIST_V4.md]] — score `11`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_CLEAN_ISOLATED_STATE_GATE|FLAG_COUNTING_LEVEL_19_CLEAN_ISOLATED_STATE_GATE.md]] — score `11`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE10_PANEL_LINE_CONTRACT|FLAG_COUNTING_LEVEL_19_PHASE10_PANEL_LINE_CONTRACT.md]] — score `11`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE13_MTF_ALIGNMENT_MAP|FLAG_COUNTING_LEVEL_19_PHASE13_MTF_ALIGNMENT_MAP.md]] — score `11`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE14_ENTRY_GEOMETRY_READINESS|FLAG_COUNTING_LEVEL_19_PHASE14_ENTRY_GEOMETRY_READINESS.md]] — score `11`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE18_PAPER_LEDGER_LIFECYCLE_TRACKING|FLAG_COUNTING_LEVEL_19_PHASE18_PAPER_LEDGER_LIFECYCLE_TRACKING.md]] — score `11`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
