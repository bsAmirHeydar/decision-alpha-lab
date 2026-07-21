---
title: "M0001 RTV Distribution Report — Retired Module Note"
type: document_card
generated_by: alpha_lab_obsidian_builder
generated_at: 2026-07-06
source_path: "docs/mql_native/M0001_RTV_DISTRIBUTION_REPORT.md"
source_ext: ".md"
category: "mql_native_docs"
source_size_bytes: "913"
entities:
  - "M0001"
concepts:
  - "MQL Native"
  - "NDS Anatomy"
---


# M0001 RTV Distribution Report — Retired Module Note

**Source:** [[docs/mql_native/M0001_RTV_DISTRIBUTION_REPORT|docs/mql_native/M0001_RTV_DISTRIBUTION_REPORT.md]]

**Category:** `mql_native_docs`  
**Status:** ok  
**Size:** `913` bytes

## خلاصه

This document describes the older verbose distribution-report phase from version `1.53`. The active runtime no longer includes: The current active report is the compact final-only node-vs-random logRTV report: The active statistical module is: It still preserves the important distribution logic in compact form: raw RTV mean/median/percentiles, logRTV mean/median, positive logRTV percentage, skewness, excess kurtosis, Jarque-Bera statistic, KS distance to fitted normal, tail ratios, node-vs-random paired comparison. For current semantics, use:

## Headings

- M0001 RTV Distribution Report — Retired Module Note

## Entities

`M0001`

## Concepts

- [[docs/obsidian/04_concepts/MQL_Native|MQL Native]]
- [[docs/evidence/nds_anatomy/6a11c75733b2_NDS_Anatomy|NDS Anatomy]]

## Related documents

- [[docs/mql_native/M0001_FINAL_VISUALS_AND_LOGIC_LOCK|M0001 Final Visuals and Logic Lock]] — `mql_native_docs`
- [[docs/evidence/exp0002_mql_native_m0001_runtime/319a21879dae_report|EXP0002 — MQL-native M0001 Runtime]] — `experiment`
- [[lab/03_experiments/EXP0003_mql_native_m0002/report|EXP0003 — M0002 Reversal/Continuation Exit Volatility]] — `experiment`
- [[docs/evidence/val_m0001_mql_native/454e81f9f0b3_report|VAL_M0001_MQL_NATIVE]] — `validation`
- [[lab/03_experiments/EXP0004_mql_native_m0004/report|EXP0004 — MQL-native M0004 Branch Regime Clustering]] — `experiment`
- [[docs/evidence/exp0000_sample/58c8a635ff91_report|Report]] — `experiment`
- [[docs/evidence/exp0001_structural_highs_lows_importance/337872464ffa_report|Report]] — `experiment`
- [[docs/evidence/val001/360462a17ab1_report|Report]] — `validation`
- [[docs/mql_native/H0007_FLAG_COUNTING_F1_START_STRUCTURE|H0007 — Flag Counting / F1 Start Structure]] — `mql_native_docs`
- [[docs/mql_native/M0001_ARROW_ANCHOR_COMPILE_FIX|M0001 Arrow Anchor Compile Fix]] — `mql_native_docs`
- [[docs/mql_native/M0001_CANDLE_GATED_RUNTIME|M0001 Candle-Gated Runtime]] — `mql_native_docs`
- [[docs/mql_native/M0001_CLEAN_REVISIT_LABELS|M0001 Clean Revisit Labels]] — `mql_native_docs`

## Recommended Obsidian use

- این card را به نوت‌های concept، hypothesis، experiment یا ADR مربوط link کن.
- اگر این سند source of truth است، در MOC مربوطه بالاتر از اسناد legacy قرارش بده.
- اگر این سند report/validation است، نتیجه نهایی آن را به registry مربوط sync کن.
