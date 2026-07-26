---
title: "08 - Trading Day and Session Calendar"
tags: [exp0019, faerie-protocol, contextual-divergence, obsidian]
status: normative
experiment: EXP0019
context_id: FP-CONTEXT-001
context_version: 2.0.0-doc-freeze
doc_version: 2.0.0
last_updated: 2026-07-13
language: en
---
# 08 - Trading Day and Session Calendar

## Purpose

Define the A, L, and N session windows, trading-day ownership, and strict session-close confirmation.

## Scope

This document defines the Faerie Protocol context-layer behavior for its subject. It does not modify the stable intermarket divergence core. The shared core continues to own symbol-local references, touch/hunt facts, hunter/protected roles, closed-candle confirmation primitives, signal identity, deduplication, and ledger mechanics.

## Frozen Decisions Applied

- Confirmation must close inside the owning session.
- One pair-global first entry is allowed in each A/L/N session.

## Normative Invariants

1. **Session intervals are explicit and half-open.**
2. **A trading day may cross midnight.**
3. **A candidate never migrates to another session.**
4. **Session quota key uses the check-session ID.**

## Deterministic Procedure

```text
Resolve NY timestamp.
Assign trading-day key.
Assign session A/L/N.
Create session interval ID.
At confirmation close, verify close instant is before session end.
```

## State and Evidence Requirements

| Field / Evidence | Requirement | Failure Behavior |
|---|---|---|
| `trading_day_key` | NY trading-day identity. | Block if unresolved. |
| `session_code` | A/L/N. | Reject unknown. |
| `session_start/end_utc` | Resolved interval. | Block malformed interval. |
| `confirmation_deadline` | Owning session end. | Expire after deadline. |

## Edge-Case Catalogue

### Hunt at final session minute

Eligible only if the resolved confirmation candle closes before session end.

### Confirmation closes exactly at boundary

Belongs to next interval and therefore candidate expires.

### Chart timeframe too large

Many late hunts will expire by design.

### Holiday/short session

Use configured FP session calendar unless an explicit holiday policy is introduced.

## Executable Test Obligations

1. Boundary tests at start, end-minus-one, and end.
2. Test overnight A session.
3. Test strict confirmation with multiple chart timeframes.

## Implementation Guidance

- Session definitions must be versioned inputs rather than constants buried in detector code.


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
