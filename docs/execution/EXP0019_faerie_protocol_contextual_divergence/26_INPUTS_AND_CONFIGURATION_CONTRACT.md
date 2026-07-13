---
title: "26 - Inputs and Configuration Contract"
tags: [exp0019, faerie-protocol, contextual-divergence, obsidian]
status: normative
experiment: EXP0019
context_id: FP-CONTEXT-001
context_version: 2.0.0-doc-freeze
doc_version: 2.0.0
last_updated: 2026-07-13
language: en
---
# 26 - Inputs and Configuration Contract

## Purpose

Define every user-configurable input, its default, mutability, validation, and identity impact.

## Scope

This document defines the Faerie Protocol context-layer behavior for its subject. It does not modify the stable intermarket divergence core. The shared core continues to own symbol-local references, touch/hunt facts, hunter/protected roles, closed-candle confirmation primitives, signal identity, deduplication, and ledger mechanics.

## Frozen Decisions Applied

- Confirmation timeframe is current chart timeframe, resolved at init.
- Calendar-day depth and spread adjustment are fixed policies but may expose values only where owner intends.

## Normative Invariants

1. **Every behavior-changing input affects config hash.**
2. **Visual-only inputs do not alter signal identity unless they change filtering.**
3. **Invalid inputs fail initialization.**
4. **Runtime changes create new epoch.**

## Deterministic Procedure

```text
Read input.
Resolve dynamic values such as PERIOD_CURRENT.
Validate ranges and pair symbols.
Create context manifest.
Hash manifest.
Initialize modules.
```

## State and Evidence Requirements

| Field / Evidence | Requirement | Failure Behavior |
|---|---|---|
| `input_name` | Stable public name. | No duplicate. |
| `resolved_value` | Post-init actual value. | Required for dynamic inputs. |
| `identity_bearing` | Boolean. | Must be reviewed. |
| `validation_rule` | Range/enum/cross-field constraint. | Fail init. |

## Edge-Case Catalogue

### Chart timeframe changes

OnDeinit/OnInit yields new epoch.

### Lookback exceeds available calendar data

Emit missing offsets; do not compress.

### Spread adjustment disabled contrary to policy

Reject production profile or mark non-canonical research profile.

### Quota consumption unset

Disable live execution.

## Executable Test Obligations

1. Default-profile manifest test.
2. Chart-timeframe resolution test.
3. Invalid pair/input tests.
4. Config-hash change matrix.

## Implementation Guidance

- Separate research overrides from canonical production profile.


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
