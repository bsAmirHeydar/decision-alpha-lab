---
title: "46 - Execution Arbitration and First-Signal Policy"
tags: [exp0019, faerie-protocol, contextual-divergence, obsidian]
status: normative
experiment: EXP0019
context_id: FP-CONTEXT-001
context_version: 2.0.0-doc-freeze
doc_version: 2.0.0
last_updated: 2026-07-13
language: en
---
# 46 - Execution Arbitration and First-Signal Policy


## Owner Rule

Within each A, L, or N session, the two-symbol pair may produce at most one entry. The first eligible setup is the setup with the earliest canonical M1 hunt time.

## Arbitration Universe

All of the following compete in one session pool:

- both symbols as potential trade symbols,
- bullish and bearish setups,
- all enabled AL/AN/LN/NA/NL/NN relations,
- direct WW setups that become eligible in that session,
- all calendar-day historical N offsets.

## Eligibility Before Ranking

A candidate enters arbitration only after:

1. closed-candle confirmation inside its owning session,
2. valid data and reference lifecycle,
3. relation execution enabled,
4. WW gate compatibility or valid no-WW allow-both state,
5. preliminary risk/geometry feasibility.

## Stable Ranking

```text
primary: first_hunt_m1_time ascending
secondary: confirmation_close_time ascending
tertiary: relation_code stable enum
quaternary: direction enum
quinary: signal_id lexical
```

The secondary fields only resolve exact M1 ties. They must not be interpreted as alpha or quality ranking.

## Atomic Reservation

The winning signal performs a compare-and-set transition:

```text
quota AVAILABLE -> RESERVED(winner_signal_id)
```

Every later eligible signal receives `SUPPRESSED_BY_QUOTA` and references the winner. Q12 controls when/if the reservation becomes permanently consumed or released.

## Historical Replay

Replay must reconstruct the same winner independent of processing batch size, symbol update order, or chart drawing order. Arbitration therefore operates on canonical events after both symbols' relevant M1 data is available.

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
