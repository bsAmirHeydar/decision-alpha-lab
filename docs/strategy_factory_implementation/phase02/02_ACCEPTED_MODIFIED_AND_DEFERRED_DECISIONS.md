---
title: "Accepted, Modified and Deferred Decisions"
---

# Accepted, Modified and Deferred Decisions

## Accepted

- MQL5 is the runtime authority.
- Python is an offline research and training companion.
- One candidate semantics must serve research, tester, paper and live.
- Shared market cache, time kernel and symbol specification cache are mandatory.
- Strategy Tester is a first-class research environment.
- Risk remains deterministic and may veto any model output.
- ONNX is the preferred live model artifact.
- Every real bug must become a fixture.

## Modified

- Generic event bus → bounded typed audit bus plus direct hot-path orchestration.
- One Host loading many strategies → one strategy per Host in V1; portfolio composition later.
- Runtime JSON → startup-validated configuration and immutable runtime generation.
- UI panel immediately → telemetry contracts first; lightweight panel in the observability phase.
- All statistics inside MQL5 → execution-sensitive metrics in MQL5, advanced inference and anti-overfit in Python.

## Deferred

- Live order sending.
- Multi-account portfolio hosting.
- Multi-strategy process-level orchestration.
- ONNX model authority.
- React or remote UI.
- Generalized multi-leg and market-making action plans.
