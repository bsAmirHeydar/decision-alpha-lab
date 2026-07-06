
---
type: canonical_concept
concept: "AI Agent Layer"
generated_at: 2026-07-06
source_count: 306
---

# AI Agent Layer

## تعریف عملیاتی

لایه automation برای پژوهش، پچ، validation، Obsidian maintenance و ژورنال؛ نه authority برای live order.

## نقش در Alpha Lab

این مفهوم باید در یکی از چهار نقش زیر قرار بگیرد:

1. **زبان دیدن بازار**: کمک به خواندن ساختار.
2. **قانون تولید فرضیه**: تبدیل مشاهده به claim قابل تست.
3. **فیچر/شرط قابل اندازه‌گیری**: ورود به Python/MQL/Backtest.
4. **قید اجرایی/اعتبارسنجی**: محدود کردن خطا، repaint، leakage یا ریسک.

## روابط مستقیم

- [[docs/obsidian_deep/02_concepts/Obsidian_Knowledge_OS|Obsidian Knowledge OS]]
- [[docs/obsidian_deep/02_concepts/Python_Brain|Python Brain]]
- [[docs/obsidian_deep/02_concepts/Validation____Audit|Validation / Audit]]
- [[docs/obsidian_deep/02_concepts/Execution____Risk|Execution / Risk]]

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
| [[docs/ai_execution/README|README.md]] | — | این پوشه برای اسناد مسیر هوش مصنوعی، بک‌تست، episode، label، algorithm layers و execution bridge است. تعریف رسمی تجربه امیر درباره ورود در اکستریم نزدیک نود L2  |
| [[docs/architecture|architecture.md]] | M0001, M0002, M0004, M0005 | Decision Alpha Lab uses a layered architecture for structural market research and execution. The project does not assume that fixed time windows are the natural |
| [[docs/articles/structural_regime_memory_without_samples|structural_regime_memory_without_samples.md]] | H0004, M0001, M0002 | A central question of Decision Alpha Lab is whether structural market regimes have memory. Early reports suggested that reversal and continuation labels cluster |
| [[docs/atomic_live_research_contract|atomic_live_research_contract.md]] | M0001 | This document defines the strict contract used to prevent future leakage, fake sequencing, and non-tradable R statistics. For every decision candle `t`, the eng |
| [[docs/debug/D0007_H5_CAUSAL_LIVE_REPLAY_AUDIT|D0007_H5_CAUSAL_LIVE_REPLAY_AUDIT.md]] | D0007, H0004, H0005, M0004 | D0007 is the root live-validity validator for H0005. It exists because the old `DAL_M0005_FINAL_*` report is a structural path report, not a live execution proo |
| [[docs/debug/D0008_H4_CAUSAL_BATCH_REPORT|D0008_H4_CAUSAL_BATCH_REPORT.md]] | D0008, H0004 | This release fixes the main H0004 live-validity ambiguity: multiple branch samples can become knowable on the same candle. The classic H0004 report sorts sample |
| [[docs/debug/D0010_H4_ATOMIC_NO_SAMPLE_REGIME_AUDIT|D0010_H4_ATOMIC_NO_SAMPLE_REGIME_AUDIT.md]] | D0010, H0004, M0001, M0002, M0004 | D0010 is the strict live-style validator for H0004 regime memory. It removes M0002 branch samples from the H4 validation path: no `DALM0002BranchSample` no `DAL |
| [[docs/debug/E0007/README|README.md]] | E0007 | E0007 is the first execution template for the idea that came from the purple-zone screenshots: > Purple is not the signal. Purple is the context. > The trade is |
| [[docs/debug/E0008/README|README.md]] | E0007, E0008, M0001 | E0008 is the execution template that matches the user objective more directly than E0007: > We do not want every purple zone. > We want purple/source zones that |
| [[docs/debug/H4_DEEP_H6_OPTIONALITY_REPORT|H4_DEEP_H6_OPTIONALITY_REPORT.md]] | M0002, M0004 | This release extends the official M0004 atomic/no-sample report without reintroducing M0002 samples or fake same-candle ordering. `sampleCalls=0` `branchSamples |
| [[docs/debug/H6_REACTION_BOX_ZONES|H6_REACTION_BOX_ZONES.md]] | M0001, M0002, M0006 | Release 112 changes the official H6 chart visual from simple horizontal survivor lines to reaction-zone rectangles. Contract: Raw M0001 nodes only. No M0002 bra |
| [[docs/debug/H6_STANDALONE_OPTIONALITY_EDGE_MAP|H6_STANDALONE_OPTIONALITY_EDGE_MAP.md]] | H0004, H0006, M0006 | H0006 is separated from H0004. H0004 remains the regime-memory hypothesis. H0006 tests a different question: > Are reversal known-time batches better optionalit |
| [[docs/debug/MARKET_LANGUAGE/README|README.md]] | M0007 | > Version: draft 0.2 > Scope: discretionary-to-algorithmic vocabulary for Decision Alpha Lab > Purpose: convert the manual multi-timeframe market-reading langua |
| [[docs/execution/E0002_CLOSE_CONFIRMED_MARKET|E0002_CLOSE_CONFIRMED_MARKET.md]] | E0001, E0002, E0003, E0004, H0005, M0001 | `E0002_CloseConfirmedMarket.mq5` is a separate Expert Advisor from `E0001_ReversalOneToOne.mq5`. It does **not** add a mode to E0001 and does not modify the lim |
| [[docs/execution/EXP0016_intermarket_divergence_execution/LEVEL_13_STC_SMT_VISUALIZATION_AUDIT_DRAWING|LEVEL_13_STC_SMT_VISUALIZATION_AUDIT_DRAWING.md]] | EXEC001 | This patch adds chart-side visualization for the EXEC001 STC SMT Cycles paper execution stack. It draws audit objects only. It does not place orders, modify sig |

## Trace Targets

- Hypothesisهای مرتبط: از [[docs/obsidian_deep/04_relationships/entity_to_document_map|Entity Map]] پیدا شود.
- Experiments مرتبط: از [[docs/obsidian_deep/04_relationships/traceability_matrix|Traceability Matrix]] پیدا شود.
- Code مرتبط: از [[docs/obsidian_deep/04_relationships/code_to_concept_map|Code Map]] پیدا شود.
- تصمیم‌های معماری: در ADRها و patch notes ثبت شود.
