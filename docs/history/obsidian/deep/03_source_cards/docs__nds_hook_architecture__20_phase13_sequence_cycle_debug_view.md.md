
---
type: source_card
source_path: "docs/nds_hook_architecture/20_phase13_sequence_cycle_debug_view.md"
source_ext: ".md"
source_size: 2361
empty: false
generated_at: 2026-07-06
concepts: ["AI Agent Layer", "Decision Node", "Hook", "MQL Native"]
entities: []
---

# Source Card — 20_phase13_sequence_cycle_debug_view.md

## Source

[[docs/nds_hook_architecture/20_phase13_sequence_cycle_debug_view|docs/nds_hook_architecture/20_phase13_sequence_cycle_debug_view.md]]

## Summary

این فاز برای وقتی است که خروجی رسمی Hook هنوز از نظر بصری شلوغ است و باید دقیقاً دیده شود که موتور Hook چطور sequence را می‌شمارد. تمرکز این فاز روی این‌هاست: Origin هر CycleHook X1 / X2 / X3 / X4 خط اتصال Xها شماره sequence تعداد Xهای همان sequence نیم‌دایره‌ی Cycle روی بازه‌ی همان sequence این فاز عمداً P05/P06 quality/type labelها، thresholdها، projectionها، و labelهای debug سنگین را خاموش می‌کند. این پروفایل فقط Phase 02 را به‌عنوان سطح اصلی نمایش فعال می‌کند: `draw_origin = true` `draw_x_nodes = true` `draw_x_lines = true` `draw_cycle_arc = true` `draw_sequence_count_label = true` و این‌ها را خاموش می‌کند: Phase 03 Y overlays Phase 04 threshold / ND / death overlays Phase 05 type labels Phase 06 quality labels Arc از `Origin` تا آخرین X معتبر sequence رسم می‌شود. برای sequence مثبت، arc پایین ساختار رسم می‌شود. برای sequence منفی، arc بالای ساختار رسم می‌شود. ارتفاع arc بر اساس فاصل

## Concepts

[[docs/obsidian_deep/02_concepts/AI_Agent_Layer|AI Agent Layer]], [[docs/obsidian_deep/02_concepts/Decision_Node|Decision Node]], [[docs/obsidian_deep/02_concepts/Hook|Hook]], [[docs/obsidian_deep/02_concepts/MQL_Native|MQL Native]]

## Entities

—

## Headings

- Phase 13 — Sequence + Cycle Arc Debug View
  - هدف
  - View Profile جدید
  - Inputهای جدید Phase 02
  - منطق نیم‌دایره
  - Recommended inputs

## Related Source Documents

- [[docs/nds_hook_architecture/08_phase01_node_source_adapter_implementation|08_phase01_node_source_adapter_implementation.md]] — score `9`
- [[docs/nds_hook_architecture/09_phase02_cyclehook_sequence_builder_implementation|09_phase02_cyclehook_sequence_builder_implementation.md]] — score `9`
- [[docs/nds_hook_architecture/13_phase06_xy_closure_quality_score_implementation|13_phase06_xy_closure_quality_score_implementation.md]] — score `9`
- [[docs/nds_hook_architecture/14_phase07_visual_profile_orchestrator_implementation|14_phase07_visual_profile_orchestrator_implementation.md]] — score `9`
- [[docs/nds_hook_architecture/15_phase08_audit_csv_reconciliation_implementation|15_phase08_audit_csv_reconciliation_implementation.md]] — score `9`
- [[docs/nds_hook_architecture/37_phase26_doc_aligned_hook_rebuild|37_phase26_doc_aligned_hook_rebuild.md]] — score `9`
- [[docs/ai_execution/AI_NATIVE_EXECUTION_ROADMAP_FA|AI_NATIVE_EXECUTION_ROADMAP_FA.md]] — score `8`
- [[docs/experience_capture/answers/BASE-04/answer_normalized_en|answer_normalized_en.md]] — score `8`
- [[docs/experience_capture/answers/BASE-04/notes_en|notes_en.md]] — score `8`
- [[docs/experience_capture/answers/BASE-06/answer_normalized_en|answer_normalized_en.md]] — score `8`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
