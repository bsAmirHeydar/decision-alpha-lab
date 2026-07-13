---
title: "07 - Time and DST Contract"
tags: [exp0019, faerie-protocol, contextual-divergence, obsidian]
status: normative
experiment: EXP0019
context_id: FP-CONTEXT-001
context_version: 2.0.0-doc-freeze
doc_version: 2.0.0
last_updated: 2026-07-13
language: en
---
# 07 - Time and DST Contract

## Purpose

Define broker-independent New York timestamps, DST transitions, interval boundaries, and configuration epochs.

## Scope

This document defines the Faerie Protocol context-layer behavior for its subject. It does not modify the stable intermarket divergence core. The shared core continues to own symbol-local references, touch/hunt facts, hunter/protected roles, closed-candle confirmation primitives, signal identity, deduplication, and ledger mechanics.

## Frozen Decisions Applied

- Weekly boundary is Sunday 18:00 to Friday 17:00 New York.
- M1 timestamps are first-sweep authority.

## Normative Invariants

1. **All session and weekly calculations use `America/New_York`.**
2. **Intervals are half-open `[start,end)`.**
3. **DST transitions use timezone rules, not fixed offsets.**
4. **Broker time is transport metadata only.**

## Deterministic Procedure

```text
Convert bar open time to UTC.
Resolve New York civil time using rule database.
Compute trading-day key.
Compute A/L/N/W interval IDs.
Persist offset and conversion version.
```

## State and Evidence Requirements

| Field / Evidence | Requirement | Failure Behavior |
|---|---|---|
| `utc_time_ms` | Canonical instant. | Block if unavailable. |
| `ny_local` | Resolved civil timestamp. | Block invalid conversion. |
| `utc_offset_seconds` | Observed offset. | Record for audit. |
| `timezone_rules_version` | Conversion implementation/version. | New epoch on change. |

## Edge-Case Catalogue

### Spring-forward gap

No nonexistent local minute is synthesized.

### Fall-back duplicate hour

Disambiguate by UTC instant and offset.

### Broker day differs from NY day

NY key remains authoritative.

### Weekend week open

Sunday 18:00 creates the new trading week.

## Executable Test Obligations

1. Golden tests across both DST transitions.
2. Verify Sunday 18:00 week open in standard and daylight time.
3. Verify Friday 17:00 exclusion.

## Implementation Guidance

- Reuse the shared New York time core; FP contributes only interval definitions.


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
