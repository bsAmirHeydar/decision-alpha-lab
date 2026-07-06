
---
type: source_card
source_path: "docs/mql_native/H0007_FLAG_COUNTING_F1_START_STRUCTURE.md"
source_ext: ".md"
source_size: 31681
empty: false
generated_at: 2026-07-06
concepts: ["AI Agent Layer", "Convexity / Optionality", "Decision Node", "Execution / Risk", "Flag Counting", "Hook", "Known-Time Causality", "MQL Native", "Path Smoothness", "UI / React", "Validation / Audit", "Zone / RTV"]
entities: ["H0001", "H0002", "H0004", "H0005", "H0006", "H0007", "M0001", "M0007"]
---

# Source Card — H0007_FLAG_COUNTING_F1_START_STRUCTURE.md

## Source

[[docs/mql_native/H0007_FLAG_COUNTING_F1_START_STRUCTURE|docs/mql_native/H0007_FLAG_COUNTING_F1_START_STRUCTURE.md]]

## Summary

> Status: design lock, topology-only. > Version: v0.2 — nested `R12` rule added and expanded. > Layer: structural grammar on top of the M0001 final-only known-time node stream. > Scope: define and audit **F1 only**. F2 and F3 are intentionally out of scope until F1 is mechanically stable. The purpose of this README is to turn the visual idea of **F1** into a mechanical object. F1 must not remain a drawing. It must become something that the code can count, draw, invalidate, confirm, export, and later compare against random baselines. This document is therefore not a trading strategy. It is a **structural counting contract**. The detector must answer one narrow question first: Only after that can H0007 ask alpha questions such as forward MFE, MAE, path cleanliness, directional memory, optionality, or execution quality. The working thesis is: But this project does not accept vague chart-pat

## Concepts

[[docs/obsidian_deep/02_concepts/AI_Agent_Layer|AI Agent Layer]], [[docs/obsidian_deep/02_concepts/Convexity____Optionality|Convexity / Optionality]], [[docs/obsidian_deep/02_concepts/Decision_Node|Decision Node]], [[docs/obsidian_deep/02_concepts/Execution____Risk|Execution / Risk]], [[docs/obsidian_deep/02_concepts/Flag_Counting|Flag Counting]], [[docs/obsidian_deep/02_concepts/Hook|Hook]], [[docs/obsidian_deep/02_concepts/Known-Time_Causality|Known-Time Causality]], [[docs/obsidian_deep/02_concepts/MQL_Native|MQL Native]], [[docs/obsidian_deep/02_concepts/Path_Smoothness|Path Smoothness]], [[docs/obsidian_deep/02_concepts/UI____React|UI / React]], [[docs/obsidian_deep/02_concepts/Validation____Audit|Validation / Audit]], [[docs/obsidian_deep/02_concepts/Zone____RTV|Zone / RTV]]

## Entities

H0001, H0002, H0004, H0005, H0006, H0007, M0001, M0007

## Headings

- H0007 — Flag Counting / F1 Start Structure
  - 0. Why this document exists
  - 1. Core thesis
  - 2. Reference sketches
  - 3. Critical corrections locked in v0.2
    - 3.1 `R12` break is not final confirmation
    - 3.2 `R12` must stay inside the main second extreme
  - 4. Canonical naming
    - 4.1 Bullish F1 names
    - 4.2 Bearish F1 names
  - 5. F1 is not a trade
  - 6. Source contract: known-time nodes only

## Related Source Documents

- [[README|README.md]] — score `49`
- [[docs/mql_native/MODULE_MAP|MODULE_MAP.md]] — score `37`
- [[lab/02_hypotheses/H0001_structural_highs_lows_as_decision_nodes|H0001_structural_highs_lows_as_decision_nodes.md]] — score `35`
- [[docs/mql_native/H0001_H0002_ALGORITHM_AND_HYPOTHESIS_README|H0001_H0002_ALGORITHM_AND_HYPOTHESIS_README.md]] — score `33`
- [[docs/mql_native/H0001_H0004_RESEARCH_LOCK|H0001_H0004_RESEARCH_LOCK.md]] — score `33`
- [[docs/mql_native/H0004_BRANCH_REGIME_CLUSTERING|H0004_BRANCH_REGIME_CLUSTERING.md]] — score `33`
- [[lab/02_hypotheses/H0005_contextual_branch_regime_state|H0005_contextual_branch_regime_state.md]] — score `33`
- [[lab/09_execution/mql5/README|README.md]] — score `33`
- [[docs/flag_counting/README|README.md]] — score `33`
- [[docs/mql_native/M0002_REVERSAL_CONTINUATION_EXIT_VOLATILITY|M0002_REVERSAL_CONTINUATION_EXIT_VOLATILITY.md]] — score `32`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
