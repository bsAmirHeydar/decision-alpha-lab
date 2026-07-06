
---
type: canonical_concept
concept: "Flag Counting"
generated_at: 2026-07-06
source_count: 224
---

# Flag Counting

## تعریف عملیاتی

سیستم شمارش F1/F2/F3 و Flag برای تشخیص ساختار، شکست، continuation/reversal و ترتیب حرکت‌ها.

## نقش در Alpha Lab

این مفهوم باید در یکی از چهار نقش زیر قرار بگیرد:

1. **زبان دیدن بازار**: کمک به خواندن ساختار.
2. **قانون تولید فرضیه**: تبدیل مشاهده به claim قابل تست.
3. **فیچر/شرط قابل اندازه‌گیری**: ورود به Python/MQL/Backtest.
4. **قید اجرایی/اعتبارسنجی**: محدود کردن خطا، repaint، leakage یا ریسک.

## روابط مستقیم

- [[docs/obsidian_deep/02_concepts/Market_Anatomy|Market Anatomy]]
- [[docs/obsidian_deep/02_concepts/Hook|Hook]]
- [[docs/obsidian_deep/02_concepts/Rally|Rally]]
- [[docs/obsidian_deep/02_concepts/Validation____Audit|Validation / Audit]]
- [[docs/obsidian_deep/02_concepts/MQL_Native|MQL Native]]

## سؤال‌های طراحی

- تعریف دقیق این مفهوم در داده چیست؟
- آیا در زمان live قابل دانستن است یا future leak دارد؟
- آیا روی چند regime تست شده است؟
- آیا ارتباطش با تحدب/هزینه شکست روشن است؟
- آیا پیاده‌سازی MQL/Python آن traceable است؟
- آیا در ژورنال دستی label می‌شود؟

## Source Documents

