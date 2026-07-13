---
title: "47 - WW Active Context Stack and Recency"
tags: [exp0019, faerie-protocol, contextual-divergence, obsidian]
status: normative
experiment: EXP0019
context_id: FP-CONTEXT-001
context_version: 2.0.0-doc-freeze
doc_version: 2.0.0
last_updated: 2026-07-13
language: en
---
# 47 - WW Active Context Stack and Recency


## Purpose

Several confirmed WW events may exist in history, including opposite directions. The owner selected "newest WW wins" and "second-symbol touch neutralizes WW." This document defines a deterministic active-context resolver.

## Event Model

- `WW_CONFIRMED`: eligible to control the gate and to execute directly.
- `WW_NEUTRALIZED`: corresponding second-symbol touch occurred; event remains history but is no longer active.
- `WW_EXPIRED`: no longer within its policy horizon.
- `WW_DATA_INCOMPLETE`: resolver cannot make a valid weekly statement.

## Active Resolver

```text
candidates = all WW_CONFIRMED
remove events with later WW_NEUTRALIZED or WW_EXPIRED child event
sort by confirmation_close_time descending
then first_hunt_m1_time descending
then signal_id lexical
active = first candidate
```

If no candidate remains and weekly data is complete, gate = BOTH. If weekly data is incomplete, gate = BLOCKED_DATA.

## Neutralization and Fallback

When the newest active WW neutralizes, the resolver recomputes. An older still-active WW may become active again. This does not rewrite history; it changes only current gate resolution.

## Direct-Trade Interaction

A WW direct setup is a normal confirmed setup for arbitration. If it loses the session quota, it remains visible as `SUPPRESSED_BY_QUOTA`. Its function as a weekly gate is independent of whether its direct trade was executed.

## Audit Output

The resolver emits active signal ID, direction, resolution timestamp, candidate list hash, and exclusion reasons for every non-active WW.

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
