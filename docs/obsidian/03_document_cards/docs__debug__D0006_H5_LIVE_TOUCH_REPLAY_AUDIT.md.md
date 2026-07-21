---
title: "D0006 — H5 Live Touch Replay Audit"
type: document_card
generated_by: alpha_lab_obsidian_builder
generated_at: 2026-07-06
source_path: "docs/debug/D0006_H5_LIVE_TOUCH_REPLAY_AUDIT.md"
source_ext: ".md"
category: "debug_docs"
source_size_bytes: "2270"
entities:
  - "D0006"
  - "E0001"
  - "E0005"
  - "H0005"
  - "M0001"
  - "M0002"
concepts:
  - "Execution"
  - "Licensing"
  - "MQL Native"
  - "NDS Anatomy"
  - "Structural Nodes"
  - "Validation"
---


# D0006 — H5 Live Touch Replay Audit

**Source:** [[docs/debug/D0006_H5_LIVE_TOUCH_REPLAY_AUDIT|docs/debug/D0006_H5_LIVE_TOUCH_REPLAY_AUDIT.md]]

**Category:** `debug_docs`  
**Status:** ok  
**Size:** `2270` bytes

## خلاصه

D0006 is the strict live-validity audit for H0005 reversal touch-entry logic. It exists because full-history H5 reports can be useful for discovery, but they are not enough to prove live validity. A live-valid H5 test must separate three times: 1. the time the regime and zones are known, 2. the later time price actually touches the zone and fills the entry, 3. the future path used only for measurement after fill. D0006 enforces this contract: The audit is deliberately separate from E0001–E0005. It is a validator, not an executor. When the latest prefix-only M0002 regime is reversal, D0006 activates live candidates: The entry is not assumed at the signal candle. The candidate must be touched

## Headings

- D0006 — H5 Live Touch Replay Audit
-   Contract
-   Reversal touch model
-   Key summary fields
-   CSV
-   Scientific meaning

## Entities

`D0006`, `E0001`, `E0005`, `H0005`, `M0001`, `M0002`

## Concepts

- [[docs/obsidian/04_concepts/Execution|Execution]]
- [[docs/obsidian/04_concepts/Licensing|Licensing]]
- [[docs/obsidian/04_concepts/MQL_Native|MQL Native]]
- [[docs/evidence/nds_anatomy/6a11c75733b2_NDS_Anatomy|NDS Anatomy]]
- [[docs/obsidian/04_concepts/Structural_Nodes|Structural Nodes]]
- [[docs/obsidian/04_concepts/Validation|Validation]]

## Related documents

- [[docs/execution/E0005_CONTINUATION_CLOSE_BREAK_FIXED_R|E0005 — Continuation Close-Break Fixed-R Executor]] — `execution_docs`
- [[docs/execution/E0002_CLOSE_CONFIRMED_MARKET|E0002 — H0005 Close-Confirmed Market Executor]] — `execution_docs`
- [[docs/execution/E0003_CONTINUATION_CLOSE_HUNT|E0003 — H0005 Continuation Close-Hunt Market Executor]] — `execution_docs`
- [[docs/execution/H0005_R1_SIX_SLOT_TOUCH_LEDGER|H0005 Reversal Structural-Target-Capped Execution — Build 1.25]] — `execution_docs`
- [[docs/execution/README|Decision Alpha Lab — Execution]] — `execution_docs`
- [[lab/04_execution/EXE0002_close_confirmed_market/README|EXE0002 — Close-Confirmed Market After Touch]] — `execution`
- [[docs/debug/D0005_H5_NO_FUTURE_WALK_FORWARD_AUDIT|D0005 — H5 No-Future Walk-Forward Audit]] — `debug_docs`
- [[lab/04_execution/EXE0001_reversal_one_to_one/README|EXE0001 — H0005 Reversal Fixed-R Executor]] — `execution`
- [[README|Decision Alpha Lab]] — `readme`
- [[lab/04_execution/EXE0004_continuation_heikin_ashi_flip/README|EXE0004 — Continuation Heikin Ashi Flip]] — `execution`
- [[docs/execution/E0004_CONTINUATION_HEIKIN_ASHI_FLIP|E0004 — Continuation Heikin Ashi Flip Executor]] — `execution_docs`
- [[docs/reports/2026-06-20_h4_h5_gold_m10_report|Report — H4/H5 GOLD M10 Review, 2026-06-20]] — `core_docs`

## Recommended Obsidian use

- این card را به نوت‌های concept، hypothesis، experiment یا ADR مربوط link کن.
- اگر این سند source of truth است، در MOC مربوطه بالاتر از اسناد legacy قرارش بده.
- اگر این سند report/validation است، نتیجه نهایی آن را به registry مربوط sync کن.
