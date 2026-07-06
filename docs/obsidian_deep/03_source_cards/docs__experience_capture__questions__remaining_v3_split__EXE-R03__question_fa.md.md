
---
type: source_card
source_path: "docs/experience_capture/questions/remaining_v3_split/EXE-R03/question_fa.md"
source_ext: ".md"
source_size: 1279
empty: false
generated_at: 2026-07-06
concepts: ["Execution / Risk", "Python Brain", "Validation / Audit"]
entities: []
---

# Source Card — question_fa.md

## Source

[[docs/experience_capture/questions/remaining_v3_split/EXE-R03/question_fa|docs/experience_capture/questions/remaining_v3_split/EXE-R03/question_fa.md]]

## Summary

چرا مهم است: چون سیستم باید مرحله‌ای جلو برود؛ اول shadow، بعد paper، بعد live. هر مرحله باید معیار عبور، safety gate و kill switch داشته باشد. برای پاسخ، حتماً این موارد را روشن کن: • Shadow mode دقیقاً چه چیزهایی را log می‌کند؟ • Paper mode چه تفاوتی با shadow دارد؟ • Live mode چه safety gateهایی می‌خواهد؟ • AI در live فقط rank/veto می‌کند یا نقش دیگری هم دارد؟ • چه metricهایی برای رفتن از shadow به paper لازم است؟ • چه metricهایی برای رفتن از paper به live لازم است؟ • چه kill switchهایی لازم است؟ • اگر مدل drift کرد، به کدام mode برمی‌گردد؟ • هر market/timeframe جدا approval می‌خواهد؟ • Audit برای هر intent و order چگونه است؟ عکس لازم: خیر. پاسخ متنی کافی است. خروجی مورد انتظار بعد از پاسخ: • shadow_mode_policy_v1.csv • paper_mode_policy_v1.csv • live_gate_policy_v1.csv • kill_switch_policy_v1.csv پاسخ شما:

## Concepts

[[docs/obsidian_deep/02_concepts/Execution____Risk|Execution / Risk]], [[docs/obsidian_deep/02_concepts/Python_Brain|Python Brain]], [[docs/obsidian_deep/02_concepts/Validation____Audit|Validation / Audit]]

## Entities

—

## Headings

- EXE-R03 — Shadow, Paper, and Live Transition

## Related Source Documents

- [[docs/experience_capture/questions/remaining_v2/by_code/EXE-R03|EXE-R03.md]] — score `10`
- [[docs/experience_capture/questions/remaining_v3_split/EXE-R03/question_en|question_en.md]] — score `7`
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
