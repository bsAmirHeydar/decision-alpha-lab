---
title: "H0006 standalone optionality and edge-map report"
type: document_card
generated_by: alpha_lab_obsidian_builder
generated_at: 2026-07-06
source_path: "docs/debug/H6_STANDALONE_OPTIONALITY_EDGE_MAP.md"
source_ext: ".md"
category: "debug_docs"
source_size_bytes: "2280"
entities:
  - "H0004"
  - "H0006"
  - "M0006"
concepts:
  - "AI Agent Layer"
  - "Atomic No-Sample"
  - "Convexity"
  - "Known-Time Causality"
  - "MQL Native"
  - "Validation"
---


# H0006 standalone optionality and edge-map report

**Source:** [[docs/debug/H6_STANDALONE_OPTIONALITY_EDGE_MAP|docs/debug/H6_STANDALONE_OPTIONALITY_EDGE_MAP.md]]

**Category:** `debug_docs`  
**Status:** ok  
**Size:** `2280` bytes

## خلاصه

H0006 is separated from H0004. H0004 remains the regime-memory hypothesis. H0006 tests a different question: > Are reversal known-time batches better optionality points for future explosive movement, independent of ordinary win-rate? The standalone expert is: It uses the same atomic no-sample known-time batch contract as H0004: `DAL_H0006_OPTIONALITY_FAST/MAIN/SLOW` compare reversal and continuation batches by future ATR-normalized movement after the known-time candle. The report does not claim win-rate. It measures optionality: absolute future excursion in ATR units directional MFE in ATR units adverse excursion in ATR units p90 / p95 / p99 tails hit rates above configurable ATR thresholds

## Headings

- H0006 standalone optionality and edge-map report
-   Reports
-   Materiality labels
-   Why this exists

## Entities

`H0004`, `H0006`, `M0006`

## Concepts

- [[docs/obsidian/04_concepts/AI_Agent_Layer|AI Agent Layer]]
- [[docs/obsidian/04_concepts/Atomic_No-Sample|Atomic No-Sample]]
- [[docs/obsidian/04_concepts/Convexity|Convexity]]
- [[docs/obsidian/04_concepts/Known-Time_Causality|Known-Time Causality]]
- [[docs/obsidian/04_concepts/MQL_Native|MQL Native]]
- [[docs/obsidian/04_concepts/Validation|Validation]]

## Related documents

- [[lab/03_validation/VAL0016_h6_standalone_optionality/README|VAL0016 — H6 standalone optionality edge map]] — `validation`
- [[docs/mql_native/H0007_FLAG_COUNTING_F1_START_STRUCTURE|H0007 — Flag Counting / F1 Start Structure]] — `mql_native_docs`
- [[docs/debug/D0008_H4_CAUSAL_BATCH_REPORT|D0008 / H0004 Causal Known-Candle Batch Report]] — `debug_docs`
- [[docs/debug/D0010_H4_ATOMIC_NO_SAMPLE_REGIME_AUDIT|D0010 — H4 Atomic No-Sample Regime Audit]] — `debug_docs`
- [[docs/debug/H6_CANDLE_STREAM_FAST|H6 Candle-Stream Fast Optionality]] — `debug_docs`
- [[docs/debug/H6_FAST_ACCURATE_OPTIONALITY|H6 Fast Accurate Optionality Report]] — `debug_docs`
- [[docs/debug/H6_REACTION_BOX_ZONES|H6 Reaction Box Zones]] — `debug_docs`
- [[lab/02_hypotheses/H0004_branch_regime_memory_atomic|H0004 — Branch Regime Memory]] — `hypothesis`
- [[lab/03_validation/VAL0008_h4_causal_batch/README|VAL0008 — H4 Causal Batch Validation]] — `validation`
- [[README|Decision Alpha Lab]] — `readme`
- [[lab/03_validation/VAL0017_h6_fast_accurate/README|VAL0017 — H6 Fast Accurate Optionality]] — `validation`
- [[docs/debug/D0007_H5_CAUSAL_LIVE_REPLAY_AUDIT|D0007 — H5 Causal Live Replay Audit]] — `debug_docs`

## Recommended Obsidian use

- این card را به نوت‌های concept، hypothesis، experiment یا ADR مربوط link کن.
- اگر این سند source of truth است، در MOC مربوطه بالاتر از اسناد legacy قرارش بده.
- اگر این سند report/validation است، نتیجه نهایی آن را به registry مربوط sync کن.
