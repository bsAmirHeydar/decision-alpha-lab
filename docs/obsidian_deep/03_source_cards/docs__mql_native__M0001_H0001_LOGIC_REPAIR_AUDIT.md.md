
---
type: source_card
source_path: "docs/mql_native/M0001_H0001_LOGIC_REPAIR_AUDIT.md"
source_ext: ".md"
source_size: 2563
empty: false
generated_at: 2026-07-06
concepts: ["Decision Node", "Execution / Risk", "UI / React", "Validation / Audit", "Zone / RTV"]
entities: ["H0001", "H0002", "M0001", "M0002"]
---

# Source Card — M0001_H0001_LOGIC_REPAIR_AUDIT.md

## Source

[[docs/mql_native/M0001_H0001_LOGIC_REPAIR_AUDIT|docs/mql_native/M0001_H0001_LOGIC_REPAIR_AUDIT.md]]

## Summary

Date: 2026-06-18 This document records the logic audit performed before repairing M0002. Structural node territories condition future volatility expansion more than matched random windows. Bars are chronological: oldest to newest. A HIGH node at index `i` requires: `high[i] >= high[i-L..i-1]` `high[i] >= high[i+1..i+L]` A LOW node at index `i` requires: `low[i] <= low[i-L..i-1]` `low[i] <= low[i+1..i+L]` Node becomes knowable at: For LOW nodes, the tracking extreme is the highest high after the active-from point. For HIGH nodes, it is the lowest low after the active-from point. Event starts when a candle intersects the live territory. The event territory freezes at event entry. Exit confirmation requires `exit_gap` consecutive candles fully outside the frozen event zone. A candle whose high/low intersects the frozen event zone resets the outside counter. RTV is calculated only after touc

## Concepts

[[docs/obsidian_deep/02_concepts/Decision_Node|Decision Node]], [[docs/obsidian_deep/02_concepts/Execution____Risk|Execution / Risk]], [[docs/obsidian_deep/02_concepts/UI____React|UI / React]], [[docs/obsidian_deep/02_concepts/Validation____Audit|Validation / Audit]], [[docs/obsidian_deep/02_concepts/Zone____RTV|Zone / RTV]]

## Entities

H0001, H0002, M0001, M0002

## Headings

- M0001 / H0001 Logic Repair Audit
  - H0001 active hypothesis
  - Locked structural-node logic
  - Locked territory logic
  - Locked M0001 event/RTV logic
  - Locked anti-lookahead rules
  - Result of audit

## Related Source Documents

- [[lab/03_experiments/EXP0003_mql_native_m0002/report|report.md]] — score `34`
- [[docs/mql_native/H0001_H0002_ALGORITHM_AND_HYPOTHESIS_README|H0001_H0002_ALGORITHM_AND_HYPOTHESIS_README.md]] — score `31`
- [[docs/mql_native/H0001_H0004_RESEARCH_LOCK|H0001_H0004_RESEARCH_LOCK.md]] — score `31`
- [[docs/mql_native/H0003_CONTINUATION_INERTIA_MEMORY_CLUSTERING|H0003_CONTINUATION_INERTIA_MEMORY_CLUSTERING.md]] — score `31`
- [[docs/mql_native/H0003_INERTIA_MEMORY_RESULTS_AND_ALGORITHM|H0003_INERTIA_MEMORY_RESULTS_AND_ALGORITHM.md]] — score `31`
- [[docs/mql_native/H0004_BRANCH_REGIME_CLUSTERING|H0004_BRANCH_REGIME_CLUSTERING.md]] — score `31`
- [[docs/mql_native/M0002_DEEP_AUDIT_AND_STABILITY|M0002_DEEP_AUDIT_AND_STABILITY.md]] — score `31`
- [[docs/mql_native/M0002_REVERSAL_CONTINUATION_EXIT_VOLATILITY|M0002_REVERSAL_CONTINUATION_EXIT_VOLATILITY.md]] — score `31`
- [[docs/mql_native/MODULE_MAP|MODULE_MAP.md]] — score `31`
- [[README|README.md]] — score `30`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
