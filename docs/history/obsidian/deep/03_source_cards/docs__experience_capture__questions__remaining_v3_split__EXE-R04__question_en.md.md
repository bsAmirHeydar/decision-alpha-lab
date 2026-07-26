
---
type: source_card
source_path: "docs/experience_capture/questions/remaining_v3_split/EXE-R04/question_en.md"
source_ext: ".md"
source_size: 1147
empty: false
generated_at: 2026-07-06
concepts: ["Execution / Risk", "Python Brain", "UI / React", "Validation / Audit", "Zone / RTV"]
entities: []
---

# Source Card — question_en.md

## Source

[[docs/experience_capture/questions/remaining_v3_split/EXE-R04/question_en|docs/experience_capture/questions/remaining_v3_split/EXE-R04/question_en.md]]

## Summary

چون باید بفهمیم سیستم چه قصدی داشته، چه چیزی به broker فرستاده شده، چه چیزی fill شده و اختلاف‌ها از کجا آمده‌اند. بدون reconciliation، backtest/paper/live قابل اعتماد نیست. Intent price و submitted price چطور مقایسه می‌شوند؟ Submitted price و filled price چطور مقایسه می‌شوند؟ Structural SL/TP و adjusted SL/TP جدا ذخیره شوند؟ Slippage چطور ثبت شود؟ Partial fills چطور ثبت شوند؟ Rejected orders چطور ثبت شوند؟ Canceled orders چطور ثبت شوند؟ Split order aggregation چطور باشد؟ Broker-side modification چطور audit شود؟ Reconciliation با scenario/zone/entry ID چطور انجام شود؟ خیر. پاسخ متنی کافی است. `execution_audit_ledger_v1.csv` `intent_to_order_reconciliation_v1.csv` `fill_quality_model_v1.csv` `split_order_audit_v1.csv`

## Concepts

[[docs/obsidian_deep/02_concepts/Execution____Risk|Execution / Risk]], [[docs/obsidian_deep/02_concepts/Python_Brain|Python Brain]], [[docs/obsidian_deep/02_concepts/UI____React|UI / React]], [[docs/obsidian_deep/02_concepts/Validation____Audit|Validation / Audit]], [[docs/obsidian_deep/02_concepts/Zone____RTV|Zone / RTV]]

## Entities

—

## Headings

- EXE-R04 — Execution Audit and Reconciliation
  - Purpose
  - Required Clarifications
  - Image Requirement
  - Expected Derived Outputs

## Related Source Documents

- [[docs/experience_capture/questions/remaining_v2/by_code/EXE-R04|EXE-R04.md]] — score `12`
- [[docs/ai_execution/AI_ALGORITHM_LAYER_MAP_FOR_EXTREME_ENGINE_FA|AI_ALGORITHM_LAYER_MAP_FOR_EXTREME_ENGINE_FA.md]] — score `10`
- [[docs/ai_execution/AI_NATIVE_EXECUTION_ROADMAP_FA|AI_NATIVE_EXECUTION_ROADMAP_FA.md]] — score `10`
- [[docs/ai_execution/AMIR_STRUCTURAL_EXPERIENCE_MAP_FA|AMIR_STRUCTURAL_EXPERIENCE_MAP_FA.md]] — score `10`
- [[docs/ai_execution/EXTREME_L2_NODE_CYCLE_LIMIT_ENTRY_FA|EXTREME_L2_NODE_CYCLE_LIMIT_ENTRY_FA.md]] — score `10`
- [[docs/architecture|architecture.md]] — score `10`
- [[docs/debug/D0006_H5_LIVE_TOUCH_REPLAY_AUDIT|D0006_H5_LIVE_TOUCH_REPLAY_AUDIT.md]] — score `10`
- [[docs/execution/EXP0016_intermarket_divergence_execution/LEVEL_02_STC_SMT_TIME_ENGINE|LEVEL_02_STC_SMT_TIME_ENGINE.md]] — score `10`
- [[docs/execution/EXP0016_intermarket_divergence_execution/LEVEL_13_STC_SMT_VISUALIZATION_AUDIT_DRAWING|LEVEL_13_STC_SMT_VISUALIZATION_AUDIT_DRAWING.md]] — score `10`
- [[docs/experience_capture/answers/BASE-02/notes_en|notes_en.md]] — score `10`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
