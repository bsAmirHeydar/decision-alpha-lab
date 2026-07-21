---
title: "Phoenix Flag Counting Implementation Ladder V1"
type: document_card
generated_by: alpha_lab_obsidian_builder
generated_at: 2026-07-06
source_path: "docs/flag_counting/implementation_ladder_v1/13_LEVEL_13_VALIDATION_MATRIX.md"
source_ext: ".md"
category: "flag_counting_docs"
source_size_bytes: "4188"
concepts:
  - "Execution"
  - "F-Counting"
  - "Hook"
  - "MQL Native"
  - "NDS Anatomy"
  - "Validation"
---


# Phoenix Flag Counting Implementation Ladder V1

**Source:** [[docs/flag_counting/implementation_ladder_v1/13_LEVEL_13_VALIDATION_MATRIX|docs/flag_counting/implementation_ladder_v1/13_LEVEL_13_VALIDATION_MATRIX.md]]

**Category:** `flag_counting_docs`  
**Status:** ok  
**Size:** `4188` bytes

## خلاصه

This document is part of the implementation ladder for the Phoenix Flag Counting engine. Level 13 turns Phoenix from a visually inspected overlay into a repeatable validation target. It runs after: The validation layer is read-only. It must never mutate events, hooks, visibility, identity, ownership, canonical state, export files from Level 11.5, or chart objects from Level 12. The EA wiring lives in: Default when validation is enabled: Unset expected ranges are reported as `WARN baseline_required` and the actual values are written to `latest_validation.csv`. This is how a new broker/range creates its first baseline. After accepting a baseline, fill the expected min/max inputs. For exact exp

## Headings

- Phoenix Flag Counting Implementation Ladder V1
- Level 13 — Validation Suite / Acceptance Matrix
-   Purpose
-   Active modules
-   Validation modes
-     Baseline mode
-     Regression mode
-   EA controls
-   Output
-   Built-in invariant checks
-   Validation case registry
-   Mandatory case families

## Concepts

- [[docs/obsidian/04_concepts/Execution|Execution]]
- [[docs/obsidian/04_concepts/F-Counting|F-Counting]]
- [[docs/obsidian/04_concepts/Hook|Hook]]
- [[docs/obsidian/04_concepts/MQL_Native|MQL Native]]
- [[docs/evidence/nds_anatomy/6a11c75733b2_NDS_Anatomy|NDS Anatomy]]
- [[docs/obsidian/04_concepts/Validation|Validation]]

## Related documents

- [[docs/flag_counting/VALIDATION_CASE_REGISTRY|Flag Counting Validation Case Registry]] — `flag_counting_docs`
- [[docs/flag_counting/implementation_ladder_v1/00_GOVERNANCE_AND_FREEZE_PROTOCOL|Phoenix Flag Counting Implementation Ladder V1]] — `flag_counting_docs`
- [[docs/flag_counting/implementation_ladder_v1/01_LEVEL_01_CANDLE_STREAM_AND_TIMEBASE|Phoenix Flag Counting Implementation Ladder V1]] — `flag_counting_docs`
- [[docs/flag_counting/implementation_ladder_v1/04_LEVEL_04_HOOK_ND_CONTEXT_ENGINE|Phoenix Flag Counting Implementation Ladder V1]] — `flag_counting_docs`
- [[docs/flag_counting/implementation_ladder_v1/10_LEVEL_10_SEQUENCE_OWNERSHIP_AND_PHASES|Phoenix Flag Counting Implementation Ladder V1]] — `flag_counting_docs`
- [[docs/flag_counting/implementation_ladder_v1/11_5_LEVEL_11_5_RAW_AUDIT_EXPORT|Level 11.5 — Raw Audit Export / Report Engine]] — `flag_counting_docs`
- [[docs/flag_counting/implementation_ladder_v1/11_LEVEL_11_CANONICALIZATION_AND_AUDIT|Phoenix Flag Counting Implementation Ladder V1]] — `flag_counting_docs`
- [[docs/flag_counting/implementation_ladder_v1/12_LEVEL_12_RENDERER_AND_LABEL_LAYOUT|Level 12 — Renderer / Labels / Visual Layer]] — `flag_counting_docs`
- [[docs/flag_counting/implementation_ladder_v1/14_LEVEL_14_RELEASE_ROLLBACK_AND_DEBUG_PROTOCOL|Phoenix Flag Counting Implementation Ladder V1]] — `flag_counting_docs`
- [[docs/flag_counting/implementation_ladder_v1/15_MODULE_INTERFACE_CONTRACTS|Phoenix Flag Counting Implementation Ladder V1]] — `flag_counting_docs`
- [[docs/flag_counting/implementation_ladder_v1/16_IMPLEMENTATION_ORDER_AND_ACCEPTANCE_MATRIX|Phoenix Flag Counting Implementation Ladder V1]] — `flag_counting_docs`
- [[docs/flag_counting/implementation_ladder_v1/README|Phoenix Flag Counting Implementation Ladder V1]] — `flag_counting_docs`

## Recommended Obsidian use

- این card را به نوت‌های concept، hypothesis، experiment یا ADR مربوط link کن.
- اگر این سند source of truth است، در MOC مربوطه بالاتر از اسناد legacy قرارش بده.
- اگر این سند report/validation است، نتیجه نهایی آن را به registry مربوط sync کن.
