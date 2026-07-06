---
title: "M0001 Touch Mode: Consume After Event Completion"
type: document_card
generated_by: alpha_lab_obsidian_builder
generated_at: 2026-07-06
source_path: "docs/mql_native/M0001_TOUCH_CONSUMES_AFTER_EVENT_CLOSE.md"
source_ext: ".md"
category: "mql_native_docs"
source_size_bytes: "1220"
entities:
  - "M0001"
concepts:
  - "MQL Native"
  - "NDS Anatomy"
  - "Structural Nodes"
---


# M0001 Touch Mode: Consume After Event Completion

**Source:** [[docs/mql_native/M0001_TOUCH_CONSUMES_AFTER_EVENT_CLOSE|docs/mql_native/M0001_TOUCH_CONSUMES_AFTER_EVENT_CLOSE.md]]

**Category:** `mql_native_docs`  
**Status:** ok  
**Size:** `1220` bytes

## خلاصه

Touch mode now follows the README semantics: Touch does **not** consume the node immediately. An event is complete when price has stayed outside the frozen event territory for `exit_gap` consecutive candles. When the first touch starts an event: These are frozen for the event. They are not updated while the event is active. Hunt mode remains separate: Zone touches in hunt mode start/revisit events, but do not consume the node unless the node price is broken. This preserves revisit semantics: `M0001_LiveVisualLab.mq5` version: `1.30`.

## Headings

- M0001 Touch Mode: Consume After Event Completion
-   Decision
-   Event completion
-   Frozen event geometry
-   HUNT mode
-   Why this matters
-   Version

## Entities

`M0001`

## Concepts

- [[docs/obsidian/04_concepts/MQL_Native|MQL Native]]
- [[docs/obsidian/04_concepts/NDS_Anatomy|NDS Anatomy]]
- [[docs/obsidian/04_concepts/Structural_Nodes|Structural Nodes]]

## Related documents

- [[docs/debug/E0006/README|E0006 — Structural Execution Layer Overview]] — `debug_docs`
- [[docs/execution/README|Decision Alpha Lab — Execution]] — `execution_docs`
- [[lab/03_validation/VAL0005_h5_no_future_walk_forward/README|VAL0005 — H5 No-Future Walk-Forward Validation]] — `validation`
- [[lab/03_validation/VAL0023_e6_all_zone_touch_limit/README|E0006 — All-Zone Touch Limit Fixed-R Executor]] — `validation`
- [[lab/04_execution/EXE0002_close_confirmed_market/README|EXE0002 — Close-Confirmed Market After Touch]] — `execution`
- [[README|Decision Alpha Lab]] — `readme`
- [[docs/debug/E0008/README|E0008 — MTF Purple Extreme Executor]] — `debug_docs`
- [[docs/ui/README|Quant Lab UI Architecture]] — `ui_docs`
- [[lab/03_validation/VAL0022_h6_reaction_box_zones/README|VAL0022 — H6 Reaction Box Zones]] — `validation`
- [[lab/04_execution/EXE0001_reversal_one_to_one/README|EXE0001 — H0005 Reversal Fixed-R Executor]] — `execution`
- [[lab/04_execution/EXE0003_continuation_close_hunt/README|EXE0003 — Continuation Close-Hunt Market Execution]] — `execution`
- [[lab/03_validation/VAL0009_h5_atomic_no_sample_replay/README|VAL0009 — H5 Atomic No-Sample Replay]] — `validation`

## Recommended Obsidian use

- این card را به نوت‌های concept، hypothesis، experiment یا ADR مربوط link کن.
- اگر این سند source of truth است، در MOC مربوطه بالاتر از اسناد legacy قرارش بده.
- اگر این سند report/validation است، نتیجه نهایی آن را به registry مربوط sync کن.
