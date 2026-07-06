---
title: "Level 20 — Deployment Profile Matrix"
type: document_card
generated_by: alpha_lab_obsidian_builder
generated_at: 2026-07-06
source_path: "lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/42_level_20_profile_matrix.md"
source_ext: ".md"
category: "experiment"
source_size_bytes: "6809"
concepts:
  - "Convexity"
  - "Execution"
  - "Intermarket Divergence"
  - "NDS Anatomy"
  - "Validation"
---


# Level 20 — Deployment Profile Matrix

**Source:** [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/42_level_20_profile_matrix|lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/42_level_20_profile_matrix.md]]

**Category:** `experiment`  
**Status:** ok  
**Size:** `6809` bytes

## خلاصه

This document defines practical deployment profiles for `EXEC001_STC_SMT_Cycles`. The profile matrix is not a replacement for the EA inputs. It is an operator guide that says which groups of inputs should be enabled together and which combinations should be avoided. These should be reviewed in every profile: Intent: produce the fullest possible historical audit without touching broker positions. Expected settings: Runtime mode: Research Backtest. Real auto-entry: off. Broker position manager: off or audit-only off. Real partial: off. Real hard close finalizer: off. Alerts: no popup/push/sound for historical backfill. Drawing: optional. All CSV audits: on. Validation pack: on. Operator notes:

## Headings

- Level 20 — Deployment Profile Matrix
-   Purpose
-   Profile summary
-   Common inputs across all profiles
-   Profile 1 — Research Backtest Full Audit
-   Profile 2 — Paper Live Observer
-   Profile 3 — Paper Live Broker Audit
-   Profile 4 — Auto Trade Entry Only Rehearsal
-   Profile 5 — Auto Trade Full Managed
-   Profile 6 — Emergency Hard Close Only
-   Forbidden combinations
-   Minimum production checklist

## Concepts

- [[docs/obsidian/04_concepts/Convexity|Convexity]]
- [[docs/obsidian/04_concepts/Execution|Execution]]
- [[docs/obsidian/04_concepts/Intermarket_Divergence|Intermarket Divergence]]
- [[docs/obsidian/04_concepts/NDS_Anatomy|NDS Anatomy]]
- [[docs/obsidian/04_concepts/Validation|Validation]]

## Related documents

- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/17_implementation_plan|EXEC001 STC SMT Cycles — Implementation Plan]] — `experiment`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/19_patch_build_sequence|EXEC001 STC SMT Cycles — Patch Build Sequence]] — `experiment`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/21_first_patch_scope|EXEC001 STC SMT Cycles — First Implementation Patch Scope]] — `experiment`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/36_level_15_broker_position_manager|Level 15 — Broker Position Manager / Magic-Only Safety Layer]] — `experiment`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/39_level_18_real_hard_close_finalizer|Level 18 — Real Hard Close Finalizer]] — `experiment`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/40_level_19_validation_pack|Level 19 — Validation Pack / Self-Test Reports]] — `experiment`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/README|EXEC001 STC SMT Cycles]] — `experiment`
- [[lab/03_experiments/EXP0002_mql_native_m0001/report|EXP0002 — MQL-native M0001 Runtime]] — `experiment`
- [[lab/03_experiments/EXP0003_mql_native_m0002/report|EXP0003 — M0002 Reversal/Continuation Exit Volatility]] — `experiment`
- [[lab/03_experiments/EXP0004_mql_native_m0004/report|EXP0004 — MQL-native M0004 Branch Regime Clustering]] — `experiment`
- [[lab/05_validation/VAL_M0001_MQL_NATIVE/report|VAL_M0001_MQL_NATIVE]] — `validation`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/02_normalized_strategy_spec|02 - Normalized Strategy Specification]] — `experiment`

## Recommended Obsidian use

- این card را به نوت‌های concept، hypothesis، experiment یا ADR مربوط link کن.
- اگر این سند source of truth است، در MOC مربوطه بالاتر از اسناد legacy قرارش بده.
- اگر این سند report/validation است، نتیجه نهایی آن را به registry مربوط sync کن.
