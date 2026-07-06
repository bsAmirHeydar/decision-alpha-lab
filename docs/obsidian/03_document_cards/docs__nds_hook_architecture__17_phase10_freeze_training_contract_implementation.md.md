---
title: "Phase 10 — Hook v1 Freeze + Training Contract"
type: document_card
generated_by: alpha_lab_obsidian_builder
generated_at: 2026-07-06
source_path: "docs/nds_hook_architecture/17_phase10_freeze_training_contract_implementation.md"
source_ext: ".md"
category: "nds_hook_architecture_docs"
source_size_bytes: "6226"
concepts:
  - "Convexity"
  - "Execution"
  - "F-Counting"
  - "Hook"
  - "MQL Native"
  - "NDS Anatomy"
  - "Rally"
  - "Validation"
---


# Phase 10 — Hook v1 Freeze + Training Contract

**Source:** [[docs/nds_hook_architecture/17_phase10_freeze_training_contract_implementation|docs/nds_hook_architecture/17_phase10_freeze_training_contract_implementation.md]]

**Category:** `nds_hook_architecture_docs`  
**Status:** ok  
**Size:** `6226` bytes

## خلاصه

Phase 10 is the final modular Hook phase for the current NDS architecture pass. It does **not** create a new Hook signal. It freezes the runtime contract that makes Hook output safe to use as downstream training input. The rule is: This phase is a gate, not a strategy. The central expert now exposes the display-family selector as the **first visible input**: Available values: Expected behavior: The default remains `RALLY_ONLY` to preserve old behavior. Documentation overlay: `FP_HookPhase10Visual.mqh` intentionally does not draw Hook structure. Reason: All Phase 10 artifacts are CSV/log contracts. Use when inspecting the contract without asserting readiness. Default. Runs the contract checks

## Headings

- Phase 10 — Hook v1 Freeze + Training Contract
-   Purpose
-   First input requirement
-   Added files
-   Phase 10 is no-draw
-   Freeze modes
-     OBSERVE_ONLY
-     V1_CANDIDATE
-     TRAINING_READY
-     STRICT_LOCK
-   Main inputs
-   Contract checks

## Concepts

- [[docs/obsidian/04_concepts/Convexity|Convexity]]
- [[docs/obsidian/04_concepts/Execution|Execution]]
- [[docs/obsidian/04_concepts/F-Counting|F-Counting]]
- [[docs/obsidian/04_concepts/Hook|Hook]]
- [[docs/obsidian/04_concepts/MQL_Native|MQL Native]]
- [[docs/obsidian/04_concepts/NDS_Anatomy|NDS Anatomy]]
- [[docs/obsidian/04_concepts/Rally|Rally]]
- [[docs/obsidian/04_concepts/Validation|Validation]]

## Related documents

- [[docs/nds_hook_architecture/07_mql5_integration_contract|07 — MQL5 Integration Contract]] — `nds_hook_architecture_docs`
- [[docs/nds_hook_architecture/15_phase08_audit_csv_reconciliation_implementation|15 — Hook Phase 08 Implementation: Audit + CSV Reconciliation]] — `nds_hook_architecture_docs`
- [[docs/nds_hook_architecture/16_phase09_visual_smoke_test_harness_implementation|Phase 09 — Visual Smoke Test Harness Implementation]] — `nds_hook_architecture_docs`
- [[docs/nds_hook_architecture/06_build_phases|06 — Build Phases]] — `nds_hook_architecture_docs`
- [[docs/nds_hook_architecture/08_phase01_node_source_adapter_implementation|08 — Hook Phase 01 Implementation: Node Source Adapter]] — `nds_hook_architecture_docs`
- [[docs/nds_hook_architecture/09_phase02_cyclehook_sequence_builder_implementation|09 — Hook Phase 02 Implementation: CycleHook Object and X-Sequence Builder]] — `nds_hook_architecture_docs`
- [[docs/nds_hook_architecture/13_phase06_xy_closure_quality_score_implementation|13 — Hook Phase 06 Implementation: X/Y Closure Strength and Quality Score]] — `nds_hook_architecture_docs`
- [[docs/nds_hook_architecture/14_phase07_visual_profile_orchestrator_implementation|14 — NDS Hook Phase 07: Visual Profile Orchestrator]] — `nds_hook_architecture_docs`
- [[docs/nds_hook_architecture/README|NDS Hook Architecture — Design Pack]] — `nds_hook_architecture_docs`
- [[docs/ai_execution/AI_NATIVE_EXECUTION_ROADMAP_FA|AI Native Execution Roadmap — نقشه راه هوش مصنوعی، بک‌تست و پل اگزکیوت]] — `ai_execution_docs`
- [[docs/experience_capture/answers/DST-R03/answer_normalized_en|DST-R03 — Normalized Interpretation]] — `experience_capture_docs`
- [[docs/experience_capture/answers/NDS-R01/answer_normalized_en|NDS-R01 — Normalized Interpretation]] — `experience_capture_docs`

## Recommended Obsidian use

- این card را به نوت‌های concept، hypothesis، experiment یا ADR مربوط link کن.
- اگر این سند source of truth است، در MOC مربوطه بالاتر از اسناد legacy قرارش بده.
- اگر این سند report/validation است، نتیجه نهایی آن را به registry مربوط sync کن.
