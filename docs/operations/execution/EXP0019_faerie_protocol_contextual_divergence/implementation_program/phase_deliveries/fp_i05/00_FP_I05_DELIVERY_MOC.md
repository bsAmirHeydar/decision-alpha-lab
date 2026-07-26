---
phase: FP-I05
experiment: EXP0019
context_id: FP-CONTEXT-001
status: normative
phase_version: 1.0.0
language: en
last_updated: 2026-07-13
---
# FP-I05 — Session/Week Window Store, Calendar-Day Selector, and Reference Engine

## Decision summary

FP-I05 is the first phase that turns synchronized market evidence into durable context objects. It produces A/L/N/W window aggregates and symbol-local HIGH/LOW references. It does **not** decide whether a hunt, divergence, confirmation, visual projection, or trade exists.

## Canonical pipeline

```text
FP-I03 Time/Calendar Kernel
            ↓
FP-I04 Pair-Aligned Closed M1 Evidence
            ↓
FP-I05 Window Descriptor + Symbol Aggregates
            ↓
Calendar-Day N Selector + Reference Sets
            ↓
Reference Lifecycle / Store / Revision Invalidation
            ↓
FP-I06 Hunt Observation Engine
```

## Non-negotiable invariants

1. Calendar-day offsets never compress.
2. A/L/N/W windows use FP-I03 boundaries and half-open semantics.
3. Each symbol owns its own high and low.
4. References require complete source windows under the canonical profile.
5. Hunter touch does not consume a reference.
6. Protected touch is the only consumption event.
7. Data revision invalidation is bounded to overlap.
8. Batch, incremental and restart rebuilds converge to the same semantic hashes.
9. No detection, drawing, alerting or execution authority exists.

## Chapter map
- [[01_PHASE_CHARTER|Phase Charter and Non-Negotiables]]
- [[02_ARCHITECTURE|Architecture and Dependency Boundaries]]
- [[03_WINDOW_DESCRIPTOR|Canonical Window Descriptor]]
- [[04_SESSION_AGGREGATION|A/L/N Session Aggregation]]
- [[05_WEEK_AGGREGATION|New York Trading Week Aggregation]]
- [[06_WINDOW_STATE_MACHINE|Window State Machine]]
- [[07_CALENDAR_DAY_SELECTOR|Calendar-Day N Selector]]
- [[08_SYMBOL_LOCAL_REFERENCES|Symbol-Local Reference Construction]]
- [[09_REFERENCE_IDENTITY|Reference Semantic Identity]]
- [[10_REFERENCE_LIFECYCLE|Reference Lifecycle and Protected Consumption]]
- [[11_HUNTER_TOUCH_POLICY|Hunter Touch Non-Consumption Policy]]
- [[12_PROTECTED_TOUCH_POLICY|Protected Touch Consumption Policy]]
- [[13_COVERAGE_AND_COMPLETENESS|Coverage, Completeness, and Blocking]]
- [[14_REVISION_INVALIDATION|Revision Impact and Bounded Invalidation]]
- [[15_STORE_INDEXING|Window Store Indexing and Query API]]
- [[16_CHECKPOINT_RESTART|Checkpoint, Restart, and Deterministic Rebuild]]
- [[17_BATCH_INCREMENTAL_PARITY|Batch and Incremental Parity]]
- [[18_REASON_CODES|Reason-Code Registry]]
- [[19_PYTHON_API|Python API Reference]]
- [[20_MQL5_MIRROR|MQL5 Contract Mirror]]
- [[21_GOLDEN_VECTORS|Golden and Negative Vectors]]
- [[22_PERFORMANCE|Performance and Long-Depth Budget]]
- [[23_OBSERVABILITY|Diagnostics and Health Evidence]]
- [[24_FAILURE_MODES|Failure Modes and Incident Response]]
- [[25_SECURITY_AUTHORITY|Security and No-Authority Boundary]]
- [[26_TEST_STRATEGY|Test Strategy and Acceptance Matrix]]
- [[27_OPERATOR_RUNBOOK|Operator Runbook]]
- [[28_MIGRATION|Migration from Legacy FP 101 Behavior]]
- [[29_HANDOFF_TO_FP_I06|Handoff to FP-I06 Hunt Engine]]


## ADRs

- [[adrs/ADR_FP_I05_001_CALENDAR_OFFSETS_DO_NOT_COMPRESS]]
- [[adrs/ADR_FP_I05_002_REFERENCES_ARE_SYMBOL_LOCAL]]
- [[adrs/ADR_FP_I05_003_HUNTER_TOUCH_IS_NON_CONSUMING]]
- [[adrs/ADR_FP_I05_004_ONLY_COMPLETE_WINDOWS_CREATE_REFERENCES]]
- [[adrs/ADR_FP_I05_005_REVISION_INVALIDATION_IS_BOUNDED]]

## Acceptance gate

The phase is accepted only when Python tests, conformance vectors, schema closure, boundary guard, MQL5 static validation, cumulative regressions, engineering policies and clean-baseline patch verification pass. MetaEditor compilation remains a separate Windows gate.
