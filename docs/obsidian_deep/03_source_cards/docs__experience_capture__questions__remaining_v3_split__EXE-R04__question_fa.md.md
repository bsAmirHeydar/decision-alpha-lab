
---
type: source_card
source_path: "docs/experience_capture/questions/remaining_v3_split/EXE-R04/question_fa.md"
source_ext: ".md"
source_size: 1261
empty: false
generated_at: 2026-07-06
concepts: ["Execution / Risk", "Python Brain", "Validation / Audit", "Zone / RTV"]
entities: []
---

# Source Card — question_fa.md

## Source

[[docs/experience_capture/questions/remaining_v3_split/EXE-R04/question_fa|docs/experience_capture/questions/remaining_v3_split/EXE-R04/question_fa.md]]

## Summary

چرا مهم است: چون باید بفهمیم سیستم چه قصدی داشته، چه چیزی به broker فرستاده شده، چه چیزی fill شده و اختلاف‌ها از کجا آمده‌اند. بدون reconciliation، backtest/paper/live قابل اعتماد نیست. برای پاسخ، حتماً این موارد را روشن کن: • Intent price و submitted price چطور مقایسه می‌شوند؟ • Submitted price و filled price چطور مقایسه می‌شوند؟ • Structural SL/TP و adjusted SL/TP جدا ذخیره شوند؟ • Slippage چطور ثبت شود؟ • Partial fills چطور ثبت شوند؟ • Rejected orders چطور ثبت شوند؟ • Canceled orders چطور ثبت شوند؟ • Split order aggregation چطور باشد؟ • Broker-side modification چطور audit شود؟ • Reconciliation با scenario/zone/entry ID چطور انجام شود؟ عکس لازم: خیر. پاسخ متنی کافی است. خروجی مورد انتظار بعد از پاسخ: • execution_audit_ledger_v1.csv • intent_to_order_reconciliation_v1.csv • fill_quality_model_v1.csv • split_order_audit_v1.csv پاسخ شما:

## Concepts

[[docs/obsidian_deep/02_concepts/Execution____Risk|Execution / Risk]], [[docs/obsidian_deep/02_concepts/Python_Brain|Python Brain]], [[docs/obsidian_deep/02_concepts/Validation____Audit|Validation / Audit]], [[docs/obsidian_deep/02_concepts/Zone____RTV|Zone / RTV]]

## Entities

—

## Headings

- EXE-R04 — Execution Audit and Reconciliation

## Related Source Documents

- [[docs/experience_capture/questions/remaining_v2/by_code/EXE-R04|EXE-R04.md]] — score `10`
- [[docs/experience_capture/questions/remaining_v3_split/EXE-R04/question_en|question_en.md]] — score `9`
- [[docs/ai_execution/AI_ALGORITHM_LAYER_MAP_FOR_EXTREME_ENGINE_FA|AI_ALGORITHM_LAYER_MAP_FOR_EXTREME_ENGINE_FA.md]] — score `8`
- [[docs/ai_execution/AI_NATIVE_EXECUTION_ROADMAP_FA|AI_NATIVE_EXECUTION_ROADMAP_FA.md]] — score `8`
- [[docs/ai_execution/AMIR_STRUCTURAL_EXPERIENCE_MAP_FA|AMIR_STRUCTURAL_EXPERIENCE_MAP_FA.md]] — score `8`
- [[docs/ai_execution/EXTREME_L2_NODE_CYCLE_LIMIT_ENTRY_FA|EXTREME_L2_NODE_CYCLE_LIMIT_ENTRY_FA.md]] — score `8`
- [[docs/architecture|architecture.md]] — score `8`
- [[docs/debug/D0006_H5_LIVE_TOUCH_REPLAY_AUDIT|D0006_H5_LIVE_TOUCH_REPLAY_AUDIT.md]] — score `8`
- [[docs/execution/EXP0016_intermarket_divergence_execution/LEVEL_02_STC_SMT_TIME_ENGINE|LEVEL_02_STC_SMT_TIME_ENGINE.md]] — score `8`
- [[docs/execution/EXP0016_intermarket_divergence_execution/LEVEL_13_STC_SMT_VISUALIZATION_AUDIT_DRAWING|LEVEL_13_STC_SMT_VISUALIZATION_AUDIT_DRAWING.md]] — score `8`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
