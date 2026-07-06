
---
type: source_card
source_path: "docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE24A_COMPILE_FIX.md"
source_ext: ".md"
source_size: 1046
empty: false
generated_at: 2026-07-06
concepts: ["Decision Node", "Flag Counting", "Hook", "Licensing", "UI / React", "Validation / Audit"]
entities: []
---

# Source Card — FLAG_COUNTING_LEVEL_19_PHASE24A_COMPILE_FIX.md

## Source

[[docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE24A_COMPILE_FIX|docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE24A_COMPILE_FIX.md]]

## Summary

Phase 24A fixes a compile error introduced during Phase 24. `persistent_paper_trade_row_count` was declared twice inside `FP_StateGateTimeframeState`. One per-timeframe declaration is required, and one snapshot-level declaration is required. The duplicate per-timeframe declaration was invalid. Remove the extra per-timeframe declaration and keep: Both reset paths remain valid: This fix does not change: It only fixes Phase 24 type ownership.

## Concepts

[[docs/obsidian_deep/02_concepts/Decision_Node|Decision Node]], [[docs/obsidian_deep/02_concepts/Flag_Counting|Flag Counting]], [[docs/obsidian_deep/02_concepts/Hook|Hook]], [[docs/obsidian_deep/02_concepts/Licensing|Licensing]], [[docs/obsidian_deep/02_concepts/UI____React|UI / React]], [[docs/obsidian_deep/02_concepts/Validation____Audit|Validation / Audit]]

## Entities

—

## Headings

- Flag Counting Level 19 — Phase 24A Compile Fix
  - Purpose
  - Error
  - Cause
  - Fix
  - Locked boundaries

## Related Source Documents

- [[docs/flag_counting/FLAG_COUNTING_CURRENT_CANON|FLAG_COUNTING_CURRENT_CANON.md]] — score `13`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_CLEAN_ISOLATED_STATE_GATE|FLAG_COUNTING_LEVEL_19_CLEAN_ISOLATED_STATE_GATE.md]] — score `13`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE10_PANEL_LINE_CONTRACT|FLAG_COUNTING_LEVEL_19_PHASE10_PANEL_LINE_CONTRACT.md]] — score `13`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE13_MTF_ALIGNMENT_MAP|FLAG_COUNTING_LEVEL_19_PHASE13_MTF_ALIGNMENT_MAP.md]] — score `13`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE14_ENTRY_GEOMETRY_READINESS|FLAG_COUNTING_LEVEL_19_PHASE14_ENTRY_GEOMETRY_READINESS.md]] — score `13`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE18_PAPER_LEDGER_LIFECYCLE_TRACKING|FLAG_COUNTING_LEVEL_19_PHASE18_PAPER_LEDGER_LIFECYCLE_TRACKING.md]] — score `13`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE19_PAPER_RESULT_METRICS|FLAG_COUNTING_LEVEL_19_PHASE19_PAPER_RESULT_METRICS.md]] — score `13`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE21_PAPER_REGIME_ATTRIBUTION|FLAG_COUNTING_LEVEL_19_PHASE21_PAPER_REGIME_ATTRIBUTION.md]] — score `13`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE22_PAPER_FILTER_DIAGNOSTICS|FLAG_COUNTING_LEVEL_19_PHASE22_PAPER_FILTER_DIAGNOSTICS.md]] — score `13`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE23_DRY_RUN_DECISION_POLICY|FLAG_COUNTING_LEVEL_19_PHASE23_DRY_RUN_DECISION_POLICY.md]] — score `13`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
