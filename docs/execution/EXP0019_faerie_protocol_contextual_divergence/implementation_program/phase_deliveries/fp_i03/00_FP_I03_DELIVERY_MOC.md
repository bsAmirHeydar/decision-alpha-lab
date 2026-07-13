---
title: "FP-I03 — Time, Trading-Day, Session, and Week Kernel Delivery"
tags: [exp0019, faerie-protocol, fp-i03, time-calendar, obsidian]
status: normative
phase: FP-I03
phase_version: 1.0.0
doc_version: 1.0.0
last_updated: 2026-07-13
language: en
---
# FP-I03 — Time, Trading-Day, Session, and Week Kernel

## Delivery summary

FP-I03 implements the exact broker-independent temporal kernel required by every later Faerie Protocol module. It freezes UTC/New York conversion, deterministic US DST rules, local ambiguity handling, trading-day labels, A/L/N windows, daily gap, weekly boundaries, semantic identities, evidence, Python/MQL5 parity surfaces, schemas, tests, and operator runbooks.

## Canonical calendar

```text
New York trading day (label = ending civil date)

previous date 18:00 ───────────── labeled date 17:00
        │ A [18:00,04:00) │ L [04:00,09:30) │ N [09:30,17:00) │
                                                             │
                                                  gap [17:00,18:00)

New York week
Sunday 18:00 inclusive ───────────────── Friday 17:00 exclusive
```

## Delivery inventory

| Surface | Delivered |
|---|---:|
| Python modules | 15 |
| Phase tests | 83 |
| Closed JSON schemas | 12 |
| Public time contracts | 11 |
| Time reason codes | 15 |
| MQL5 include modules | 12 |
| MQL5 entry points | 2 |
| Golden conformance checks | 20 |
| Boundary fixtures | 12 |
| Documentation chapters | 42 |
| ADRs | 9 |
| Atomic concepts | 7 |

