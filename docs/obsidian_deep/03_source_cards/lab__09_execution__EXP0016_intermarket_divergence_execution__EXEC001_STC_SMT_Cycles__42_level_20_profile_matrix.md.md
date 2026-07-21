
---
type: source_card
source_path: "docs/evidence/level_20_deployment_profile_matrix/97ecd654ebb6_42_level_20_profile_matrix.md"
source_ext: ".md"
source_size: 6809
empty: false
generated_at: 2026-07-06
concepts: ["Convexity / Optionality", "Execution / Risk", "Intermarket Divergence", "Python Brain", "UI / React", "Validation / Audit"]
entities: []
---

# Source Card — 42_level_20_profile_matrix.md

## Source

[[docs/evidence/level_20_deployment_profile_matrix/97ecd654ebb6_42_level_20_profile_matrix|docs/evidence/level_20_deployment_profile_matrix/97ecd654ebb6_42_level_20_profile_matrix.md]]

## Summary

This document defines practical deployment profiles for `EXEC001_STC_SMT_Cycles`. The profile matrix is not a replacement for the EA inputs. It is an operator guide that says which groups of inputs should be enabled together and which combinations should be avoided. These should be reviewed in every profile: Intent: produce the fullest possible historical audit without touching broker positions. Expected settings: Runtime mode: Research Backtest. Real auto-entry: off. Broker position manager: off or audit-only off. Real partial: off. Real hard close finalizer: off. Alerts: no popup/push/sound for historical backfill. Drawing: optional. All CSV audits: on. Validation pack: on. Operator notes: Use this before every code change is trusted. The output is the main evidence for strategy correctness. Historical backfill may produce many rows, so alerts should not fire for every historical row.

## Concepts

[[docs/obsidian_deep/02_concepts/Convexity____Optionality|Convexity / Optionality]], [[docs/obsidian_deep/02_concepts/Execution____Risk|Execution / Risk]], [[docs/obsidian_deep/02_concepts/Intermarket_Divergence|Intermarket Divergence]], [[docs/obsidian_deep/02_concepts/Python_Brain|Python Brain]], [[docs/obsidian_deep/02_concepts/UI____React|UI / React]], [[docs/obsidian_deep/02_concepts/Validation____Audit|Validation / Audit]]

## Entities

—

## Headings

- Level 20 — Deployment Profile Matrix
  - Purpose
  - Profile summary
  - Common inputs across all profiles
  - Profile 1 — Research Backtest Full Audit
  - Profile 2 — Paper Live Observer
  - Profile 3 — Paper Live Broker Audit
  - Profile 4 — Auto Trade Entry Only Rehearsal
  - Profile 5 — Auto Trade Full Managed
  - Profile 6 — Emergency Hard Close Only
  - Forbidden combinations
  - Minimum production checklist

## Related Source Documents

- [[lab/03_experiments/EXP0004_mql_native_m0004/report|report.md]] — score `14`
- [signals.yaml](../../registry/signals.yaml) — score `14`
- [[docs/evidence/val_m0001_mql_native/454e81f9f0b3_report|report.md]] — score `14`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/06_mql5_architecture_plan|06_mql5_architecture_plan.md]] — score `13`
- [[docs/evidence/exec001_stc_smt_cycles_implementation_plan/0d054880f96a_17_implementation_plan|17_implementation_plan.md]] — score `13`
- [[docs/evidence/exec001_stc_smt_cycles_module_breakdown/0e4565d59512_18_module_breakdown|18_module_breakdown.md]] — score `13`
- [[docs/evidence/exec001_stc_smt_cycles_build_sequence/f494e5d7db74_19_patch_build_sequence|19_patch_build_sequence.md]] — score `13`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/21_first_patch_scope|21_first_patch_scope.md]] — score `13`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/26_level_05_reference_matrix_hunt_detector|26_level_05_reference_matrix_hunt_detector.md]] — score `13`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/39_level_18_real_hard_close_finalizer|39_level_18_real_hard_close_finalizer.md]] — score `13`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
