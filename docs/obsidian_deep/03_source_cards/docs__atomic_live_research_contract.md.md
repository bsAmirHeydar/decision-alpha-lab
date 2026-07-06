
---
type: source_card
source_path: "docs/atomic_live_research_contract.md"
source_ext: ".md"
source_size: 3122
empty: false
generated_at: 2026-07-06
concepts: ["AI Agent Layer", "Atomic No-Sample", "Decision Node", "Execution / Risk", "Known-Time Causality", "UI / React", "Validation / Audit", "Zone / RTV"]
entities: ["M0001"]
---

# Source Card — atomic_live_research_contract.md

## Source

[[docs/atomic_live_research_contract|docs/atomic_live_research_contract.md]]

## Summary

This document defines the strict contract used to prevent future leakage, fake sequencing, and non-tradable R statistics. For every decision candle `t`, the engine may only use information derived from closed candles up to `t`. Forbidden: using future-completed branch samples to decide at `t`, using a future outcome label before its known candle, ordering labels inside the same known candle, exiting on a regime change before that regime change is knowable. Required fields for any live-valid label: `known_index`, `known_time`, `source_event_id` or equivalent raw event reference, `energy_label`: reversal, continuation, or ambiguous, `direction_label` where applicable, `is_ambiguous`. All events or labels that become known on the same candle/time form one batch. A batch can be: pure reversal, pure continuation, ambiguous mixed energy, unknown or invalid. A pure batch may participate in regi

## Concepts

[[docs/obsidian_deep/02_concepts/AI_Agent_Layer|AI Agent Layer]], [[docs/obsidian_deep/02_concepts/Atomic_No-Sample|Atomic No-Sample]], [[docs/obsidian_deep/02_concepts/Decision_Node|Decision Node]], [[docs/obsidian_deep/02_concepts/Execution____Risk|Execution / Risk]], [[docs/obsidian_deep/02_concepts/Known-Time_Causality|Known-Time Causality]], [[docs/obsidian_deep/02_concepts/UI____React|UI / React]], [[docs/obsidian_deep/02_concepts/Validation____Audit|Validation / Audit]], [[docs/obsidian_deep/02_concepts/Zone____RTV|Zone / RTV]]

## Entities

M0001

## Headings

- Atomic Live Research Contract
  - 1. Decision-time contract
  - 2. Same-candle batch contract
  - 3. No-sample contract
  - 4. Entry contract
  - 5. R contract
  - 6. Report contract

## Related Source Documents

- [[docs/architecture|architecture.md]] — score `22`
- [[lab/05_validation/VAL_M0001_MQL_NATIVE/report|report.md]] — score `21`
- [[papers/001_atomic_live_regime_framework|001_atomic_live_regime_framework.md]] — score `21`
- [[README|README.md]] — score `21`
- [[docs/debug/H6_REACTION_BOX_ZONES|H6_REACTION_BOX_ZONES.md]] — score `19`
- [[docs/mql_native/H0007_FLAG_COUNTING_F1_START_STRUCTURE|H0007_FLAG_COUNTING_F1_START_STRUCTURE.md]] — score `19`
- [[docs/reports/2026-06-20_h4_h5_gold_m10_report|2026-06-20_h4_h5_gold_m10_report.md]] — score `19`
- [[docs/ui/ROADMAP|ROADMAP.md]] — score `19`
- [[lab/02_hypotheses/H0004_branch_regime_memory_atomic|H0004_branch_regime_memory_atomic.md]] — score `19`
- [[lab/02_hypotheses/H0005_directional_memory_atomic|H0005_directional_memory_atomic.md]] — score `19`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
