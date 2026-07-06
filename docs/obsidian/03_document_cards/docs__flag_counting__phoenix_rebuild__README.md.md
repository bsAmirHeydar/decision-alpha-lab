---
title: "Flag Counting Phoenix Rebuild"
type: document_card
generated_by: alpha_lab_obsidian_builder
generated_at: 2026-07-06
source_path: "docs/flag_counting/phoenix_rebuild/README.md"
source_ext: ".md"
category: "flag_counting_docs"
source_size_bytes: "1300"
concepts:
  - "F-Counting"
  - "Hook"
  - "NDS Anatomy"
  - "Validation"
---


# Flag Counting Phoenix Rebuild

**Source:** [[docs/flag_counting/phoenix_rebuild/README|docs/flag_counting/phoenix_rebuild/README.md]]

**Category:** `flag_counting_docs`  
**Status:** ok  
**Size:** `1300` bytes

## خلاصه

This package replaces the failed patch-on-patch lineage with a clean engine. The old code must be removed before applying this patch. The design goal is not to hide complexity. The goal is to make every layer explicit: 1. Node extraction. 2. Hook/ND branch discovery. 3. Two-leg body construction. 4. Post-flag internal counting. 5. F1/F2/F3 sequence orchestration. 6. Renderer-only visualization. 7. Audit-only diagnostics. The previous implementation failed for four root reasons: 1. Audit events were rendered as chart structures. 2. F1 roots were created from arbitrary two-leg windows instead of phase boundaries. 3. F2/F3 ownership was not hard enough, so children could drift away from their p

## Headings

- Flag Counting Phoenix Rebuild
-   Why the previous attempts failed
-   Apply policy

## Concepts

- [[docs/obsidian/04_concepts/F-Counting|F-Counting]]
- [[docs/obsidian/04_concepts/Hook|Hook]]
- [[docs/obsidian/04_concepts/NDS_Anatomy|NDS Anatomy]]
- [[docs/obsidian/04_concepts/Validation|Validation]]

## Related documents

- [[docs/debug/MARKET_LANGUAGE/README|DAL Market Language — Nodes, Cycles, Hooks, Rallies, Flags, 123 Flags, and Open 1/2s]] — `debug_docs`
- [[docs/experience_capture/questions/README|Quant Lab Experience Capture Questionnaire]] — `experience_capture_docs`
- [[docs/flag_counting/engineering_pack_v5/01_concepts/README|01 Concepts README]] — `flag_counting_docs`
- [[docs/flag_counting/engineering_pack_v5/04_algorithms/README|04 Algorithms README]] — `flag_counting_docs`
- [[docs/flag_counting/engineering_pack_v5/README|Flag Counting Engineering Pack V5]] — `flag_counting_docs`
- [[docs/flag_counting/implementation_ladder_v1/README|Phoenix Flag Counting Implementation Ladder V1]] — `flag_counting_docs`
- [[docs/flag_counting/README|Flag Counting Documentation]] — `flag_counting_docs`
- [[docs/nds_hook_architecture/README|NDS Hook Architecture — Design Pack]] — `nds_hook_architecture_docs`
- [[lab/03_experiments/EXP_flag_counting/README|EXP Flag Counting]] — `experiment`
- [[lab/03_experiments/EXP_flag_counting/validation_cases/README|Phoenix Flag Counting Validation Cases]] — `experiment`
- [[docs/ai_execution/README|AI Execution Docs]] — `ai_execution_docs`
- [[docs/debug/E0008/README|E0008 — MTF Purple Extreme Executor]] — `debug_docs`

## Recommended Obsidian use

- این card را به نوت‌های concept، hypothesis، experiment یا ADR مربوط link کن.
- اگر این سند source of truth است، در MOC مربوطه بالاتر از اسناد legacy قرارش بده.
- اگر این سند report/validation است، نتیجه نهایی آن را به registry مربوط sync کن.
