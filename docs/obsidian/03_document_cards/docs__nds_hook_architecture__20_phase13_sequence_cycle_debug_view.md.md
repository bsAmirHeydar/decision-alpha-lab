---
title: "Phase 13 — Sequence + Cycle Arc Debug View"
type: document_card
generated_by: alpha_lab_obsidian_builder
generated_at: 2026-07-06
source_path: "docs/nds_hook_architecture/20_phase13_sequence_cycle_debug_view.md"
source_ext: ".md"
category: "nds_hook_architecture_docs"
source_size_bytes: "2361"
concepts:
  - "AI Agent Layer"
  - "Hook"
  - "MQL Native"
  - "NDS Anatomy"
---


# Phase 13 — Sequence + Cycle Arc Debug View

**Source:** [[docs/nds_hook_architecture/20_phase13_sequence_cycle_debug_view|docs/nds_hook_architecture/20_phase13_sequence_cycle_debug_view.md]]

**Category:** `nds_hook_architecture_docs`  
**Status:** ok  
**Size:** `2361` bytes

## خلاصه

این فاز برای وقتی است که خروجی رسمی Hook هنوز از نظر بصری شلوغ است و باید دقیقاً دیده شود که موتور Hook چطور sequence را می‌شمارد. تمرکز این فاز روی این‌هاست: Origin هر CycleHook X1 / X2 / X3 / X4 خط اتصال Xها شماره sequence تعداد Xهای همان sequence نیم‌دایره‌ی Cycle روی بازه‌ی همان sequence این فاز عمداً P05/P06 quality/type labelها، thresholdها، projectionها، و labelهای debug سنگین را خاموش می‌کند. این پروفایل فقط Phase 02 را به‌عنوان سطح اصلی نمایش فعال می‌کند: `draw_origin = true` `draw_x_nodes = true` `draw_x_lines = true` `draw_cycle_arc = true` `draw_sequence_count_label = true` و این‌ها را خاموش می‌کند: Phase 03 Y overlays Phase 04 threshold / ND / death overlays Phase 05 type labels

## Headings

- Phase 13 — Sequence + Cycle Arc Debug View
-   هدف
-   View Profile جدید
-   Inputهای جدید Phase 02
-   منطق نیم‌دایره
-   Recommended inputs

## Concepts

- [[docs/obsidian/04_concepts/AI_Agent_Layer|AI Agent Layer]]
- [[docs/obsidian/04_concepts/Hook|Hook]]
- [[docs/obsidian/04_concepts/MQL_Native|MQL Native]]
- [[docs/evidence/nds_anatomy/6a11c75733b2_NDS_Anatomy|NDS Anatomy]]

## Related documents

- [[docs/architecture|System Architecture]] — `core_docs`
- [[docs/nds_hook_architecture/08_phase01_node_source_adapter_implementation|08 — Hook Phase 01 Implementation: Node Source Adapter]] — `nds_hook_architecture_docs`
- [[docs/nds_hook_architecture/09_phase02_cyclehook_sequence_builder_implementation|09 — Hook Phase 02 Implementation: CycleHook Object and X-Sequence Builder]] — `nds_hook_architecture_docs`
- [[docs/nds_hook_architecture/13_phase06_xy_closure_quality_score_implementation|13 — Hook Phase 06 Implementation: X/Y Closure Strength and Quality Score]] — `nds_hook_architecture_docs`
- [[docs/nds_hook_architecture/14_phase07_visual_profile_orchestrator_implementation|14 — NDS Hook Phase 07: Visual Profile Orchestrator]] — `nds_hook_architecture_docs`
- [[docs/nds_hook_architecture/15_phase08_audit_csv_reconciliation_implementation|15 — Hook Phase 08 Implementation: Audit + CSV Reconciliation]] — `nds_hook_architecture_docs`
- [[docs/nds_hook_architecture/37_phase26_doc_aligned_hook_rebuild|Phase 26 — Doc-Aligned Hook / ND Branch Rebuild]] — `nds_hook_architecture_docs`
- [[docs/ui/ARCHITECTURE|UI System Architecture]] — `ui_docs`
- [[docs/nds_hook_architecture/01_scope_and_inputs|01 — Scope and Inputs]] — `nds_hook_architecture_docs`
- [[docs/nds_hook_architecture/04_x_y_closure_and_hook_types|04 — X/Y Closure and Hook Types]] — `nds_hook_architecture_docs`
- [[docs/nds_hook_architecture/05_visualization_and_diagnostics|05 — Visualization and Diagnostics]] — `nds_hook_architecture_docs`
- [[docs/nds_hook_architecture/06_build_phases|06 — Build Phases]] — `nds_hook_architecture_docs`

## Recommended Obsidian use

- این card را به نوت‌های concept، hypothesis، experiment یا ADR مربوط link کن.
- اگر این سند source of truth است، در MOC مربوطه بالاتر از اسناد legacy قرارش بده.
- اگر این سند report/validation است، نتیجه نهایی آن را به registry مربوط sync کن.
