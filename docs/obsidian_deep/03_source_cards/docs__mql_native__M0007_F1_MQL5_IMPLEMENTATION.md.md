
---
type: source_card
source_path: "docs/mql_native/M0007_F1_MQL5_IMPLEMENTATION.md"
source_ext: ".md"
source_size: 1507
empty: false
generated_at: 2026-07-06
concepts: ["Decision Node", "Execution / Risk", "Flag Counting", "MQL Native", "Validation / Audit"]
entities: ["M0007"]
---

# Source Card — M0007_F1_MQL5_IMPLEMENTATION.md

## Source

[[docs/mql_native/M0007_F1_MQL5_IMPLEMENTATION|docs/mql_native/M0007_F1_MQL5_IMPLEMENTATION.md]]

## Summary

The module is placed using the clean M-series folder convention: No folder repeats the project name. The project root already carries that identity. This is an MQL module, so its runtime/module name is `M0007`. Code, EA file names, include names, object prefixes, print tags, and module folders all use `M0007`. Bullish sequence: Rules: `H2 > H1` `N2 < N1` `N2 > W` `R12 < H2` break of `R12` arms the structure break of `H2` confirms the structure break of `W` before confirmation invalidates the structure Bearish sequence: Rules: `L2 < L1` `N2 > N1` `N2 < W` `R12 > L2` break of `R12` arms the structure break of `L2` confirms the structure break of `W` before confirmation invalidates the structure The detector scans a range of L values and merges overlapping representations. Each event stores: `L_used` `matched_L_values` This keeps counting adaptive while still deterministic. The Expert Advis

## Concepts

[[docs/obsidian_deep/02_concepts/Decision_Node|Decision Node]], [[docs/obsidian_deep/02_concepts/Execution____Risk|Execution / Risk]], [[docs/obsidian_deep/02_concepts/Flag_Counting|Flag Counting]], [[docs/obsidian_deep/02_concepts/MQL_Native|MQL Native]], [[docs/obsidian_deep/02_concepts/Validation____Audit|Validation / Audit]]

## Entities

M0007

## Headings

- M0007 — Adaptive F1 Flag Counting MQL5 Implementation
  - Correct project layout
  - Naming lock
  - F1 rules implemented
  - Adaptive L
  - Scope

## Related Source Documents

- [[docs/mql_native/H0007_F1_MQL5_IMPLEMENTATION|H0007_F1_MQL5_IMPLEMENTATION.md]] — score `16`
- [[docs/mql_native/H0007_FLAG_COUNTING_F1_START_STRUCTURE|H0007_FLAG_COUNTING_F1_START_STRUCTURE.md]] — score `16`
- [[docs/flag_counting/FLAG_COUNTING_CURRENT_CANON|FLAG_COUNTING_CURRENT_CANON.md]] — score `15`
- [[docs/flag_counting/implementation_ladder_v1/16_IMPLEMENTATION_ORDER_AND_ACCEPTANCE_MATRIX|16_IMPLEMENTATION_ORDER_AND_ACCEPTANCE_MATRIX.md]] — score `15`
- [[docs/flag_counting/README|README.md]] — score `15`
- [metadata.yaml](../../lab/03_experiments/EXP_flag_counting/metadata.yaml) — score `15`
- [[lab/03_experiments/EXP_flag_counting/README|README.md]] — score `15`
- [[mql5/Include/M0007/README_M0007_FlagCountingF1|README_M0007_FlagCountingF1.md]] — score `15`
- [[docs/debug/MARKET_LANGUAGE/README|README.md]] — score `13`
- [[docs/flag_counting/FLAG_COUNTING_VNEXT_IMPLEMENTATION|FLAG_COUNTING_VNEXT_IMPLEMENTATION.md]] — score `13`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
