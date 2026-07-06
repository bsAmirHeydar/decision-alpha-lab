
---
type: source_card
source_path: "docs/experience_capture/questions/remaining_v3_split/EXE-R02/question_fa.md"
source_ext: ".md"
source_size: 1320
empty: false
generated_at: 2026-07-06
concepts: ["Execution / Risk", "Python Brain", "Validation / Audit"]
entities: []
---

# Source Card — question_fa.md

## Source

[[docs/experience_capture/questions/remaining_v3_split/EXE-R02/question_fa|docs/experience_capture/questions/remaining_v3_split/EXE-R02/question_fa.md]]

## Summary

چرا مهم است: چون حتی اگر NDS یک intent عالی بسازد، broker ممکن است به خاطر min stop، tick، margin، freeze level یا max lot اجازه اجرا ندهد. این لایه باید جلوی اجرای خراب را بگیرد. برای پاسخ، حتماً این موارد را روشن کن: • کدام broker constraints باید حتماً چک شوند؟ • Min stop distance چطور با structural stop مقایسه می‌شود؟ • Tick size و digits چطور normalize می‌شوند؟ • Lot step، min lot و max lot چطور اعمال می‌شوند؟ • Margin کافی نبود، intent veto می‌شود یا حجم adjust می‌شود؟ • Spread چه زمانی باعث veto می‌شود؟ • Freeze level و trade mode چطور لحاظ می‌شوند؟ • Market open/session مهم است؟ • Order rejection handling چطور باشد؟ • چه زمانی adjust مجاز است و چه زمانی veto؟ عکس لازم: خیر. پاسخ متنی کافی است. خروجی مورد انتظار بعد از پاسخ: • broker_validation_model_v1.csv • send_gate_policy_v1.csv • execution_veto_reason_taxonomy_v1.csv • order_rejection_handling_v1.csv پاسخ شما:

## Concepts

[[docs/obsidian_deep/02_concepts/Execution____Risk|Execution / Risk]], [[docs/obsidian_deep/02_concepts/Python_Brain|Python Brain]], [[docs/obsidian_deep/02_concepts/Validation____Audit|Validation / Audit]]

## Entities

—

## Headings

- EXE-R02 — Broker Validator and Send Gate

## Related Source Documents

- [[docs/experience_capture/questions/remaining_v2/by_code/EXE-R02|EXE-R02.md]] — score `10`
- [[docs/experience_capture/questions/remaining_v3_split/EXE-R02/question_en|question_en.md]] — score `7`
- [[docs/ai_execution/AI_ALGORITHM_LAYER_MAP_FOR_EXTREME_ENGINE_FA|AI_ALGORITHM_LAYER_MAP_FOR_EXTREME_ENGINE_FA.md]] — score `6`
- [[docs/ai_execution/AI_NATIVE_EXECUTION_ROADMAP_FA|AI_NATIVE_EXECUTION_ROADMAP_FA.md]] — score `6`
- [[docs/ai_execution/AMIR_STRUCTURAL_EXPERIENCE_MAP_FA|AMIR_STRUCTURAL_EXPERIENCE_MAP_FA.md]] — score `6`
- [[docs/ai_execution/EXTREME_L2_NODE_CYCLE_LIMIT_ENTRY_FA|EXTREME_L2_NODE_CYCLE_LIMIT_ENTRY_FA.md]] — score `6`
- [[docs/architecture|architecture.md]] — score `6`
- [[docs/debug/D0005_H5_NO_FUTURE_WALK_FORWARD_AUDIT|D0005_H5_NO_FUTURE_WALK_FORWARD_AUDIT.md]] — score `6`
- [[docs/debug/D0006_H5_LIVE_TOUCH_REPLAY_AUDIT|D0006_H5_LIVE_TOUCH_REPLAY_AUDIT.md]] — score `6`
- [[docs/execution/EXP0016_intermarket_divergence_execution/LEVEL_02_STC_SMT_TIME_ENGINE|LEVEL_02_STC_SMT_TIME_ENGINE.md]] — score `6`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
