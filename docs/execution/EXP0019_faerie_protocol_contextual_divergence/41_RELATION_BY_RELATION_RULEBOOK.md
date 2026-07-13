---
title: "41 - Relation-by-Relation Rulebook"
tags: [exp0019, faerie-protocol, contextual-divergence, obsidian]
status: normative
experiment: EXP0019
context_id: FP-CONTEXT-001
context_version: 2.0.0-doc-freeze
doc_version: 2.0.0
last_updated: 2026-07-13
language: en
---
# 41 - Relation-by-Relation Rulebook


## Registry Summary

| Relation | Reference | Check | Historical selector | Confirmation deadline | WW-gated | Directly tradeable |
|---|---|---|---|---|---|---|
| `AL` | A same trading day | L same day | N/A | L end | Yes | Yes |
| `AN` | A same trading day | N same day | N/A | N end | Yes | Yes |
| `LN` | L same trading day | N same day | N/A | N end | Yes | Yes |
| `NA` | N at exact prior calendar offset | A current day | calendar-day depth | A end | Yes | Yes |
| `NL` | N at exact prior calendar offset | L current day | calendar-day depth | L end | Yes | Yes |
| `NN` | N at exact prior calendar offset | N current day | calendar-day depth | N end | Yes | Yes |
| `WW` | previous completed NY week | current NY week | previous week | weekly candidate close; neutralizable | It is the gate | Yes |

## Direction Semantics

- **Bullish divergence:** one symbol hunts its own reference low while the other symbol preserves its own corresponding low.
- **Bearish divergence:** one symbol hunts its own reference high while the other symbol preserves its own corresponding high.
- The protected symbol is the non-hunting symbol at candidate creation.
- Trade-symbol selection must be explicit in the execution adapter; the relation detector only reports roles.

## Same-Day Relations

### AL

- Reference becomes eligible only after A coverage is complete enough to freeze its high/low.
- Hunt must occur in L.
- Confirmation must close before L end.
- Pair-session quota belongs to L.

### AN

- A reference is reused in N even if AL produced a signal, unless protected touch consumed the relevant side.
- Confirmation must close before N end.
- Pair-session quota belongs to N.

### LN

- L reference must be complete before N evaluation.
- Confirmation must close before N end.
- It competes with AN and NN for the same N pair-session quota.

## Cross-Day Relations

For NA/NL/NN, each `calendar_offset` is a separate reference identity. If offset 2 is a weekend/missing day, offset 3 remains offset 3 and is not promoted into the second slot.

### NA

- Historical N side versus current A.
- A pair-session quota.

### NL

- Historical N side versus current L.
- L pair-session quota.

### NN

- Historical N side versus current N.
- N pair-session quota.

## Weekly Relation

WW uses previous completed New York week versus current week. It confirms like a divergence setup, is independently tradeable, participates in the current A/L/N quota according to the session in which its entry becomes eligible, and also determines lower-relation direction.

## Multi-Reference Competition

Several historical N offsets may confirm in the same session. The owner-selected first-entry rule ranks their candidates by canonical M1 hunt time. Calendar offset does not imply priority. If hunt times tie, technical tie-breaks apply.

## Consumption Interaction

The same reference side may produce distinct NA, NL, and NN confirmed signals until the protected symbol touches that side. Quota suppression does not consume the reference and does not delete the signal.

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
