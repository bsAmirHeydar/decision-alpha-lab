---
title: "FP-I04 — Multi-Symbol M1 Synchronization, Coverage, and Data Revision"
tags: [exp0019, faerie-protocol, fp-i04, implementation-delivery]
status: implemented_python_and_static_validated
phase_version: 1.0.0
doc_version: 1.0.0
last_updated: 2026-07-13
language: en
---
# FP-I04 — Multi-Symbol M1 Synchronization, Coverage, and Data Revision

## Decision summary

FP-I04 creates the canonical two-symbol M1 data plane used by every later Faerie Protocol phase. It does not detect divergence. It guarantees that both symbols are represented on the same UTC minute axis, that absence is classified rather than hidden, and that late or corrected history produces bounded revision evidence.

## Architecture

```text
broker/vendor aliases + M1 deliveries
                │
        SymbolResolver / M1Bar validation
                │
        duplicate normalization
                │
FP-I03 calendar ─┼─ expected minute axis
                │
        per-symbol coverage + gaps
                │
        AlignedMinute sequence
                │
   DataRevision / Cursor / Backfill
                │
        PairDatasetSnapshot
                │
               FP-I05
```

## Delivery inventory

| Surface | Delivery |
|---|---|
| Python | 18 modules |
| Tests | 67 phase tests before release metadata tests |
| Contracts | 15 immutable public contracts |
| Reasons | 30 closed data reason codes |
| Schemas | 15 closed Draft 2020-12 schemas |
| MQL5 | 13 include modules + self-test + diagnostic |
| Golden fixtures | complete, missing, conflict, correction |
| Authority | NONE |

## Chapter map
- [[01_MISSION_SCOPE_AND_NON_GOALS|Mission, Scope, and Non-Goals]]
- [[02_UPSTREAM_FP_I03_HANDOFF|Upstream FP-I03 Handoff]]
- [[03_DATA_PLANE_ARCHITECTURE|Data Plane Architecture]]
- [[04_SYMBOL_PAIR_AND_ALIAS_RESOLUTION|Symbol Pair and Alias Resolution]]
- [[05_CANONICAL_M1_BAR_CONTRACT|Canonical M1 Bar Contract]]
- [[06_CLOSED_BAR_FINALITY_POLICY|Closed-Bar Finality Policy]]
- [[07_PRICE_GRID_AND_OHLC_VALIDATION|Price Grid and OHLC Validation]]
- [[08_DUPLICATE_DELIVERY_RESOLUTION|Duplicate Delivery Resolution]]
- [[09_EXPECTED_MINUTE_AXIS|Expected Minute Axis]]
- [[10_CALENDAR_EXCLUSION_ACCOUNTING|Calendar Exclusion Accounting]]
- [[11_COVERAGE_INTERVAL_MODEL|Coverage Interval Model]]
- [[12_GAP_TAXONOMY|Gap Taxonomy]]
- [[13_MINUTE_CELL_STATE_MACHINE|Minute Cell State Machine]]
- [[14_ALIGNED_PAIR_ROW_CONTRACT|Aligned Pair Row Contract]]
- [[15_SYNCHRONIZATION_ALGORITHM|Synchronization Algorithm]]
- [[16_HEALTH_READY_DEGRADED_BLOCKED|Health: READY, DEGRADED, and BLOCKED]]
- [[17_BATCH_PROCESSING_MODEL|Batch Processing Model]]
- [[18_INCREMENTAL_PROCESSING_MODEL|Incremental Processing Model]]
- [[19_CURSOR_CONTRACT_AND_RESUME|Cursor Contract and Resume]]
- [[20_DATA_REVISION_LINEAGE|Data Revision Lineage]]
- [[21_INITIAL_AND_APPEND_REVISIONS|Initial and Append Revisions]]
- [[22_LATE_INSERT_REVISIONS|Late Insert Revisions]]
- [[23_VALUE_CORRECTION_AND_DELETE|Value Correction and Delete]]
- [[24_REVISION_IMPACT_SCOPING|Revision Impact Scoping]]
- [[25_SOURCE_REVISION_AND_TRANSPORT_METADATA|Source Revision and Transport Metadata]]
- [[26_BACKFILL_PLANNER|Backfill Planner]]
- [[27_BOUNDED_REPAIR_AND_PERFORMANCE|Bounded Repair and Performance]]
- [[28_DATASET_SNAPSHOT_AND_CACHE_IDENTITY|Dataset Snapshot and Cache Identity]]
- [[29_REASON_CODE_REGISTRY|Reason-Code Registry]]
- [[30_SEMANTIC_IDENTITY_RULES|Semantic Identity Rules]]
- [[31_RESTART_AND_REBUILD_PARITY|Restart and Rebuild Parity]]
- [[32_TELEMETRY_AND_COUNTERS|Telemetry and Counters]]
- [[33_FAILURE_MATRIX|Failure Matrix]]
- [[34_TEST_STRATEGY|Test Strategy]]
- [[35_GOLDEN_FIXTURES|Golden Fixtures]]
- [[36_NEGATIVE_AND_FAILURE_INJECTION|Negative and Failure Injection]]
- [[37_DIFFERENTIAL_BATCH_INCREMENTAL_PARITY|Differential Batch/Incremental Parity]]
- [[38_MQL5_CONTRACT_MIRROR|MQL5 Contract Mirror]]
- [[39_DIAGNOSTIC_EA|Diagnostic EA]]
- [[40_SECURITY_AND_AUTHORITY_BOUNDARY|Security and Authority Boundary]]
- [[41_OPERATOR_RUNBOOK|Operator Runbook]]
- [[42_DATA_INCIDENT_RUNBOOK|Data Incident Runbook]]
- [[43_ROLLBACK_AND_REBASELINE|Rollback and Rebaseline]]
- [[44_ACCEPTANCE_GATE_MATRIX|Acceptance Gate Matrix]]
- [[45_HANDOFF_TO_FP_I05|Handoff to FP-I05 Reference Engine]]
- [[46_PUBLIC_API_CATALOG|Public API Catalog]]
- [[47_JSON_SCHEMA_CATALOG|JSON Schema Catalog]]
- [[48_MODULE_AND_FILE_MAP|Module and File Map]]
- [[49_WORK_BREAKDOWN_AND_COMMIT_SLICES|Work Breakdown and Commit Slices]]
- [[50_LIMITATIONS_AND_FUTURE_WORK|Limitations and Future Work]]


## ADRs

- [[adrs/ADR_I04_001_UTC_M1_OPEN_IS_ALIGNMENT_KEY]]
- [[adrs/ADR_I04_002_NO_SYNTHETIC_GAP_FILL]]
- [[adrs/ADR_I04_003_CONFLICTING_DUPLICATES_BLOCK]]
- [[adrs/ADR_I04_004_TRANSPORT_METADATA_IS_NOT_BAR_SEMANTICS]]
- [[adrs/ADR_I04_005_REVISIONS_INVALIDATE_ONLY_DEPENDENT_WINDOWS]]
- [[adrs/ADR_I04_006_BATCH_IS_INCREMENTAL_PARITY_ORACLE]]

## Golden acceptance

1. Both symbols align by exact UTC M1 open.
2. Missing, out-of-coverage, conflict, and revised states remain distinct.
3. Calendar exclusions do not reduce coverage or generate backfill.
4. Late inserts and corrections create parent-linked revisions.
5. Batch and incremental semantic sequences match.
6. No reference, divergence, drawing, or execution authority exists.

## Next phase

FP-I05 builds A/L/N/W window aggregation, calendar-day selectors, symbol-local references, and protected-touch lifecycle on top of the aligned revision-bearing rows.
