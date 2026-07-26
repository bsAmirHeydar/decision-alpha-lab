
---
type: canonical_concept
concept: "Zone / RTV"
generated_at: 2026-07-06
source_count: 327
---

# Zone / RTV

## تعریف عملیاتی

بازه یا قلمرو قیمتی که بر اساس node، revisit، reaction box یا RTV معنا می‌گیرد و می‌تواند محل واکنش، انفجار یا رد سناریو باشد.

## نقش در Alpha Lab

این مفهوم باید در یکی از چهار نقش زیر قرار بگیرد:

1. **زبان دیدن بازار**: کمک به خواندن ساختار.
2. **قانون تولید فرضیه**: تبدیل مشاهده به claim قابل تست.
3. **فیچر/شرط قابل اندازه‌گیری**: ورود به Python/MQL/Backtest.
4. **قید اجرایی/اعتبارسنجی**: محدود کردن خطا، repaint، leakage یا ریسک.

## روابط مستقیم

- [[docs/obsidian_deep/02_concepts/Decision_Node|Decision Node]]
- [[docs/obsidian_deep/02_concepts/Execution____Risk|Execution / Risk]]
- [[docs/obsidian_deep/02_concepts/Convexity____Optionality|Convexity / Optionality]]

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
| [[docs/ai_execution/EXTREME_L2_NODE_CYCLE_LIMIT_ENTRY_FA|EXTREME_L2_NODE_CYCLE_LIMIT_ENTRY_FA.md]] | — | این سند تعریف رسمی تجربه‌ی امیر درباره ورود در اکستریم‌هاست. موضوع اصلی: این سند کد اجرایی نیست. این سند پایه‌ی مرحله‌های بعدی است: در تصویر نمونه، ناحیه قرمز ح |
| [[docs/architecture|architecture.md]] | M0001, M0002, M0004, M0005 | Decision Alpha Lab uses a layered architecture for structural market research and execution. The project does not assume that fixed time windows are the natural |
| [[docs/articles/reversal_vs_continuation_execution|reversal_vs_continuation_execution.md]] | E0001, E0002, E0003, E0004, E0005, H0005 | Reversal and continuation are not two names for the same edge. They describe different market behaviors and require different execution logic. This article summ |
| [[docs/atomic_live_research_contract|atomic_live_research_contract.md]] | M0001 | This document defines the strict contract used to prevent future leakage, fake sequencing, and non-tradable R statistics. For every decision candle `t`, the eng |
| [[docs/debug/D0006_H5_LIVE_TOUCH_REPLAY_AUDIT|D0006_H5_LIVE_TOUCH_REPLAY_AUDIT.md]] | D0006, E0001, E0005, H0005, M0001, M0002 | D0006 is the strict live-validity audit for H0005 reversal touch-entry logic. It exists because full-history H5 reports can be useful for discovery, but they ar |
| [[docs/debug/D0007_H5_CAUSAL_LIVE_REPLAY_AUDIT|D0007_H5_CAUSAL_LIVE_REPLAY_AUDIT.md]] | D0007, H0004, H0005, M0004 | D0007 is the root live-validity validator for H0005. It exists because the old `DAL_M0005_FINAL_*` report is a structural path report, not a live execution proo |
| [[docs/debug/D0009_H5_ATOMIC_NO_SAMPLE_REPLAY_AUDIT|D0009_H5_ATOMIC_NO_SAMPLE_REPLAY_AUDIT.md]] | D0009, M0001 | D0009 is the strict H5 validator for the "do not build samples first" contract. It never calls `DAL_M0002CollectBranchSamples` and never creates `DALM0002Branch |
| [[docs/debug/E0006/ENTRY_QUALIFICATION_README|ENTRY_QUALIFICATION_README.md]] | E0006, M0001 | This document describes how E0006 decides whether a structural zone is allowed to receive a limit order. The entry decision is not simply “every zone gets an or |
| [[docs/debug/E0006/EXIT_AND_RISK_README|EXIT_AND_RISK_README.md]] | E0006, M0001 | This document explains how E0006 places entries, anchors stops, handles spread, sizes risk, and manages take profit after a trade opens. E0006 uses limit orders |
| [[docs/debug/E0006/INPUT_REFERENCE_README|INPUT_REFERENCE_README.md]] | E0006, M0001 | This file groups the current E0006 inputs by purpose. `InpSymbol=""` means current chart symbol. `InpTimeframe=PERIOD_CURRENT` means current chart timeframe. `I |
| [[docs/debug/E0006/MODULE_KERNEL_README|MODULE_KERNEL_README.md]] | E0006, M0001 | This document describes the reusable modules extracted from the E0006 execution work. The goal is to stop rewriting the same structural ideas inside every EA an |
| [[docs/debug/E0006/README|README.md]] | E0006, M0001 | E0006 is the execution-facing layer of Decision Alpha Lab. It does **not** try to discover an alpha by itself and it does **not** redefine the structural market |
| [[docs/debug/E0006/REVISIT_ONLY_README|REVISIT_ONLY_README.md]] | E0006, M0001 | The revisit-only mode is designed for experiments where the first touch of a zone is not traded. The zone must first survive a non-hunted touch cycle, then beco |
| [[docs/debug/E0006/REVISIT_SECONDARY_NODE_ANCHORS_README|REVISIT_SECONDARY_NODE_ANCHORS_README.md]] | E0006 | This document defines the third stop-anchor mode and the second revisit-entry mode added after the original E0006 execution design. In the first E0006 revisit m |
| [[docs/debug/E0006_ALL_ZONE_TOUCH_LIMIT_README|E0006_ALL_ZONE_TOUCH_LIMIT_README.md]] | E0006, M0001 | E0006 is a lightweight execution module that uses existing M0001 / execution modules instead of rebuilding structure logic. Source of truth for zones: M0001 liv |
| [[docs/debug/E0007/README|README.md]] | E0007 | E0007 is the first execution template for the idea that came from the purple-zone screenshots: > Purple is not the signal. Purple is the context. > The trade is |
| [[docs/debug/E0008/README|README.md]] | E0007, E0008, M0001 | E0008 is the execution template that matches the user objective more directly than E0007: > We do not want every purple zone. > We want purple/source zones that |

## Trace Targets

- Hypothesisهای مرتبط: از [[docs/obsidian_deep/04_relationships/entity_to_document_map|Entity Map]] پیدا شود.
- Experiments مرتبط: از [[docs/obsidian_deep/04_relationships/traceability_matrix|Traceability Matrix]] پیدا شود.
- Code مرتبط: از [[docs/obsidian_deep/04_relationships/code_to_concept_map|Code Map]] پیدا شود.
- تصمیم‌های معماری: در ADRها و patch notes ثبت شود.
