
---
type: source_card
source_path: "lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/43_level_21_drawing_audit.md"
source_ext: ".md"
source_size: 2641
empty: false
generated_at: 2026-07-06
concepts: ["AI Agent Layer", "Execution / Risk", "Intermarket Divergence", "MQL Native", "UI / React", "Validation / Audit", "Zone / RTV"]
entities: []
---

# Source Card — 43_level_21_drawing_audit.md

## Source

[[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/43_level_21_drawing_audit|lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/43_level_21_drawing_audit.md]]

## Summary

Level 21 does not change STC signal logic, paper simulation, real auto entry, real partial close, or real hard close behavior. It hardens the visual audit layer so the chart can be used as a practical verification surface for the locked STC rules: STC day projection from 20:00 New York to 15:30 New York. M1/M2/M3 active windows. 02:00–03:00 and 09:00–09:30 no-detection/no-entry gaps. 15:30 New York hard-close boundary and post-close zone. W1/W2/W3/W4 boundaries and W1 no-signal reminder. Closed W high/low levels for the active chart symbol only. Recent check-candle boxes for the active chart symbol only. Final check candles marked as audited but no-entry. Raw high/low hunt markers per legal previous-W reference. BOTH-hunted no-SMT markers. Clean-symbol SMT markers. Selected reference line used as the protective stop source. Paper entry line, SL line, TP line, partial marker, hard-close-i

## Concepts

[[docs/obsidian_deep/02_concepts/AI_Agent_Layer|AI Agent Layer]], [[docs/obsidian_deep/02_concepts/Execution____Risk|Execution / Risk]], [[docs/obsidian_deep/02_concepts/Intermarket_Divergence|Intermarket Divergence]], [[docs/obsidian_deep/02_concepts/MQL_Native|MQL Native]], [[docs/obsidian_deep/02_concepts/UI____React|UI / React]], [[docs/obsidian_deep/02_concepts/Validation____Audit|Validation / Audit]], [[docs/obsidian_deep/02_concepts/Zone____RTV|Zone / RTV]]

## Entities

—

## Headings

- Level 21 — Drawing Audit Hardening + HardClose Warning Fix
  - Chart symbol rule
  - Visual replay state
  - HardClose warning fix
  - Acceptance checklist

## Related Source Documents

- [[docs/evidence/level_13_visualization_audit_drawing/b5b7350fdc84_34_level_13_visualization_audit_drawing|34_level_13_visualization_audit_drawing.md]] — score `15`
- [[docs/execution/EXP0016_intermarket_divergence_execution/LEVEL_13_STC_SMT_VISUALIZATION_AUDIT_DRAWING|LEVEL_13_STC_SMT_VISUALIZATION_AUDIT_DRAWING.md]] — score `14`
- [[docs/evidence/11_algorithm_layers/07355f60fef2_11_algorithm_layers|11_algorithm_layers.md]] — score `13`
- [[docs/evidence/15_visualization_contract/0ccec648c2ec_15_visualization_contract|15_visualization_contract.md]] — score `13`
- [[docs/evidence/exec001_stc_smt_cycles_build_sequence/f494e5d7db74_19_patch_build_sequence|19_patch_build_sequence.md]] — score `13`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/21_first_patch_scope|21_first_patch_scope.md]] — score `13`
- [[docs/evidence/exec001_stc_smt_cycles_implementation_plan/0d054880f96a_17_implementation_plan|17_implementation_plan.md]] — score `13`
- [[docs/evidence/exec001_stc_smt_cycles_module_breakdown/0e4565d59512_18_module_breakdown|18_module_breakdown.md]] — score `13`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/41_level_20_operator_manual_deployment_profiles|41_level_20_operator_manual_deployment_profiles.md]] — score `13`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/README|README.md]] — score `13`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
