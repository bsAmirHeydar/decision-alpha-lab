
---
type: source_card
source_path: "docs/MQL_NATIVE_MIGRATION_DECISION.md"
source_ext: ".md"
source_size: 3936
empty: false
generated_at: 2026-07-06
concepts: ["Decision Node", "Execution / Risk", "MQL Native", "Python Brain", "UI / React", "Validation / Audit", "Zone / RTV"]
entities: ["M0001"]
---

# Source Card — MQL_NATIVE_MIGRATION_DECISION.md

## Source

[[docs/MQL_NATIVE_MIGRATION_DECISION|docs/MQL_NATIVE_MIGRATION_DECISION.md]]

## Summary

The Decision Alpha Lab project will migrate M0001 from a Python-brain / MQL-visual bridge architecture to a native MQL5 execution architecture. The previous Python implementation is preserved as an archived reference in the branch: Going forward, MQL5 will become the primary runtime for live logic, visual validation, strategy testing, and research iteration. The Python bridge achieved an important goal: it proved the core M0001 idea, clarified the event model, and produced a useful reference implementation. However, it introduced runtime problems that are unacceptable for th… The main issues were: **Asynchronous execution lag** MT5 Strategy Tester advances through simulated market time, while Python runs outside the terminal. Even with aggressive polling, the bridge can create timing lag between candle availability, Python computation, and visu… **File-locking and adapter friction** The

## Concepts

[[docs/obsidian_deep/02_concepts/Decision_Node|Decision Node]], [[docs/obsidian_deep/02_concepts/Execution____Risk|Execution / Risk]], [[docs/obsidian_deep/02_concepts/MQL_Native|MQL Native]], [[docs/obsidian_deep/02_concepts/Python_Brain|Python Brain]], [[docs/obsidian_deep/02_concepts/UI____React|UI / React]], [[docs/obsidian_deep/02_concepts/Validation____Audit|Validation / Audit]], [[docs/obsidian_deep/02_concepts/Zone____RTV|Zone / RTV]]

## Entities

M0001

## Headings

- MQL-Native Migration Decision
  - Summary
  - Why Python Is Being Removed From the Active Runtime
  - What Is Not Being Removed
  - New Direction
  - Archived Reference
  - Decision

## Related Source Documents

- [[docs/architecture|architecture.md]] — score `28`
- [[lab/05_validation/VAL_M0001_MQL_NATIVE/report|report.md]] — score `25`
- [[lab/03_experiments/EXP0002_mql_native_m0001/report|report.md]] — score `21`
- [[lab/03_experiments/EXP0003_mql_native_m0002/report|report.md]] — score `21`
- [[docs/M0001_MQL_INPUT_PARAMETER_BRIDGE|M0001_MQL_INPUT_PARAMETER_BRIDGE.md]] — score `20`
- [[docs/MQL_LIVE_ALL_IN_ONE_APPLY|MQL_LIVE_ALL_IN_ONE_APPLY.md]] — score `20`
- [[docs/mql_visual_lab|mql_visual_lab.md]] — score `20`
- [[docs/ui/ARCHITECTURE|ARCHITECTURE.md]] — score `20`
- [[docs/debug/D0006_H5_LIVE_TOUCH_REPLAY_AUDIT|D0006_H5_LIVE_TOUCH_REPLAY_AUDIT.md]] — score `19`
- [[docs/mql_native/M0001_EXCEL_AUDIT_REPORT|M0001_EXCEL_AUDIT_REPORT.md]] — score `19`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
