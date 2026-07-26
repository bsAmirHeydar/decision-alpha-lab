---
title: "M1 Windows Make Detection Timeframe-Invariant"
tags: [exp0019, atomic-concept, faerie-protocol]
status: canonical
context_id: FP-CONTEXT-001
doc_version: 2.0.0
last_updated: 2026-07-13
language: en
---
# M1 Windows Make Detection Timeframe-Invariant

## Definition

A/L/N/W ranges and first-sweep facts are built from M1, so chart timeframe cannot alter raw detection. The chart timeframe is behavior-bearing only for closed-candle confirmation.

## Operational Consequence

- The rule is represented in a closed contract or state transition.
- The rule is included in identity when it changes signal or execution behavior.
- At least one golden and one negative test are required.
- Violations are fail-closed and reason-coded.

## Related Documentation

- [[../../execution/EXP0019_faerie_protocol_contextual_divergence/00_EXP0019_MOC|EXP0019 Master MOC]]
- [[../../execution/EXP0019_faerie_protocol_contextual_divergence/38_OWNER_DECISION_FREEZE_V2|Owner Decision Freeze v2]]
- [[../../execution/EXP0019_faerie_protocol_contextual_divergence/40_NORMATIVE_ALGORITHM_SPECIFICATION|Normative Algorithm Specification]]
