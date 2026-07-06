
---
type: source_card
source_path: "docs/nds_hook_architecture/22_phase15_hard_sequence_lens_cleanup.md"
source_ext: ".md"
source_size: 2203
empty: false
generated_at: 2026-07-06
concepts: ["AI Agent Layer", "Hook", "Rally"]
entities: []
---

# Source Card — 22_phase15_hard_sequence_lens_cleanup.md

## Source

[[docs/nds_hook_architecture/22_phase15_hard_sequence_lens_cleanup|docs/nds_hook_architecture/22_phase15_hard_sequence_lens_cleanup.md]]

## Summary

بعد از اضافه شدن نیم‌دایره‌ی Cycle و حالت promoted origin، هنوز ممکن بود روی چارت آبجکت‌های قدیمی P05/P06 یا رندر اصلی Rally باقی بمانند. دلیل عملی این بود که MT5 مقدار inputهای قبلی را روی instance چارت نگه می‌دارد و بع… این فاز حالت `SEQUENCE_CYCLE_DEBUG` را از یک view معمولی به یک hard inspector lens تبدیل می‌کند. Phase 01 فقط برای ساخت داده‌ی نود استفاده می‌شود و چیزی رسم نمی‌کند. Phase 02 تنها لایه‌ی قابل نمایش است. Phase 03، Phase 04، Phase 05 و Phase 06 از نظر runtime disabled می‌شوند، نه فقط draw=false. تعداد sequence قابل رسم به‌صورت hard cap روی 1 قرار می‌گیرد. P03/P04/P05/P06 نمی‌توانند label یا marker جدید تولید کنند. قبل از هر run، آبجکت‌های خانواده‌ی Hook و آبجکت‌های رندر اصلی با prefixهای input پاک می‌شوند. حتی اگر `CleanBeforeApply=false` از تنظیمات قدیمی MT5 باقی مانده باشد، sequence lens cleanup اجباری اجرا می‌شود. روی چارت باید فقط این‌ها بماند: و این‌ها نباید دوباره د

## Concepts

[[docs/obsidian_deep/02_concepts/AI_Agent_Layer|AI Agent Layer]], [[docs/obsidian_deep/02_concepts/Hook|Hook]], [[docs/obsidian_deep/02_concepts/Rally|Rally]]

## Entities

—

## Headings

- Phase 15 — Hard Sequence Lens Cleanup
  - هدف
  - رفتار جدید در `FP_HOOK_P07_VIEW_SEQUENCE_CYCLE_DEBUG`
  - نتیجه
  - Recommended inputs

## Related Source Documents

- [[docs/nds_hook_architecture/01_scope_and_inputs|01_scope_and_inputs.md]] — score `7`
- [[docs/nds_hook_architecture/06_build_phases|06_build_phases.md]] — score `7`
- [[docs/nds_hook_architecture/08_phase01_node_source_adapter_implementation|08_phase01_node_source_adapter_implementation.md]] — score `7`
- [[docs/nds_hook_architecture/09_phase02_cyclehook_sequence_builder_implementation|09_phase02_cyclehook_sequence_builder_implementation.md]] — score `7`
- [[docs/nds_hook_architecture/13_phase06_xy_closure_quality_score_implementation|13_phase06_xy_closure_quality_score_implementation.md]] — score `7`
- [[docs/nds_hook_architecture/14_phase07_visual_profile_orchestrator_implementation|14_phase07_visual_profile_orchestrator_implementation.md]] — score `7`
- [[docs/nds_hook_architecture/15_phase08_audit_csv_reconciliation_implementation|15_phase08_audit_csv_reconciliation_implementation.md]] — score `7`
- [[docs/nds_hook_architecture/18_phase11_official_schematic_visual_cleanup|18_phase11_official_schematic_visual_cleanup.md]] — score `7`
- [[docs/nds_hook_architecture/42_phase30_responsive_label_stack_spacing|42_phase30_responsive_label_stack_spacing.md]] — score `7`
- [[docs/ai_execution/AI_ALGORITHM_LAYER_MAP_FOR_EXTREME_ENGINE_FA|AI_ALGORITHM_LAYER_MAP_FOR_EXTREME_ENGINE_FA.md]] — score `6`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
