
---
type: source_card
source_path: "docs/flag_counting/FLAG_COUNTING_VNEXT_IMPLEMENTATION.md"
source_ext: ".md"
source_size: 4437
empty: false
generated_at: 2026-07-06
concepts: ["AI Agent Layer", "Decision Node", "Flag Counting", "Hook", "MQL Native", "Path Smoothness", "UI / React", "Validation / Audit"]
entities: ["M0007", "M0008"]
---

# Source Card — FLAG_COUNTING_VNEXT_IMPLEMENTATION.md

## Source

[[docs/flag_counting/FLAG_COUNTING_VNEXT_IMPLEMENTATION|docs/flag_counting/FLAG_COUNTING_VNEXT_IMPLEMENTATION.md]]

## Summary

<!-- CURRENT CANON NOTICE This file is retained as historical/context documentation. For current Phoenix implementation decisions, use: docs/flag_counting/FLAG_COUNTING_CURRENT_CANON.md If this file conflicts with the current canon, the current canon wins. --> This document maps the v3 concept specification into the first clean MQL5 implementation module. Previous implementations evolved through patches over a pattern scanner. That architecture was not aligned with the final concept: Flag counting is fractal. Several sequences can be active in parallel. A confirmed F1 must spawn the search for F2. A confirmed F2 must spawn the search for F3. Different swing scales can produce different valid sequences. The vNext module starts from a clean event model and avoids the old M0007/M0008 path. Each detected structure is an `FCN_Event` with: scale level `scale_L` sequence id parent event id chai

## Concepts

[[docs/obsidian_deep/02_concepts/AI_Agent_Layer|AI Agent Layer]], [[docs/obsidian_deep/02_concepts/Decision_Node|Decision Node]], [[docs/obsidian_deep/02_concepts/Flag_Counting|Flag Counting]], [[docs/obsidian_deep/02_concepts/Hook|Hook]], [[docs/obsidian_deep/02_concepts/MQL_Native|MQL Native]], [[docs/obsidian_deep/02_concepts/Path_Smoothness|Path Smoothness]], [[docs/obsidian_deep/02_concepts/UI____React|UI / React]], [[docs/obsidian_deep/02_concepts/Validation____Audit|Validation / Audit]]

## Entities

M0007, M0008

## Headings

- Flag Counting vNext Implementation Notes
  - 1. Why a vNext module exists
  - 2. Data model
  - 3. Node engine
  - 4. F1 logic
  - 5. F2 logic
  - 6. F3 logic
  - 7. Rendering
  - 8. Inputs
  - 9. Next work
  - Origin identity and live-root display contract

## Related Source Documents

- [[docs/flag_counting/FLAG_COUNTING_CURRENT_CANON|FLAG_COUNTING_CURRENT_CANON.md]] — score `28`
- [[docs/mql_native/H0007_FLAG_COUNTING_F1_START_STRUCTURE|H0007_FLAG_COUNTING_F1_START_STRUCTURE.md]] — score `21`
- [[docs/flag_counting/README|README.md]] — score `20`
- [[docs/flag_counting/implementation_ladder_v1/16_IMPLEMENTATION_ORDER_AND_ACCEPTANCE_MATRIX|16_IMPLEMENTATION_ORDER_AND_ACCEPTANCE_MATRIX.md]] — score `19`
- [[lab/03_experiments/EXP_flag_counting/README|README.md]] — score `19`
- [[mql5/Include/M0007/README_M0007_FlagCountingF1|README_M0007_FlagCountingF1.md]] — score `19`
- [[docs/architecture|architecture.md]] — score `18`
- [[docs/debug/MARKET_LANGUAGE/README|README.md]] — score `17`
- [[docs/releases/legacy_migration/general/b7d4f188eb79_README_FLAG_COUNTING_PHOENIX|README_FLAG_COUNTING_PHOENIX.md]] — score `17`
- [[docs/flag_counting/FLAG_COUNTING_V6_IMPLEMENTATION_NOTES|FLAG_COUNTING_V6_IMPLEMENTATION_NOTES.md]] — score `17`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
