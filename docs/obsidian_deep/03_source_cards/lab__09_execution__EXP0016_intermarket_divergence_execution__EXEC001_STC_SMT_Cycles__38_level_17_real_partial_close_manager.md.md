
---
type: source_card
source_path: "lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/38_level_17_real_partial_close_manager.md"
source_ext: ".md"
source_size: 4616
empty: false
generated_at: 2026-07-06
concepts: ["Execution / Risk", "Intermarket Divergence", "Python Brain", "UI / React", "Validation / Audit"]
entities: ["EXEC001"]
---

# Source Card — 38_level_17_real_partial_close_manager.md

## Source

[[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/38_level_17_real_partial_close_manager|lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/38_level_17_real_partial_close_manager.md]]

## Summary

Level 17 adds the first real broker-side partial close layer for EXEC001 STC SMT Cycles. The layer does not create entries. Real entries remain controlled by Level 16 and remain disabled unless the user explicitly enables auto trading. Level 17 only watches already-open broker positions that belong to this S… The owner-locked rule is: partial close is evaluated exactly at the end of W4 / end of the M cycle; delayed partial must still be recovered later if the EA was offline; M3 partial is disabled because 15:30 New York hard close has priority; partial closes about 50% of volume; close volume is rounded upward to broker volume step; tiny positions can be fully closed if rounded half-volume consumes the entire position; foreign/manual positions must never be managed. Default configuration is safe: `InpEnableRealPartialClose = false` `InpAllowRealPartialInPaperLive = false` `InpRuntimeMode

## Concepts

[[docs/obsidian_deep/02_concepts/Execution____Risk|Execution / Risk]], [[docs/obsidian_deep/02_concepts/Intermarket_Divergence|Intermarket Divergence]], [[docs/obsidian_deep/02_concepts/Python_Brain|Python Brain]], [[docs/obsidian_deep/02_concepts/UI____React|UI / React]], [[docs/obsidian_deep/02_concepts/Validation____Audit|Validation / Audit]]

## Entities

EXEC001

## Headings

- Level 17 — Real Partial Close Manager
  - Purpose
  - Safety Status
  - Managed Positions
  - W4 Due Times
  - Duplicate Prevention
  - Volume Rule
  - Runtime Transport Gate
  - Outputs
  - Non-Goals
  - Acceptance Criteria

## Related Source Documents

- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/17_implementation_plan|17_implementation_plan.md]] — score `16`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/18_module_breakdown|18_module_breakdown.md]] — score `16`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/19_patch_build_sequence|19_patch_build_sequence.md]] — score `16`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/21_first_patch_scope|21_first_patch_scope.md]] — score `16`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/22_level_01_skeleton|22_level_01_skeleton.md]] — score `16`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/30_level_09_paper_outcome_simulator|30_level_09_paper_outcome_simulator.md]] — score `16`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/32_level_11_hard_close_simulator|32_level_11_hard_close_simulator.md]] — score `16`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/34_level_13_visualization_audit_drawing|34_level_13_visualization_audit_drawing.md]] — score `16`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/35_level_14_paper_live_alerts|35_level_14_paper_live_alerts.md]] — score `16`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/40_level_19_validation_pack|40_level_19_validation_pack.md]] — score `16`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
