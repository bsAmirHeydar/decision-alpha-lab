
---
type: source_card
source_path: "docs/experience_capture/questions/remaining_v3_split/TEST-R02/question_fa.md"
source_ext: ".md"
source_size: 1054
empty: false
generated_at: 2026-07-06
concepts: ["Python Brain", "Validation / Audit"]
entities: []
---

# Source Card — question_fa.md

## Source

[[docs/experience_capture/questions/remaining_v3_split/TEST-R02/question_fa|docs/experience_capture/questions/remaining_v3_split/TEST-R02/question_fa.md]]

## Summary

چرا مهم است: چون اگر سیاست‌ها train می‌شوند، خطر overfit جدی است. باید معلوم شود چه زمانی یک rule یا policy واقعاً قابل اعتماد و deployable است. برای پاسخ، حتماً این موارد را روشن کن: • In-sample / out-of-sample split چطور باشد؟ • Walk-forward چطور طراحی شود؟ • Market split لازم است؟ • Timeframe split لازم است؟ • Regime split چطور تعریف شود؟ • Minimum sample size چقدر باشد؟ • Stability metrics چیست؟ • Failure cases چطور گزارش شوند؟ • Degradation tolerance چقدر است؟ • Deployment threshold چیست؟ عکس لازم: خیر. پاسخ متنی کافی است. خروجی مورد انتظار بعد از پاسخ: • anti_overfit_test_plan_v1.csv • oos_validation_policy_v1.csv • walk_forward_evaluation_v1.csv • deployment_criteria_v1.csv پاسخ شما:

## Concepts

[[docs/obsidian_deep/02_concepts/Python_Brain|Python Brain]], [[docs/obsidian_deep/02_concepts/Validation____Audit|Validation / Audit]]

## Entities

—

## Headings

- TEST-R02 — Anti-Overfit, OOS, and Deployment Criteria

## Related Source Documents

- [[docs/experience_capture/questions/remaining_v2/by_code/TEST-R02|TEST-R02.md]] — score `8`
- [[lab/07_monitoring/MON001/metrics|metrics.md]] — score `8`
- [[docs/experience_capture/questions/remaining_v3_split/TEST-R02/question_en|question_en.md]] — score `5`
- [[docs/ai_execution/AI_ALGORITHM_LAYER_MAP_FOR_EXTREME_ENGINE_FA|AI_ALGORITHM_LAYER_MAP_FOR_EXTREME_ENGINE_FA.md]] — score `4`
- [[docs/ai_execution/AI_NATIVE_EXECUTION_ROADMAP_FA|AI_NATIVE_EXECUTION_ROADMAP_FA.md]] — score `4`
- [[docs/ai_execution/AMIR_STRUCTURAL_EXPERIENCE_MAP_FA|AMIR_STRUCTURAL_EXPERIENCE_MAP_FA.md]] — score `4`
- [[docs/ai_execution/EXTREME_L2_NODE_CYCLE_LIMIT_ENTRY_FA|EXTREME_L2_NODE_CYCLE_LIMIT_ENTRY_FA.md]] — score `4`
- [[docs/architecture|architecture.md]] — score `4`
- [[docs/debug/D0005_H5_NO_FUTURE_WALK_FORWARD_AUDIT|D0005_H5_NO_FUTURE_WALK_FORWARD_AUDIT.md]] — score `4`
- [[docs/debug/D0006_H5_LIVE_TOUCH_REPLAY_AUDIT|D0006_H5_LIVE_TOUCH_REPLAY_AUDIT.md]] — score `4`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
