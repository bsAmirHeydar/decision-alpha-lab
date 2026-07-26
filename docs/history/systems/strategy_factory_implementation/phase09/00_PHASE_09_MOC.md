---
title: "Phase 09 — Virtual Outcome Engine and Cost Models MOC"
phase: 09
status: canonical
---
# Phase 09 — Virtual Outcome Engine and Cost Models

## Canonical flow

```text
TradeCandidate
→ register immutable runtime state
→ ordered PriceObservation stream
→ activation and fill resolver
→ bounded path tracker
→ stop / target / time / ambiguity resolution
→ exact cost model
→ terminal OutcomeRecord
→ replayable outcome queue
```

## Documents

- [[01_PHASE_CHARTER|Phase Charter]]
- [[02_AUTHORITY_MODEL|Authority Model]]
- [[03_OUTCOME_DOMAIN_MODEL|Outcome Domain Model]]
- [[04_PRICE_OBSERVATION_CONTRACT|Price Observation Contract]]
- [[05_DATA_FIDELITY_LADDER|Data Fidelity Ladder]]
- [[06_SIMULATION_POLICY|Simulation Policy]]
- [[07_CANDIDATE_LIFECYCLE|Candidate Lifecycle]]
- [[08_ACTIVATION_AND_EXPIRATION|Activation and Expiration]]
- [[09_MARKET_ENTRY_SEMANTICS|Market Entry Semantics]]
- [[10_LIMIT_ENTRY_SEMANTICS|Limit Entry Semantics]]
- [[11_STOP_ENTRY_SEMANTICS|Stop Entry Semantics]]
- [[12_STOP_RESOLUTION|Stop Resolution]]
- [[13_TARGET_RESOLUTION|Target Resolution]]
- [[14_TIME_EXIT_RESOLUTION|Time Exit Resolution]]
- [[15_INTRABAR_AMBIGUITY|Intrabar Ambiguity]]
- [[16_GAP_POLICY|Gap Policy]]
- [[17_BID_ASK_AND_SIDE_AWARE_PRICES|Bid, Ask and Side-Aware Prices]]
- [[18_COST_MODEL_ARCHITECTURE|Cost Model Architecture]]
- [[19_COST_REGISTRY|Cost Registry]]
- [[20_PATH_TRACKING|Path Tracking]]
- [[21_MFE_MAE|MFE and MAE]]
- [[22_PARTIAL_EXIT_PROTOCOL|Partial Exit Protocol]]
- [[23_OUTCOME_RECORD|Outcome Record]]
- [[24_OUTCOME_IDENTITY|Outcome Identity]]
- [[25_IDEMPOTENCY_AND_ORDERING|Idempotency and Ordering]]
- [[26_BOUNDED_MEMORY|Bounded Memory]]
- [[27_FAILURE_SEMANTICS|Failure Semantics]]
- [[28_TELEMETRY|Telemetry]]
- [[29_REPLAY_PROTOCOL|Replay Protocol]]
- [[30_BAR_TO_TICK_PROMOTION|Bar-to-Tick Promotion]]
- [[31_SENSITIVITY_MATRIX|Sensitivity Matrix]]
- [[32_PERFORMANCE_ARCHITECTURE|Performance Architecture]]
- [[33_SECURITY_AND_NO_AUTHORITY|Security and No Authority]]
- [[34_MQL5_API_REFERENCE|MQL5 API Reference]]
- [[35_PYTHON_API_REFERENCE|Python API Reference]]
- [[36_SCHEMA_AND_ARTIFACTS|Schema and Artifacts]]
- [[37_TEST_MATRIX|Test Matrix]]
- [[38_GOLDEN_CASE_REQUIREMENTS|Golden Case Requirements]]
- [[39_LOCAL_COMPILE_RUNBOOK|Local Compile Runbook]]
- [[40_PHASE10_HANDOFF|Phase 10 Handoff]]
- [[41_DEFINITION_OF_DONE|Definition of Done]]
- [[42_KNOWN_LIMITATIONS|Known Limitations]]
