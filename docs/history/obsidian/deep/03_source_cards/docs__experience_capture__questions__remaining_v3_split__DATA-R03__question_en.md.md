
---
type: source_card
source_path: "docs/experience_capture/questions/remaining_v3_split/DATA-R03/question_en.md"
source_ext: ".md"
source_size: 1191
empty: false
generated_at: 2026-07-06
concepts: ["Python Brain", "UI / React"]
entities: []
---

# Source Card — question_en.md

## Source

[[docs/experience_capture/questions/remaining_v3_split/DATA-R03/question_en|docs/experience_capture/questions/remaining_v3_split/DATA-R03/question_en.md]]

## Summary

چون گفتی شاید حتی در یک market/timeframe هم وزن‌ها ثابت نمانند. باید معلوم شود آموزش global، market-specific، timeframe-specific و dynamic weight regime چطور انجام می‌شود. Global training دقیقاً چه چیزهایی را یاد می‌گیرد؟ Market-specific training چه زمانی لازم است؟ Market-timeframe-specific training چه زمانی لازم است؟ Dynamic weight regime یعنی چه؟ Rolling windows چطور استفاده شوند؟ Minimum sample برای اعتماد به وزن‌ها چقدر است؟ Stability criteria چیست؟ Drift detection چطور انجام شود؟ Weight decay/boost چطور تعریف شود؟ چه زمانی یک rule جهانی کنار گذاشته یا فقط local می‌شود؟ خیر. پاسخ متنی کافی است. `training_granularity_model_v1.csv` `market_timeframe_policy_v1.csv` `dynamic_weight_regime_model_v1.csv` `weight_drift_detection_v1.csv`

## Concepts

[[docs/obsidian_deep/02_concepts/Python_Brain|Python Brain]], [[docs/obsidian_deep/02_concepts/UI____React|UI / React]]

## Entities

—

## Headings

- DATA-R03 — Training Granularity and Regime Weight Drift
  - Purpose
  - Required Clarifications
  - Image Requirement
  - Expected Derived Outputs

## Related Source Documents

- [[docs/experience_capture/questions/remaining_v2/by_code/DATA-R03|DATA-R03.md]] — score `10`
- [[docs/ai_execution/AI_ALGORITHM_LAYER_MAP_FOR_EXTREME_ENGINE_FA|AI_ALGORITHM_LAYER_MAP_FOR_EXTREME_ENGINE_FA.md]] — score `4`
- [[docs/ai_execution/AI_NATIVE_EXECUTION_ROADMAP_FA|AI_NATIVE_EXECUTION_ROADMAP_FA.md]] — score `4`
- [[docs/ai_execution/AMIR_STRUCTURAL_EXPERIENCE_MAP_FA|AMIR_STRUCTURAL_EXPERIENCE_MAP_FA.md]] — score `4`
- [[docs/ai_execution/EXTREME_L2_NODE_CYCLE_LIMIT_ENTRY_FA|EXTREME_L2_NODE_CYCLE_LIMIT_ENTRY_FA.md]] — score `4`
- [[docs/architecture|architecture.md]] — score `4`
- [[docs/debug/D0005_H5_NO_FUTURE_WALK_FORWARD_AUDIT|D0005_H5_NO_FUTURE_WALK_FORWARD_AUDIT.md]] — score `4`
- [[docs/debug/D0006_H5_LIVE_TOUCH_REPLAY_AUDIT|D0006_H5_LIVE_TOUCH_REPLAY_AUDIT.md]] — score `4`
- [[docs/debug/H4_FAST_ATOMIC_MAIN_REPORT|H4_FAST_ATOMIC_MAIN_REPORT.md]] — score `4`
- [[docs/execution/EXP0016_intermarket_divergence_execution/LEVEL_02_STC_SMT_TIME_ENGINE|LEVEL_02_STC_SMT_TIME_ENGINE.md]] — score `4`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
