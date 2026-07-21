
---
type: source_card
source_path: "docs/mql_native/M0001_STRESS_VALIDATION_SUITE.md"
source_ext: ".md"
source_size: 4826
empty: false
generated_at: 2026-07-06
concepts: ["Decision Node", "Execution / Risk", "UI / React", "Validation / Audit", "Zone / RTV"]
entities: ["M0001"]
---

# Source Card — M0001_STRESS_VALIDATION_SUITE.md

## Source

[[docs/mql_native/M0001_STRESS_VALIDATION_SUITE|docs/mql_native/M0001_STRESS_VALIDATION_SUITE.md]]

## Summary

Version: 1.61 This document locks the additional validation layer around M0001. The structural-node, territory, touch/HUNT, revisit, RTV, logRTV, warmup, analysis-start, and final visual semantics are unchanged. Version 1.61 adds fina… The EA remains candle-gated and final-only by default: No stress test changes the event definition. Stress tests operate after the final event set is built. `InpBrokerUtcOffsetHours` converts broker-server hour to UTC hour for session reports. If broker time is UTC+2, set it to `2`. If broker time is UTC+3, set it to `3`. `InpRegimeLookbackBars` defines the pre-entry realized-volatility regime: Regimes are terciles of this pre-entry value. This replaces the older diagnostic `randomLogTercile` regime and is live-safe because it only uses information before event entry. Printed as: For every node event, the test tries to find random windows that match: If no

## Concepts

[[docs/obsidian_deep/02_concepts/Decision_Node|Decision Node]], [[docs/obsidian_deep/02_concepts/Execution____Risk|Execution / Risk]], [[docs/obsidian_deep/02_concepts/UI____React|UI / React]], [[docs/obsidian_deep/02_concepts/Validation____Audit|Validation / Audit]], [[docs/obsidian_deep/02_concepts/Zone____RTV|Zone / RTV]]

## Entities

M0001

## Headings

- M0001 Stress Validation Suite
  - Runtime principle
  - New inputs
  - Final stress reports
    - HARD_NULL
    - PLACEBO
    - OUTLIER_STRESS
    - NONOVERLAP
    - CLUSTER_ROBUST
    - BLOCK_BOOT
    - HORIZON
    - NEGATIVE_CONTROL

## Related Source Documents

- [[docs/evidence/val_m0001_mql_native/454e81f9f0b3_report|report.md]] — score `21`
- [[lab/03_experiments/EXP0003_mql_native_m0002/report|report.md]] — score `19`
- [[docs/evidence/exp0002_mql_native_m0001_runtime/319a21879dae_report|report.md]] — score `17`
- [[docs/mql_native/H0001_H0002_ALGORITHM_AND_HYPOTHESIS_README|H0001_H0002_ALGORITHM_AND_HYPOTHESIS_README.md]] — score `16`
- [[docs/mql_native/H0001_H0004_RESEARCH_LOCK|H0001_H0004_RESEARCH_LOCK.md]] — score `16`
- [[docs/mql_native/H0003_CONTINUATION_INERTIA_MEMORY_CLUSTERING|H0003_CONTINUATION_INERTIA_MEMORY_CLUSTERING.md]] — score `16`
- [[docs/mql_native/H0003_INERTIA_MEMORY_RESULTS_AND_ALGORITHM|H0003_INERTIA_MEMORY_RESULTS_AND_ALGORITHM.md]] — score `16`
- [[docs/mql_native/H0004_BRANCH_REGIME_CLUSTERING|H0004_BRANCH_REGIME_CLUSTERING.md]] — score `16`
- [[docs/mql_native/H0007_FLAG_COUNTING_F1_START_STRUCTURE|H0007_FLAG_COUNTING_F1_START_STRUCTURE.md]] — score `16`
- [[docs/evidence/m0001_excel_audit/ff999bc7279e_M0001_EXCEL_AUDIT_REPORT|M0001_EXCEL_AUDIT_REPORT.md]] — score `16`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
