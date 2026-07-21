---
title: "M0007 — Adaptive F1 Flag Counting MQL5 Implementation"
type: document_card
generated_by: alpha_lab_obsidian_builder
generated_at: 2026-07-06
source_path: "docs/mql_native/M0007_F1_MQL5_IMPLEMENTATION.md"
source_ext: ".md"
category: "mql_native_docs"
source_size_bytes: "1507"
entities:
  - "M0007"
concepts:
  - "Execution"
  - "F-Counting"
  - "MQL Native"
  - "NDS Anatomy"
  - "Validation"
---


# M0007 — Adaptive F1 Flag Counting MQL5 Implementation

**Source:** [[docs/mql_native/M0007_F1_MQL5_IMPLEMENTATION|docs/mql_native/M0007_F1_MQL5_IMPLEMENTATION.md]]

**Category:** `mql_native_docs`  
**Status:** ok  
**Size:** `1507` bytes

## خلاصه

The module is placed using the clean M-series folder convention: No folder repeats the project name. The project root already carries that identity. This is an MQL module, so its runtime/module name is `M0007`. Code, EA file names, include names, object prefixes, print tags, and module folders all use `M0007`. Bullish sequence: Rules: `H2 > H1` `N2 < N1` `N2 > W` `R12 < H2` break of `R12` arms the structure break of `H2` confirms the structure break of `W` before confirmation invalidates the structure Bearish sequence: Rules: `L2 < L1` `N2 > N1` `N2 < W` `R12 > L2` break of `R12` arms the structure break of `L2` confirms the structure break of `W` before confirmation invalidates the structur

## Headings

- M0007 — Adaptive F1 Flag Counting MQL5 Implementation
-   Correct project layout
-   Naming lock
-   F1 rules implemented
-   Adaptive L
-   Scope

## Entities

`M0007`

## Concepts

- [[docs/obsidian/04_concepts/Execution|Execution]]
- [[docs/obsidian/04_concepts/F-Counting|F-Counting]]
- [[docs/obsidian/04_concepts/MQL_Native|MQL Native]]
- [[docs/evidence/nds_anatomy/6a11c75733b2_NDS_Anatomy|NDS Anatomy]]
- [[docs/obsidian/04_concepts/Validation|Validation]]

## Related documents

- [[docs/mql_native/H0007_F1_MQL5_IMPLEMENTATION|H0007 / M0007 — F1 Adaptive Flag Counting MQL5 Implementation]] — `mql_native_docs`
- [[docs/mql_native/H0007_FLAG_COUNTING_F1_START_STRUCTURE|H0007 — Flag Counting / F1 Start Structure]] — `mql_native_docs`
- [[docs/flag_counting/FLAG_COUNTING_CURRENT_CANON|Flag Counting Current Canon]] — `flag_counting_docs`
- [[docs/flag_counting/implementation_ladder_v1/16_IMPLEMENTATION_ORDER_AND_ACCEPTANCE_MATRIX|Phoenix Flag Counting Implementation Ladder V1]] — `flag_counting_docs`
- [[docs/flag_counting/README|Flag Counting Documentation]] — `flag_counting_docs`
- [[lab/03_experiments/EXP_flag_counting/README|EXP Flag Counting]] — `experiment`
- [[mql5/Include/M0007/README_M0007_FlagCountingF1|M0007 — F1 Flag Counting MQL5 Module]] — `mql5_docs`
- [[docs/debug/MARKET_LANGUAGE/README|DAL Market Language — Nodes, Cycles, Hooks, Rallies, Flags, 123 Flags, and Open 1/2s]] — `debug_docs`
- [[docs/flag_counting/FLAG_COUNTING_VNEXT_IMPLEMENTATION|Flag Counting vNext Implementation Notes]] — `flag_counting_docs`
- [[docs/releases/legacy_migration/general/b7d4f188eb79_README_FLAG_COUNTING_PHOENIX|EXP Flag Counting Phoenix]] — `experiment`
- [[docs/mql_native/FLAG_COUNTING_MQL5_IMPLEMENTATION|Flag Counting MQL5 Implementation]] — `mql_native_docs`
- [[docs/evidence/m0001_excel_audit/ff999bc7279e_M0001_EXCEL_AUDIT_REPORT|M0001 Excel Audit Report]] — `mql_native_docs`

## Recommended Obsidian use

- این card را به نوت‌های concept، hypothesis، experiment یا ADR مربوط link کن.
- اگر این سند source of truth است، در MOC مربوطه بالاتر از اسناد legacy قرارش بده.
- اگر این سند report/validation است، نتیجه نهایی آن را به registry مربوط sync کن.
