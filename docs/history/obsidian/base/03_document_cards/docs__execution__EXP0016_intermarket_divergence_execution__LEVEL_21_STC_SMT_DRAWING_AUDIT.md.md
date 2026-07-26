---
title: "LEVEL 21 — STC SMT Drawing Audit Hardening"
type: document_card
generated_by: alpha_lab_obsidian_builder
generated_at: 2026-07-06
source_path: "docs/execution/EXP0016_intermarket_divergence_execution/LEVEL_21_STC_SMT_DRAWING_AUDIT.md"
source_ext: ".md"
category: "execution_docs"
source_size_bytes: "809"
concepts:
  - "AI Agent Layer"
  - "Execution"
  - "Intermarket Divergence"
  - "Validation"
---


# LEVEL 21 — STC SMT Drawing Audit Hardening

**Source:** [[docs/execution/EXP0016_intermarket_divergence_execution/LEVEL_21_STC_SMT_DRAWING_AUDIT|docs/execution/EXP0016_intermarket_divergence_execution/LEVEL_21_STC_SMT_DRAWING_AUDIT.md]]

**Category:** `execution_docs`  
**Status:** ok  
**Size:** `809` bytes

## خلاصه

Level 21 is a visual verification patch for `EXEC001_STC_SMT_Cycles`. It improves the chart overlay so an operator can verify the locked STC rules directly on the active `Symbol1` or `Symbol2` chart: New York STC session structure. M cycles and no-entry gaps. W boundaries and closed W high/low levels. Recent check-candle boxes. W1 no-signal and final-check no-entry conditions. Raw previous-W hunt markers. BOTH-hunted no-SMT cases. Clean-symbol SMT side and selected reference. Paper entry, SL, TP, W4 partial marker, 15:30 hard-close marker and outcome labels. No trading logic changes were made. The patch also fixes the hard-close compile warning by explicitly casting `SYMBOL_SPREAD` to `doubl

## Headings

- LEVEL 21 — STC SMT Drawing Audit Hardening

## Concepts

- [[docs/obsidian/04_concepts/AI_Agent_Layer|AI Agent Layer]]
- [[docs/obsidian/04_concepts/Execution|Execution]]
- [[docs/obsidian/04_concepts/Intermarket_Divergence|Intermarket Divergence]]
- [[docs/obsidian/04_concepts/Validation|Validation]]

## Related documents

- [[lab/03_experiments/EXP0004_mql_native_m0004/report|EXP0004 — MQL-native M0004 Branch Regime Clustering]] — `experiment`
- [[docs/execution/EXP0016_intermarket_divergence_execution/LEVEL_13_STC_SMT_VISUALIZATION_AUDIT_DRAWING|LEVEL 13 — EXEC001 STC SMT Visualization / Audit Drawing]] — `execution_docs`
- [[lab/03_experiments/EXP0002_mql_native_m0001/report|EXP0002 — MQL-native M0001 Runtime]] — `experiment`
- [[lab/03_experiments/EXP0003_mql_native_m0002/report|EXP0003 — M0002 Reversal/Continuation Exit Volatility]] — `experiment`
- [[lab/05_validation/VAL001/report|Report]] — `validation`
- [[lab/05_validation/VAL_M0001_MQL_NATIVE/report|VAL_M0001_MQL_NATIVE]] — `validation`
- [[docs/execution/EXP0016_intermarket_divergence_execution/LEVEL_02_STC_SMT_TIME_ENGINE|Level 02 — STC Time Engine and Cycle Classifier]] — `execution_docs`
- [[docs/execution/EXP0016_intermarket_divergence_execution/LEVEL_03_STC_SMT_CHECK_CANDLE_AGGREGATOR|LEVEL 03 — STC SMT Check Candle Aggregator]] — `execution_docs`
- [[docs/execution/EXP0016_intermarket_divergence_execution/LEVEL_04_STC_SMT_W_LEVEL_BUILDER|Level 04 — W Level Builder]] — `execution_docs`
- [[docs/execution/EXP0016_intermarket_divergence_execution/LEVEL_05_STC_SMT_REFERENCE_HUNT_DETECTOR|Level 05 — STC SMT Reference Matrix and Raw Hunt Detector]] — `execution_docs`
- [[docs/execution/EXP0016_intermarket_divergence_execution/LEVEL_06_STC_SMT_CANDIDATE_ENGINE|Level 06 STC SMT Candidate Engine]] — `execution_docs`
- [[docs/execution/EXP0016_intermarket_divergence_execution/LEVEL_07_STC_SMT_CONFIRMATION_SIGNAL_REGISTRY|LEVEL 07 STC SMT Confirmation and Signal Registry]] — `execution_docs`

## Recommended Obsidian use

- این card را به نوت‌های concept، hypothesis، experiment یا ADR مربوط link کن.
- اگر این سند source of truth است، در MOC مربوطه بالاتر از اسناد legacy قرارش بده.
- اگر این سند report/validation است، نتیجه نهایی آن را به registry مربوط sync کن.
