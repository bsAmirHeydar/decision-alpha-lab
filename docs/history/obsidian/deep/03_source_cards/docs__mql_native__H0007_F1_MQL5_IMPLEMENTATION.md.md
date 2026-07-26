
---
type: source_card
source_path: "docs/mql_native/H0007_F1_MQL5_IMPLEMENTATION.md"
source_ext: ".md"
source_size: 1338
empty: false
generated_at: 2026-07-06
concepts: ["Decision Node", "Execution / Risk", "Flag Counting", "MQL Native", "Validation / Audit"]
entities: ["H0007", "M0007"]
---

# Source Card — H0007_F1_MQL5_IMPLEMENTATION.md

## Source

[[docs/mql_native/H0007_F1_MQL5_IMPLEMENTATION|docs/mql_native/H0007_F1_MQL5_IMPLEMENTATION.md]]

## Summary

The implementation follows the DecisionAlphaLab MQL5 layout: The EA file stays inside `mql5/Experts/DecisionAlphaLab`. The reusable `.mqh` files stay inside `mql5/Include/DecisionAlphaLab/H0007_FlagCountingF1`. The module is a native MQL5 visual audit implementation of H0007 F1. It performs: adaptive L scanning, L-rule node extraction, bullish and bearish F1 topology detection, protected waist invalidation, R12 internal trigger detection, H2/L2 final confirmation detection, overlap merge between candidate structures, chart drawing of the complete F1 count. This is not a trading robot. It does not call `OrderSend`, does not place pending orders, does not open positions, and does not define risk logic. Its only purpose is to make F1 mechanically countable and visually auditable before F2 is defined.

## Concepts

[[docs/obsidian_deep/02_concepts/Decision_Node|Decision Node]], [[docs/obsidian_deep/02_concepts/Execution____Risk|Execution / Risk]], [[docs/obsidian_deep/02_concepts/Flag_Counting|Flag Counting]], [[docs/obsidian_deep/02_concepts/MQL_Native|MQL Native]], [[docs/obsidian_deep/02_concepts/Validation____Audit|Validation / Audit]]

## Entities

H0007, M0007

## Headings

- H0007 / M0007 — F1 Adaptive Flag Counting MQL5 Implementation
  - Correct folder structure
  - Design
  - No trading execution

## Related Source Documents

- [[docs/mql_native/H0007_FLAG_COUNTING_F1_START_STRUCTURE|H0007_FLAG_COUNTING_F1_START_STRUCTURE.md]] — score `21`
- [[docs/mql_native/M0007_F1_MQL5_IMPLEMENTATION|M0007_F1_MQL5_IMPLEMENTATION.md]] — score `16`
- [[docs/flag_counting/FLAG_COUNTING_CURRENT_CANON|FLAG_COUNTING_CURRENT_CANON.md]] — score `15`
- [[docs/flag_counting/implementation_ladder_v1/16_IMPLEMENTATION_ORDER_AND_ACCEPTANCE_MATRIX|16_IMPLEMENTATION_ORDER_AND_ACCEPTANCE_MATRIX.md]] — score `15`
- [[docs/flag_counting/README|README.md]] — score `15`
- [metadata.yaml](../../lab/03_experiments/EXP_flag_counting/metadata.yaml) — score `15`
- [[lab/03_experiments/EXP_flag_counting/README|README.md]] — score `15`
- [[mql5/Include/M0007/README_M0007_FlagCountingF1|README_M0007_FlagCountingF1.md]] — score `15`
- [[lab/02_hypotheses/H0007_flag_counting_f1_start_structure|H0007_flag_counting_f1_start_structure.md]] — score `13`
- [[docs/debug/MARKET_LANGUAGE/README|README.md]] — score `13`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
