
---
type: source_card
source_path: "docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE20A_COMPILE_FIX.md"
source_ext: ".md"
source_size: 952
empty: false
generated_at: 2026-07-06
concepts: ["Decision Node", "Flag Counting", "Hook", "Licensing", "Validation / Audit"]
entities: []
---

# Source Card — FLAG_COUNTING_LEVEL_19_PHASE20A_COMPILE_FIX.md

## Source

[[docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE20A_COMPILE_FIX|docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE20A_COMPILE_FIX.md]]

## Summary

Phase 20A fixes a compile error introduced during Phase 20. The paper portfolio aggregate fields are snapshot-level fields, but their reset assignments were accidentally inserted into `FP_ResetStateGateTimeframeState`. `FP_StateGateTimeframeState` correctly does not own portfolio aggregate fields. Move the paper portfolio aggregate reset assignments to `FP_ResetStateGateSnapshot`. The fix keeps the Phase 20 portfolio aggregate model intact and only corrects the type ownership boundary. This fix does not change: It only fixes Phase 20 State Gate type reset ownership.

## Concepts

[[docs/obsidian_deep/02_concepts/Decision_Node|Decision Node]], [[docs/obsidian_deep/02_concepts/Flag_Counting|Flag Counting]], [[docs/obsidian_deep/02_concepts/Hook|Hook]], [[docs/obsidian_deep/02_concepts/Licensing|Licensing]], [[docs/obsidian_deep/02_concepts/Validation____Audit|Validation / Audit]]

## Entities

—

## Headings

- Flag Counting Level 19 — Phase 20A Compile Fix
  - Purpose
  - Error
  - Cause
  - Fix
  - Locked boundaries

## Related Source Documents

- [[docs/flag_counting/FLAG_COUNTING_CURRENT_CANON|FLAG_COUNTING_CURRENT_CANON.md]] — score `11`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_CLEAN_ISOLATED_STATE_GATE|FLAG_COUNTING_LEVEL_19_CLEAN_ISOLATED_STATE_GATE.md]] — score `11`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE10_PANEL_LINE_CONTRACT|FLAG_COUNTING_LEVEL_19_PHASE10_PANEL_LINE_CONTRACT.md]] — score `11`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE11_ENTRY_BRIDGE_READINESS|FLAG_COUNTING_LEVEL_19_PHASE11_ENTRY_BRIDGE_READINESS.md]] — score `11`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE12_EXTREME_CANDIDATE_MAP|FLAG_COUNTING_LEVEL_19_PHASE12_EXTREME_CANDIDATE_MAP.md]] — score `11`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE13_MTF_ALIGNMENT_MAP|FLAG_COUNTING_LEVEL_19_PHASE13_MTF_ALIGNMENT_MAP.md]] — score `11`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE13A_COMPILE_FIX|FLAG_COUNTING_LEVEL_19_PHASE13A_COMPILE_FIX.md]] — score `11`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE14_ENTRY_GEOMETRY_READINESS|FLAG_COUNTING_LEVEL_19_PHASE14_ENTRY_GEOMETRY_READINESS.md]] — score `11`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE15_ENTRY_IDEA_LAYER|FLAG_COUNTING_LEVEL_19_PHASE15_ENTRY_IDEA_LAYER.md]] — score `11`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE16_ENTRY_DECISION_DRY_RUN|FLAG_COUNTING_LEVEL_19_PHASE16_ENTRY_DECISION_DRY_RUN.md]] — score `11`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
