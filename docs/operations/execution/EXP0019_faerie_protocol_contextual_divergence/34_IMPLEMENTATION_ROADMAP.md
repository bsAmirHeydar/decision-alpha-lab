---
title: "34 - Implementation Roadmap"
tags: [exp0019, faerie-protocol, implementation-program, obsidian]
status: normative
experiment: EXP0019
context_id: FP-CONTEXT-001
implementation_program: FP-IMP-001
program_version: 1.0.0
doc_version: 1.0.0
last_updated: 2026-07-13
language: en
---

# 34 - Implementation Roadmap

## Canonical roadmap

The short roadmap has been replaced by the full implementation program:

> [[implementation_program/00_IMPLEMENTATION_PROGRAM_MOC|FP-IMP-001 — Faerie Protocol Implementation Program]]

The program treats the **complete indicator as a mandatory independent product**, not as an afterthought to the trading EA.

## Milestone sequence

| Milestone | Phases | Result |
|---|---|---|
| Governance and compatibility | FP-I00–FP-I01 | stable baseline and no-regression adapters |
| Contracts and context engine | FP-I02–FP-I09 | deterministic signals, WW, ledger, quota eligibility, restart |
| Complete indicator | FP-I10–FP-I13 | full visuals, panel, filters, alerts, export, replay/performance release |
| Diagnostic parity | FP-I14 | Indicator/EA semantic equality |
| Paper execution | FP-I15 | risk and simulated order lifecycle |
| Live execution | FP-I16 | gated by FP-DEC-012 and safety authorization |

## Why the indicator precedes execution

The indicator is the human-auditable projection of the context engine. It exposes time/session ownership, symbol-local references, Hunt facts, confirmation, WW state, suppression, and quota arbitration. Requiring it before execution prevents a hidden EA detector from becoming canonical without visual and replay evidence.

## Phase list

- [[implementation_program/phases/FP_I00_GOVERNANCE_BASELINE_FREEZE_AND_SOURCE-CONTROL_HARNESS|FP-I00]]
- [[implementation_program/phases/FP_I01_SHARED-CORE_COMPATIBILITY_HARNESS_AND_ADAPTER_CONTRACTS|FP-I01]]
- [[implementation_program/phases/FP_I02_CONTRACTS_ENUMS_IDENTITY_CONFIGURATION_AND_REASON_CODES|FP-I02]]
- [[implementation_program/phases/FP_I03_NEW_YORK_TIME_TRADING-DAY_SESSION_AND_WEEK_KERNEL|FP-I03]]
- [[implementation_program/phases/FP_I04_MULTI-SYMBOL_M1_SYNCHRONIZATION_COVERAGE_AND_DATA_REVISION|FP-I04]]
- [[implementation_program/phases/FP_I05_SESSION_WEEK_WINDOW_STORE_CALENDAR-DAY_SELECTOR_AND_REFERENCE_ENGINE|FP-I05]]
- [[implementation_program/phases/FP_I06_RELATION_COMPILER_HUNT_FACTS_FIRST-SWEEP_CLASSIFICATION_AND_CANDIDATES|FP-I06]]
- [[implementation_program/phases/FP_I07_HOST-CANDLE_CONFIRMATION_STRICT_SESSION_DEADLINE_INVALIDATION_AND_LIFECYCLE|FP-I07]]
- [[implementation_program/phases/FP_I08_WEEKLY_WW_DETECTION_NEUTRALIZATION_ACTIVE_STACK_AND_DIRECTIONAL_POLICY|FP-I08]]
- [[implementation_program/phases/FP_I09_SIGNAL_LEDGER_DEDUPLICATION_PAIR-SESSION_ARBITRATION_CHECKPOINTS_AND_RESTART|FP-I09]]
- [[implementation_program/phases/FP_I10_COMPLETE_INDICATOR_SHELL_ENGINE_COMPOSITION_HEALTH_AND_MACHINE-READABLE_OUTPUTS|FP-I10]]
- [[implementation_program/phases/FP_I11_INDICATOR_VISUAL_PROJECTION_SESSIONS_REFERENCES_HUNTS_SIGNALS_WW_AND_SUPPRESSION|FP-I11]]
- [[implementation_program/phases/FP_I12_INDICATOR_PANEL_FILTERS_ALERTS_AUDIT_EXPORT_AND_OPERATOR_UX|FP-I12]]
- [[implementation_program/phases/FP_I13_INDICATOR_HISTORICAL_REPLAY_INCREMENTAL_PERFORMANCE_MULTI-CHART_ISOLATION_AND_RELEASE|FP-I13]]
- [[implementation_program/phases/FP_I14_DIAGNOSTIC_EA_AND_CROSS-PRODUCT_DIFFERENTIAL_VALIDATION|FP-I14]]
- [[implementation_program/phases/FP_I15_RISK_GEOMETRY_PAIR-SESSION_RESERVATION_AND_PAPER_EXECUTION|FP-I15]]
- [[implementation_program/phases/FP_I16_LIVE_EXECUTION_DECISION_GATE_AUTHORIZATION_MICRO-RELEASE_AND_MONITORING|FP-I16]]

## Live decision boundary

FP-I00 through FP-I14, including the complete indicator, are not blocked by `FP-DEC-012`. Paper execution may use a clearly named test profile. The canonical live quota lifecycle remains blocked until the owner selects the consumption/release policy.

## Navigation

- [[00_EXP0019_MOC|EXP0019 Master MOC]]
- [[implementation_program/00_IMPLEMENTATION_PROGRAM_MOC|Implementation Program MOC]]
- [[44_ACCEPTANCE_GATE_FOR_CODING|Acceptance Gate for Coding]]
