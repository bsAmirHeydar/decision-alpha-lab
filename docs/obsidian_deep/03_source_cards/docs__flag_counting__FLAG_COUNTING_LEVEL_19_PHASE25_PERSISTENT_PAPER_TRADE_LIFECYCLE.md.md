
---
type: source_card
source_path: "docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE25_PERSISTENT_PAPER_TRADE_LIFECYCLE.md"
source_ext: ".md"
source_size: 4428
empty: false
generated_at: 2026-07-06
concepts: ["Decision Node", "Execution / Risk", "Flag Counting", "Hook", "Licensing", "MQL Native", "Python Brain", "UI / React", "Validation / Audit"]
entities: []
---

# Source Card — FLAG_COUNTING_LEVEL_19_PHASE25_PERSISTENT_PAPER_TRADE_LIFECYCLE.md

## Source

[[docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE25_PERSISTENT_PAPER_TRADE_LIFECYCLE|docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE25_PERSISTENT_PAPER_TRADE_LIFECYCLE.md]]

## Summary

Phase 25 adds a lifecycle engine above the Phase 24 Persistent Paper Trade Ledger. This phase still does **not** send real orders. It takes persistent paper trade rows and evaluates their current paper lifecycle using the latest closed candle close only. Phase 25 writes: Each State Gate timeframe state now stores: The snapshot now stores: Phase 25 can classify persistent paper trades as: Phase 25 remains close-only: It does not use intrabar high/low yet. For BUY-like paper trade directions: For SELL-like paper trade directions: When a non-zero invalidation distance exists, the engine computes: If invalidation distance is unavailable, R stays pending. Every Phase 25 row keeps: No order is opened, modified, deleted, closed, or sent. Phase 25 does not modify: It only reads persistent paper trade rows and writes paper lifecycle diagnostics. The next phase can be: That phase should aggregate

## Concepts

[[docs/obsidian_deep/02_concepts/Decision_Node|Decision Node]], [[docs/obsidian_deep/02_concepts/Execution____Risk|Execution / Risk]], [[docs/obsidian_deep/02_concepts/Flag_Counting|Flag Counting]], [[docs/obsidian_deep/02_concepts/Hook|Hook]], [[docs/obsidian_deep/02_concepts/Licensing|Licensing]], [[docs/obsidian_deep/02_concepts/MQL_Native|MQL Native]], [[docs/obsidian_deep/02_concepts/Python_Brain|Python Brain]], [[docs/obsidian_deep/02_concepts/UI____React|UI / React]], [[docs/obsidian_deep/02_concepts/Validation____Audit|Validation / Audit]]

## Entities

—

## Headings

- Flag Counting Level 19 — Phase 25 Persistent Paper Trade Lifecycle Engine
  - Purpose
  - Hard safety contract
  - New CSV
  - New input
  - New per-timeframe fields
  - Snapshot aggregate fields
  - Lifecycle states
  - Terminal states
  - Path states
  - Evaluation method
  - R-equivalent

## Related Source Documents

- [[docs/flag_counting/FLAG_COUNTING_CURRENT_CANON|FLAG_COUNTING_CURRENT_CANON.md]] — score `19`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_CLEAN_ISOLATED_STATE_GATE|FLAG_COUNTING_LEVEL_19_CLEAN_ISOLATED_STATE_GATE.md]] — score `19`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE10_PANEL_LINE_CONTRACT|FLAG_COUNTING_LEVEL_19_PHASE10_PANEL_LINE_CONTRACT.md]] — score `19`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE13_MTF_ALIGNMENT_MAP|FLAG_COUNTING_LEVEL_19_PHASE13_MTF_ALIGNMENT_MAP.md]] — score `19`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE14_ENTRY_GEOMETRY_READINESS|FLAG_COUNTING_LEVEL_19_PHASE14_ENTRY_GEOMETRY_READINESS.md]] — score `19`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE18_PAPER_LEDGER_LIFECYCLE_TRACKING|FLAG_COUNTING_LEVEL_19_PHASE18_PAPER_LEDGER_LIFECYCLE_TRACKING.md]] — score `19`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE19_PAPER_RESULT_METRICS|FLAG_COUNTING_LEVEL_19_PHASE19_PAPER_RESULT_METRICS.md]] — score `19`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE21_PAPER_REGIME_ATTRIBUTION|FLAG_COUNTING_LEVEL_19_PHASE21_PAPER_REGIME_ATTRIBUTION.md]] — score `19`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE22_PAPER_FILTER_DIAGNOSTICS|FLAG_COUNTING_LEVEL_19_PHASE22_PAPER_FILTER_DIAGNOSTICS.md]] — score `19`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE23_DRY_RUN_DECISION_POLICY|FLAG_COUNTING_LEVEL_19_PHASE23_DRY_RUN_DECISION_POLICY.md]] — score `19`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
