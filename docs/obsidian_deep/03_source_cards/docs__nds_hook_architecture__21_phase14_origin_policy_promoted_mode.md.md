
---
type: source_card
source_path: "docs/nds_hook_architecture/21_phase14_origin_policy_promoted_mode.md"
source_ext: ".md"
source_size: 2235
empty: false
generated_at: 2026-07-06
concepts: ["Decision Node", "Execution / Risk", "Hook"]
entities: []
---

# Source Card — 21_phase14_origin_policy_promoted_mode.md

## Source

[[docs/nds_hook_architecture/21_phase14_origin_policy_promoted_mode|docs/nds_hook_architecture/21_phase14_origin_policy_promoted_mode.md]]

## Summary

قبل از Inspector، منطق مبدا Hook باید دوحالته شود. مشکل قبلی این بود که در حالت fixed هر نود هم‌جهت، مخصوصاً در scaleهای کوچک مثل L2، می‌توانست origin مستقل شود و تعداد Hookهای هم‌پوشان زیاد می‌شد. حالت‌ها: همان رفتار قبلی است: هر نود واجد شرایط می‌تواند origin شود. origin تا انتهای sequence ثابت می‌ماند. برای debug کامل همه candidateها مفید است. روی چارت بسیار شلوغ می‌شود. این حالت برای خواندن تمیزتر Hook اضافه شد: sequence به‌صورت rolling window ساخته می‌شود. وقتی داخل Hook تعداد Xها از ظرفیت `max_x_nodes_per_sequence` عبور کند، origin به جلو promote می‌شود. یعنی origin قدیمی دیگر origin Hook فعلی نیست. مبدا جدید از X1 قبلی ساخته می‌شود و Xها یک خانه به جلو شیفت می‌شوند. مثال مفهومی: اگر X جدید بیاید: در ساختار محدود فعلی، `X1` قدیمی origin جدید می‌شود و آخرین X جدید در آخرین slot قرار می‌گیرد. این حالت تعداد originهای قدیمی و هم‌پوشان را کم می‌کند و برای Inspector / Sequence Cycle Deb

## Concepts

[[docs/obsidian_deep/02_concepts/Decision_Node|Decision Node]], [[docs/obsidian_deep/02_concepts/Execution____Risk|Execution / Risk]], [[docs/obsidian_deep/02_concepts/Hook|Hook]]

## Entities

—

## Headings

- Phase 14 — Hook Origin Policy / Promoted Origin Mode
  - هدف
  - Input جدید
  - حالت ۱ — Fixed Every Node
  - حالت ۲ — Promote With Internal X
  - نتیجه عملی
  - Default جدید

## Related Source Documents

- [[docs/nds_hook_architecture/02_cyclehook_object_model|02_cyclehook_object_model.md]] — score `7`
- [[docs/nds_hook_architecture/03_sequence_builder|03_sequence_builder.md]] — score `7`
- [[docs/nds_hook_architecture/04_x_y_closure_and_hook_types|04_x_y_closure_and_hook_types.md]] — score `7`
- [[docs/nds_hook_architecture/06_build_phases|06_build_phases.md]] — score `7`
- [[docs/nds_hook_architecture/07_mql5_integration_contract|07_mql5_integration_contract.md]] — score `7`
- [[docs/nds_hook_architecture/08_phase01_node_source_adapter_implementation|08_phase01_node_source_adapter_implementation.md]] — score `7`
- [[docs/nds_hook_architecture/09_phase02_cyclehook_sequence_builder_implementation|09_phase02_cyclehook_sequence_builder_implementation.md]] — score `7`
- [[docs/nds_hook_architecture/10_phase03_y_axis_opposite_extremes_implementation|10_phase03_y_axis_opposite_extremes_implementation.md]] — score `7`
- [[docs/nds_hook_architecture/11_phase04_nd_death_x_closure_skeleton_implementation|11_phase04_nd_death_x_closure_skeleton_implementation.md]] — score `7`
- [[docs/nds_hook_architecture/12_phase05_hook_type_abc_classifier_implementation|12_phase05_hook_type_abc_classifier_implementation.md]] — score `7`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
