
---
type: source_card
source_path: "reports/mql_native/M0004/README.md"
source_ext: ".md"
source_size: 1482
empty: false
generated_at: 2026-07-06
concepts: ["AI Agent Layer", "Execution / Risk", "Validation / Audit", "Zone / RTV"]
entities: ["M0004"]
---

# Source Card — README.md

## Source

[[reports/mql_native/M0004/README|reports/mql_native/M0004/README.md]]

## Summary

Paste or archive MT5 Journal output for `DAL_M0004_*` final reports here. M0004 v1.01 adds expanded regime detail and strict engineered random/null diagnostics: `FINAL_BLOCK_PROFILE_FAST/MAIN/SLOW` for branch concentration across multiple event-block granularities. `FINAL_RUN_LENGTH_TRANSITION` for duration-dependent branch persistence. `FINAL_LAG_DECAY` for local-vs-far branch memory decay. `FINAL_STRATIFIED_PERM_SESSION/PREVOL/REVISIT/COMPOSITE` for stricter label shuffles preserving branch counts inside regime strata. `FINAL_CIRCULAR_SHIFT_STRESS` for far-shift adjacency placebo. `FINAL_BLOCK_ORDER_SHUFFLE_STRESS` for a block-preserving null. `FINAL_*_DETAIL_*` lines for richer session, pre-volatility, revisit, and event-spacing regime diagnostics. The strongest null is the composite stratified permutation, which preserves branch counts within `session × pre-vol tercile × trend regime

## Concepts

[[docs/obsidian_deep/02_concepts/AI_Agent_Layer|AI Agent Layer]], [[docs/obsidian_deep/02_concepts/Execution____Risk|Execution / Risk]], [[docs/obsidian_deep/02_concepts/Validation____Audit|Validation / Audit]], [[docs/obsidian_deep/02_concepts/Zone____RTV|Zone / RTV]]

## Entities

M0004

## Headings

- M0004 reports
  - v1.01 report additions
  - v1.04 consensus quality diagnostics

## Related Source Documents

- [[lab/03_experiments/EXP0004_mql_native_m0004/report|report.md]] — score `19`
- [signals.yaml](../../registry/signals.yaml) — score `14`
- [[docs/architecture|architecture.md]] — score `13`
- [[docs/debug/D0007_H5_CAUSAL_LIVE_REPLAY_AUDIT|D0007_H5_CAUSAL_LIVE_REPLAY_AUDIT.md]] — score `13`
- [[docs/mql_native/H0001_H0002_ALGORITHM_AND_HYPOTHESIS_README|H0001_H0002_ALGORITHM_AND_HYPOTHESIS_README.md]] — score `13`
- [[docs/mql_native/H0001_H0004_RESEARCH_LOCK|H0001_H0004_RESEARCH_LOCK.md]] — score `13`
- [[docs/mql_native/H0004_BRANCH_REGIME_CLUSTERING|H0004_BRANCH_REGIME_CLUSTERING.md]] — score `13`
- [[docs/mql_native/H0005_CONTEXTUAL_BRANCH_REGIME_STATE|H0005_CONTEXTUAL_BRANCH_REGIME_STATE.md]] — score `13`
- [[docs/mql_native/MODULE_MAP|MODULE_MAP.md]] — score `13`
- [[lab/02_hypotheses/H0004_branch_regime_clustering|H0004_branch_regime_clustering.md]] — score `13`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
