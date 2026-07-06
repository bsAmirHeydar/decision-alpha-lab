
---
type: canonical_concept
concept: "Python Brain"
generated_at: 2026-07-06
source_count: 329
---

# Python Brain

## تعریف عملیاتی

موتور پژوهش، تولید گزارش، استخراج داده، feature engineering و backtest/analysis.

## نقش در Alpha Lab

این مفهوم باید در یکی از چهار نقش زیر قرار بگیرد:

1. **زبان دیدن بازار**: کمک به خواندن ساختار.
2. **قانون تولید فرضیه**: تبدیل مشاهده به claim قابل تست.
3. **فیچر/شرط قابل اندازه‌گیری**: ورود به Python/MQL/Backtest.
4. **قید اجرایی/اعتبارسنجی**: محدود کردن خطا، repaint، leakage یا ریسک.

## روابط مستقیم

- [[docs/obsidian_deep/02_concepts/MQL_Native|MQL Native]]
- [[docs/obsidian_deep/02_concepts/Validation____Audit|Validation / Audit]]
- [[docs/obsidian_deep/02_concepts/AI_Agent_Layer|AI Agent Layer]]

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
| [[docs/debug/D0005_H5_NO_FUTURE_WALK_FORWARD_AUDIT|D0005_H5_NO_FUTURE_WALK_FORWARD_AUDIT.md]] | D0005, H0005, M0001, M0002 | D0005 is a diagnostic Expert Advisor for H0005/M0001/M0002 live-validity debugging. The goal is to detect and prevent look-ahead leakage in H5 regime and node l |
| [[docs/debug/D0006_H5_LIVE_TOUCH_REPLAY_AUDIT|D0006_H5_LIVE_TOUCH_REPLAY_AUDIT.md]] | D0006, E0001, E0005, H0005, M0001, M0002 | D0006 is the strict live-validity audit for H0005 reversal touch-entry logic. It exists because full-history H5 reports can be useful for discovery, but they ar |
| [[docs/debug/H4_FAST_ATOMIC_MAIN_REPORT|H4_FAST_ATOMIC_MAIN_REPORT.md]] | M0001, M0002, M0004 | M0004 build 1.07 keeps the official no-sample contract but removes the heavy strict prefix replay from the default main report path. The first atomic no-sample  |
| [[docs/execution/EXP0016_intermarket_divergence_execution/LEVEL_02_STC_SMT_TIME_ENGINE|LEVEL_02_STC_SMT_TIME_ENGINE.md]] | — | Status: implemented in patch `EXP0016_STC_SMT_LEVEL02_TIME_ENGINE`. This level is still a no-trade layer. It does not build W highs/lows, does not detect SMT di |
| [[docs/execution/EXP0016_intermarket_divergence_execution/LEVEL_03_STC_SMT_CHECK_CANDLE_AGGREGATOR|LEVEL_03_STC_SMT_CHECK_CANDLE_AGGREGATOR.md]] | EXEC001 | This document mirrors the implementation-level notes for: `lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/24_level_03_check_ca |
| [[docs/execution/EXP0016_intermarket_divergence_execution/LEVEL_04_STC_SMT_W_LEVEL_BUILDER|LEVEL_04_STC_SMT_W_LEVEL_BUILDER.md]] | — | Level 04 adds the first structural market object required by STC: the closed 90-minute W high/low levels for both symbols. This level is still non-trading. It d |
| [[docs/execution/EXP0016_intermarket_divergence_execution/LEVEL_05_STC_SMT_REFERENCE_HUNT_DETECTOR|LEVEL_05_STC_SMT_REFERENCE_HUNT_DETECTOR.md]] | — | Level 05 adds the previous-W reference matrix and raw touch-only hunt detector for `EXEC001_STC_SMT_Cycles`. It is still an audit-only level. It creates no SMT  |
| [[docs/execution/EXP0016_intermarket_divergence_execution/LEVEL_06_STC_SMT_CANDIDATE_ENGINE|LEVEL_06_STC_SMT_CANDIDATE_ENGINE.md]] | EXEC001 | This document indexes the Level 06 implementation for EXEC001 STC SMT Cycles. Level 06 converts raw touch-only previous-W hunts into audit-only SMT candidate ro |
| [[docs/execution/EXP0016_intermarket_divergence_execution/LEVEL_07_STC_SMT_CONFIRMATION_SIGNAL_REGISTRY|LEVEL_07_STC_SMT_CONFIRMATION_SIGNAL_REGISTRY.md]] | — | Level 07 adds the first signal registry layer for `EXEC001_STC_SMT_Cycles`. It confirms Level 06 SMT candidates at the close of their check candle and writes co |
| [[docs/execution/EXP0016_intermarket_divergence_execution/LEVEL_08_STC_SMT_RISK_PLAN_PAPER_ENTRY|LEVEL_08_STC_SMT_RISK_PLAN_PAPER_ENTRY.md]] | EXEC001 | Level 08 adds the no-order paper entry model for EXEC001 STC SMT Cycles. It converts confirmed Level 07 signals into paper trade plans using: next-check open en |
| [[docs/execution/EXP0016_intermarket_divergence_execution/LEVEL_09_STC_SMT_PAPER_OUTCOME_SIMULATOR|LEVEL_09_STC_SMT_PAPER_OUTCOME_SIMULATOR.md]] | EXEC001 | This level adds the audit-only paper outcome layer for EXEC001 STC SMT Cycles. It scans closed check candles after planned paper entries and writes TP, SL, AMBI |
| [[docs/execution/EXP0016_intermarket_divergence_execution/LEVEL_10_STC_SMT_PARTIAL_CLOSE_SIMULATOR|LEVEL_10_STC_SMT_PARTIAL_CLOSE_SIMULATOR.md]] | EXEC001 | This level adds paper partial-close accounting for EXEC001 STC SMT Cycles. The EA remains no-order. It writes `stc_level10_partial_actions.csv` and simulates on |
| [[docs/execution/EXP0016_intermarket_divergence_execution/LEVEL_11_STC_SMT_HARD_CLOSE_SIMULATOR|LEVEL_11_STC_SMT_HARD_CLOSE_SIMULATOR.md]] | EXEC001 | Level 11 adds paper-only 15:30 New York hard-close accounting for EXEC001 STC SMT Cycles. It extends Level 10 by adding: a new hard-close audit file, 15:30 New  |
| [[docs/execution/EXP0016_intermarket_divergence_execution/LEVEL_12_STC_SMT_PERSISTENCE_RESTART_RECOVERY|LEVEL_12_STC_SMT_PERSISTENCE_RESTART_RECOVERY.md]] | — | Level 12 adds current-day persistence for the paper/audit engine of `EXEC001_STC_SMT_Cycles`. It writes: `stc_level12_persistence_snapshot.csv` `stc_level12_per |
| [[docs/execution/EXP0016_intermarket_divergence_execution/LEVEL_13_STC_SMT_VISUALIZATION_AUDIT_DRAWING|LEVEL_13_STC_SMT_VISUALIZATION_AUDIT_DRAWING.md]] | EXEC001 | This patch adds chart-side visualization for the EXEC001 STC SMT Cycles paper execution stack. It draws audit objects only. It does not place orders, modify sig |

## Trace Targets

- Hypothesisهای مرتبط: از [[docs/obsidian_deep/04_relationships/entity_to_document_map|Entity Map]] پیدا شود.
- Experiments مرتبط: از [[docs/obsidian_deep/04_relationships/traceability_matrix|Traceability Matrix]] پیدا شود.
- Code مرتبط: از [[docs/obsidian_deep/04_relationships/code_to_concept_map|Code Map]] پیدا شود.
- تصمیم‌های معماری: در ADRها و patch notes ثبت شود.
