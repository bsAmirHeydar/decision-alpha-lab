---
title: "13 - WW Weekly Context Relation"
tags: [exp0019, faerie-protocol, contextual-divergence, obsidian]
status: normative
experiment: EXP0019
context_id: FP-CONTEXT-001
context_version: 2.0.0-doc-freeze
doc_version: 2.0.0
last_updated: 2026-07-13
language: en
---
# 13 - WW Weekly Context Relation

## Purpose

Define the previous-week/current-week relation, weekly asymmetry lifecycle, tradeability, and neutralization.

## Scope

This document defines the Faerie Protocol context-layer behavior for its subject. It does not modify the stable intermarket divergence core. The shared core continues to own symbol-local references, touch/hunt facts, hunter/protected roles, closed-candle confirmation primitives, signal identity, deduplication, and ledger mechanics.

## Frozen Decisions Applied

- New York week boundary is frozen.
- Second-symbol touch neutralizes WW.
- WW is independently tradeable and also gates lower relations.

## Normative Invariants

1. **Previous weekly window must be complete.**
2. **Current weekly window is built incrementally from M1.**
3. **Raw one-sided touch becomes a WW candidate.**
4. **Confirmation uses resolved host chart timeframe.**
5. **A later corresponding touch by the second symbol neutralizes the active WW but does not delete history.**

## Deterministic Procedure

```text
Build prior NY week references.
Observe current NY week M1 range.
Detect one-sided weekly touch.
Create WW_RAW.
Confirm on host-chart close while asymmetry remains.
Publish WW_CONFIRMED.
On second-symbol touch publish WW_NEUTRALIZED.
```

## State and Evidence Requirements

| Field / Evidence | Requirement | Failure Behavior |
|---|---|---|
| `weekly_reference_id` | Previous completed NY week. | Block incomplete. |
| `ww_state` | RAW/CONFIRMED/NEUTRALIZED/EXPIRED. | Reject invalid transition. |
| `confirmation_time` | Host-chart close. | Must precede neutralization. |
| `gate_rank_time` | Confirmation close used for recency. | Tie-break deterministically. |

## Edge-Case Catalogue

### Second symbol touches before confirmation

Cancel raw WW; no confirmed gate.

### Second symbol touches after confirmation

Neutralize active context and retain confirmed event.

### Friday 17:00

Current week closes; no later M1 belongs to it.

### New WW opposite direction

Recency resolver selects newest active confirmed WW.

## Executable Test Obligations

1. DST week-boundary tests.
2. Neutralization before and after confirmation.
3. WW direct-trade eligibility fixture.
4. Opposite-WW recency fixture.

## Implementation Guidance

- Keep detection and active-gate resolution separate modules.


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
