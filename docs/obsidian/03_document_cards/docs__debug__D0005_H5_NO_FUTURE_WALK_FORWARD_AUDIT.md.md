---
title: "D0005 — H5 No-Future Walk-Forward Audit"
type: document_card
generated_by: alpha_lab_obsidian_builder
generated_at: 2026-07-06
source_path: "docs/debug/D0005_H5_NO_FUTURE_WALK_FORWARD_AUDIT.md"
source_ext: ".md"
category: "debug_docs"
source_size_bytes: "2791"
entities:
  - "D0005"
  - "H0005"
  - "M0001"
  - "M0002"
concepts:
  - "Execution"
  - "MQL Native"
  - "NDS Anatomy"
  - "Structural Nodes"
  - "Validation"
---


# D0005 — H5 No-Future Walk-Forward Audit

**Source:** [[docs/debug/D0005_H5_NO_FUTURE_WALK_FORWARD_AUDIT|docs/debug/D0005_H5_NO_FUTURE_WALK_FORWARD_AUDIT.md]]

**Category:** `debug_docs`  
**Status:** ok  
**Size:** `2791` bytes

## خلاصه

D0005 is a diagnostic Expert Advisor for H0005/M0001/M0002 live-validity debugging. The goal is to detect and prevent look-ahead leakage in H5 regime and node logic. The audit does not build one full historical array at startup for decisions. Instead, it replays history candle by candle. On each simulated candle, it requests only the prefix ending at that candle and then rebuilds M0001 nodes, M0001 events, and M0002 branch regime from that prefix only. For every simulated step: 1. The cursor is a closed candle. 2. The EA calls `CopyRates` only for `oldest_time -> cursor_time`. 3. No candle after `cursor_time` is copied into the working `DALBar` array. 4. Structural nodes are accepted only wh

## Headings

- D0005 — H5 No-Future Walk-Forward Audit
-   Strict no-future contract
-   Main outputs
-   Recommended first run
-   Interpretation
-   Important distinction

## Entities

`D0005`, `H0005`, `M0001`, `M0002`

## Concepts

- [[docs/obsidian/04_concepts/Execution|Execution]]
- [[docs/obsidian/04_concepts/MQL_Native|MQL Native]]
- [[docs/obsidian/04_concepts/NDS_Anatomy|NDS Anatomy]]
- [[docs/obsidian/04_concepts/Structural_Nodes|Structural Nodes]]
- [[docs/obsidian/04_concepts/Validation|Validation]]

## Related documents

- [[docs/debug/D0006_H5_LIVE_TOUCH_REPLAY_AUDIT|D0006 — H5 Live Touch Replay Audit]] — `debug_docs`
- [[README|Decision Alpha Lab]] — `readme`
- [[docs/execution/E0002_CLOSE_CONFIRMED_MARKET|E0002 — H0005 Close-Confirmed Market Executor]] — `execution_docs`
- [[docs/execution/E0003_CONTINUATION_CLOSE_HUNT|E0003 — H0005 Continuation Close-Hunt Market Executor]] — `execution_docs`
- [[docs/execution/E0005_CONTINUATION_CLOSE_BREAK_FIXED_R|E0005 — Continuation Close-Break Fixed-R Executor]] — `execution_docs`
- [[docs/execution/H0005_R1_SIX_SLOT_TOUCH_LEDGER|H0005 Reversal Structural-Target-Capped Execution — Build 1.25]] — `execution_docs`
- [[docs/execution/README|Decision Alpha Lab — Execution]] — `execution_docs`
- [[docs/reports/2026-06-20_h4_h5_gold_m10_report|Report — H4/H5 GOLD M10 Review, 2026-06-20]] — `core_docs`
- [[lab/02_hypotheses/H0004_branch_regime_memory_atomic|H0004 — Branch Regime Memory]] — `hypothesis`
- [[lab/03_validation/VAL0005_h5_no_future_walk_forward/README|VAL0005 — H5 No-Future Walk-Forward Validation]] — `validation`
- [[lab/04_execution/EXE0002_close_confirmed_market/README|EXE0002 — Close-Confirmed Market After Touch]] — `execution`
- [[lab/03_experiments/EXP0003_mql_native_m0002/report|EXP0003 — M0002 Reversal/Continuation Exit Volatility]] — `experiment`

## Recommended Obsidian use

- این card را به نوت‌های concept، hypothesis، experiment یا ADR مربوط link کن.
- اگر این سند source of truth است، در MOC مربوطه بالاتر از اسناد legacy قرارش بده.
- اگر این سند report/validation است، نتیجه نهایی آن را به registry مربوط sync کن.
