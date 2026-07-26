---
title: "H0007 / M0007 — F1 Adaptive Flag Counting MQL5 Implementation"
type: document_card
generated_by: alpha_lab_obsidian_builder
generated_at: 2026-07-06
source_path: "docs/mql_native/H0007_F1_MQL5_IMPLEMENTATION.md"
source_ext: ".md"
category: "mql_native_docs"
source_size_bytes: "1338"
entities:
  - "H0007"
  - "M0007"
concepts:
  - "Execution"
  - "F-Counting"
  - "MQL Native"
  - "NDS Anatomy"
  - "Validation"
---


# H0007 / M0007 — F1 Adaptive Flag Counting MQL5 Implementation

**Source:** [[docs/mql_native/H0007_F1_MQL5_IMPLEMENTATION|docs/mql_native/H0007_F1_MQL5_IMPLEMENTATION.md]]

**Category:** `mql_native_docs`  
**Status:** ok  
**Size:** `1338` bytes

## خلاصه

The implementation follows the DecisionAlphaLab MQL5 layout: The EA file stays inside `mql5/Experts/DecisionAlphaLab`. The reusable `.mqh` files stay inside `mql5/Include/DecisionAlphaLab/H0007_FlagCountingF1`. The module is a native MQL5 visual audit implementation of H0007 F1. It performs: adaptive L scanning, L-rule node extraction, bullish and bearish F1 topology detection, protected waist invalidation, R12 internal trigger detection, H2/L2 final confirmation detection, overlap merge between candidate structures, chart drawing of the complete F1 count. This is not a trading robot. It does not call `OrderSend`, does not place pending orders, does not open positions, and does not define ri

## Headings

- H0007 / M0007 — F1 Adaptive Flag Counting MQL5 Implementation
-   Correct folder structure
-   Design
-   No trading execution

## Entities

`H0007`, `M0007`

## Concepts

- [[docs/obsidian/04_concepts/Execution|Execution]]
- [[docs/obsidian/04_concepts/F-Counting|F-Counting]]
- [[docs/obsidian/04_concepts/MQL_Native|MQL Native]]
- [[docs/evidence/nds_anatomy/6a11c75733b2_NDS_Anatomy|NDS Anatomy]]
- [[docs/obsidian/04_concepts/Validation|Validation]]

## Related documents

- [[docs/mql_native/H0007_FLAG_COUNTING_F1_START_STRUCTURE|H0007 — Flag Counting / F1 Start Structure]] — `mql_native_docs`
- [[docs/mql_native/M0007_F1_MQL5_IMPLEMENTATION|M0007 — Adaptive F1 Flag Counting MQL5 Implementation]] — `mql_native_docs`
- [[docs/flag_counting/FLAG_COUNTING_CURRENT_CANON|Flag Counting Current Canon]] — `flag_counting_docs`
- [[docs/flag_counting/implementation_ladder_v1/16_IMPLEMENTATION_ORDER_AND_ACCEPTANCE_MATRIX|Phoenix Flag Counting Implementation Ladder V1]] — `flag_counting_docs`
- [[docs/flag_counting/README|Flag Counting Documentation]] — `flag_counting_docs`
- [[lab/03_experiments/EXP_flag_counting/README|EXP Flag Counting]] — `experiment`
- [[mql5/Include/M0007/README_M0007_FlagCountingF1|M0007 — F1 Flag Counting MQL5 Module]] — `mql5_docs`
- [[docs/evidence/h0007_flag_counting_f1_start_structure/d02c831e47bd_H0007_flag_counting_f1_start_structure|H0007 — Flag Counting / F1 Start Structure]] — `hypothesis`
- [[docs/debug/MARKET_LANGUAGE/README|DAL Market Language — Nodes, Cycles, Hooks, Rallies, Flags, 123 Flags, and Open 1/2s]] — `debug_docs`
- [[docs/flag_counting/FLAG_COUNTING_VNEXT_IMPLEMENTATION|Flag Counting vNext Implementation Notes]] — `flag_counting_docs`
- [[docs/releases/legacy_migration/general/b7d4f188eb79_README_FLAG_COUNTING_PHOENIX|EXP Flag Counting Phoenix]] — `experiment`
- [[docs/mql_native/FLAG_COUNTING_MQL5_IMPLEMENTATION|Flag Counting MQL5 Implementation]] — `mql_native_docs`

## Recommended Obsidian use

- این card را به نوت‌های concept، hypothesis، experiment یا ADR مربوط link کن.
- اگر این سند source of truth است، در MOC مربوطه بالاتر از اسناد legacy قرارش بده.
- اگر این سند report/validation است، نتیجه نهایی آن را به registry مربوط sync کن.
