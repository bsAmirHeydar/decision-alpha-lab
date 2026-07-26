---
title: "FP-I01 Public Contract Summary"
tags: [exp0019, faerie-protocol, fp-i01, compatibility, adapter-contracts]
status: normative
phase: FP-I01
phase_version: 1.0.0
doc_version: 1.0.0
last_updated: 2026-07-13
language: en
---

# FP-I01 Public Contract Summary

## Neutral contracts

| Contract | Purpose |
|---|---|
| `FP_I01_TimeSnapshot` | broker/UTC/New York and trading-day boundary facts |
| `FP_I01_ReferencePair` | symbol-local reference range and readiness facts |
| `FP_I01_HuntObservation` | HIGH/LOW pair-state and hunter/protected facts |
| `FP_I01_DivergenceCandidate` | source-resolved direction and one-sided/symmetric state |
| `FP_I01_ConfirmationResult` | host-close finalization and replay/immutability facts |
| `FP_I01_LifecycleRecord` | reference survival/retirement and use-count facts |

## Consumer prohibition

A consumer may not treat these neutral contracts as Faerie Protocol signals. Native FP relation, session, identity, lifecycle, WW, suppression, and quota semantics begin in later phases.

## Compatibility identity

Every contract carries:

- source context;
- source type;
- source fingerprint;
- explicit health;
- closed reason code;
- exact timestamps and symbol-local facts relevant to that contract.
