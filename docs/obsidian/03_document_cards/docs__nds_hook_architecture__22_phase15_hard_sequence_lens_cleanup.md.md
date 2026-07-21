---
title: "Phase 15 — Hard Sequence Lens Cleanup"
type: document_card
generated_by: alpha_lab_obsidian_builder
generated_at: 2026-07-06
source_path: "docs/nds_hook_architecture/22_phase15_hard_sequence_lens_cleanup.md"
source_ext: ".md"
category: "nds_hook_architecture_docs"
source_size_bytes: "2203"
concepts:
  - "AI Agent Layer"
  - "Hook"
  - "NDS Anatomy"
  - "Rally"
---


# Phase 15 — Hard Sequence Lens Cleanup

**Source:** [[docs/nds_hook_architecture/22_phase15_hard_sequence_lens_cleanup|docs/nds_hook_architecture/22_phase15_hard_sequence_lens_cleanup.md]]

**Category:** `nds_hook_architecture_docs`  
**Status:** ok  
**Size:** `2203` bytes

## خلاصه

بعد از اضافه شدن نیم‌دایره‌ی Cycle و حالت promoted origin، هنوز ممکن بود روی چارت آبجکت‌های قدیمی P05/P06 یا رندر اصلی Rally باقی بمانند. دلیل عملی این بود که MT5 مقدار inputهای قبلی را روی instance چارت نگه می‌دارد و بعضی overlayها قبل از reset کامل دوباره روی چارت دیده می‌شدند. این فاز حالت `SEQUENCE_CYCLE_DEBUG` را از یک view معمولی به یک hard inspector lens تبدیل می‌کند. Phase 01 فقط برای ساخت داده‌ی نود استفاده می‌شود و چیزی رسم نمی‌کند. Phase 02 تنها لایه‌ی قابل نمایش است. Phase 03، Phase 04، Phase 05 و Phase 06 از نظر runtime disabled می‌شوند، نه فقط draw=false. تعداد sequence قابل رسم به‌صورت hard cap روی 1 قرار می‌گیرد. P03/P04/P05/P06 نمی‌توانند label یا marker جدید تولید کنند. قبل

## Headings

- Phase 15 — Hard Sequence Lens Cleanup
-   هدف
-   رفتار جدید در `FP_HOOK_P07_VIEW_SEQUENCE_CYCLE_DEBUG`
-   نتیجه
-   Recommended inputs

## Concepts

- [[docs/obsidian/04_concepts/AI_Agent_Layer|AI Agent Layer]]
- [[docs/obsidian/04_concepts/Hook|Hook]]
- [[docs/evidence/nds_anatomy/6a11c75733b2_NDS_Anatomy|NDS Anatomy]]
- [[docs/obsidian/04_concepts/Rally|Rally]]

## Related documents

- [[docs/architecture|System Architecture]] — `core_docs`
- [[docs/nds_hook_architecture/01_scope_and_inputs|01 — Scope and Inputs]] — `nds_hook_architecture_docs`
- [[docs/nds_hook_architecture/06_build_phases|06 — Build Phases]] — `nds_hook_architecture_docs`
- [[docs/nds_hook_architecture/08_phase01_node_source_adapter_implementation|08 — Hook Phase 01 Implementation: Node Source Adapter]] — `nds_hook_architecture_docs`
- [[docs/nds_hook_architecture/09_phase02_cyclehook_sequence_builder_implementation|09 — Hook Phase 02 Implementation: CycleHook Object and X-Sequence Builder]] — `nds_hook_architecture_docs`
- [[docs/nds_hook_architecture/13_phase06_xy_closure_quality_score_implementation|13 — Hook Phase 06 Implementation: X/Y Closure Strength and Quality Score]] — `nds_hook_architecture_docs`
- [[docs/nds_hook_architecture/14_phase07_visual_profile_orchestrator_implementation|14 — NDS Hook Phase 07: Visual Profile Orchestrator]] — `nds_hook_architecture_docs`
- [[docs/nds_hook_architecture/15_phase08_audit_csv_reconciliation_implementation|15 — Hook Phase 08 Implementation: Audit + CSV Reconciliation]] — `nds_hook_architecture_docs`
- [[docs/nds_hook_architecture/18_phase11_official_schematic_visual_cleanup|NDS Hook Official Schematic Visual Cleanup]] — `nds_hook_architecture_docs`
- [[docs/nds_hook_architecture/42_phase30_responsive_label_stack_spacing|Phase 30 — Responsive Label Stack Spacing]] — `nds_hook_architecture_docs`
- [[docs/ui/ARCHITECTURE|UI System Architecture]] — `ui_docs`
- [[docs/nds_hook_architecture/02_cyclehook_object_model|02 — CycleHook Object Model]] — `nds_hook_architecture_docs`

## Recommended Obsidian use

- این card را به نوت‌های concept، hypothesis، experiment یا ADR مربوط link کن.
- اگر این سند source of truth است، در MOC مربوطه بالاتر از اسناد legacy قرارش بده.
- اگر این سند report/validation است، نتیجه نهایی آن را به registry مربوط sync کن.
