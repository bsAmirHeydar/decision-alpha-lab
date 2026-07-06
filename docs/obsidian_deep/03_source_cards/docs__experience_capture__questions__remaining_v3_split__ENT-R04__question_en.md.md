
---
type: source_card
source_path: "docs/experience_capture/questions/remaining_v3_split/ENT-R04/question_en.md"
source_ext: ".md"
source_size: 1970
empty: false
generated_at: 2026-07-06
concepts: ["Execution / Risk", "Python Brain", "UI / React", "Validation / Audit", "Zone / RTV"]
entities: []
---

# Source Card — question_en.md

## Source

[[docs/experience_capture/questions/remaining_v3_split/ENT-R04/question_en|docs/experience_capture/questions/remaining_v3_split/ENT-R04/question_en.md]]

## Summary

چون وقتی limit پر شد، سیستم از تحلیل و intent وارد position واقعی می‌شود. باید معلوم باشد بعد از fill، سناریو هنوز زنده است، تبدیل به position thread می‌شود، یا وارد مدیریت مستقل معامله می‌شود. بعد از fill، ScenarioThread همچنان زنده می‌ماند یا به PositionThread تبدیل می‌شود؟ اگر parent scenario بعد از ورود ضعیف شد، position چه واکنشی دارد؟ اگر سناریوی مخالف بعد از ورود قوی‌تر شد، position کاهش پیدا می‌کند، hedge می‌شود، یا فقط با stop/TP مدیریت می‌شود؟ استاپ بعد از fill ثابت می‌ماند یا با ساختار جدید می‌تواند جابه‌جا شود؟ اگر مقصد اول خورده شد، position partially completed می‌شود یا سناریو همچنان زنده است؟ خروج پله‌ای جزو scenario است یا position management؟ اگر چند entry داخل یک zone داریم، بعد از fill جدا مدیریت می‌شوند یا یک position bucket می‌شوند؟ اگر max lot split شده بود، معامله‌ها جدا هستند یا یک logical position واحد؟ چه چیزی position را کامل می‌کند: TP کامل، invalidation، پایا

## Concepts

[[docs/obsidian_deep/02_concepts/Execution____Risk|Execution / Risk]], [[docs/obsidian_deep/02_concepts/Python_Brain|Python Brain]], [[docs/obsidian_deep/02_concepts/UI____React|UI / React]], [[docs/obsidian_deep/02_concepts/Validation____Audit|Validation / Audit]], [[docs/obsidian_deep/02_concepts/Zone____RTV|Zone / RTV]]

## Entities

—

## Headings

- ENT-R04 — After Fill: Scenario-to-Position Transition
  - Purpose
  - Required Clarifications
  - Image Requirement
  - Expected Derived Outputs

## Related Source Documents

- [[docs/experience_capture/questions/remaining_v2/by_code/ENT-R04|ENT-R04.md]] — score `12`
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