| سند | entityها | خلاصه |
|---|---|---|
| [[docs/00_project_index|00_project_index.md]] | M0007 | M0007 — Adaptive F1 Flag Counting Project-name repetition inside MQL folders is avoided. Correct MQL module layout: |
| [[docs/ai_execution/AI_ALGORITHM_LAYER_MAP_FOR_EXTREME_ENGINE_FA|AI_ALGORITHM_LAYER_MAP_FOR_EXTREME_ENGINE_FA.md]] | — | این سند مشخص می‌کند برای استفاده از تجربه‌ی اکستریم L2، چه لایه‌های الگوریتمی و هوش مصنوعی لازم است. اصل مهم: AI در این سیستم predictor خام نیست. AI این کارها ر |
| [[docs/ai_execution/AI_NATIVE_EXECUTION_ROADMAP_FA|AI_NATIVE_EXECUTION_ROADMAP_FA.md]] | — | این سند مرجع فلسفی و مهندسی مسیر بعدی پروژه است. این سند کد اجرایی نیست. این سند قرار است قبل از ورود به train، backtest، مدل‌های هوش مصنوعی و execution bridge، |
| [[docs/ai_execution/AMIR_STRUCTURAL_EXPERIENCE_MAP_FA|AMIR_STRUCTURAL_EXPERIENCE_MAP_FA.md]] | — | این سند، تجربه‌های خام امیر درباره بازار، اکستریم‌ها، اف‌شماری، هوک/رالی، سناریوهای دوطرفه، فرکتال و اجرای لیمیت را تبدیل می‌کند به یک چارچوب قابل‌کدنویسی، قابل |
| [[docs/ai_execution/EXPERIENCE_CAPTURE_LOG_TEMPLATE_FA|EXPERIENCE_CAPTURE_LOG_TEMPLATE_FA.md]] | — | این فایل قالب خام ثبت تجربه‌هاست. هر تجربه باید به یکی از این فرم‌ها تبدیل شود: |
| [[docs/ai_execution/README|README.md]] | — | این پوشه برای اسناد مسیر هوش مصنوعی، بک‌تست، episode، label، algorithm layers و execution bridge است. تعریف رسمی تجربه امیر درباره ورود در اکستریم نزدیک نود L2  |
| [[docs/debug/E0008/README|README.md]] | E0007, E0008, M0001 | E0008 is the execution template that matches the user objective more directly than E0007: > We do not want every purple zone. > We want purple/source zones that |
| [[docs/debug/MARKET_LANGUAGE/README|README.md]] | M0007 | > Version: draft 0.2 > Scope: discretionary-to-algorithmic vocabulary for Decision Alpha Lab > Purpose: convert the manual multi-timeframe market-reading langua |
| [[docs/experience_capture/answers/BASE-01/answer_normalized_en|answer_normalized_en.md]] | — | The market should not be interpreted as a single fixed state. Every market snapshot must be evaluated through at least two axes: Therefore, each market state sh |
| [[docs/experience_capture/answers/BASE-01/answer_raw_en|answer_raw_en.md]] | — | Multi-state market interpretation: direction and context. The market's multi-state nature means that two categories must always be considered: direction and con |
| [[docs/experience_capture/answers/BASE-01/notes_en|notes_en.md]] | — | This experience should be treated as: It is not a simple trading rule. It defines how the whole system should represent market state. What exactly makes a Hook  |
| [[docs/experience_capture/answers/BASE-02/answer_normalized_en|answer_normalized_en.md]] | — | A scenario is not just a direction. A scenario is a structured case file. It starts with a directional thesis, but it becomes a real scenario only when it is co |
| [[docs/experience_capture/answers/BASE-02/answer_raw_en|answer_raw_en.md]] | — | Definition of scenario. A scenario means that we must bring reasons for the states I described earlier and then compare them. That means we try to build a bulli |
| [[docs/experience_capture/answers/BASE-03/answer_normalized_en|answer_normalized_en.md]] | — | A valid reason is not any market observation. A valid reason must come from the project's own anatomy. The primary source of valid reasons is structural countin |
| [[docs/experience_capture/answers/BASE-03/answer_raw_en|answer_raw_en.md]] | — | What counts as a reason and what counts as noise. The main reasons come from the countings. From the Rally view, the important thing is: which F we are in, and  |
| [[docs/experience_capture/answers/BASE-03/notes_en|notes_en.md]] | — | This experience should be treated as: The system must distinguish between: The model should not consume arbitrary chart features. It should consume only reasons |
| [[docs/experience_capture/answers/BASE-04/answer_normalized_en|answer_normalized_en.md]] | — | The system must be ontology-pure. Only the project's own concepts are allowed. The complete ontology package is named: Everything outside NDS is forbidden by de |
| [[docs/experience_capture/answers/BASE-04/answer_raw_en|answer_raw_en.md]] | — | Forbidden concepts and ontology boundaries. Everything outside our own concepts is forbidden. Our concepts include things like: Hook Rally F-counting Node-count |
| [[docs/experience_capture/answers/BASE-05/answer_normalized_en|answer_normalized_en.md]] | — | Ambiguity is allowed only as a structured multi-hypothesis state. It is useful when it preserves multiple valid structural interpretations. It becomes dangerous |
| [[docs/experience_capture/answers/BASE-05/answer_raw_en|answer_raw_en.md]] | — | Allowed uncertainty, ambiguity, context power, and moving from multi-state interpretation to execution. The point is that we must see the structure. Even if we  |

## Trace Targets

- Hypothesisهای مرتبط: از [[docs/obsidian_deep/04_relationships/entity_to_document_map|Entity Map]] پیدا شود.
- Experiments مرتبط: از [[docs/obsidian_deep/04_relationships/traceability_matrix|Traceability Matrix]] پیدا شود.
- Code مرتبط: از [[docs/obsidian_deep/04_relationships/code_to_concept_map|Code Map]] پیدا شود.
- تصمیم‌های معماری: در ADRها و patch notes ثبت شود.
