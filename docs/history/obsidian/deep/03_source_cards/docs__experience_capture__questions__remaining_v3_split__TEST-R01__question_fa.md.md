
---
type: source_card
source_path: "docs/experience_capture/questions/remaining_v3_split/TEST-R01/question_fa.md"
source_ext: ".md"
source_size: 1128
empty: false
generated_at: 2026-07-06
concepts: ["Execution / Risk", "Hook", "Python Brain", "Rally", "Validation / Audit", "Zone / RTV"]
entities: []
---

# Source Card — question_fa.md

## Source

[[docs/experience_capture/questions/remaining_v3_split/TEST-R01/question_fa|docs/experience_capture/questions/remaining_v3_split/TEST-R01/question_fa.md]]

## Summary

چرا مهم است: چون برای فهمیدن ارزش واقعی هر قید باید آن را جدا، ترکیبی، با و بدون بقیه تست کنیم. بدون ablation معلوم نمی‌شود کدام رشته واقعاً edge می‌دهد. برای پاسخ، حتماً این موارد را روشن کن: • Baseline pure Hook چطور باشد؟ • Baseline pure Rally/F چطور باشد؟ • X-only چطور تست شود؟ • Y-only چطور تست شود؟ • XY چطور تست شود؟ • Symmetry-only یا symmetry-added چطور تست شود؟ • Zone with/without destination چطور مقایسه شود؟ • Entry with/without near-death چطور مقایسه شود؟ • Buffer variants چطور تست شوند؟ • Global vs market-specific results چطور مقایسه شوند؟ عکس لازم: خیر. پاسخ متنی کافی است. خروجی مورد انتظار بعد از پاسخ: • baseline_experiment_plan_v1.csv • ablation_matrix_v1.csv • family_comparison_report_v1.csv پاسخ شما:

## Concepts

[[docs/obsidian_deep/02_concepts/Execution____Risk|Execution / Risk]], [[docs/obsidian_deep/02_concepts/Hook|Hook]], [[docs/obsidian_deep/02_concepts/Python_Brain|Python Brain]], [[docs/obsidian_deep/02_concepts/Rally|Rally]], [[docs/obsidian_deep/02_concepts/Validation____Audit|Validation / Audit]], [[docs/obsidian_deep/02_concepts/Zone____RTV|Zone / RTV]]

## Entities

—

## Headings

- TEST-R01 — Baseline, Ablation, and Family Testing

## Related Source Documents

- [[lab/05_validation/VAL_M0001_MQL_NATIVE/report|report.md]] — score `14`
- [[docs/experience_capture/questions/remaining_v3_split/TEST-R01/question_en|question_en.md]] — score `13`
- [[docs/ai_execution/AI_ALGORITHM_LAYER_MAP_FOR_EXTREME_ENGINE_FA|AI_ALGORITHM_LAYER_MAP_FOR_EXTREME_ENGINE_FA.md]] — score `12`
- [[docs/ai_execution/AI_NATIVE_EXECUTION_ROADMAP_FA|AI_NATIVE_EXECUTION_ROADMAP_FA.md]] — score `12`
- [[docs/ai_execution/AMIR_STRUCTURAL_EXPERIENCE_MAP_FA|AMIR_STRUCTURAL_EXPERIENCE_MAP_FA.md]] — score `12`
- [[docs/ai_execution/EXTREME_L2_NODE_CYCLE_LIMIT_ENTRY_FA|EXTREME_L2_NODE_CYCLE_LIMIT_ENTRY_FA.md]] — score `12`
- [[docs/experience_capture/answers/BASE-02/notes_en|notes_en.md]] — score `12`
- [[docs/experience_capture/answers/EXT-02/notes_en|notes_en.md]] — score `12`
- [[docs/experience_capture/answers/EXT-04/notes_en|notes_en.md]] — score `12`
- [[docs/experience_capture/answers/EXT-08/notes_en|notes_en.md]] — score `12`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
