---
title: "Phase 23 Compile Fix — Grouped Semicircle Visual Helper"
type: document_card
generated_by: alpha_lab_obsidian_builder
generated_at: 2026-07-06
source_path: "docs/nds_hook_architecture/33_phase23_grouped_semicircle_compile_fix.md"
source_ext: ".md"
category: "nds_hook_architecture_docs"
source_size_bytes: "719"
concepts:
  - "Hook"
  - "MQL Native"
  - "NDS Anatomy"
---


# Phase 23 Compile Fix — Grouped Semicircle Visual Helper

**Source:** [[docs/nds_hook_architecture/33_phase23_grouped_semicircle_compile_fix|docs/nds_hook_architecture/33_phase23_grouped_semicircle_compile_fix.md]]

**Category:** `nds_hook_architecture_docs`  
**Status:** ok  
**Size:** `719` bytes

## خلاصه

MetaEditor reported that `FP_HookP02CreateArcBetweenPoints` was undeclared and also rejected local reference variables such as: Adds the missing `FP_HookP02CreateArcBetweenPoints` helper before `FP_HookP02CreateCycleArc`. Replaces invalid local reference aliases with value copies: No visual semantics changed. The grouped Hook semicircle remains: one arc per Hook-origin group start at origin end at directional group extreme dim gray envelope arc

## Headings

- Phase 23 Compile Fix — Grouped Semicircle Visual Helper
-   Issue
-   Fix
-   Behavior

## Concepts

- [[docs/obsidian/04_concepts/Hook|Hook]]
- [[docs/obsidian/04_concepts/MQL_Native|MQL Native]]
- [[docs/obsidian/04_concepts/NDS_Anatomy|NDS Anatomy]]

## Related documents

- [[docs/architecture|System Architecture]] — `core_docs`
- [[lab/03_experiments/EXP0002_mql_native_m0001/report|EXP0002 — MQL-native M0001 Runtime]] — `experiment`
- [[lab/03_experiments/EXP0003_mql_native_m0002/report|EXP0003 — M0002 Reversal/Continuation Exit Volatility]] — `experiment`
- [[lab/03_experiments/EXP0004_mql_native_m0004/report|EXP0004 — MQL-native M0004 Branch Regime Clustering]] — `experiment`
- [[lab/05_validation/VAL_M0001_MQL_NATIVE/report|VAL_M0001_MQL_NATIVE]] — `validation`
- [[docs/ui/ARCHITECTURE|UI System Architecture]] — `ui_docs`
- [[docs/nds_hook_architecture/07_mql5_integration_contract|07 — MQL5 Integration Contract]] — `nds_hook_architecture_docs`
- [[docs/nds_hook_architecture/08_phase01_node_source_adapter_implementation|08 — Hook Phase 01 Implementation: Node Source Adapter]] — `nds_hook_architecture_docs`
- [[docs/nds_hook_architecture/09_phase02_cyclehook_sequence_builder_implementation|09 — Hook Phase 02 Implementation: CycleHook Object and X-Sequence Builder]] — `nds_hook_architecture_docs`
- [[docs/nds_hook_architecture/13_phase06_xy_closure_quality_score_implementation|13 — Hook Phase 06 Implementation: X/Y Closure Strength and Quality Score]] — `nds_hook_architecture_docs`
- [[docs/nds_hook_architecture/14_phase07_visual_profile_orchestrator_implementation|14 — NDS Hook Phase 07: Visual Profile Orchestrator]] — `nds_hook_architecture_docs`
- [[docs/nds_hook_architecture/15_phase08_audit_csv_reconciliation_implementation|15 — Hook Phase 08 Implementation: Audit + CSV Reconciliation]] — `nds_hook_architecture_docs`

## Recommended Obsidian use

- این card را به نوت‌های concept، hypothesis، experiment یا ADR مربوط link کن.
- اگر این سند source of truth است، در MOC مربوطه بالاتر از اسناد legacy قرارش بده.
- اگر این سند report/validation است، نتیجه نهایی آن را به registry مربوط sync کن.
