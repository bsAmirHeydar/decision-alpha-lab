
---
type: canonical_concept
concept: "Intermarket Divergence"
generated_at: 2026-07-06
source_count: 93
---

# Intermarket Divergence

## تعریف عملیاتی

تحلیل واگرایی زمانی/ساختاری بین چند نماد یا بازار؛ مرتبط با SMT، CME و execution profiles.

## نقش در Alpha Lab

این مفهوم باید در یکی از چهار نقش زیر قرار بگیرد:

1. **زبان دیدن بازار**: کمک به خواندن ساختار.
2. **قانون تولید فرضیه**: تبدیل مشاهده به claim قابل تست.
3. **فیچر/شرط قابل اندازه‌گیری**: ورود به Python/MQL/Backtest.
4. **قید اجرایی/اعتبارسنجی**: محدود کردن خطا، repaint، leakage یا ریسک.

## روابط مستقیم

- [[docs/obsidian_deep/02_concepts/Execution____Risk|Execution / Risk]]
- [[docs/obsidian_deep/02_concepts/Validation____Audit|Validation / Audit]]
- [[docs/obsidian_deep/02_concepts/Python_Brain|Python Brain]]

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
| [[docs/execution/EXP0015_intermarket_time_divergence/LEGACY_COMPILE_FIX|LEGACY_COMPILE_FIX.md]] | EXP0015 | This patch fixes compile errors triggered by the deprecated expert: `mql5/Experts/IntermarketDivergence/IMD001_SPX_NDX_TimeDivergence.mq5` `mql5/Include/Interma |
| [[docs/execution/EXP0016_intermarket_divergence_execution/IMPLEMENTATION_PLAN_INDEX|IMPLEMENTATION_PLAN_INDEX.md]] | EXEC001, EXP0016 | The EXEC001 STC SMT Cycles implementation plan is documented in the strategy folder: `17_implementation_plan.md` — full staged implementation plan `18_module_br |
| [[docs/execution/EXP0016_intermarket_divergence_execution/LEVEL_01_STC_SMT_SKELETON|LEVEL_01_STC_SMT_SKELETON.md]] | — | This patch adds the first compileable MQL5 shell for `EXEC001_STC_SMT_Cycles`. The level is deliberately safe: it validates inputs, creates runtime journals, st |
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
| [[docs/execution/EXP0016_intermarket_divergence_execution/LEVEL_14_STC_SMT_PAPER_LIVE_ALERTS|LEVEL_14_STC_SMT_PAPER_LIVE_ALERTS.md]] | EXEC001 | Level 14 adds no-order paper-live alerts for EXEC001 STC SMT Cycles. It monitors newly created signal registry rows, paper entries, paper outcomes, partial acti |
| [[docs/execution/EXP0016_intermarket_divergence_execution/LEVEL_15_STC_SMT_BROKER_POSITION_MANAGER|LEVEL_15_STC_SMT_BROKER_POSITION_MANAGER.md]] | — | This level adds a magic-only broker position safety layer for `EXEC001_STC_SMT_Cycles`. It does not enable auto-entry. It only scans real broker positions, audi |
| [[docs/execution/EXP0016_intermarket_divergence_execution/LEVEL_16_STC_SMT_REAL_AUTO_ENTRY_ROUTER|LEVEL_16_STC_SMT_REAL_AUTO_ENTRY_ROUTER.md]] | — | Patch scope: gated real market entry from confirmed STC paper plans. Main document: `lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_C |
| [[docs/execution/EXP0016_intermarket_divergence_execution/LEVEL_17_STC_SMT_REAL_PARTIAL_CLOSE_MANAGER|LEVEL_17_STC_SMT_REAL_PARTIAL_CLOSE_MANAGER.md]] | EXEC001 | Level 17 adds a magic-only real broker partial close layer for EXEC001 STC SMT Cycles. It is disabled by default and only closes real broker volume when the use |
| [[docs/execution/EXP0016_intermarket_divergence_execution/LEVEL_18_STC_SMT_REAL_HARD_CLOSE_FINALIZER|LEVEL_18_STC_SMT_REAL_HARD_CLOSE_FINALIZER.md]] | EXEC001 | Patch scope: add the final real broker hard-close layer for EXEC001 STC SMT Cycles. This level is disabled by default. When explicitly enabled, it retries closi |

## Trace Targets

- Hypothesisهای مرتبط: از [[docs/obsidian_deep/04_relationships/entity_to_document_map|Entity Map]] پیدا شود.
- Experiments مرتبط: از [[docs/obsidian_deep/04_relationships/traceability_matrix|Traceability Matrix]] پیدا شود.
- Code مرتبط: از [[docs/obsidian_deep/04_relationships/code_to_concept_map|Code Map]] پیدا شود.
- تصمیم‌های معماری: در ADRها و patch notes ثبت شود.
