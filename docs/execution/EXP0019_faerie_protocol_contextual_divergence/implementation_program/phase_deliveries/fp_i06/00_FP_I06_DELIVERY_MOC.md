---
tags: [exp0019, faerie-protocol, fp-i06, relation-compiler, hunt-engine]
status: normative
phase: FP-I06
version: 1.0.0
last_updated: 2026-07-13
language: en
---
# FP-I06 — Relation Compiler, Hunt Facts, First-Sweep Classification, and Candidates

## Decision summary

FP-I06 is the first phase that turns frozen Faerie Protocol reference windows into raw divergence candidates. It compiles six non-weekly relation families, derives HIGH and LOW plans, scans canonical aligned M1 evidence, records symbol-local HuntFacts, classifies first sweep without tick-order invention, assigns Hunter/Protected roles, and emits deterministic raw candidates.

## Authority boundary

`NONE`. No confirmation, WW policy, drawing, alerting, quota, risk, broker, order, or network surface exists.

## Core invariants

- Six supported relations: `AL`, `AN`, `LN`, `NA`, `NL`, `NN`.
- `WW` remains registered but deferred to FP-I08.
- LOW one-sided hunt is Bullish; HIGH one-sided hunt is Bearish.
- Same-M1 dual touch is symmetric and creates no candidate.
- Protected second touch cancels the raw candidate.
- Missing/conflicting M1 blocks classification.
- Candidate identity is deterministic and projection-free.

## Documentation map

- [[01_PHASE_CHARTER|Phase Charter]]
- [[02_ARCHITECTURE|Architecture]]
- [[03_RELATION_REGISTRY|Relation Registry]]
- [[04_RELATION_COMPILER|Relation Compiler]]
- [[05_SAME_DAY_RELATIONS|Same-Day Relation Compilation]]
- [[06_PRIOR_N_RELATIONS|Prior-N Calendar-Offset Relations]]
- [[07_SIDE_PLAN_COMPILATION|HIGH and LOW Side Plans]]
- [[08_REFERENCE_ELIGIBILITY|Reference Eligibility]]
- [[09_HUNT_FACT_CONTRACT|Hunt Fact Contract]]
- [[10_M1_FIRST_SWEEP_AUTHORITY|M1-Only First-Sweep Authority]]
- [[11_MINUTE_CONTACT_OBSERVATION|Minute Contact Observation]]
- [[12_FIRST_SWEEP_CLASSIFICATION|First-Sweep Classification]]
- [[13_SAME_M1_AMBIGUITY|Same-M1 Symmetric Ambiguity]]
- [[14_HUNTER_PROTECTED_ROLES|Hunter and Protected Roles]]
- [[15_DIRECTION_CLASSIFICATION|Bullish and Bearish Direction]]
- [[16_CANDIDATE_IDENTITY|Raw Candidate Identity]]
- [[17_CANDIDATE_STATE_MACHINE|Raw Candidate State Machine]]
- [[18_SECOND_TOUCH_CANCELLATION|Second Protected Touch Cancellation]]
- [[19_DATA_BLOCKING|Missing and Conflicting Data]]
- [[20_CHECK_WINDOW_END|Check-Window End Semantics]]
- [[21_MULTI_REFERENCE_COMPETITION|Multi-Reference Competition]]
- [[22_REFERENCE_REUSE_INTERACTION|Cross-Relation Reference Reuse]]
- [[23_BATCH_INCREMENTAL_PARITY|Batch and Incremental Parity]]
- [[24_DUPLICATION_AND_IDEMPOTENCY|Deduplication and Idempotency]]
- [[25_REVISION_INVALIDATION|Bounded Revision Invalidation]]
- [[26_CHECKPOINT_AND_RESTART|Checkpoint and Restart]]
- [[27_ENGINE_SNAPSHOT|Engine Snapshot]]
- [[28_REASON_CODE_REGISTRY|Reason-Code Registry]]
- [[29_PUBLIC_API_AND_SCHEMAS|Public API and JSON Schemas]]
- [[30_MQL5_CONTRACT_MIRROR|MQL5 Contract Mirror]]
- [[31_GOLDEN_VECTORS|Golden Vectors]]
- [[32_TEST_STRATEGY|Test Strategy]]
- [[33_PERFORMANCE|Performance and Incremental Work]]
- [[34_OBSERVABILITY|Observability]]
- [[35_FAILURE_MODES|Failure Modes]]
- [[36_SECURITY_AND_AUTHORITY|Security and Authority Boundary]]
- [[37_OPERATOR_RUNBOOK|Operator Runbook]]
- [[38_RELEASE_ROLLBACK|Release, Patch, and Rollback]]
- [[39_ACCEPTANCE_GATE|Acceptance Gate]]
- [[40_HANDOFF_TO_FP_I07|Handoff to FP-I07]]

## ADRs

- [[adrs/ADR_FP_I06_001_M1_IS_THE_ONLY_FIRST_SWEEP_AUTHORITY]]
- [[adrs/ADR_FP_I06_002_SAME_M1_HAS_NO_ORDER]]
- [[adrs/ADR_FP_I06_003_RELATION_SIDE_PLANS_ARE_INDEPENDENT]]
- [[adrs/ADR_FP_I06_004_WW_IS_DEFERRED_TO_FP_I08]]
- [[adrs/ADR_FP_I06_005_SECOND_PROTECTED_TOUCH_CANCELS_RAW_CANDIDATE]]
- [[adrs/ADR_FP_I06_006_REVISION_INVALIDATION_IS_BOUNDED]]

## Handoff

FP-I07 receives raw candidates and adds host-candle confirmation under strict same-session deadline. It may not alter first-sweep time, side, direction, roles, or same-M1 classification.
