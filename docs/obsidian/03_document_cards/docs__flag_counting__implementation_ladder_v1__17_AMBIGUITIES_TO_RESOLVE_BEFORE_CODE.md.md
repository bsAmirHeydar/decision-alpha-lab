---
title: "Phoenix Level 17 — Ambiguity Resolution / Final Decision Lock"
type: document_card
generated_by: alpha_lab_obsidian_builder
generated_at: 2026-07-06
source_path: "docs/flag_counting/implementation_ladder_v1/17_AMBIGUITIES_TO_RESOLVE_BEFORE_CODE.md"
source_ext: ".md"
category: "flag_counting_docs"
source_size_bytes: "4341"
concepts:
  - "Convexity"
  - "F-Counting"
  - "Hook"
  - "MQL Native"
  - "NDS Anatomy"
  - "Validation"
---


# Phoenix Level 17 — Ambiguity Resolution / Final Decision Lock

**Source:** [[docs/flag_counting/implementation_ladder_v1/17_AMBIGUITIES_TO_RESOLVE_BEFORE_CODE|docs/flag_counting/implementation_ladder_v1/17_AMBIGUITIES_TO_RESOLVE_BEFORE_CODE.md]]

**Category:** `flag_counting_docs`  
**Status:** ok  
**Size:** `4341` bytes

## خلاصه

Implemented in Phoenix Level 17. Runtime modules: EA support: The old purpose of this document was to list unresolved questions before code. That is now closed. Level 17 turns those decisions into a runtime decision registry and emits `FP_LEVEL17` after Level 16 acceptance and before `FP_SUMMARY`. The canonical source remains: Level 17 does not replace the canon. It audits whether the active EA inputs and runtime reports are aligned with the canon decisions. Level 17 checks the following decision families: 1. Canon source is `FLAG_COUNTING_CURRENT_CANON.md`. 2. `identity_generation_pass` is `phoenix_level17`. 3. Closed-bar timebase remains default. 4. Confirmed F bodies do not consume live p

## Headings

- Phoenix Level 17 — Ambiguity Resolution / Final Decision Lock
-   Status
-   Source of truth
-   Runtime position
-   Level 17 decisions checked
-   EA inputs
-   Optional CSV
-   Non-authority rule
-   Acceptance

## Concepts

- [[docs/obsidian/04_concepts/Convexity|Convexity]]
- [[docs/obsidian/04_concepts/F-Counting|F-Counting]]
- [[docs/obsidian/04_concepts/Hook|Hook]]
- [[docs/obsidian/04_concepts/MQL_Native|MQL Native]]
- [[docs/obsidian/04_concepts/NDS_Anatomy|NDS Anatomy]]
- [[docs/obsidian/04_concepts/Validation|Validation]]

## Related documents

- [[docs/flag_counting/FLAG_COUNTING_CURRENT_CANON|Flag Counting Current Canon]] — `flag_counting_docs`
- [[docs/flag_counting/implementation_ladder_v1/05_LEVEL_05_FLAG_BODY_ENGINE|Phoenix Flag Counting Implementation Ladder V1]] — `flag_counting_docs`
- [[docs/flag_counting/implementation_ladder_v1/07_LEVEL_07_F1_LIFECYCLE_ENGINE|Phoenix Flag Counting Implementation Ladder V1]] — `flag_counting_docs`
- [[docs/flag_counting/implementation_ladder_v1/11_LEVEL_11_CANONICALIZATION_AND_AUDIT|Phoenix Flag Counting Implementation Ladder V1]] — `flag_counting_docs`
- [[docs/flag_counting/implementation_ladder_v1/12_LEVEL_12_RENDERER_AND_LABEL_LAYOUT|Level 12 — Renderer / Labels / Visual Layer]] — `flag_counting_docs`
- [[docs/flag_counting/implementation_ladder_v1/15_MODULE_INTERFACE_CONTRACTS|Phoenix Flag Counting Implementation Ladder V1]] — `flag_counting_docs`
- [[docs/flag_counting/implementation_ladder_v1/16_IMPLEMENTATION_ORDER_AND_ACCEPTANCE_MATRIX|Phoenix Flag Counting Implementation Ladder V1]] — `flag_counting_docs`
- [[docs/flag_counting/implementation_ladder_v1/README|Phoenix Flag Counting Implementation Ladder V1]] — `flag_counting_docs`
- [[lab/03_experiments/EXP0002_mql_native_m0001/report|EXP0002 — MQL-native M0001 Runtime]] — `experiment`
- [[lab/03_experiments/EXP0003_mql_native_m0002/report|EXP0003 — M0002 Reversal/Continuation Exit Volatility]] — `experiment`
- [[lab/03_experiments/EXP0004_mql_native_m0004/report|EXP0004 — MQL-native M0004 Branch Regime Clustering]] — `experiment`
- [[lab/05_validation/VAL_M0001_MQL_NATIVE/report|VAL_M0001_MQL_NATIVE]] — `validation`

## Recommended Obsidian use

- این card را به نوت‌های concept، hypothesis، experiment یا ADR مربوط link کن.
- اگر این سند source of truth است، در MOC مربوطه بالاتر از اسناد legacy قرارش بده.
- اگر این سند report/validation است، نتیجه نهایی آن را به registry مربوط sync کن.
