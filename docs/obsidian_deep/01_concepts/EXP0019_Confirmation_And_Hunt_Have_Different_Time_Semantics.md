---
title: "Confirmation and Hunt Have Different Time Semantics"
tags: [exp0019, atomic-concept, faerie-protocol]
status: canonical
context_id: FP-CONTEXT-001
doc_version: 2.0.0
last_updated: 2026-07-13
language: en
---
# Confirmation and Hunt Have Different Time Semantics

## Definition

Hunt ordering is a canonical M1 fact. Confirmation is a closed-candle decision on the resolved host chart timeframe and must close inside the owning session. The two timestamps must never be conflated.

## Operational Consequence

- The rule is represented in a closed contract or state transition.
- The rule is included in identity when it changes signal or execution behavior.
- At least one golden and one negative test are required.
- Violations are fail-closed and reason-coded.

## Related Documentation

- [[../../execution/EXP0019_faerie_protocol_contextual_divergence/00_EXP0019_MOC|EXP0019 Master MOC]]
- [[../../execution/EXP0019_faerie_protocol_contextual_divergence/38_OWNER_DECISION_FREEZE_V2|Owner Decision Freeze v2]]
- [[../../execution/EXP0019_faerie_protocol_contextual_divergence/40_NORMATIVE_ALGORITHM_SPECIFICATION|Normative Algorithm Specification]]
