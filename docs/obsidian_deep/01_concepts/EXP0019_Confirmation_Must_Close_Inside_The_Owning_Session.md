---
title: "Confirmation Must Close Inside the Owning Session"
tags: [exp0019, faerie-protocol, contextual-divergence, obsidian]
status: canonical-concept
experiment: EXP0019
context_id: FP-CONTEXT-001
context_version: 2.0.0-doc-freeze
doc_version: 2.0.0
last_updated: 2026-07-13
language: en
---
# Confirmation Must Close Inside the Owning Session

## Definition

A candidate expires if its resolved host-chart confirmation candle closes at or after the check-session boundary.

## Operational Consequence

- The rule is serialized in the v2 owner-decision set.
- The rule affects signal or execution identity where applicable.
- At least one golden and one negative test are required.
- Violations are fail-closed and reason-coded.

## Related Documents

- [[../../execution/EXP0019_faerie_protocol_contextual_divergence/38_OWNER_DECISION_FREEZE_V2|Owner Decision Freeze v2]]
- [[../../execution/EXP0019_faerie_protocol_contextual_divergence/40_NORMATIVE_ALGORITHM_SPECIFICATION|Normative Algorithm Specification]]
