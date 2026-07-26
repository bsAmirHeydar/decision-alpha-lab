
---
type: source_card
source_path: "docs/M0001_MQL_INPUT_PARAMETER_BRIDGE.md"
source_ext: ".md"
source_size: 2791
empty: false
generated_at: 2026-07-06
concepts: ["Decision Node", "Execution / Risk", "MQL Native", "Python Brain", "UI / React", "Validation / Audit", "Zone / RTV"]
entities: ["M0001"]
---

# Source Card — M0001_MQL_INPUT_PARAMETER_BRIDGE.md

## Source

[[docs/M0001_MQL_INPUT_PARAMETER_BRIDGE|docs/M0001_MQL_INPUT_PARAMETER_BRIDGE.md]]

## Summary

M0001 must have one metric brain. Python is the only source of truth for: L-rule reference extraction reference point normalization territory construction entry/exit state machine before/inside samples RTV calculation hunt detection random baseline generation visual contract generation MQL5 is a visual terminal only. The practical issue is that parameter changes must still feel native inside MT5. This bridge solves that without duplicating the brain. The code being tested is the code producing the chart output. MQL does not recompute the metric. Recommended defaults: Attach `M0001_LiveVisualLab.mq5` to an MT5 chart. Set the Python brain parameters inside the Expert inputs. Start the Python watcher: Whenever you change inputs in MT5 and press OK: MQL writes a new config file. Python reads it on the next cycle. Python recomputes the CSV with the same research engine. MQL reloads and redraw

## Concepts

[[docs/obsidian_deep/02_concepts/Decision_Node|Decision Node]], [[docs/obsidian_deep/02_concepts/Execution____Risk|Execution / Risk]], [[docs/obsidian_deep/02_concepts/MQL_Native|MQL Native]], [[docs/obsidian_deep/02_concepts/Python_Brain|Python Brain]], [[docs/obsidian_deep/02_concepts/UI____React|UI / React]], [[docs/obsidian_deep/02_concepts/Validation____Audit|Validation / Audit]], [[docs/obsidian_deep/02_concepts/Zone____RTV|Zone / RTV]]

## Entities

M0001

## Headings

- M0001 Python Brain / MQL Input Bridge
  - Purpose
  - Architecture
  - Important MQL inputs
    - Python brain parameters
    - Bridge controls
  - How to run
  - Why this is strict
  - Validation mindset

## Related Source Documents

- [[docs/architecture|architecture.md]] — score `28`
- [[docs/evidence/val_m0001_mql_native/454e81f9f0b3_report|report.md]] — score `25`
- [[docs/evidence/exp0002_mql_native_m0001_runtime/319a21879dae_report|report.md]] — score `21`
- [[lab/03_experiments/EXP0003_mql_native_m0002/report|report.md]] — score `21`
- [[docs/MQL_LIVE_ALL_IN_ONE_APPLY|MQL_LIVE_ALL_IN_ONE_APPLY.md]] — score `20`
- [[docs/MQL_NATIVE_MIGRATION_DECISION|MQL_NATIVE_MIGRATION_DECISION.md]] — score `20`
- [[docs/mql_visual_lab|mql_visual_lab.md]] — score `20`
- [[docs/ui/ARCHITECTURE|ARCHITECTURE.md]] — score `20`
- [[docs/debug/D0006_H5_LIVE_TOUCH_REPLAY_AUDIT|D0006_H5_LIVE_TOUCH_REPLAY_AUDIT.md]] — score `19`
- [[docs/evidence/m0001_excel_audit/ff999bc7279e_M0001_EXCEL_AUDIT_REPORT|M0001_EXCEL_AUDIT_REPORT.md]] — score `19`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
