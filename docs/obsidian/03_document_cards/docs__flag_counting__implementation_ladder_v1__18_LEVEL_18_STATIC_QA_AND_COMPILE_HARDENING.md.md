---
title: "Level 18 — Static QA / Compile Hardening"
type: document_card
generated_by: alpha_lab_obsidian_builder
generated_at: 2026-07-06
source_path: "docs/flag_counting/implementation_ladder_v1/18_LEVEL_18_STATIC_QA_AND_COMPILE_HARDENING.md"
source_ext: ".md"
category: "flag_counting_docs"
source_size_bytes: "2522"
concepts:
  - "Convexity"
  - "Execution"
  - "F-Counting"
  - "MQL Native"
  - "Validation"
---


# Level 18 — Static QA / Compile Hardening

**Source:** [[docs/flag_counting/implementation_ladder_v1/18_LEVEL_18_STATIC_QA_AND_COMPILE_HARDENING|docs/flag_counting/implementation_ladder_v1/18_LEVEL_18_STATIC_QA_AND_COMPILE_HARDENING.md]]

**Category:** `flag_counting_docs`  
**Status:** ok  
**Size:** `2522` bytes

## خلاصه

Level 18 is an extension after the original Level 17 decision lock. It exists because the Phoenix engine became large enough that runtime logic can be correct while MQL5 compile hazards still break execution. This layer is **read-only**. It does not create, mutate, hide, reveal, confirm, invalidate, lock, re-parent, export, render, validate, release, accept, or reinterpret market structures. Level 18 hardens Phoenix against recurring MQL5 failure modes: empty `Print()` calls oversized multi-argument `Print(...)` calls duplicate `input` declarations stale `identity_generation_pass` values stale interface contract versions stale short report alias references missing public Level modules final

## Headings

- Level 18 — Static QA / Compile Hardening
-   Purpose
-   Runtime modules
-   Source-side tool
-   Execution order
-   Acceptance

## Concepts

- [[docs/obsidian/04_concepts/Convexity|Convexity]]
- [[docs/obsidian/04_concepts/Execution|Execution]]
- [[docs/obsidian/04_concepts/F-Counting|F-Counting]]
- [[docs/obsidian/04_concepts/MQL_Native|MQL Native]]
- [[docs/obsidian/04_concepts/Validation|Validation]]

## Related documents

- [[docs/flag_counting/implementation_ladder_v1/11_LEVEL_11_CANONICALIZATION_AND_AUDIT|Phoenix Flag Counting Implementation Ladder V1]] — `flag_counting_docs`
- [[docs/flag_counting/implementation_ladder_v1/12_LEVEL_12_RENDERER_AND_LABEL_LAYOUT|Level 12 — Renderer / Labels / Visual Layer]] — `flag_counting_docs`
- [[docs/flag_counting/implementation_ladder_v1/15_MODULE_INTERFACE_CONTRACTS|Phoenix Flag Counting Implementation Ladder V1]] — `flag_counting_docs`
- [[docs/flag_counting/implementation_ladder_v1/16_IMPLEMENTATION_ORDER_AND_ACCEPTANCE_MATRIX|Phoenix Flag Counting Implementation Ladder V1]] — `flag_counting_docs`
- [[docs/flag_counting/implementation_ladder_v1/README|Phoenix Flag Counting Implementation Ladder V1]] — `flag_counting_docs`
- [[lab/03_experiments/EXP0002_mql_native_m0001/report|EXP0002 — MQL-native M0001 Runtime]] — `experiment`
- [[lab/03_experiments/EXP0003_mql_native_m0002/report|EXP0003 — M0002 Reversal/Continuation Exit Volatility]] — `experiment`
- [[lab/03_experiments/EXP0004_mql_native_m0004/report|EXP0004 — MQL-native M0004 Branch Regime Clustering]] — `experiment`
- [[lab/05_validation/VAL_M0001_MQL_NATIVE/report|VAL_M0001_MQL_NATIVE]] — `validation`
- [[docs/flag_counting/implementation_ladder_v1/00_GOVERNANCE_AND_FREEZE_PROTOCOL|Phoenix Flag Counting Implementation Ladder V1]] — `flag_counting_docs`
- [[docs/flag_counting/implementation_ladder_v1/01_LEVEL_01_CANDLE_STREAM_AND_TIMEBASE|Phoenix Flag Counting Implementation Ladder V1]] — `flag_counting_docs`
- [[docs/flag_counting/implementation_ladder_v1/04_LEVEL_04_HOOK_ND_CONTEXT_ENGINE|Phoenix Flag Counting Implementation Ladder V1]] — `flag_counting_docs`

## Recommended Obsidian use

- این card را به نوت‌های concept، hypothesis، experiment یا ADR مربوط link کن.
- اگر این سند source of truth است، در MOC مربوطه بالاتر از اسناد legacy قرارش بده.
- اگر این سند report/validation است، نتیجه نهایی آن را به registry مربوط sync کن.
