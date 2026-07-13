---
title: "FP-I04 Missing Is Not Out Of Coverage"
tags: [atomic-concept, exp0019, fp-i04]
status: canonical
---
# FP-I04 Missing Is Not Out Of Coverage

## Definition

MISSING means an absent minute inside known source coverage. OUT_OF_COVERAGE means history does not extend to that minute. They have different repair and eligibility consequences.

## Why it matters

All downstream reference, hunt, divergence, confirmation, WW, ledger, indicator, and execution identities depend on the exact two-symbol M1 evidence. Losing this distinction creates repainting, false completeness, or non-reproducible first-sweep ordering.

## Enforcement

- Immutable Python contract and closed JSON schema.
- Equivalent MQL5 type/reason-code mirror.
- Golden, negative, permutation, revision, and batch/incremental tests.
- Content-addressed artifact and phase file inventory.

## Related documentation

- [[../../execution/EXP0019_faerie_protocol_contextual_divergence/implementation_program/phase_deliveries/fp_i04/00_FP_I04_DELIVERY_MOC|FP-I04 Delivery MOC]]
- [[../../execution/EXP0019_faerie_protocol_contextual_divergence/implementation_program/phases/FP_I04_MULTI-SYMBOL_M1_SYNCHRONIZATION_COVERAGE_AND_DATA_REVISION|Canonical Phase Specification]]
