
---
type: source_card
source_path: "docs/ui/ROADMAP.md"
source_ext: ".md"
source_size: 4031
empty: false
generated_at: 2026-07-06
concepts: ["AI Agent Layer", "Decision Node", "Execution / Risk", "Known-Time Causality", "Python Brain", "UI / React", "Validation / Audit", "Zone / RTV"]
entities: ["EXP0001", "H0001", "H0002", "M0001"]
---

# Source Card — ROADMAP.md

## Source

[[docs/ui/ROADMAP|docs/ui/ROADMAP.md]]

## Summary

Build the UI as a professional research terminal in layers. Do not start by drawing every possible feature. Start by building the central replay engine and typed visualization API. Deliverables: `docs/ui/README.md` `docs/ui/ARCHITECTURE.md` `docs/ui/FOLDER_STRUCTURE.md` `docs/ui/VISUAL_REPLAY_PROTOCOL.md` `docs/ui/VISUALIZATION_API.md` `docs/ui/ROADMAP.md` `apps/README.md` `apps/api/README.md` `apps/web/README.md` Definition of done: UI purpose is clear. Research/UI boundary is clear. Replay behavior is specified. Visualization contract is metric-agnostic. Folder structure is agreed before code is written. Goal: Expose existing research data to the UI without changing the lab engine. Endpoints: Definition of done: API reads existing parquet cache. API can return GOLD M15 and #US30 M15 candles. API can return confirmed L-rule nodes. API can return M0001 events. API can produce `ui.visuali

## Concepts

[[docs/obsidian_deep/02_concepts/AI_Agent_Layer|AI Agent Layer]], [[docs/obsidian_deep/02_concepts/Decision_Node|Decision Node]], [[docs/obsidian_deep/02_concepts/Execution____Risk|Execution / Risk]], [[docs/obsidian_deep/02_concepts/Known-Time_Causality|Known-Time Causality]], [[docs/obsidian_deep/02_concepts/Python_Brain|Python Brain]], [[docs/obsidian_deep/02_concepts/UI____React|UI / React]], [[docs/obsidian_deep/02_concepts/Validation____Audit|Validation / Audit]], [[docs/obsidian_deep/02_concepts/Zone____RTV|Zone / RTV]]

## Entities

EXP0001, H0001, H0002, M0001

## Headings

- UI Implementation Roadmap
  - Strategy
  - Phase 0 — Architecture Freeze
  - Phase 1 — Backend Read API
  - Phase 2 — Frontend Shell
  - Phase 3 — Market Replay Core
  - Phase 4 — M0001 Visual Adapter
  - Phase 5 — Research Lineage Browser
  - Phase 6 — Experiment and Validation Workbench
  - Phase 7 — Live Monitor Mode

## Related Source Documents

- [[docs/ui/VISUALIZATION_API|VISUALIZATION_API.md]] — score `43`
- [[README|README.md]] — score `37`
- [[docs/mql_native/H0007_FLAG_COUNTING_F1_START_STRUCTURE|H0007_FLAG_COUNTING_F1_START_STRUCTURE.md]] — score `29`
- [[docs/mql_native/MODULE_MAP|MODULE_MAP.md]] — score `29`
- [[docs/architecture|architecture.md]] — score `29`
- [[docs/mql_native/H0001_H0002_ALGORITHM_AND_HYPOTHESIS_README|H0001_H0002_ALGORITHM_AND_HYPOTHESIS_README.md]] — score `27`
- [[docs/mql_native/H0001_H0004_RESEARCH_LOCK|H0001_H0004_RESEARCH_LOCK.md]] — score `27`
- [[docs/mql_native/H0003_CONTINUATION_INERTIA_MEMORY_CLUSTERING|H0003_CONTINUATION_INERTIA_MEMORY_CLUSTERING.md]] — score `27`
- [[docs/mql_native/H0003_INERTIA_MEMORY_RESULTS_AND_ALGORITHM|H0003_INERTIA_MEMORY_RESULTS_AND_ALGORITHM.md]] — score `27`
- [[docs/mql_native/H0004_BRANCH_REGIME_CLUSTERING|H0004_BRANCH_REGIME_CLUSTERING.md]] — score `27`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
