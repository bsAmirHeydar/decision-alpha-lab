---
project: EXP0018
phase: P10
status: implemented-evidence-package
authority: visual-projection-only
execution_authority: false
schema_version: 2
---

# Master Visual Layer Map

## Purpose

Provide a complete inventory so no required visual is hidden inside an unrelated module.

## Canonical inventory

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

## Default profile

The default profile shows all Core time anatomy while keeping micro labels off to reduce clutter. Extended True Opens and provisional weekly boundaries remain off because they are supplemental or doctrine-gated.

## Layer independence

Disabling one P10 time layer must not suppress P08 divergence evidence or mutate period, hunt, confirmation, or lifecycle states.


## Non-authority statement

This document and the corresponding implementation do not authorize entries, exits, risk sizing, order placement, strategy mutation, model promotion, network access, or execution. Chart objects are projections of upstream immutable evidence and time contracts.
