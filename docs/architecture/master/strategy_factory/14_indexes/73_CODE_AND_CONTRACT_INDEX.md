---
type: strategy-factory-document
status: canonical
title: "Code and Contract Index"
tags:
  - strategy-factory
---

# Code and Contract Index

This index maps documentation concepts to concrete implementation files.

## Python

| Concern | File |
|---|---|
| Contracts | `contracts.py` |
| Manifest | `manifest.py` |
| Adapters | `adapters/base.py`, `adapters/csv_adapter.py` |
| Candidate engine | `candidate_engine.py` |
| Simulation | `simulation.py` |
| Costs | `costs.py` |
| Labels | `labels.py` |
| Statistics | `statistics.py` |
| Fold splitter | `validation/folds.py` |
| Anti-overfit | `anti_overfit.py` |
| Models | `models/baselines.py`, `models/training.py` |
| Risk/paper | `execution/*` |
| Artifacts/registry | `artifacts.py`, `registry.py` |
| Promotion | `promotion.py` |
| Audit/reporting | `audit.py`, `reporting.py` |

## MQL5

`SF_Contracts.mqh`, `SF_AnatomyAdapter.mqh`, `SF_CandidatePolicies.mqh`, `SF_RiskGate.mqh`, `SF_PaperBroker.mqh`, and `SF_ExecutionBridge.mqh` define the shared terminal boundary. No live send implementation is included.

