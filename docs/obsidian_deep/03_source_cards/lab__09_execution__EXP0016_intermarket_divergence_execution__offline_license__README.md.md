
---
type: source_card
source_path: "lab/09_execution/EXP0016_intermarket_divergence_execution/offline_license/README.md"
source_ext: ".md"
source_size: 1497
empty: false
generated_at: 2026-07-06
concepts: ["Execution / Risk", "Intermarket Divergence", "Licensing", "MQL Native", "Python Brain", "Validation / Audit"]
entities: ["EXEC001", "EXP0015"]
---

# Source Card — README.md

## Source

[[lab/09_execution/EXP0016_intermarket_divergence_execution/offline_license/README|lab/09_execution/EXP0016_intermarket_divergence_execution/offline_license/README.md]]

## Summary

This patch ports the FlagCounting Phoenix offline-license architecture to the divergence / time-cycle execution project. The license is intentionally exposed as neutral strategy/profile fields: By default, the issuer archive is written under: The recipient only receives the `*_recipient_inputs.txt` values. The `*_issuer_audit.json` and `*_full_record.txt` files stay private. `IMDEXEC001_STC_SMT_Cycles.mq5` checks the license before `g_stc_engine.Init()` and before every timer pulse. The two EXP0015 research wrappers check the same license before batch/live-monitor execution. If the license is absent, expired, copied to another account/server, or has wrong gates/signature, init fails or the timer pulse returns without running the engine.

## Concepts

[[docs/obsidian_deep/02_concepts/Execution____Risk|Execution / Risk]], [[docs/obsidian_deep/02_concepts/Intermarket_Divergence|Intermarket Divergence]], [[docs/obsidian_deep/02_concepts/Licensing|Licensing]], [[docs/obsidian_deep/02_concepts/MQL_Native|MQL Native]], [[docs/obsidian_deep/02_concepts/Python_Brain|Python Brain]], [[docs/obsidian_deep/02_concepts/Validation____Audit|Validation / Audit]]

## Entities

EXEC001, EXP0015

## Headings

- Offline License Layer - EXEC001 STC SMT Cycles
  - MT5 recipient inputs
  - Issuer command
  - Saved files
  - Runtime behavior

## Related Source Documents

- [[docs/architecture|architecture.md]] — score `16`
- [[docs/execution/EXP0016_intermarket_divergence_execution/LEVEL_11_STC_SMT_HARD_CLOSE_SIMULATOR|LEVEL_11_STC_SMT_HARD_CLOSE_SIMULATOR.md]] — score `15`
- [[docs/execution/EXP0016_intermarket_divergence_execution/LEVEL_13_STC_SMT_VISUALIZATION_AUDIT_DRAWING|LEVEL_13_STC_SMT_VISUALIZATION_AUDIT_DRAWING.md]] — score `15`
- [[docs/execution/EXP0016_intermarket_divergence_execution/LEVEL_18_STC_SMT_REAL_HARD_CLOSE_FINALIZER|LEVEL_18_STC_SMT_REAL_HARD_CLOSE_FINALIZER.md]] — score `15`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/17_implementation_plan|17_implementation_plan.md]] — score `15`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/18_module_breakdown|18_module_breakdown.md]] — score `15`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/21_first_patch_scope|21_first_patch_scope.md]] — score `15`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/22_level_01_skeleton|22_level_01_skeleton.md]] — score `15`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/34_level_13_visualization_audit_drawing|34_level_13_visualization_audit_drawing.md]] — score `15`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/35_level_14_paper_live_alerts|35_level_14_paper_live_alerts.md]] — score `15`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
