---
title: "Phase 14 — Hook Origin Policy / Promoted Origin Mode"
type: document_card
generated_by: alpha_lab_obsidian_builder
generated_at: 2026-07-06
source_path: "docs/nds_hook_architecture/21_phase14_origin_policy_promoted_mode.md"
source_ext: ".md"
category: "nds_hook_architecture_docs"
source_size_bytes: "2235"
concepts:
  - "Hook"
  - "NDS Anatomy"
---


# Phase 14 — Hook Origin Policy / Promoted Origin Mode

**Source:** [[docs/nds_hook_architecture/21_phase14_origin_policy_promoted_mode|docs/nds_hook_architecture/21_phase14_origin_policy_promoted_mode.md]]

**Category:** `nds_hook_architecture_docs`  
**Status:** ok  
**Size:** `2235` bytes

## خلاصه

قبل از Inspector، منطق مبدا Hook باید دوحالته شود. مشکل قبلی این بود که در حالت fixed هر نود هم‌جهت، مخصوصاً در scaleهای کوچک مثل L2، می‌توانست origin مستقل شود و تعداد Hookهای هم‌پوشان زیاد می‌شد. حالت‌ها: همان رفتار قبلی است: هر نود واجد شرایط می‌تواند origin شود. origin تا انتهای sequence ثابت می‌ماند. برای debug کامل همه candidateها مفید است. روی چارت بسیار شلوغ می‌شود. این حالت برای خواندن تمیزتر Hook اضافه شد: sequence به‌صورت rolling window ساخته می‌شود. وقتی داخل Hook تعداد Xها از ظرفیت `max_x_nodes_per_sequence` عبور کند، origin به جلو promote می‌شود. یعنی origin قدیمی دیگر origin Hook فعلی نیست. مبدا جدید از X1 قبلی ساخته می‌شود و Xها یک خانه به جلو شیفت می‌شوند. مثال مفهومی: اگر X

## Headings

- Phase 14 — Hook Origin Policy / Promoted Origin Mode
-   هدف
-   Input جدید
-   حالت ۱ — Fixed Every Node
-   حالت ۲ — Promote With Internal X
-   نتیجه عملی
-   Default جدید

## Concepts

- [[docs/obsidian/04_concepts/Hook|Hook]]
- [[docs/evidence/nds_anatomy/6a11c75733b2_NDS_Anatomy|NDS Anatomy]]

## Related documents

- [[docs/architecture|System Architecture]] — `core_docs`
- [[docs/ui/ARCHITECTURE|UI System Architecture]] — `ui_docs`
- [[docs/nds_hook_architecture/01_scope_and_inputs|01 — Scope and Inputs]] — `nds_hook_architecture_docs`
- [[docs/nds_hook_architecture/02_cyclehook_object_model|02 — CycleHook Object Model]] — `nds_hook_architecture_docs`
- [[docs/nds_hook_architecture/03_sequence_builder|03 — Sequence Builder]] — `nds_hook_architecture_docs`
- [[docs/nds_hook_architecture/04_x_y_closure_and_hook_types|04 — X/Y Closure and Hook Types]] — `nds_hook_architecture_docs`
- [[docs/nds_hook_architecture/05_visualization_and_diagnostics|05 — Visualization and Diagnostics]] — `nds_hook_architecture_docs`
- [[docs/nds_hook_architecture/06_build_phases|06 — Build Phases]] — `nds_hook_architecture_docs`
- [[docs/nds_hook_architecture/07_mql5_integration_contract|07 — MQL5 Integration Contract]] — `nds_hook_architecture_docs`
- [[docs/nds_hook_architecture/08_phase01_node_source_adapter_implementation|08 — Hook Phase 01 Implementation: Node Source Adapter]] — `nds_hook_architecture_docs`
- [[docs/nds_hook_architecture/09_phase02_cyclehook_sequence_builder_implementation|09 — Hook Phase 02 Implementation: CycleHook Object and X-Sequence Builder]] — `nds_hook_architecture_docs`
- [[docs/nds_hook_architecture/10_phase03_y_axis_opposite_extremes_implementation|10 — Hook Phase 03 Implementation: Y-Axis Opposite Extremes]] — `nds_hook_architecture_docs`

## Recommended Obsidian use

- این card را به نوت‌های concept، hypothesis، experiment یا ADR مربوط link کن.
- اگر این سند source of truth است، در MOC مربوطه بالاتر از اسناد legacy قرارش بده.
- اگر این سند report/validation است، نتیجه نهایی آن را به registry مربوط sync کن.
