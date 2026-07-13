---
title: "FP-I04 UTC M1 Open Is The Pair Join Key"
tags: [atomic-concept, exp0019, fp-i04]
status: canonical
---
# FP-I04 UTC M1 Open Is The Pair Join Key

## Definition

Two symbol bars are comparable only when they share the exact canonical UTC M1 open. Bar index, broker time, and nearest timestamps are not join keys.

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
