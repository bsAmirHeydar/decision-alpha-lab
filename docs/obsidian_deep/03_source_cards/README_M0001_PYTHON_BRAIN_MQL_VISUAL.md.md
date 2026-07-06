
---
type: source_card
source_path: "README_M0001_PYTHON_BRAIN_MQL_VISUAL.md"
source_ext: ".md"
source_size: 7661
empty: false
generated_at: 2026-07-06
concepts: ["Decision Node", "Execution / Risk", "Intermarket Divergence", "MQL Native", "Python Brain", "UI / React", "Validation / Audit", "Zone / RTV"]
entities: ["M0001"]
---

# Source Card — README_M0001_PYTHON_BRAIN_MQL_VISUAL.md

## Source

[[README_M0001_PYTHON_BRAIN_MQL_VISUAL|README_M0001_PYTHON_BRAIN_MQL_VISUAL.md]]

## Summary

M0001 now follows one strict architecture rule: The same Python code path is used for: MQL does not compute the metric. It reads the Python-generated visual contract and draws it on the chart. The lab rejects a two-engine architecture: That creates logic drift. The chart can look right while the tested code is different, or the backtest can pass while live visual behavior is computed by a different implementation. The accepted architecture is: Compile and attach: The expert reloads the CSV contract on a timer: All manual visual toggles default to `false`. Use `InpViewPreset` to activate one audit package at a time. The MT5 Expert now exposes the Python brain parameters as inputs. Changing `InpBrainL`, `InpBrainZoneRatio`, `InpBrainExitGap`, `InpBrainBars`, mode, random baseline settings or symbol/timeframe in MT5 does **not** move the brain to MQL. Instead, MQL writes those inputs into:

## Concepts

[[docs/obsidian_deep/02_concepts/Decision_Node|Decision Node]], [[docs/obsidian_deep/02_concepts/Execution____Risk|Execution / Risk]], [[docs/obsidian_deep/02_concepts/Intermarket_Divergence|Intermarket Divergence]], [[docs/obsidian_deep/02_concepts/MQL_Native|MQL Native]], [[docs/obsidian_deep/02_concepts/Python_Brain|Python Brain]], [[docs/obsidian_deep/02_concepts/UI____React|UI / React]], [[docs/obsidian_deep/02_concepts/Validation____Audit|Validation / Audit]], [[docs/obsidian_deep/02_concepts/Zone____RTV|Zone / RTV]]

## Entities

M0001

## Headings

- M0001 Python Brain / MQL Visual Architecture
  - Why this exists
  - Main files
  - Run once
  - Run continuously
  - MT5 expert
  - Recommended visual validation order
  - Professional description
  - MQL input bridge
  - Event bridge sync mode
  - M0001 Parquet Event Bridge
  - Common Files Sync

## Related Source Documents

- [[docs/architecture|architecture.md]] — score `27`
- [[docs/ui/ARCHITECTURE|ARCHITECTURE.md]] — score `20`
- [[docs/debug/D0006_H5_LIVE_TOUCH_REPLAY_AUDIT|D0006_H5_LIVE_TOUCH_REPLAY_AUDIT.md]] — score `19`
- [[docs/M0001_MQL_INPUT_PARAMETER_BRIDGE|M0001_MQL_INPUT_PARAMETER_BRIDGE.md]] — score `19`
- [[docs/M0001_SINGLE_SOURCE_LIVE_ARCHITECTURE|M0001_SINGLE_SOURCE_LIVE_ARCHITECTURE.md]] — score `19`
- [[docs/MQL_LIVE_ALL_IN_ONE_APPLY|MQL_LIVE_ALL_IN_ONE_APPLY.md]] — score `19`
- [[docs/mql_native/M0001_EXCEL_AUDIT_REPORT|M0001_EXCEL_AUDIT_REPORT.md]] — score `19`
- [[docs/mql_native/M0001_PROFESSIONAL_VALIDATION_METRICS|M0001_PROFESSIONAL_VALIDATION_METRICS.md]] — score `19`
- [[docs/mql_native/MODULE_MAP|MODULE_MAP.md]] — score `19`
- [[docs/mql_native/MQL_NATIVE_ARCHITECTURE|MQL_NATIVE_ARCHITECTURE.md]] — score `19`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
