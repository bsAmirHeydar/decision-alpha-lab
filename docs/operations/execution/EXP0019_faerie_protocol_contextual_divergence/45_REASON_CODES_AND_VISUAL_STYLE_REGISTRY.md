---
title: "45 - Reason Codes and Visual Style Registry"
tags: [exp0019, faerie-protocol, contextual-divergence, obsidian]
status: normative
experiment: EXP0019
context_id: FP-CONTEXT-001
context_version: 2.0.0-doc-freeze
doc_version: 2.0.0
last_updated: 2026-07-13
language: en
---
# 45 - Reason Codes and Visual Style Registry

## Registry

| Code | Meaning | Required Visual Treatment |
|---|---|---|
| `CONFIRMED_ACTIVE` | Normal confirmed signal | solid/high opacity |
| `SUPPRESSED_BY_WW` | Direction conflicts with active WW | dashed/medium opacity |
| `SUPPRESSED_BY_QUOTA` | Another earlier signal owns pair-session quota | dotted/medium opacity |
| `WW_NONE_ALLOW_BOTH` | No active WW with complete data | normal plus context badge |
| `WW_DATA_INCOMPLETE` | Weekly data insufficient | warning/low opacity |
| `WW_NEUTRALIZED` | Second symbol touched corresponding weekly side | muted neutral |
| `CONFIRMATION_DEADLINE_MISSED` | Chart candle closed outside owning session | expired style |
| `SYMMETRIC_SAME_M1` | Both symbols touched in same M1 | neutral diagnostic |
| `REFERENCE_INCOMPLETE` | Source window incomplete | warning diagnostic |
| `REFERENCE_CONSUMED` | Protected side previously touched | muted unavailable |
| `SELL_SPREAD_UNAVAILABLE` | Cannot form adjusted SELL stop | execution warning |
| `GEOMETRY_INVALID` | Broker/local stop geometry invalid | execution warning |
| `QUOTA_POLICY_UNSET` | Live execution disabled pending Q12 | critical diagnostic |
| `CANCELLED_BY_SECOND_TOUCH` | Protected symbol touched before confirmation | cancelled style |
| `NON_CANONICAL_PROFILE` | Research override active | distinct banner/style |


## Drawing Rule

The owner selected **always draw suppressed signals**. Therefore every reason above must map to a visible style. The system may offer filters, but the canonical default must not silently remove suppressed signals.

## Style Identity

Style changes are visual-only unless they change filtering or history retention. A style registry version is stored in the visual artifact descriptor, while the underlying signal identity remains unchanged.

## Minimum Annotation

Every visible signal should expose relation, direction, hunter, protected, reference/check IDs, first-hunt M1 time, confirmation time, current eligibility, suppression reason, and active WW/quota linkage.

## Authority Classification

| Classification | Meaning |
|---|---|
| `OWNER_CONFIRMED` | Explicitly selected by the owner in the 15-question decision response. |
| `SOURCE_CONFIRMED` | Directly present in the original Faerie Protocol source package or owner narrative. |
| `ARCHITECTURAL_DERIVATION` | Required to make the confirmed behavior deterministic, modular, testable, or compatible with shared cores. |
| `LEGACY_OBSERVATION` | Behavior observed in `FP 101.mq5`; not automatically canonical. |
| `OPEN_DECISION` | Must not be silently hard-coded. |

Canonical priority is: `OWNER_CONFIRMED` > `SOURCE_CONFIRMED` > reviewed `ARCHITECTURAL_DERIVATION` > `LEGACY_OBSERVATION`.

## Navigation

- [[00_EXP0019_MOC|EXP0019 Master MOC]]
- [[38_OWNER_DECISION_FREEZE_V2|Owner Decision Freeze v2]]
- [[33_AMBIGUITY_AND_DECISION_REGISTER|Decision Register]]
- [[40_NORMATIVE_ALGORITHM_SPECIFICATION|Normative Algorithm Specification]]
- [[44_ACCEPTANCE_GATE_FOR_CODING|Acceptance Gate for Coding]]
