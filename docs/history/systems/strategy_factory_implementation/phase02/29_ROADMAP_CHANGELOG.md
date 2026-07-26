---
title: "Roadmap Changelog"
---

# Roadmap Changelog

## Version 2.1 — MQL5 First

### Moved Earlier

- Shared Market Cache
- UTC Time Kernel
- Symbol Specification Cache
- Multi-Symbol Synchronization
- Strategy Tester research harness

### Constrained

- Event bus is audit-oriented, not the sole hot-path mechanism.
- V1 Host runs one strategy plugin.
- Runtime configuration is startup-compiled.
- UI follows telemetry rather than preceding it.

### Clarified

- MQL5 owns candidate and fill semantics.
- Python owns advanced statistics, anti-overfit and training.
- ONNX inference is subordinate to schema validation, calibration and hard risk.
- Result sinks must become append-only and versioned.

### Preserved

- Canonical contracts.
- Plugin architecture.
- Candidate matrix.
- Outcome studies.
- paper/live parity.
- staged promotion.