## Chapter map
- [[01_PHASE_MISSION_SCOPE_AND_AUTHORITY|Phase Mission, Scope, and Authority Boundary]]
- [[02_UPSTREAM_I02_CONTRACT_AND_I01_COMPATIBILITY|Upstream FP-I02 Contract and FP-I01 Compatibility]]
- [[03_CANONICAL_UTC_AXIS|Canonical UTC Axis]]
- [[04_EXPLICIT_BROKER_TIME_ADAPTER|Explicit Broker-Time Adapter]]
- [[05_TIME_RULE_VERSION_AND_SUPPORTED_RANGE|Time-Rule Version and Supported Year Range]]
- [[06_US_NEW_YORK_DST_ALGORITHM|US/New York DST Algorithm]]
- [[07_SPRING_FORWARD_NONEXISTENT_LOCAL_TIME|Spring-Forward Nonexistent Local Time]]
- [[08_FALL_BACK_AMBIGUOUS_LOCAL_TIME|Fall-Back Ambiguous Local Time]]
- [[09_LOCAL_TO_UTC_RESOLUTION_CONTRACT|Local-to-UTC Resolution Contract]]
- [[10_TRADING_DAY_IDENTITY_AND_LABELING|Trading-Day Identity and Labeling]]
- [[11_A_SESSION_CONTRACT|A Session Contract]]
- [[12_L_SESSION_CONTRACT|L Session Contract]]
- [[13_N_SESSION_CONTRACT|N Session Contract]]
- [[14_DAILY_GAP_CONTRACT|Daily Gap Contract]]
- [[15_NEW_YORK_WEEK_CONTRACT|New York Week Contract]]
- [[16_PREVIOUS_COMPLETED_WEEK_SELECTION|Previous Completed Week Selection]]
- [[17_HALF_OPEN_BOUNDARY_OWNERSHIP|Half-Open Boundary Ownership]]
- [[18_CALENDAR_SNAPSHOT_AGGREGATE|Calendar Snapshot Aggregate]]
- [[19_SEMANTIC_IDENTITIES_AND_HASHES|Semantic Identities and Hashes]]
- [[20_BOUNDARY_EVIDENCE_CHAIN|Boundary Evidence Chain]]
- [[21_SESSION_REGISTRY|Frozen Session Registry]]
- [[22_TIME_REASON_CODE_REGISTRY|Time Reason-Code Registry]]
- [[23_PUBLIC_CONTRACT_REGISTRY|Public Contract Registry]]
- [[24_JSON_SCHEMA_CATALOG|JSON Schema Catalog]]
- [[25_PYTHON_API_REFERENCE|Python API Reference]]
- [[26_MQL5_SHARED_CORE_ADAPTER|MQL5 Shared-Core Adapter]]
- [[27_MQL5_TYPE_AND_IDENTITY_PARITY|MQL5 Type and Identity Parity]]
- [[28_BROKER_TIME_INVARIANCE|Broker-Time Invariance]]
- [[29_IANA_DIFFERENTIAL_CONFORMANCE|IANA Differential Conformance]]
- [[30_GOLDEN_BOUNDARY_FIXTURES|Golden Boundary Fixtures]]
- [[31_DST_GOLDEN_FIXTURES|DST Golden Fixtures]]
- [[32_REPLAY_RESTART_AND_DETERMINISM|Replay, Restart, and Determinism]]
- [[33_PERFORMANCE_AND_INCREMENTAL_USAGE|Performance and Incremental Usage]]
- [[34_FAILURE_AND_HEALTH_MODEL|Failure and Health Model]]
- [[35_AUTHORITY_AND_SECURITY_BOUNDARY|Authority and Security Boundary]]
- [[36_TEST_STRATEGY|Test Strategy]]
- [[37_OPERATOR_DIAGNOSTIC_RUNBOOK|Operator Diagnostic Runbook]]
- [[38_METAEDITOR_COMPILE_AND_RUNTIME_EVIDENCE|MetaEditor Compile and Runtime Evidence]]
- [[39_VERSIONING_MIGRATION_AND_REBASELINE|Versioning, Migration, and Rebaseline]]
- [[40_ROLLBACK_BOUNDARY|Rollback Boundary]]
- [[41_ACCEPTANCE_GATE_AND_EVIDENCE|Acceptance Gate and Evidence]]
- [[42_HANDOFF_TO_FP_I04|Handoff to FP-I04 M1 Synchronization]]

## ADRs

- [[adrs/ADR_FP_I03_001_UTC_IS_CANONICAL]]
- [[adrs/ADR_FP_I03_002_BROKER_OFFSET_IS_EXPLICIT]]
- [[adrs/ADR_FP_I03_003_DST_RULE_IS_VERSIONED]]
- [[adrs/ADR_FP_I03_004_TRADING_DAY_LABELS_ENDING_DATE]]
- [[adrs/ADR_FP_I03_005_SESSIONS_ARE_HALF_OPEN]]
- [[adrs/ADR_FP_I03_006_DAILY_GAP_IS_EXPLICIT]]
- [[adrs/ADR_FP_I03_007_WEEK_IS_SUNDAY_18_TO_FRIDAY_17]]
- [[adrs/ADR_FP_I03_008_AMBIGUOUS_LOCAL_TIME_REQUIRES_POLICY]]
- [[adrs/ADR_FP_I03_009_NO_HOLIDAY_CALENDAR_IN_I03]]

## Acceptance command chain

```powershell
$env:PYTHONPATH = ".\lab\10_infrastructure\EXP0019_faerie_protocol\phase_i02\python;.\lab\10_infrastructure\EXP0019_faerie_protocol\phase_i03\python"
python -m pytest -q .\lab\10_infrastructure\EXP0019_faerie_protocol\phase_i03\tests
python .\tools\exp0019\check_fp_i03_boundaries.py .
python .\tools\exp0019\check_fp_i03_mql5_static.py .
python .\tools\exp0019\generate_fp_i03_vectors.py . --verify-only
python .\tools\exp0019\validate_fp_i03_delivery.py .
```

## Next phase

FP-I04 consumes the accepted calendar to align both symbols by canonical M1 UTC open time. It may not reinterpret session or weekly boundaries.
