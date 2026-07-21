
---
type: source_card
source_path: "docs/evidence/15_visualization_contract/0ccec648c2ec_15_visualization_contract.md"
source_ext: ".md"
source_size: 2410
empty: false
generated_at: 2026-07-06
concepts: ["AI Agent Layer", "Execution / Risk", "Intermarket Divergence", "UI / React", "Validation / Audit", "Zone / RTV"]
entities: []
---

# Source Card — 15_visualization_contract.md

## Source

[[docs/evidence/15_visualization_contract/0ccec648c2ec_15_visualization_contract|docs/evidence/15_visualization_contract/0ccec648c2ec_15_visualization_contract.md]]

## Summary

Visualization is required for audit, debugging, and human trust. It is not part of the decision engine. The drawing layer must never change signal logic. The EA can run on any chart. Drawings should be placed on the attached chart for audit, but the underlying logic still uses Symbol1 and Symbol2. Because a single chart can show only one symbol's price scale, drawings should support two modes: Attached-chart mode: draw events related to the chart symbol if it is Symbol1 or Symbol2. Audit-panel mode: draw textual event summaries regardless of chart symbol. All objects should use a safe prefix: `DAL_STC_EXEC001_` The renderer may delete and redraw only objects with this prefix. Cycle drawings: STC day boundary markers. M cycle background zones. W cycle separators. Gap zones as no-entry shaded areas. Level drawings: W high and W low per visible symbol. Eligible reference W levels. Selected

## Concepts

[[docs/obsidian_deep/02_concepts/AI_Agent_Layer|AI Agent Layer]], [[docs/obsidian_deep/02_concepts/Execution____Risk|Execution / Risk]], [[docs/obsidian_deep/02_concepts/Intermarket_Divergence|Intermarket Divergence]], [[docs/obsidian_deep/02_concepts/UI____React|UI / React]], [[docs/obsidian_deep/02_concepts/Validation____Audit|Validation / Audit]], [[docs/obsidian_deep/02_concepts/Zone____RTV|Zone / RTV]]

## Entities

—

## Headings

- 15 - Visualization Contract
  - 1. Purpose
  - 2. Chart independence
  - 3. Drawing object prefix
  - 4. Recommended drawings
  - 5. Drawing defaults
  - 6. Drawing density controls
  - 7. No further strategy questions

## Related Source Documents

- [[docs/evidence/11_algorithm_layers/07355f60fef2_11_algorithm_layers|11_algorithm_layers.md]] — score `13`
- [[docs/evidence/exec001_stc_smt_cycles_build_sequence/f494e5d7db74_19_patch_build_sequence|19_patch_build_sequence.md]] — score `13`
- [[docs/evidence/level_13_visualization_audit_drawing/b5b7350fdc84_34_level_13_visualization_audit_drawing|34_level_13_visualization_audit_drawing.md]] — score `13`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/43_level_21_drawing_audit|43_level_21_drawing_audit.md]] — score `13`
- [[docs/execution/EXP0016_intermarket_divergence_execution/LEVEL_13_STC_SMT_VISUALIZATION_AUDIT_DRAWING|LEVEL_13_STC_SMT_VISUALIZATION_AUDIT_DRAWING.md]] — score `12`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/03_cycle_calendar|03_cycle_calendar.md]] — score `11`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/21_first_patch_scope|21_first_patch_scope.md]] — score `11`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/29_level_08_risk_plan_paper_entry|29_level_08_risk_plan_paper_entry.md]] — score `11`
- [[docs/evidence/16_implementation_checklist/29731b650a84_16_implementation_checklist|16_implementation_checklist.md]] — score `11`
- [[docs/evidence/exec001_stc_smt_cycles_implementation_plan/0d054880f96a_17_implementation_plan|17_implementation_plan.md]] — score `11`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
