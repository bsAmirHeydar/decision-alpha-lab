
---
type: source_card
source_path: "docs/evidence/level_07_confirmation_signal_registry/c5f8b7b0b328_28_level_07_confirmation_signal_registry.md"
source_ext: ".md"
source_size: 4693
empty: false
generated_at: 2026-07-06
concepts: ["Execution / Risk", "Intermarket Divergence", "MQL Native", "Python Brain", "Validation / Audit"]
entities: []
---

# Source Card — 28_level_07_confirmation_signal_registry.md

## Source

[[docs/evidence/level_07_confirmation_signal_registry/c5f8b7b0b328_28_level_07_confirmation_signal_registry|docs/evidence/level_07_confirmation_signal_registry/c5f8b7b0b328_28_level_07_confirmation_signal_registry.md]]

## Summary

Level 07 converts the audit-only SMT candidates from Level 06 into an audit-only signal registry. It still does not place paper trades and it still does not send real orders. This level is the first layer where the strategy speaks in terms of a confirmed STC signal rather than a raw hunt or a raw SMT candidate. The locked owner rule is that the signal only exists at the close of a valid check candle. If the expert was offline at that exact entry moment, the system must never enter later because the stop quality is no longer the… `InpWriteSignalRegistryAudit` `InpMaxSignalBackfillOnInit` `InpMaxSignalCatchupPerPulse` These inputs control the signal registry audit output. They do not enable trading. `mql5/Include/IntermarketDivergenceExecution/STC/DAL_STC_Signals.mqh` The module depends on the Level 06 candidate engine and registers closed-check signal rows. Common Files path: `dal/stc/EXE

## Concepts

[[docs/obsidian_deep/02_concepts/Execution____Risk|Execution / Risk]], [[docs/obsidian_deep/02_concepts/Intermarket_Divergence|Intermarket Divergence]], [[docs/obsidian_deep/02_concepts/MQL_Native|MQL Native]], [[docs/obsidian_deep/02_concepts/Python_Brain|Python Brain]], [[docs/obsidian_deep/02_concepts/Validation____Audit|Validation / Audit]]

## Entities

—

## Headings

- Level 07 — Confirmation and Signal Registry
  - Purpose
  - Inputs Added
  - New MQL5 Module
  - New Output File
  - Signal Registry Rules
  - Confirmation Meaning
  - Entry OFF Rule
  - Offline / Late Entry Rule
  - Simultaneous Buy and Sell Rule
  - Final Check Candle Rule
  - Signal Consumption

## Related Source Documents

- [signals.yaml](../../registry/signals.yaml) — score `12`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/06_mql5_architecture_plan|06_mql5_architecture_plan.md]] — score `11`
- [[docs/evidence/exec001_stc_smt_cycles_implementation_plan/0d054880f96a_17_implementation_plan|17_implementation_plan.md]] — score `11`
- [[docs/evidence/exec001_stc_smt_cycles_module_breakdown/0e4565d59512_18_module_breakdown|18_module_breakdown.md]] — score `11`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/21_first_patch_scope|21_first_patch_scope.md]] — score `11`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/22_level_01_skeleton|22_level_01_skeleton.md]] — score `11`
- [[docs/evidence/level_12_persistence_restart_recovery/965c940d2cdd_33_level_12_persistence_restart_recovery|33_level_12_persistence_restart_recovery.md]] — score `11`
- [[docs/evidence/level_13_visualization_audit_drawing/b5b7350fdc84_34_level_13_visualization_audit_drawing|34_level_13_visualization_audit_drawing.md]] — score `11`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/35_level_14_paper_live_alerts|35_level_14_paper_live_alerts.md]] — score `11`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/41_level_20_operator_manual_deployment_profiles|41_level_20_operator_manual_deployment_profiles.md]] — score `11`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
