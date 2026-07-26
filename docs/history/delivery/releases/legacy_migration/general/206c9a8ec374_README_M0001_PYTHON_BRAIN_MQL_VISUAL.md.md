---
title: "M0001 Python Brain / MQL Visual Architecture"
type: document_card
generated_by: alpha_lab_obsidian_builder
generated_at: 2026-07-06
source_path: "README_M0001_PYTHON_BRAIN_MQL_VISUAL.md"
source_ext: ".md"
category: "readme"
source_size_bytes: "7661"
entities:
  - "M0001"
concepts:
  - "Execution"
  - "Intermarket Divergence"
  - "MQL Native"
  - "NDS Anatomy"
  - "Structural Nodes"
  - "Validation"
---


# M0001 Python Brain / MQL Visual Architecture

**Source:** [[README_M0001_PYTHON_BRAIN_MQL_VISUAL|README_M0001_PYTHON_BRAIN_MQL_VISUAL.md]]

**Category:** `readme`  
**Status:** ok  
**Size:** `7661` bytes

## خلاصه

M0001 now follows one strict architecture rule: The same Python code path is used for: MQL does not compute the metric. It reads the Python-generated visual contract and draws it on the chart. The lab rejects a two-engine architecture: That creates logic drift. The chart can look right while the tested code is different, or the backtest can pass while live visual behavior is computed by a different implementation. The accepted architecture is: Compile and attach: The expert reloads the CSV contract on a timer: All manual visual toggles default to `false`. Use `InpViewPreset` to activate one audit package at a time. The MT5 Expert now exposes the Python brain parameters as inputs. Changing `I

## Headings

- M0001 Python Brain / MQL Visual Architecture
-   Why this exists
-   Main files
-   Run once
-   Run continuously
-   MT5 expert
-   Recommended visual validation order
-   Professional description
-   MQL input bridge
-   Event bridge sync mode
-   M0001 Parquet Event Bridge
-   Common Files Sync

## Entities

`M0001`

## Concepts

- [[docs/obsidian/04_concepts/Execution|Execution]]
- [[docs/obsidian/04_concepts/Intermarket_Divergence|Intermarket Divergence]]
- [[docs/obsidian/04_concepts/MQL_Native|MQL Native]]
- [[docs/evidence/nds_anatomy/6a11c75733b2_NDS_Anatomy|NDS Anatomy]]
- [[docs/obsidian/04_concepts/Structural_Nodes|Structural Nodes]]
- [[docs/obsidian/04_concepts/Validation|Validation]]

## Related documents

- [[README|Decision Alpha Lab]] — `readme`
- [[docs/architecture|System Architecture]] — `core_docs`
- [[docs/debug/E0006/README|E0006 — Structural Execution Layer Overview]] — `debug_docs`
- [[lab/03_validation/VAL0023_e6_all_zone_touch_limit/README|E0006 — All-Zone Touch Limit Fixed-R Executor]] — `validation`
- [[docs/execution/README|Decision Alpha Lab — Execution]] — `execution_docs`
- [[docs/ui/README|Quant Lab UI Architecture]] — `ui_docs`
- [[lab/03_validation/VAL0005_h5_no_future_walk_forward/README|VAL0005 — H5 No-Future Walk-Forward Validation]] — `validation`
- [[lab/03_validation/VAL0022_h6_reaction_box_zones/README|VAL0022 — H6 Reaction Box Zones]] — `validation`
- [[lab/04_execution/EXE0002_close_confirmed_market/README|EXE0002 — Close-Confirmed Market After Touch]] — `execution`
- [[docs/debug/E0008/README|E0008 — MTF Purple Extreme Executor]] — `debug_docs`
- [[lab/03_validation/VAL0009_h5_atomic_no_sample_replay/README|VAL0009 — H5 Atomic No-Sample Replay]] — `validation`
- [[lab/04_execution/EXE0001_reversal_one_to_one/README|EXE0001 — H0005 Reversal Fixed-R Executor]] — `execution`

## Recommended Obsidian use

- این card را به نوت‌های concept، hypothesis، experiment یا ADR مربوط link کن.
- اگر این سند source of truth است، در MOC مربوطه بالاتر از اسناد legacy قرارش بده.
- اگر این سند report/validation است، نتیجه نهایی آن را به registry مربوط sync کن.
