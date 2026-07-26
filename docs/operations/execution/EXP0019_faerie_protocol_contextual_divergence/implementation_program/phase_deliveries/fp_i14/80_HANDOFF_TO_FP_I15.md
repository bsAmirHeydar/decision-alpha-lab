---
title: "FP-I14 — Handoff To Fp I15"
tags: [exp0019, faerie-protocol, fp-i14, diagnostic, differential]
status: implemented
phase: FP-I14
version: 1.0.0
last_updated: 2026-07-13
---
# FP-I14 — Handoff To Fp I15


## Contract

This document is normative for FP-I14. The Diagnostic EA, Indicator adapter, and Python reference model must consume the same context epoch, pair identity, configuration hash, source revision, resolved host timeframe, and exact module-version manifest. Product-specific transport metadata is excluded from semantic identity.

## Implementation linkage

- Python reference implementation: `lab/10_infrastructure/EXP0019_faerie_protocol/phase_i14/python/fp_i14_diagnostic/`
- MQL5 diagnostic modules: `mql5/Include/AlphaLab/EXP0019/FaerieProtocol/I14/`
- Diagnostic EA: `mql5/Experts/EXP0019/FaerieProtocol/EXP0019_FaerieProtocol_Diagnostic.mq5`
- Machine schemas and golden vectors live under the FP-I14 phase directory.

## Failure behavior

Missing data, incompatible manifests, source-revision drift, sequence gaps, ID collisions, and product absence are explicit evidence. The comparator never guesses equivalence. Any unexplained semantic differential blocks phase acceptance. Duplicate identical records are idempotent; duplicate identities with different meaning fail closed.

## Evidence and operations

Every acceptance statement must reference a fixture ID, product manifests, trace hashes, event counts, mismatch inventory, source revision, and tool version. Local MetaEditor compilation and same-terminal runtime differential evidence remain separate external gates. `FP-DEC-012` remains `UNSET`; no paper or live quota-consumption policy is introduced here.

## Change policy

Changes to event identity, canonical fields, module versions, comparison fields, or mismatch classification require a contract-version change, updated schemas, regenerated goldens, cumulative regression, and a new accepted patch manifest. UI formatting and dashboard layout are nonsemantic unless they alter exported semantic inventory.


## Phase-specific requirement

This note governs **Handoff To Fp I15**. Acceptance requires deterministic behavior across all three products and a reason-coded report for every negative branch. The operational owner must be able to reproduce the result from the trace and manifest alone, without inspecting mutable chart state.
