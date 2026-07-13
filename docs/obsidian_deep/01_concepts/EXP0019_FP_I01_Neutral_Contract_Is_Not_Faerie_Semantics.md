---
title: "EXP0019 FP I01 Neutral Contract Is Not Faerie Semantics"
tags: [exp0019, faerie-protocol, fp-i01, compatibility, adapter-contracts]
status: normative
phase: FP-I01
phase_version: 1.0.0
doc_version: 1.0.0
last_updated: 2026-07-13
language: en
---
# EXP0019 FP I01 Neutral Contract Is Not Faerie Semantics

## Definition

Neutral time/reference/hunt/confirmation facts do not imply A/L/N relations, WW policy, quota, or tradeability.

## Operational rule

- Encode the rule in a closed contract or exact hash guard.
- Test the positive and rejected path.
- Preserve evidence in `FP_I01_COMPATIBILITY_REPORT.json`.
- Block downstream handoff when violated.

## Related notes

- [[../../execution/EXP0019_faerie_protocol_contextual_divergence/implementation_program/phase_deliveries/fp_i01/00_FP_I01_DELIVERY_MOC|FP-I01 Delivery MOC]]
