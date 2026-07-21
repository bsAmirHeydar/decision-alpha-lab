---
title: "EXEC001 STC SMT Cycles — Implementation Plan"
type: document_card
generated_by: alpha_lab_obsidian_builder
generated_at: 2026-07-06
source_path: "docs/evidence/exec001_stc_smt_cycles_implementation_plan/0d054880f96a_17_implementation_plan.md"
source_ext: ".md"
category: "experiment"
source_size_bytes: "18102"
entities:
  - "EXEC001"
concepts:
  - "Convexity"
  - "Execution"
  - "Intermarket Divergence"
  - "Known-Time Causality"
  - "MQL Native"
  - "NDS Anatomy"
  - "Structural Nodes"
  - "Validation"
---


# EXEC001 STC SMT Cycles — Implementation Plan

**Source:** [[docs/evidence/exec001_stc_smt_cycles_implementation_plan/0d054880f96a_17_implementation_plan|docs/evidence/exec001_stc_smt_cycles_implementation_plan/0d054880f96a_17_implementation_plan.md]]

**Category:** `experiment`  
**Status:** ok  
**Size:** `18102` bytes

## خلاصه

This document defines the staged implementation plan for `EXEC001_STC_SMT_Cycles`. The goal is not to build one large monolithic Expert Advisor. The strategy must be implemented as a layered execution system where each layer can be tested, audited, and replaced independently. This plan is based on the locked strategy specification, owner decisions, and the original STC Expert Advisor SRS. The implementation must be deterministic, modular, and auditable. The EA must not depend on the chart symbol or chart timeframe. It must operate only on `Symbol1` and `Symbol2`. All strategy decisions must be based only on the current STC trading day. A hard daily reset and hard close must occur at 15:30 Ne

## Headings

- EXEC001 STC SMT Cycles — Implementation Plan
-   1. Implementation Philosophy
-   2. Main Phases
-     Phase 0 — Documentation and Contracts
-     Phase 1 — MQL5 Project Skeleton and Core Types
-     Phase 2 — Time Engine and STC Trading Day Engine
-     Phase 3 — Data Access and Check Candle Aggregation
-     Phase 4 — W Level Builder and Cycle Audit
-     Phase 5 — Hunt and SMT Candidate Engine
-     Phase 6 — Confirmation, Ambiguity, and Signal Locking
-     Phase 7 — Reference Selector and Risk Model
-     Phase 8 — Research and Paper Trade Simulator

## Entities

`EXEC001`

## Concepts

- [[docs/obsidian/04_concepts/Convexity|Convexity]]
- [[docs/obsidian/04_concepts/Execution|Execution]]
- [[docs/obsidian/04_concepts/Intermarket_Divergence|Intermarket Divergence]]
- [[docs/obsidian/04_concepts/Known-Time_Causality|Known-Time Causality]]
- [[docs/obsidian/04_concepts/MQL_Native|MQL Native]]
- [[docs/evidence/nds_anatomy/6a11c75733b2_NDS_Anatomy|NDS Anatomy]]
- [[docs/obsidian/04_concepts/Structural_Nodes|Structural Nodes]]
- [[docs/obsidian/04_concepts/Validation|Validation]]

## Related documents

- [[docs/evidence/exec001_stc_smt_cycles_module_breakdown/0e4565d59512_18_module_breakdown|EXEC001 STC SMT Cycles — Module Breakdown]] — `experiment`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/README|EXEC001 STC SMT Cycles]] — `experiment`
- [[docs/evidence/exec001_stc_smt_cycles_build_sequence/f494e5d7db74_19_patch_build_sequence|EXEC001 STC SMT Cycles — Patch Build Sequence]] — `experiment`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/21_first_patch_scope|EXEC001 STC SMT Cycles — First Implementation Patch Scope]] — `experiment`
- [[docs/evidence/level_13_visualization_audit_drawing/b5b7350fdc84_34_level_13_visualization_audit_drawing|Level 13 — Visualization / Audit Drawing]] — `experiment`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/40_level_19_validation_pack|Level 19 — Validation Pack / Self-Test Reports]] — `experiment`
- [[docs/evidence/exec001_stc_smt_cycles_implementation_risk_register/b5f9b48975ee_20_implementation_risk_register|EXEC001 STC SMT Cycles — Implementation Risk Register]] — `experiment`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/22_level_01_skeleton|EXEC001 STC SMT Cycles — Level 01 Skeleton Implementation]] — `experiment`
- [[docs/execution/EXP0016_intermarket_divergence_execution/LEVEL_13_STC_SMT_VISUALIZATION_AUDIT_DRAWING|LEVEL 13 — EXEC001 STC SMT Visualization / Audit Drawing]] — `execution_docs`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/30_level_09_paper_outcome_simulator|Level 09 — Paper Outcome Simulator and Trade Journal]] — `experiment`
- [[docs/evidence/level_11_paper_hard_close_simulator_15_30_end_day_accounting/d27b26fac569_32_level_11_hard_close_simulator|Level 11 — Paper Hard-Close Simulator and 15:30 End-of-Day Accounting]] — `experiment`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/35_level_14_paper_live_alerts|Level 14 — Paper Live Alerts / No-Order Monitoring Layer]] — `experiment`

## Recommended Obsidian use

- این card را به نوت‌های concept، hypothesis، experiment یا ADR مربوط link کن.
- اگر این سند source of truth است، در MOC مربوطه بالاتر از اسناد legacy قرارش بده.
- اگر این سند report/validation است، نتیجه نهایی آن را به registry مربوط sync کن.
