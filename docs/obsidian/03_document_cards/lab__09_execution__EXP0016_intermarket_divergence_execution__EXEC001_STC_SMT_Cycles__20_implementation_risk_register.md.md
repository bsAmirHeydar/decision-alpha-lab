---
title: "EXEC001 STC SMT Cycles — Implementation Risk Register"
type: document_card
generated_by: alpha_lab_obsidian_builder
generated_at: 2026-07-06
source_path: "docs/evidence/exec001_stc_smt_cycles_implementation_risk_register/b5f9b48975ee_20_implementation_risk_register.md"
source_ext: ".md"
category: "experiment"
source_size_bytes: "3692"
entities:
  - "EXEC001"
concepts:
  - "Execution"
  - "Intermarket Divergence"
  - "Known-Time Causality"
  - "MQL Native"
  - "Validation"
---


# EXEC001 STC SMT Cycles — Implementation Risk Register

**Source:** [[docs/evidence/exec001_stc_smt_cycles_implementation_risk_register/b5f9b48975ee_20_implementation_risk_register|docs/evidence/exec001_stc_smt_cycles_implementation_risk_register/b5f9b48975ee_20_implementation_risk_register.md]]

**Category:** `experiment`  
**Status:** ok  
**Size:** `3692` bytes

## خلاصه

This document lists the main engineering risks and how the implementation plan controls them. Wrong New York time or DST handling can shift M/W cycles and invalidate all signals. Time conversion is isolated in `DAL_STC_Time.mqh` and must be tested before signal logic exists. No SMT logic is allowed before the time gate passes. 3m and 10m candles may be aligned differently by broker data or chart timeframe. All check candles are internally aggregated from M1 and anchored from 20:00 New York. Check candle audit must show exact expected open/close times. The same divergence can be entered twice after restart or repeated check candles. Every candidate and signal has deterministic IDs and is pers

## Headings

- EXEC001 STC SMT Cycles — Implementation Risk Register
-   1. Time Conversion Risk
-     Risk
-     Control
-     Gate
-   2. Check Candle Anchoring Risk
-     Risk
-     Control
-     Gate
-   3. Duplicate Entry Risk
-     Risk
-     Control

## Entities

`EXEC001`

## Concepts

- [[docs/obsidian/04_concepts/Execution|Execution]]
- [[docs/obsidian/04_concepts/Intermarket_Divergence|Intermarket Divergence]]
- [[docs/obsidian/04_concepts/Known-Time_Causality|Known-Time Causality]]
- [[docs/obsidian/04_concepts/MQL_Native|MQL Native]]
- [[docs/obsidian/04_concepts/Validation|Validation]]

## Related documents

- [[docs/evidence/exec001_stc_smt_cycles_implementation_plan/0d054880f96a_17_implementation_plan|EXEC001 STC SMT Cycles — Implementation Plan]] — `experiment`
- [[docs/evidence/exec001_stc_smt_cycles_module_breakdown/0e4565d59512_18_module_breakdown|EXEC001 STC SMT Cycles — Module Breakdown]] — `experiment`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/21_first_patch_scope|EXEC001 STC SMT Cycles — First Implementation Patch Scope]] — `experiment`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/22_level_01_skeleton|EXEC001 STC SMT Cycles — Level 01 Skeleton Implementation]] — `experiment`
- [[docs/evidence/level_13_visualization_audit_drawing/b5b7350fdc84_34_level_13_visualization_audit_drawing|Level 13 — Visualization / Audit Drawing]] — `experiment`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/README|EXEC001 STC SMT Cycles]] — `experiment`
- [[docs/evidence/09_owner_decisions_pass_1/d64c20e06d5e_09_owner_decisions_pass_1|09 - Owner Decisions Pass 1]] — `experiment`
- [[docs/evidence/exec001_stc_smt_cycles_build_sequence/f494e5d7db74_19_patch_build_sequence|EXEC001 STC SMT Cycles — Patch Build Sequence]] — `experiment`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/30_level_09_paper_outcome_simulator|Level 09 — Paper Outcome Simulator and Trade Journal]] — `experiment`
- [[docs/evidence/level_11_paper_hard_close_simulator_15_30_end_day_accounting/d27b26fac569_32_level_11_hard_close_simulator|Level 11 — Paper Hard-Close Simulator and 15:30 End-of-Day Accounting]] — `experiment`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/35_level_14_paper_live_alerts|Level 14 — Paper Live Alerts / No-Order Monitoring Layer]] — `experiment`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/38_level_17_real_partial_close_manager|Level 17 — Real Partial Close Manager]] — `experiment`

## Recommended Obsidian use

- این card را به نوت‌های concept، hypothesis، experiment یا ADR مربوط link کن.
- اگر این سند source of truth است، در MOC مربوطه بالاتر از اسناد legacy قرارش بده.
- اگر این سند report/validation است، نتیجه نهایی آن را به registry مربوط sync کن.
