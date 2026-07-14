---
title: UCEE I01–I18 Compatibility
status: canonical
version: 3.0.0
created: '2026-07-13'
updated: '2026-07-13'
tags:
- saed-v3
- ucee
- compatibility
---

# Compatibility contract

SAED V3 is an additive post-context architecture. It does not fork or replace UCEE. Every component binds to exact upstream hashes and emits artifacts accepted by the downstream phase.

| UCEE phase | SAED V3 usage |
|---|---|
| I01 | canonical context identity and occurrence contract |
| I02 | temporal truth, event clocks and decision-time semantics |
| I03 | lifecycle, validity, expiry and state-transition semantics |
| I04 | multi-view context evidence and support boundaries |
| I05 | feature DAG and point-in-time materialization |
| I06 | known-time snapshot and leakage-control contracts |
| I07 | outcome, treatment economics and executable replay contracts |
| I08 | clustered dataset and evidence-role semantics |
| I09 | purged fold, embargo and temporal validation contracts |
| I10 | experiment manifest, trial identity and reproducible orchestration |
| I11 | model training, calibration and reproducibility primitives |
| I12 | anti-overfit challenge and signed promotion admission |
| I13 | manual/AI/hybrid policy graph and fallback authority |
| I14 | immutable runtime compilation and Python/export/MQL5 parity |
| I15 | context treatment tournament and prospective paper governance |
| I16 | context onboarding and legacy adapter migration |
| I17 | opportunity ranking, risk reservation, capacity and portfolio allocation |
| I18 | compile, shadow, no-send, authorization, micro-live and operations evidence |

# Invariants

1. SAED cannot create a context occurrence.
2. SAED cannot alter known time or lifecycle history.
3. Candidate treatments must reference an exact context specification version.
4. Dataset rows retain occurrence cluster identity.
5. Promotion admission defines the maximum support of the policy graph.
6. Runtime cannot load a partial SAED package.
7. Portfolio and risk vetoes dominate model preference.
8. Static or fixture evidence cannot be labelled actual production evidence.
