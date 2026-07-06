
---
type: source_card
source_path: "docs/flag_counting/FLAG_COUNTING_STATE_MACHINE_V4.md"
source_ext: ".md"
source_size: 4798
empty: false
generated_at: 2026-07-06
concepts: ["Decision Node", "Flag Counting", "Hook", "UI / React"]
entities: []
---

# Source Card — FLAG_COUNTING_STATE_MACHINE_V4.md

## Source

[[docs/flag_counting/FLAG_COUNTING_STATE_MACHINE_V4|docs/flag_counting/FLAG_COUNTING_STATE_MACHINE_V4.md]]

## Summary

<!-- CURRENT CANON NOTICE This file is retained as historical/context documentation. For current Phoenix implementation decisions, use: docs/flag_counting/FLAG_COUNTING_CURRENT_CANON.md If this file conflicts with the current canon, the current canon wins. --> This document converts the sequence contract into implementation states. The state machine is sequence-based. It is not a sliding-window detector. A directional chain has the following high-level states: The engine waits for a legal F1 start context: terminal ND/Hook extreme; end/lock of opposite sequence; first confirmed opposite F1 that locks a previous F3. No arbitrary mid-move F1 is allowed. The engine builds a two-leg F1 candidate: F1 is drawn only after Leg2 exists. Leg1 and Waist must update to their true extremes: bullish Leg1 = highest high before correction; bullish Waist = lowest low before Leg2; bearish Leg1 = lowest lo

## Concepts

[[docs/obsidian_deep/02_concepts/Decision_Node|Decision Node]], [[docs/obsidian_deep/02_concepts/Flag_Counting|Flag Counting]], [[docs/obsidian_deep/02_concepts/Hook|Hook]], [[docs/obsidian_deep/02_concepts/UI____React|UI / React]]

## Entities

—

## Headings

- Flag Counting State Machine V4
  - 1. Main Chain State
  - 2. WAIT_PHASE_BOUNDARY
  - 3. BUILD_F1_BODY
  - 4. F1_POST_FLAG_COUNTING
  - 5. F1_CONFIRMED_BUILD_F2
  - 6. F2_BODY_OR_SEED
  - 7. F2_POST_FLAG_COUNTING
  - 8. F2_CONFIRMED_BUILD_F3
  - 9. F3_BODY_OR_SEED
  - 10. F3_COMPLETED_EXTENSION
  - 11. F3_LOCKED_CHAIN_DONE

## Related Source Documents

- [[docs/flag_counting/FLAG_COUNTING_CURRENT_CANON|FLAG_COUNTING_CURRENT_CANON.md]] — score `17`
- [[docs/flag_counting/FLAG_COUNTING_ALGORITHM_BLUEPRINT|FLAG_COUNTING_ALGORITHM_BLUEPRINT.md]] — score `9`
- [[docs/flag_counting/FLAG_COUNTING_CONCEPT_SPEC_V2|FLAG_COUNTING_CONCEPT_SPEC_V2.md]] — score `9`
- [[docs/flag_counting/FLAG_COUNTING_CONCEPT_SPEC_V3|FLAG_COUNTING_CONCEPT_SPEC_V3.md]] — score `9`
- [[docs/flag_counting/FLAG_COUNTING_GLOSSARY|FLAG_COUNTING_GLOSSARY.md]] — score `9`
- [[docs/flag_counting/FLAG_COUNTING_IMPLEMENTATION_CHECKLIST_V3|FLAG_COUNTING_IMPLEMENTATION_CHECKLIST_V3.md]] — score `9`
- [[docs/flag_counting/FLAG_COUNTING_IMPLEMENTATION_CHECKLIST_V4|FLAG_COUNTING_IMPLEMENTATION_CHECKLIST_V4.md]] — score `9`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_CLEAN_ISOLATED_STATE_GATE|FLAG_COUNTING_LEVEL_19_CLEAN_ISOLATED_STATE_GATE.md]] — score `9`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE10_PANEL_LINE_CONTRACT|FLAG_COUNTING_LEVEL_19_PHASE10_PANEL_LINE_CONTRACT.md]] — score `9`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE13_MTF_ALIGNMENT_MAP|FLAG_COUNTING_LEVEL_19_PHASE13_MTF_ALIGNMENT_MAP.md]] — score `9`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
