
---
type: canonical_concept
concept: "Convexity / Optionality"
generated_at: 2026-07-06
source_count: 242
---

# Convexity / Optionality

## تعریف عملیاتی

منطق تصمیم‌گیری پروژه: هزینه شکست کم، سود بالقوه باز، عدم وابستگی اولیه به win rate و تمرکز روی پتانسیل انفجار.

## نقش در Alpha Lab

این مفهوم باید در یکی از چهار نقش زیر قرار بگیرد:

1. **زبان دیدن بازار**: کمک به خواندن ساختار.
2. **قانون تولید فرضیه**: تبدیل مشاهده به claim قابل تست.
3. **فیچر/شرط قابل اندازه‌گیری**: ورود به Python/MQL/Backtest.
4. **قید اجرایی/اعتبارسنجی**: محدود کردن خطا، repaint، leakage یا ریسک.

## روابط مستقیم

- [[docs/obsidian_deep/02_concepts/Execution____Risk|Execution / Risk]]
- [[docs/obsidian_deep/02_concepts/Validation____Audit|Validation / Audit]]
- [[docs/obsidian_deep/02_concepts/Path_Smoothness|Path Smoothness]]

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
| [[docs/ai_execution/AI_ALGORITHM_LAYER_MAP_FOR_EXTREME_ENGINE_FA|AI_ALGORITHM_LAYER_MAP_FOR_EXTREME_ENGINE_FA.md]] | — | این سند مشخص می‌کند برای استفاده از تجربه‌ی اکستریم L2، چه لایه‌های الگوریتمی و هوش مصنوعی لازم است. اصل مهم: AI در این سیستم predictor خام نیست. AI این کارها ر |
| [[docs/ai_execution/AI_NATIVE_EXECUTION_ROADMAP_FA|AI_NATIVE_EXECUTION_ROADMAP_FA.md]] | — | این سند مرجع فلسفی و مهندسی مسیر بعدی پروژه است. این سند کد اجرایی نیست. این سند قرار است قبل از ورود به train، backtest، مدل‌های هوش مصنوعی و execution bridge، |
| [[docs/ai_execution/AMIR_STRUCTURAL_EXPERIENCE_MAP_FA|AMIR_STRUCTURAL_EXPERIENCE_MAP_FA.md]] | — | این سند، تجربه‌های خام امیر درباره بازار، اکستریم‌ها، اف‌شماری، هوک/رالی، سناریوهای دوطرفه، فرکتال و اجرای لیمیت را تبدیل می‌کند به یک چارچوب قابل‌کدنویسی، قابل |
| [[docs/ai_execution/EXPERIENCE_CAPTURE_LOG_TEMPLATE_FA|EXPERIENCE_CAPTURE_LOG_TEMPLATE_FA.md]] | — | این فایل قالب خام ثبت تجربه‌هاست. هر تجربه باید به یکی از این فرم‌ها تبدیل شود: |
| [[docs/ai_execution/EXTREME_L2_NODE_CYCLE_LIMIT_ENTRY_FA|EXTREME_L2_NODE_CYCLE_LIMIT_ENTRY_FA.md]] | — | این سند تعریف رسمی تجربه‌ی امیر درباره ورود در اکستریم‌هاست. موضوع اصلی: این سند کد اجرایی نیست. این سند پایه‌ی مرحله‌های بعدی است: در تصویر نمونه، ناحیه قرمز ح |
| [[docs/articles/distribution_engineering_for_conditional_sequence_extraction|distribution_engineering_for_conditional_sequence_extraction.md]] | EXP0012, H0008 | Decision Alpha Lab is moving from **edge discovery** to **distribution engineering**: the objective is not merely to find a strategy with positive expectancy, b |
| [[docs/articles/reversal_vs_continuation_execution|reversal_vs_continuation_execution.md]] | E0001, E0002, E0003, E0004, E0005, H0005 | Reversal and continuation are not two names for the same edge. They describe different market behaviors and require different execution logic. This article summ |
| [[docs/debug/E0006/MODULE_KERNEL_README|MODULE_KERNEL_README.md]] | E0006, M0001 | This document describes the reusable modules extracted from the E0006 execution work. The goal is to stop rewriting the same structural ideas inside every EA an |
| [[docs/debug/E0006/README|README.md]] | E0006, M0001 | E0006 is the execution-facing layer of Decision Alpha Lab. It does **not** try to discover an alpha by itself and it does **not** redefine the structural market |
| [[docs/debug/E0006_ALL_ZONE_TOUCH_LIMIT_README|E0006_ALL_ZONE_TOUCH_LIMIT_README.md]] | E0006, M0001 | E0006 is a lightweight execution module that uses existing M0001 / execution modules instead of rebuilding structure logic. Source of truth for zones: M0001 liv |
| [[docs/debug/E0008/README|README.md]] | E0007, E0008, M0001 | E0008 is the execution template that matches the user objective more directly than E0007: > We do not want every purple zone. > We want purple/source zones that |
| [[docs/debug/H4_DEEP_H6_OPTIONALITY_REPORT|H4_DEEP_H6_OPTIONALITY_REPORT.md]] | M0002, M0004 | This release extends the official M0004 atomic/no-sample report without reintroducing M0002 samples or fake same-candle ordering. `sampleCalls=0` `branchSamples |
| [[docs/debug/H6_CANDLE_STREAM_FAST|H6_CANDLE_STREAM_FAST.md]] | H0006, M0001, M0002 | Release 108 changes the standalone H0006 report from a heavy batch/edge-map workflow into a fast forward candle-stream workflow by default. Still atomic and no- |
| [[docs/debug/H6_FAST_ACCURATE_OPTIONALITY|H6_FAST_ACCURATE_OPTIONALITY.md]] | H0006, M0001 | This release makes the standalone H0006 optionality report faster and more execution-realistic without returning to samples. H6 remains atomic and no-sample: `s |
| [[docs/debug/H6_REACTION_BOX_ZONES|H6_REACTION_BOX_ZONES.md]] | M0001, M0002, M0006 | Release 112 changes the official H6 chart visual from simple horizontal survivor lines to reaction-zone rectangles. Contract: Raw M0001 nodes only. No M0002 bra |
| [[docs/debug/H6_STANDALONE_OPTIONALITY_EDGE_MAP|H6_STANDALONE_OPTIONALITY_EDGE_MAP.md]] | H0004, H0006, M0006 | H0006 is separated from H0004. H0004 remains the regime-memory hypothesis. H0006 tests a different question: > Are reversal known-time batches better optionalit |
| [[docs/execution/E0002_CLOSE_CONFIRMED_MARKET|E0002_CLOSE_CONFIRMED_MARKET.md]] | E0001, E0002, E0003, E0004, H0005, M0001 | `E0002_CloseConfirmedMarket.mq5` is a separate Expert Advisor from `E0001_ReversalOneToOne.mq5`. It does **not** add a mode to E0001 and does not modify the lim |
| [[docs/execution/E0003_CONTINUATION_CLOSE_HUNT|E0003_CONTINUATION_CLOSE_HUNT.md]] | E0001, E0002, E0003, E0004, H0005, M0001 | `E0003_ContinuationCloseHunt.mq5` is the third execution adapter for Decision Alpha Lab. It is separate from `E0001` and `E0002`. Build 1.06 adds a selectable D |
| [[docs/execution/E0004_CONTINUATION_HEIKIN_ASHI_FLIP|E0004_CONTINUATION_HEIKIN_ASHI_FLIP.md]] | E0001, E0002, E0003, E0004, M0001, M0002 | `E0004_ContinuationHeikinAshiFlip.mq5` is the fourth execution adapter for Decision Alpha Lab. It is intentionally separate from E0001, E0002, and E0003. E0004  |
| [[docs/execution/E0005_CONTINUATION_CLOSE_BREAK_FIXED_R|E0005_CONTINUATION_CLOSE_BREAK_FIXED_R.md]] | E0001, E0002, E0003, E0004, E0005, H0005 | E0005 is the fifth H0005 execution module. It is a separate Expert Advisor. It does not modify E0001, E0002, E0003, or E0004. E0005 trades only the continuation |

## Trace Targets

- Hypothesisهای مرتبط: از [[docs/obsidian_deep/04_relationships/entity_to_document_map|Entity Map]] پیدا شود.
- Experiments مرتبط: از [[docs/obsidian_deep/04_relationships/traceability_matrix|Traceability Matrix]] پیدا شود.
- Code مرتبط: از [[docs/obsidian_deep/04_relationships/code_to_concept_map|Code Map]] پیدا شود.
- تصمیم‌های معماری: در ADRها و patch notes ثبت شود.
