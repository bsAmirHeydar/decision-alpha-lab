
---
type: source_card
source_path: "docs/research-roadmap.md"
source_ext: ".md"
source_size: 1525
empty: false
generated_at: 2026-07-06
concepts: ["Atomic No-Sample", "Decision Node", "Execution / Risk", "Known-Time Causality", "UI / React", "Validation / Audit", "Zone / RTV"]
entities: []
---

# Source Card — research-roadmap.md

## Source

[[docs/research-roadmap|docs/research-roadmap.md]]

## Summary

Objective: determine whether decision nodes can be systematically extracted from price. Status: active foundation. Objective: model structural nodes as zones with revisit, hunt, break, consumption, and termination. Status: active foundation. Objective: detect whether reversal and continuation states cluster in live-valid known-time sequences. Current standard: classic sample reports are legacy, causal sample-batch reports are diagnostic, atomic no-sample reports are official. Objective: test whether known regime state improves the next structural decision. Current standard: reversal and continuation must be separated, entry must occur after regime is known, risk must be explicit, continuation path R and execution R must be separated. Objective: transform validated structural facts into executable EAs. Current families: reversal reaction execution, continuation path execution. Objective:

## Concepts

[[docs/obsidian_deep/02_concepts/Atomic_No-Sample|Atomic No-Sample]], [[docs/obsidian_deep/02_concepts/Decision_Node|Decision Node]], [[docs/obsidian_deep/02_concepts/Execution____Risk|Execution / Risk]], [[docs/obsidian_deep/02_concepts/Known-Time_Causality|Known-Time Causality]], [[docs/obsidian_deep/02_concepts/UI____React|UI / React]], [[docs/obsidian_deep/02_concepts/Validation____Audit|Validation / Audit]], [[docs/obsidian_deep/02_concepts/Zone____RTV|Zone / RTV]]

## Entities

—

## Headings

- Research Roadmap
  - Phase 1 — Structural Nodes
  - Phase 2 — Node Territory and Lifecycle
  - Phase 3 — Regime Memory
  - Phase 4 — Directional Memory
  - Phase 5 — Execution Families
  - Phase 6 — Robustness and Baselines
  - Phase 7 — Production Hardening

## Related Source Documents

- [[docs/ui/ROADMAP|ROADMAP.md]] — score `20`
- [[lab/05_validation/VAL_M0001_MQL_NATIVE/report|report.md]] — score `16`
- [[docs/architecture|architecture.md]] — score `15`
- [[docs/atomic_live_research_contract|atomic_live_research_contract.md]] — score `15`
- [[docs/glossary|glossary.md]] — score `15`
- [[papers/001_atomic_live_regime_framework|001_atomic_live_regime_framework.md]] — score `14`
- [[README|README.md]] — score `14`
- [[lab/03_experiments/EXP0002_mql_native_m0001/report|report.md]] — score `14`
- [[lab/03_experiments/EXP0003_mql_native_m0002/report|report.md]] — score `14`
- [[lab/03_experiments/EXP0004_mql_native_m0004/report|report.md]] — score `14`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
