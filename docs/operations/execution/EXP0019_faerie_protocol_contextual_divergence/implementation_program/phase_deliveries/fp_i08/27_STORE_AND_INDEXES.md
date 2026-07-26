---
tags: [exp0019, faerie-protocol, fp-i08, weekly-context]
status: normative
phase: FP-I08
version: 1.0.0
last_updated: 2026-07-13
language: en
---
# Store and Indexes

## Normative statement

Indexes are by context ID, signal ID, week ID, direction, state, and confirmation time. Upsert is identity-safe.

## Invariants

- M1 remains first-sweep authority.
- FP-I07 remains confirmation authority.
- Weekly evidence is append-only after confirmation.
- No hidden chart state or broker time may affect semantics.
- Suppression is a decision record, not signal deletion.
- FP-DEC-012 remains open and blocks live execution only.

## Verification

- Python unit and negative tests.
- Closed-schema parse and registry checks.
- MQL5 static authority scan.
- Golden-vector replay.
- Clean-baseline patch application.

## Navigation

- [[00_FP_I08_DELIVERY_MOC|FP-I08 Delivery MOC]]
- [[../fp_i07/00_FP_I07_DELIVERY_MOC|FP-I07 Confirmation Engine]]
- [[43_HANDOFF_TO_FP_I09|FP-I09 Handoff]]
