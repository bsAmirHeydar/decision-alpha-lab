
---
type: source_card
source_path: "docs/mql_native/M0001_NODE_DUAL_OUTCOME_STATE.md"
source_ext: ".md"
source_size: 1421
empty: false
generated_at: 2026-07-06
concepts: ["Decision Node", "Execution / Risk", "Python Brain", "Validation / Audit", "Zone / RTV"]
entities: ["M0001"]
---

# Source Card — M0001_NODE_DUAL_OUTCOME_STATE.md

## Source

[[docs/mql_native/M0001_NODE_DUAL_OUTCOME_STATE|docs/mql_native/M0001_NODE_DUAL_OUTCOME_STATE.md]]

## Summary

Version: active semantics preserved in 1.59 Every node stores TOUCH and HUNT information independently of the selected consumption model. The consumption model decides when a node becomes inactive. A zone touch starts only a pending touch event: The touch is confirmed only after strict exit-gap closure: If the node price breaks before touch confirmation: That outcome becomes HUNT. In TOUCH mode: In HUNT mode: Once a node is consumed, no further candles are scanned for that node. The old validation-journal CSV writer is retired. Current audit state is used for final chart drawings and final compact node-vs-random logRTV reports.

## Concepts

[[docs/obsidian_deep/02_concepts/Decision_Node|Decision Node]], [[docs/obsidian_deep/02_concepts/Execution____Risk|Execution / Risk]], [[docs/obsidian_deep/02_concepts/Python_Brain|Python Brain]], [[docs/obsidian_deep/02_concepts/Validation____Audit|Validation / Audit]], [[docs/obsidian_deep/02_concepts/Zone____RTV|Zone / RTV]]

## Entities

M0001

## Headings

- M0001 Node Dual Outcome State
  - Purpose
  - Stored on each audit state
  - Logic
  - Consumption model
  - Reporting

## Related Source Documents

- [[docs/evidence/val_m0001_mql_native/454e81f9f0b3_report|report.md]] — score `21`
- [[docs/evidence/exp0002_mql_native_m0001_runtime/319a21879dae_report|report.md]] — score `19`
- [[lab/03_experiments/EXP0003_mql_native_m0002/report|report.md]] — score `19`
- [[docs/mql_native/M0001_CANDLE_GATED_RUNTIME|M0001_CANDLE_GATED_RUNTIME.md]] — score `16`
- [[docs/evidence/m0001_excel_audit/ff999bc7279e_M0001_EXCEL_AUDIT_REPORT|M0001_EXCEL_AUDIT_REPORT.md]] — score `16`
- [[docs/mql_native/M0001_PROFESSIONAL_VALIDATION_METRICS|M0001_PROFESSIONAL_VALIDATION_METRICS.md]] — score `16`
- [[docs/mql_native/MODULE_MAP|MODULE_MAP.md]] — score `16`
- [[docs/mql_native/MQL_NATIVE_ARCHITECTURE|MQL_NATIVE_ARCHITECTURE.md]] — score `16`
- [[docs/architecture|architecture.md]] — score `15`
- [[docs/debug/D0006_H5_LIVE_TOUCH_REPLAY_AUDIT|D0006_H5_LIVE_TOUCH_REPLAY_AUDIT.md]] — score `15`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
