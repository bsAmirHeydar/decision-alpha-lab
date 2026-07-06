
---
type: source_card
source_path: "lab/09_execution/mql5/README.md"
source_ext: ".md"
source_size: 1571
empty: false
generated_at: 2026-07-06
concepts: ["Atomic No-Sample", "Execution / Risk", "Known-Time Causality", "MQL Native", "UI / React", "Validation / Audit"]
entities: ["D0009", "D0010", "H0004", "H0005", "M0001"]
---

# Source Card — README.md

## Source

[[lab/09_execution/mql5/README|lab/09_execution/mql5/README.md]]

## Summary

MQL5 is the project layer used for fast replay, MetaTrader-native execution, and Expert Advisor validation. MQL5 is no longer only an execution bridge. It is also the strictest environment for live-style validation because it can replay candle state and execution policies close to the platform that will trade the system. Main hypothesis Experts must not depend on completed samples for live validity. For H0004 and H0005, the official direction is: Debug Experts are allowed to test new contracts. Once a contract is accepted, it must be moved into the main Expert or a shared include used by the main Expert. Accepted examples: D0010 proved H4 atomic no-sample regime batching. D0009 proved H5 atomic no-sample replay. Main H4/H5 should default to the atomic contract. Every trading EA must distinguish: structural path metrics, execution metrics, realized R with real risk, floating MFE/MAE R, fi

## Concepts

[[docs/obsidian_deep/02_concepts/Atomic_No-Sample|Atomic No-Sample]], [[docs/obsidian_deep/02_concepts/Execution____Risk|Execution / Risk]], [[docs/obsidian_deep/02_concepts/Known-Time_Causality|Known-Time Causality]], [[docs/obsidian_deep/02_concepts/MQL_Native|MQL Native]], [[docs/obsidian_deep/02_concepts/UI____React|UI / React]], [[docs/obsidian_deep/02_concepts/Validation____Audit|Validation / Audit]]

## Entities

D0009, D0010, H0004, H0005, M0001

## Headings

- MQL5 Execution and Validation Layer
  - Current role
  - Official research rule
  - Debug vs main Experts
  - Execution reporting rule
  - Compile discipline

## Related Source Documents

- [[docs/research_lessons_and_failure_modes|research_lessons_and_failure_modes.md]] — score `30`
- [[README|README.md]] — score `27`
- [[lab/05_validation/VAL0010_h4_atomic_no_sample_regime/README|README.md]] — score `25`
- [[docs/mql_native/H0007_FLAG_COUNTING_F1_START_STRUCTURE|H0007_FLAG_COUNTING_F1_START_STRUCTURE.md]] — score `25`
- [[docs/reports/2026-06-20_h4_h5_gold_m10_report|2026-06-20_h4_h5_gold_m10_report.md]] — score `25`
- [[lab/02_hypotheses/H0004_branch_regime_memory_atomic|H0004_branch_regime_memory_atomic.md]] — score `25`
- [[lab/05_validation/VAL0011_main_atomic_no_sample_unification/README|README.md]] — score `25`
- [[docs/debug/D0010_H4_ATOMIC_NO_SAMPLE_REGIME_AUDIT|D0010_H4_ATOMIC_NO_SAMPLE_REGIME_AUDIT.md]] — score `23`
- [[lab/03_validation/VAL0010_h4_atomic_no_sample_regime/README|README.md]] — score `23`
- [[lab/02_hypotheses/H0001_structural_highs_lows_as_decision_nodes|H0001_structural_highs_lows_as_decision_nodes.md]] — score `21`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
