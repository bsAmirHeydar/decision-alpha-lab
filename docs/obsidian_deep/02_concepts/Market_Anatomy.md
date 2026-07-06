
---
type: canonical_concept
concept: "Market Anatomy"
generated_at: 2026-07-06
source_count: 54
---

# Market Anatomy

## تعریف عملیاتی

لایه مادر پروژه؛ زبان داخلی برای دیدن بازار به عنوان ساختار، نه مجموعه‌ای از اندیکاتورها. Hook، Rally، F-counting، Decision Node، Zone و RTV همگی زیر این چتر معنا می‌گیرند.

## نقش در Alpha Lab

این مفهوم باید در یکی از چهار نقش زیر قرار بگیرد:

1. **زبان دیدن بازار**: کمک به خواندن ساختار.
2. **قانون تولید فرضیه**: تبدیل مشاهده به claim قابل تست.
3. **فیچر/شرط قابل اندازه‌گیری**: ورود به Python/MQL/Backtest.
4. **قید اجرایی/اعتبارسنجی**: محدود کردن خطا، repaint، leakage یا ریسک.

## روابط مستقیم

- [[docs/obsidian_deep/02_concepts/Hook|Hook]]
- [[docs/obsidian_deep/02_concepts/Rally|Rally]]
- [[docs/obsidian_deep/02_concepts/Flag_Counting|Flag Counting]]
- [[docs/obsidian_deep/02_concepts/Decision_Node|Decision Node]]
- [[docs/obsidian_deep/02_concepts/Zone____RTV|Zone / RTV]]

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
| [[docs/ai_execution/AI_NATIVE_EXECUTION_ROADMAP_FA|AI_NATIVE_EXECUTION_ROADMAP_FA.md]] | — | این سند مرجع فلسفی و مهندسی مسیر بعدی پروژه است. این سند کد اجرایی نیست. این سند قرار است قبل از ورود به train، backtest، مدل‌های هوش مصنوعی و execution bridge، |
| [[docs/debug/MARKET_LANGUAGE/README|README.md]] | M0007 | > Version: draft 0.2 > Scope: discretionary-to-algorithmic vocabulary for Decision Alpha Lab > Purpose: convert the manual multi-timeframe market-reading langua |
| [[docs/experience_capture/answers/BASE-02/answer_normalized_en|answer_normalized_en.md]] | — | A scenario is not just a direction. A scenario is a structured case file. It starts with a directional thesis, but it becomes a real scenario only when it is co |
| [[docs/experience_capture/answers/BASE-02/answer_raw_en|answer_raw_en.md]] | — | Definition of scenario. A scenario means that we must bring reasons for the states I described earlier and then compare them. That means we try to build a bulli |
| [[docs/experience_capture/answers/BASE-03/answer_normalized_en|answer_normalized_en.md]] | — | A valid reason is not any market observation. A valid reason must come from the project's own anatomy. The primary source of valid reasons is structural countin |
| [[docs/experience_capture/answers/BASE-03/answer_raw_en|answer_raw_en.md]] | — | What counts as a reason and what counts as noise. The main reasons come from the countings. From the Rally view, the important thing is: which F we are in, and  |
| [[docs/experience_capture/answers/BASE-03/notes_en|notes_en.md]] | — | This experience should be treated as: The system must distinguish between: The model should not consume arbitrary chart features. It should consume only reasons |
| [[docs/experience_capture/answers/BASE-04/answer_normalized_en|answer_normalized_en.md]] | — | The system must be ontology-pure. Only the project's own concepts are allowed. The complete ontology package is named: Everything outside NDS is forbidden by de |
| [[docs/experience_capture/answers/BASE-04/notes_en|notes_en.md]] | — | This experience should be treated as: Every future dataset, model, feature, label, and execution reason must pass an ontology filter. The system must not allow  |
| [[docs/experience_capture/answers/BASE-06/answer_normalized_en|answer_normalized_en.md]] | — | The ontology is fixed. The usage policy is learnable. This means: AI may learn how to use the anatomy, but it may not redefine the anatomy or import concepts fr |
| [[docs/experience_capture/answers/BASE-06/answer_raw_en|answer_raw_en.md]] | — | Hard rules versus learnable layers. The red line is that all reasons, viewpoints, and decisions must be based on this anatomy and these concepts only. Nothing e |
| [[docs/experience_capture/answers/BASE-06/notes_en|notes_en.md]] | — | This experience should be treated as: The system must have two separated layers: Layer 1 is not trainable. Layer 2 is trainable. Every dataset should separate:  |
| [[docs/experience_capture/answers/DATA-R03/answer_normalized_en|answer_normalized_en.md]] | — | NDS training must be layered, cumulative, inspectable, and consolidating. The AI should not train all problems at once. It should train one structural layer, st |
| [[docs/experience_capture/answers/DATA-R03/answer_raw_en|answer_raw_en.md]] | — | Layered training, context-zone-entry learning sequence, knowledge consolidation, reusable trained infrastructure, human inspectability, and training as capital. |
| [[docs/experience_capture/answers/DATA-R03/question_en|question_en.md]] | — | How should NDS training be organized so that learned knowledge becomes stable infrastructure, instead of starting from zero every time? How should context, zone |
| [[docs/experience_capture/answers/DST-R03/answer_normalized_en|answer_normalized_en.md]] | — | Destination lifecycle must remain inside NDS. The system should not introduce external target logic, generic technical targets, indicator targets, or non-NDS de |
| [[docs/experience_capture/answers/DST-R03/answer_raw_en|answer_raw_en.md]] | — | Destination repricing, completion, internal NDS-only destination logic, anatomy-based destination lifecycle, and weight-based updates. For destination, we use o |
| [[docs/experience_capture/answers/DST-R03/notes_en|notes_en.md]] | — | This answer should be treated as: The destination layer must not become a generic target engine. Recommended flow: Any destination output should be explainable  |
| [[docs/experience_capture/answers/DST-R03/question_en|question_en.md]] | — | How should Destination candidates update, reprice, complete, become consumed, or lose usefulness as market structure evolves? DST-R01 established that destinati |
| [[docs/experience_capture/answers/ENT-R01/answer_normalized_en|answer_normalized_en.md]] | — | NDS must distinguish two different Extreme concepts: They are not the same object. The Hook Extreme is an internal structural extreme of a Hook/CycleHook. The E |

## Trace Targets

- Hypothesisهای مرتبط: از [[docs/obsidian_deep/04_relationships/entity_to_document_map|Entity Map]] پیدا شود.
- Experiments مرتبط: از [[docs/obsidian_deep/04_relationships/traceability_matrix|Traceability Matrix]] پیدا شود.
- Code مرتبط: از [[docs/obsidian_deep/04_relationships/code_to_concept_map|Code Map]] پیدا شود.
- تصمیم‌های معماری: در ADRها و patch notes ثبت شود.
