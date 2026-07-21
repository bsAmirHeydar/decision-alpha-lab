---
title: "Level 06 STC SMT Candidate Engine"
type: document_card
generated_by: alpha_lab_obsidian_builder
generated_at: 2026-07-06
source_path: "docs/execution/EXP0016_intermarket_divergence_execution/LEVEL_06_STC_SMT_CANDIDATE_ENGINE.md"
source_ext: ".md"
category: "execution_docs"
source_size_bytes: "732"
entities:
  - "EXEC001"
concepts:
  - "Execution"
  - "Intermarket Divergence"
  - "Validation"
---


# Level 06 STC SMT Candidate Engine

**Source:** [[docs/execution/EXP0016_intermarket_divergence_execution/LEVEL_06_STC_SMT_CANDIDATE_ENGINE|docs/execution/EXP0016_intermarket_divergence_execution/LEVEL_06_STC_SMT_CANDIDATE_ENGINE.md]]

**Category:** `execution_docs`  
**Status:** ok  
**Size:** `732` bytes

## خلاصه

This document indexes the Level 06 implementation for EXEC001 STC SMT Cycles. Level 06 converts raw touch-only previous-W hunts into audit-only SMT candidate rows. It adds: high-side SMT candidate detection, low-side SMT candidate detection, clean-symbol trade mapping, same-check buy/sell forgetting, largest-stop reference selection using the clean symbol check close as the provisional entry proxy, candidate audit CSV output. It still does not confirm, consume, trade, simulate, draw, partially close, or hard-close positions. Primary detailed document: `docs/evidence/level_06_smt_candidate_engine/97fffdd7f422_27_level_06_smt_candidate_engine.md`

## Headings

- Level 06 STC SMT Candidate Engine

## Entities

`EXEC001`

## Concepts

- [[docs/obsidian/04_concepts/Execution|Execution]]
- [[docs/obsidian/04_concepts/Intermarket_Divergence|Intermarket Divergence]]
- [[docs/obsidian/04_concepts/Validation|Validation]]

## Related documents

- [[docs/evidence/level_06_smt_candidate_engine/97fffdd7f422_27_level_06_smt_candidate_engine|Level 06 — SMT Candidate Engine]] — `experiment`
- [[docs/execution/EXP0016_intermarket_divergence_execution/LEVEL_03_STC_SMT_CHECK_CANDLE_AGGREGATOR|LEVEL 03 — STC SMT Check Candle Aggregator]] — `execution_docs`
- [[docs/execution/EXP0016_intermarket_divergence_execution/LEVEL_08_STC_SMT_RISK_PLAN_PAPER_ENTRY|Level 08 STC SMT Risk Plan and Paper Entry]] — `execution_docs`
- [[docs/execution/EXP0016_intermarket_divergence_execution/LEVEL_09_STC_SMT_PAPER_OUTCOME_SIMULATOR|LEVEL 09 — STC SMT Paper Outcome Simulator]] — `execution_docs`
- [[docs/execution/EXP0016_intermarket_divergence_execution/LEVEL_11_STC_SMT_HARD_CLOSE_SIMULATOR|Level 11 STC SMT Hard Close Simulator]] — `execution_docs`
- [[docs/execution/EXP0016_intermarket_divergence_execution/LEVEL_13_STC_SMT_VISUALIZATION_AUDIT_DRAWING|LEVEL 13 — EXEC001 STC SMT Visualization / Audit Drawing]] — `execution_docs`
- [[docs/execution/EXP0016_intermarket_divergence_execution/LEVEL_14_STC_SMT_PAPER_LIVE_ALERTS|Level 14 — STC SMT Paper Live Alerts]] — `execution_docs`
- [[docs/execution/EXP0016_intermarket_divergence_execution/LEVEL_18_STC_SMT_REAL_HARD_CLOSE_FINALIZER|LEVEL 18 — STC SMT Real Hard Close Finalizer]] — `execution_docs`
- [[docs/execution/EXP0016_intermarket_divergence_execution/README|EXP0016 Intermarket Divergence Execution Documentation]] — `execution_docs`
- [[docs/execution/EXP0016_intermarket_divergence_execution/IMPLEMENTATION_PLAN_INDEX|EXP0016 Intermarket Divergence Execution — Implementation Plan Index]] — `execution_docs`
- [[docs/execution/EXP0016_intermarket_divergence_execution/LEVEL_10_STC_SMT_PARTIAL_CLOSE_SIMULATOR|LEVEL 10 — STC SMT Partial Close Simulator]] — `execution_docs`
- [[docs/execution/EXP0016_intermarket_divergence_execution/LEVEL_17_STC_SMT_REAL_PARTIAL_CLOSE_MANAGER|LEVEL 17 — STC SMT Real Partial Close Manager]] — `execution_docs`

## Recommended Obsidian use

- این card را به نوت‌های concept، hypothesis، experiment یا ADR مربوط link کن.
- اگر این سند source of truth است، در MOC مربوطه بالاتر از اسناد legacy قرارش بده.
- اگر این سند report/validation است، نتیجه نهایی آن را به registry مربوط sync کن.
