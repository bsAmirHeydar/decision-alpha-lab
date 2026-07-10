---
project: EXP0018
phase: P10
status: implemented-evidence-package
authority: visual-projection-only
execution_authority: false
schema_version: 2
---

# P10 Unified Visual Anatomy v2 — Index

## Purpose

Canonical chart-facing implementation packet for the complete EXP0018 Core visual language. P10 composes P08 immutable divergence projection and all required Daye time-cycle drawings in one Expert because MetaTrader permits only one Expert Advisor per chart.

## Start here

Compile and attach `mql5/Experts/DayeTrader/EXP0018_Daye_Visual_Anatomy.mq5`. Keep the standalone P08 and P09 Experts only as diagnostics. The unified Expert is the operational chart-facing renderer.

## Visual layer register

| Layer | Source | Default | Object | Namespace |
|---|---|---:|---|---|
| Confirmed divergence | P07 accepted use through P08 | On | `OBJ_TREND` + major `OBJ_TEXT` | `EXP0018_P08_` |
| Daily frame | P03 Daily snapshot | On | `OBJ_RECTANGLE` | `EXP0018_P10_DAY_` |
| Daily start/end | P03 Daily window | On | `OBJ_VLINE` | `EXP0018_P10_DAY_START/END_` |
| Session range | P03 A/L/N/P snapshot | On | `OBJ_RECTANGLE` | `EXP0018_P10_SESSION_BOX_` |
| Session/Q labels | P03 Session code | On | `OBJ_TEXT` | `EXP0018_P10_SESSION_LABEL_` |
| 90-minute range | P03 a1-p3 snapshot | On | `OBJ_RECTANGLE` | `EXP0018_P10_SUB_BOX_` |
| p4 tail | P03 p4 snapshot | On | `OBJ_RECTANGLE` + `30m` label | `EXP0018_P10_SUB_` |
| 22.5-minute quarters | P01 local time inside full 90m window | Boundaries on, labels off | `OBJ_VLINE` / `OBJ_TEXT` | `EXP0018_P10_MICRO_` |
| Declared gap | Daily end 17:00 to next 18:00 NY | On | band + boundaries | `EXP0018_P10_GAP_` |
| TDO | L open 00:00 NY | On | finite `OBJ_TREND` | `EXP0018_P10_TDO_` |
| TWO | configured Tuesday-open policy | On | finite `OBJ_TREND` | `EXP0018_P10_TWO_` |
| Extended TSO | a2/l2/n2/p2 opens | Off | finite `OBJ_TREND` | `EXP0018_P10_TSO_` |
| Provisional week | provisional policy only | Off | `OBJ_VLINE` | `EXP0018_P10_WEEK_` |

## Reading order

Read scope and composition first, then the hierarchy and each geometry contract, then ownership/idempotency, runtime validation, and Definition of Done.


## Non-authority statement

This document and the corresponding implementation do not authorize entries, exits, risk sizing, order placement, strategy mutation, model promotion, network access, or execution. Chart objects are projections of upstream immutable evidence and time contracts.
