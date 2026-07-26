---
title: "EXP0019 FP I01 Adapter Is Not An Engine"
tags: [exp0019, faerie-protocol, fp-i01, compatibility, adapter-contracts]
status: normative
phase: FP-I01
phase_version: 1.0.0
doc_version: 1.0.0
last_updated: 2026-07-13
language: en
---
# EXP0019 FP I01 Adapter Is Not An Engine

## Definition

An adapter projects already-decided source facts into neutral contracts. It cannot aggregate markets, detect hunts, confirm signals, manage lifecycle, draw, or trade.

## Operational rule

- Encode the rule in a closed contract or exact hash guard.
- Test the positive and rejected path.
- Preserve evidence in `FP_I01_COMPATIBILITY_REPORT.json`.
- Block downstream handoff when violated.

## Related notes

- [[../../execution/EXP0019_faerie_protocol_contextual_divergence/implementation_program/phase_deliveries/fp_i01/00_FP_I01_DELIVERY_MOC|FP-I01 Delivery MOC]]
