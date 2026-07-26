---
title: "Phase 30 — Responsive Label Stack Spacing"
type: document_card
generated_by: alpha_lab_obsidian_builder
generated_at: 2026-07-06
source_path: "docs/nds_hook_architecture/42_phase30_responsive_label_stack_spacing.md"
source_ext: ".md"
category: "nds_hook_architecture_docs"
source_size_bytes: "1487"
concepts:
  - "AI Agent Layer"
  - "Hook"
  - "NDS Anatomy"
  - "Rally"
  - "Structural Nodes"
---


# Phase 30 — Responsive Label Stack Spacing

**Source:** [[docs/nds_hook_architecture/42_phase30_responsive_label_stack_spacing|docs/nds_hook_architecture/42_phase30_responsive_label_stack_spacing.md]]

**Category:** `nds_hook_architecture_docs`  
**Status:** ok  
**Size:** `1487` bytes

## خلاصه

Fixed label offsets and fixed stack-step distances become visually wrong across timeframes: on smaller timeframes they can be too wide; on larger timeframes they can be too tight; crowded Hook zones need spacing that adapts to the local candle scale. Make Hook/branch label stacking responsive instead of relying on one dry absolute number. The label renderer now estimates the average candle range around the anchor node using a configurable local lookback window. From that local range it derives: base offset distance from the node; per-stack vertical step distance. Responsive values are clamped between configurable minima and maxima so spacing does not become absurdly tiny or huge. The existin

## Headings

- Phase 30 — Responsive Label Stack Spacing
-   Problem
-   Goal
-   What changed
-     1) Dynamic spacing from local candle range
-     2) Clamp bounds
-     3) Manual values remain floors
-   New config knobs
-   Result

## Concepts

- [[docs/obsidian/04_concepts/AI_Agent_Layer|AI Agent Layer]]
- [[docs/obsidian/04_concepts/Hook|Hook]]
- [[docs/evidence/nds_anatomy/6a11c75733b2_NDS_Anatomy|NDS Anatomy]]
- [[docs/obsidian/04_concepts/Rally|Rally]]
- [[docs/obsidian/04_concepts/Structural_Nodes|Structural Nodes]]

## Related documents

- [[docs/architecture|System Architecture]] — `core_docs`
- [[docs/nds_hook_architecture/06_build_phases|06 — Build Phases]] — `nds_hook_architecture_docs`
- [[docs/nds_hook_architecture/13_phase06_xy_closure_quality_score_implementation|13 — Hook Phase 06 Implementation: X/Y Closure Strength and Quality Score]] — `nds_hook_architecture_docs`
- [[docs/ui/ARCHITECTURE|UI System Architecture]] — `ui_docs`
- [[docs/nds_hook_architecture/01_scope_and_inputs|01 — Scope and Inputs]] — `nds_hook_architecture_docs`
- [[docs/nds_hook_architecture/04_x_y_closure_and_hook_types|04 — X/Y Closure and Hook Types]] — `nds_hook_architecture_docs`
- [[docs/nds_hook_architecture/05_visualization_and_diagnostics|05 — Visualization and Diagnostics]] — `nds_hook_architecture_docs`
- [[docs/nds_hook_architecture/08_phase01_node_source_adapter_implementation|08 — Hook Phase 01 Implementation: Node Source Adapter]] — `nds_hook_architecture_docs`
- [[docs/nds_hook_architecture/09_phase02_cyclehook_sequence_builder_implementation|09 — Hook Phase 02 Implementation: CycleHook Object and X-Sequence Builder]] — `nds_hook_architecture_docs`
- [[docs/nds_hook_architecture/12_phase05_hook_type_abc_classifier_implementation|12 — Hook Phase 05 Implementation: Hook Type A/B/C Classifier]] — `nds_hook_architecture_docs`
- [[docs/nds_hook_architecture/14_phase07_visual_profile_orchestrator_implementation|14 — NDS Hook Phase 07: Visual Profile Orchestrator]] — `nds_hook_architecture_docs`
- [[docs/nds_hook_architecture/15_phase08_audit_csv_reconciliation_implementation|15 — Hook Phase 08 Implementation: Audit + CSV Reconciliation]] — `nds_hook_architecture_docs`

## Recommended Obsidian use

- این card را به نوت‌های concept، hypothesis، experiment یا ADR مربوط link کن.
- اگر این سند source of truth است، در MOC مربوطه بالاتر از اسناد legacy قرارش بده.
- اگر این سند report/validation است، نتیجه نهایی آن را به registry مربوط sync کن.
