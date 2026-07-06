
---
type: source_card
source_path: "docs/experience_capture/questions/remaining_v3_split/AI-R01/question_fa.md"
source_ext: ".md"
source_size: 1276
empty: false
generated_at: 2026-07-06
concepts: ["Execution / Risk", "Python Brain", "Validation / Audit", "Zone / RTV"]
entities: []
---

# Source Card — question_fa.md

## Source

[[docs/experience_capture/questions/remaining_v3_split/AI-R01/question_fa|docs/experience_capture/questions/remaining_v3_split/AI-R01/question_fa.md]]

## Summary

چرا مهم است: چون AI نباید ontology را خراب کند یا نقش decision god بگیرد. باید دقیق مشخص شود AI چه کارهایی مجاز است انجام دهد و چه چیزهایی hard rule باقی می‌ماند. برای پاسخ، حتماً این موارد را روشن کن: • AI مجاز است ontology را تغییر دهد یا فقط پیشنهاد بدهد؟ • AI فقط rank/veto/select/score می‌کند؟ • AI می‌تواند zone family جدید پیشنهاد دهد؟ • AI می‌تواند entry را replace کند؟ • AI می‌تواند risk budget پیشنهاد دهد؟ • AI می‌تواند order send کند؟ طبق معماری فعلی جواب پیش‌فرض: نه. • چه چیزهایی hard rule هستند؟ • چه چیزهایی learnable policy هستند؟ • AI output باید explainable باشد؟ • هر تصمیم AI چطور audit می‌شود؟ عکس لازم: خیر. پاسخ متنی کافی است. خروجی مورد انتظار بعد از پاسخ: • ai_boundary_model_v1.csv • ai_allowed_actions_v1.csv • ai_veto_rank_select_policy_v1.csv • ai_audit_contract_v1.csv پاسخ شما:

## Concepts

[[docs/obsidian_deep/02_concepts/Execution____Risk|Execution / Risk]], [[docs/obsidian_deep/02_concepts/Python_Brain|Python Brain]], [[docs/obsidian_deep/02_concepts/Validation____Audit|Validation / Audit]], [[docs/obsidian_deep/02_concepts/Zone____RTV|Zone / RTV]]

## Entities

—

## Headings

- AI-R01 — AI Boundary and Allowed Decisions

## Related Source Documents

- [[docs/experience_capture/questions/remaining_v2/by_code/AI-R01|AI-R01.md]] — score `10`
- [[docs/experience_capture/questions/remaining_v3_split/AI-R01/question_en|question_en.md]] — score `9`
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
