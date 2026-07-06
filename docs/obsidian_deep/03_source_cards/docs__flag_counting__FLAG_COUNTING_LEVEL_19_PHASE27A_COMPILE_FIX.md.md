
---
type: source_card
source_path: "docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE27A_COMPILE_FIX.md"
source_ext: ".md"
source_size: 801
empty: false
generated_at: 2026-07-06
concepts: ["Decision Node", "Execution / Risk", "Flag Counting", "Hook", "Licensing", "Path Smoothness"]
entities: []
---

# Source Card — FLAG_COUNTING_LEVEL_19_PHASE27A_COMPILE_FIX.md

## Source

[[docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE27A_COMPILE_FIX|docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE27A_COMPILE_FIX.md]]

## Summary

Phase 27A fixes a compile error introduced in Phase 27. Phase 27 used `FP_StateGateClampDouble` inside the paper path smoothness score function, but that helper was not defined in the current State Gate rules module. Replace the undefined helper call with explicit local clamp logic: This patch only changes the Phase 27 path quality smoothness score clamp. It does not modify:

## Concepts

[[docs/obsidian_deep/02_concepts/Decision_Node|Decision Node]], [[docs/obsidian_deep/02_concepts/Execution____Risk|Execution / Risk]], [[docs/obsidian_deep/02_concepts/Flag_Counting|Flag Counting]], [[docs/obsidian_deep/02_concepts/Hook|Hook]], [[docs/obsidian_deep/02_concepts/Licensing|Licensing]], [[docs/obsidian_deep/02_concepts/Path_Smoothness|Path Smoothness]]

## Entities

—

## Headings

- Flag Counting Level 19 — Phase 27A Compile Fix
  - Purpose
  - Error
  - Cause
  - Fix
  - Scope

## Related Source Documents

- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE26_PAPER_PERFORMANCE_REPORT|FLAG_COUNTING_LEVEL_19_PHASE26_PAPER_PERFORMANCE_REPORT.md]] — score `13`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE27_PAPER_MFE_MAE_PATH_QUALITY|FLAG_COUNTING_LEVEL_19_PHASE27_PAPER_MFE_MAE_PATH_QUALITY.md]] — score `13`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE28_CONTEXT_PERFORMANCE_MATRIX|FLAG_COUNTING_LEVEL_19_PHASE28_CONTEXT_PERFORMANCE_MATRIX.md]] — score `13`
- [[docs/flag_counting/FLAG_COUNTING_ALGORITHM_BLUEPRINT|FLAG_COUNTING_ALGORITHM_BLUEPRINT.md]] — score `11`
- [[docs/flag_counting/FLAG_COUNTING_CONCEPT_SPEC_V2|FLAG_COUNTING_CONCEPT_SPEC_V2.md]] — score `11`
- [[docs/flag_counting/FLAG_COUNTING_CURRENT_CANON|FLAG_COUNTING_CURRENT_CANON.md]] — score `11`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_CLEAN_ISOLATED_STATE_GATE|FLAG_COUNTING_LEVEL_19_CLEAN_ISOLATED_STATE_GATE.md]] — score `11`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE10_PANEL_LINE_CONTRACT|FLAG_COUNTING_LEVEL_19_PHASE10_PANEL_LINE_CONTRACT.md]] — score `11`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE11_ENTRY_BRIDGE_READINESS|FLAG_COUNTING_LEVEL_19_PHASE11_ENTRY_BRIDGE_READINESS.md]] — score `11`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE12_EXTREME_CANDIDATE_MAP|FLAG_COUNTING_LEVEL_19_PHASE12_EXTREME_CANDIDATE_MAP.md]] — score `11`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
