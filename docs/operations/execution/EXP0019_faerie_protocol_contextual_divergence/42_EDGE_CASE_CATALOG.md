---
title: "42 - Edge-Case Catalog"
tags: [exp0019, faerie-protocol, contextual-divergence, obsidian]
status: normative
experiment: EXP0019
context_id: FP-CONTEXT-001
context_version: 2.0.0-doc-freeze
doc_version: 2.0.0
last_updated: 2026-07-13
language: en
---
# 42 - Edge-Case Catalog

## Canonical Cases

| ID | Condition | Required Outcome |
|---|---|---|
| `EC-001` | Both symbols touch the same side in the same M1 | No first-sweep order; emit symmetric touch, no divergence candidate. |
| `EC-002` | Tick data suggests order inside a shared M1 | Ignore for canonical result; M1 authority remains. |
| `EC-003` | Candidate confirmation closes exactly at session end | Expire; intervals are half-open and close is outside owning session. |
| `EC-004` | Candidate confirmation closes in next session | Expire; never transfer ownership. |
| `EC-005` | Historical N offset is weekend | Offset remains occupied and yields no reference; do not backfill. |
| `EC-006` | Historical N offset partially covered | Mark PARTIAL and ineligible. |
| `EC-007` | Hunter touches same reference in A and later L | Allowed if protected side has not touched. |
| `EC-008` | Protected high touches but low does not | Consume high side only. |
| `EC-009` | WW second symbol touches before confirmation | Cancel raw WW. |
| `EC-010` | WW second symbol touches after confirmation | Neutralize current WW, retain historical event/drawing. |
| `EC-011` | No active WW with complete data | Allow both directions. |
| `EC-012` | Weekly data incomplete | Block execution; do not classify as no WW. |
| `EC-013` | Two opposite active WW events | Newest confirmed active event wins. |
| `EC-014` | Newest WW neutralizes | Recompute active gate from remaining active WW events. |
| `EC-015` | Two eligible signals in same session | Earliest M1 hunt wins pair-global quota. |
| `EC-016` | Eligible signals have same M1 hunt time | Use technical tie-break order; retain all signals. |
| `EC-017` | Winning plan fails local geometry | Quota result depends on open Q12; reason-coded reservation event required. |
| `EC-018` | SELL spread unavailable | No SELL order; draw/ledger signal with spread-unavailable reason. |
| `EC-019` | SELL spread widens before send | Revalidate adjusted stop and risk immediately before send. |
| `EC-020` | Chart timeframe changes | New context epoch; resolved timeframe changes signal identity. |
| `EC-021` | EA restarts | Rebuild state from canonical windows/ledger; IDs must match. |
| `EC-022` | Drawing object is deleted manually | Rebuild from ledger; object deletion does not change business state. |
| `EC-023` | Suppressed by WW | Always draw with alternate style and reason. |
| `EC-024` | Suppressed by quota | Always draw with alternate style and identify winner signal. |
| `EC-025` | Broker W1 differs from NY week | Ignore broker W1 boundaries for WW. |


## Test Requirement

Each edge case must map to at least one executable fixture and one reason/state code. Cases involving Q12 may test multiple policies, but the canonical expected live behavior remains unset until the owner freezes it.

## Review Rule

A new edge case is added when any of the following appears:

- a new state transition,
- a new data-quality category,
- a new broker response class,
- a new policy suppression reason,
- a new tie condition,
- a new historical/live parity risk.

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
