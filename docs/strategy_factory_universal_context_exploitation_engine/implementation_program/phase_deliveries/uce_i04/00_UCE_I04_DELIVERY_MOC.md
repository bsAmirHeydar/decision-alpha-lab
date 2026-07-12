---
tags:
  - strategy-factory
  - universal-context-engine
  - ucee-i04
status: implemented
doc_version: 1.0.0
last_updated: 2026-07-12
---
# UCE-I04 — Complete Treatment Compiler and Causal Trade Path State Machine

## Mission

UCE-I04 turns the atom registries delivered by UCE-I03 into immutable, executable, and comparable treatments. A treatment is not a loose configuration bag. It is a fully resolved behavior program containing exact atom versions, complete parameter packets, explicit compatibility evidence, a canonical action order, one versioned intrabar policy, one causal path state machine, and stable identity material.

This phase closes the semantic gap between “we have entry/stop/target/trailing/management/sizing atoms” and “research, paper, shadow, and runtime can execute the exact same treatment semantics.”

## Navigation

- [[01_SCOPE_AND_NON_GOALS]]
- [[02_ARCHITECTURE_AND_DATA_FLOW]]
- [[03_CANONICAL_TREATMENT_CONTRACT]]
- [[04_COMPATIBILITY_RULE_LANGUAGE]]
- [[05_TREATMENT_COMPILER_PIPELINE]]
- [[06_ACTION_ORDER_AND_ATOMIC_ACTIVATION]]
- [[07_CAUSAL_PATH_STATE_MACHINE]]
- [[08_INTRABAR_AMBIGUITY_AND_GAP_POLICY]]
- [[09_PARTIAL_FILLS_SCALING_AND_PARTIAL_EXITS]]
- [[10_TREATMENT_MATRIX_GENERATOR]]
- [[11_MANUAL_TREATMENT_PARITY]]
- [[12_GOLDEN_PATH_LIBRARY]]
- [[13_DETERMINISM_IDENTITY_AND_CANONICALIZATION]]
- [[14_CAUSALITY_AND_KNOWN_TIME_GUARDS]]
- [[15_FAILURE_SEMANTICS_AND_FAIL_CLOSED_BEHAVIOR]]
- [[16_TELEMETRY_AND_EVIDENCE]]
- [[17_PYTHON_MQL5_CONFORMANCE]]
- [[18_TEST_STRATEGY_AND_ACCEPTANCE_GATES]]
- [[19_PERFORMANCE_BOUNDS_AND_RESOURCE_BUDGETS]]
- [[20_MIGRATION_FROM_SF08_SF09_SF17]]
- [[21_SECURITY_AUTHORITY_AND_RUNTIME_BOUNDARIES]]
- [[22_OPERATIONAL_RUNBOOK]]
- [[23_RESIDUAL_RISKS_AND_DEFERRED_WORK]]
- [[24_HANDOFF_TO_UCE_I05]]
- [[ADR_010_DECLARATIVE_COMPATIBILITY_RULES]]
- [[ADR_011_TREATMENT_IDENTITY_EXCLUDES_PROVENANCE_ONLY_METADATA]]
- [[ADR_012_SINGLE_CAUSAL_PATH_STATE_MACHINE]]
- [[ADR_013_EXPLICIT_INTRABAR_POLICY]]
- [[ADR_014_BOUNDED_TREATMENT_MATRIX_GENERATION]]

## Delivery Summary

The phase delivers:

1. A Python treatment compiler suitable for exhaustive research matrices, manual baselines, and conformance replay.
2. An MQL5 compiler surface and deterministic reference implementation for runtime-side validation and activation.
3. A typed compatibility rule language with fail-closed cardinality, capability, context-field, market-mode, account-mode, and parameter-relation checks.
4. A causal state machine covering draft, pending, triggered, partial fill, open, scale, partial exit, trail, stop, target, timeout, cancel, reject, and closed states.
5. Centralized intrabar ambiguity, gap-through, stale observation, latency, and priority policies.
6. A bounded treatment matrix generator with deterministic overflow behavior.
7. Manual treatment bundles that preserve exact behavior parity with research treatments.
8. Golden long/short and path scenarios shared by Python and MQL5 conformance.

## Hard Invariants

- Exact atom versions are mandatory.
- Every behavior-changing parameter participates in selection, invocation, plan, and treatment identity.
- Treatment identity is independent of non-behavior provenance such as a human-readable draft name or whether the same behavior came from manual or AI search.
- Invalid combinations fail before simulation.
- State transitions are contiguous, monotonic, causal, and append-only.
- Ambiguous bars never use undocumented ordering.
- Matrix generation cannot exceed declared budgets silently.
- This phase has no broker authority and performs no economic normalization; UCE-I05 owns spread, commission, slippage, tick-value, volume, and capital-risk normalization.

