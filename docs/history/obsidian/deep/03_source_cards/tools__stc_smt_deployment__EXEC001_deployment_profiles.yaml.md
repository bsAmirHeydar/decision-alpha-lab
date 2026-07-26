
---
type: source_card
source_path: "tools/stc_smt_deployment/EXEC001_deployment_profiles.yaml"
source_ext: ".yaml"
source_size: 2741
empty: false
generated_at: 2026-07-06
concepts: ["Convexity / Optionality", "Execution / Risk", "Intermarket Divergence", "MQL Native", "UI / React", "Validation / Audit"]
entities: []
---

# Source Card — EXEC001_deployment_profiles.yaml

## Source

[tools/stc_smt_deployment/EXEC001_deployment_profiles.yaml](../../tools/stc_smt_deployment/EXEC001_deployment_profiles.yaml)

## Summary

profiles: research_backtest_full_audit: runtime_mode: RESEARCH_BACKTEST real_auto_entry: false broker_position_manager: false real_partial_close: false real_hard_close_finalizer: false alerts_transport: false validation_pack: true drawing: optional purpose: "Historical audit and research only." paper_live_observer: runtime_mode: PAPER_LIVE real_auto_entry: false broker_position_manager: false real_partial_close: false real_hard_close_finalizer: false alerts_transport: true validation_pack: true drawing: true purpose: "Live signal monitoring without broker interaction." paper_live_broker_audit: runtime_mode: PAPER_LIVE real_auto_entry: false broker_position_manager: true real_partial_close: false real_hard_close_finalizer: false paper_live_real_action_overrides: false alerts_transport: true validation_pack: true drawing: true purpose: "Live signal monitoring plus broker position classific

## Concepts

[[docs/obsidian_deep/02_concepts/Convexity____Optionality|Convexity / Optionality]], [[docs/obsidian_deep/02_concepts/Execution____Risk|Execution / Risk]], [[docs/obsidian_deep/02_concepts/Intermarket_Divergence|Intermarket Divergence]], [[docs/obsidian_deep/02_concepts/MQL_Native|MQL Native]], [[docs/obsidian_deep/02_concepts/UI____React|UI / React]], [[docs/obsidian_deep/02_concepts/Validation____Audit|Validation / Audit]]

## Entities

—

## Headings

- EXEC001_STC_SMT_Cycles deployment profiles
- This file is a human-readable operator guide, not an MQL5 .set file.
- Use it to configure EA inputs deliberately in MetaTrader.

## Related Source Documents

- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/06_mql5_architecture_plan|06_mql5_architecture_plan.md]] — score `12`
- [[docs/evidence/exec001_stc_smt_cycles_implementation_plan/0d054880f96a_17_implementation_plan|17_implementation_plan.md]] — score `12`
- [[docs/evidence/exec001_stc_smt_cycles_module_breakdown/0e4565d59512_18_module_breakdown|18_module_breakdown.md]] — score `12`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/21_first_patch_scope|21_first_patch_scope.md]] — score `12`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/41_level_20_operator_manual_deployment_profiles|41_level_20_operator_manual_deployment_profiles.md]] — score `12`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/README|README.md]] — score `12`
- [[docs/ai_execution/AI_NATIVE_EXECUTION_ROADMAP_FA|AI_NATIVE_EXECUTION_ROADMAP_FA.md]] — score `10`
- [[docs/debug/E0006/README|README.md]] — score `10`
- [[docs/debug/E0006_ALL_ZONE_TOUCH_LIMIT_README|E0006_ALL_ZONE_TOUCH_LIMIT_README.md]] — score `10`
- [[docs/execution/H0005_R1_SIX_SLOT_TOUCH_LEDGER|H0005_R1_SIX_SLOT_TOUCH_LEDGER.md]] — score `10`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
