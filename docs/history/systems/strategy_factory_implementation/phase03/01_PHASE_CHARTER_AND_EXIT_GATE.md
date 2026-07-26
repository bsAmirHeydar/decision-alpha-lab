---
title: "Phase 03 Charter and Exit Gate"
status: implemented
phase: PHASE_03
language: en
tags:
  - strategy-factory
  - phase03
  - mql5
  - market-services
---

# Objective

Build the central, reusable market-services layer that every future anatomy plugin will depend on. The phase closes only when market truth can be requested through typed ports without importing any strategy-specific code.

## Scope

Phase 03 implements:

1. A canonical UTC clock and broker-time mapping.
2. Deterministic New York daylight-saving rules.
3. Trading-day and data-driven session primitives.
4. A bounded latest-tick cache.
5. A bounded closed-bar cache with replacement, duplicate, ordering, and gap semantics.
6. Canonical new-bar identity.
7. Multi-symbol synchronization with explicit skew and freshness requirements.
8. A terminal source boundary that is the sole owner of terminal market APIs.
9. A symbol specification cache with material-change generation.
10. Market health and performance telemetry.
11. An offline Python mirror for conformance, fixtures, and research tooling.
12. MQL5 self-test and terminal diagnostic EAs.

## Explicit non-goals

- No anatomy adapters.
- No entry, stop, exit, candidate, or outcome logic.
- No Strategy Tester optimization.
- No ONNX.
- No risk sizing.
- No order sending.
- No integration of EXP0017, NDS, Daye, ICT, Astro, or legacy execution code.
- No external UI.

## Exit gate

Automated evidence:

- Phase 01, 02, and 03 Python tests pass together.
- Python packages compile from clean checkout.
- Static dependency guard reports zero violations.
- Terminal API calls exist only inside `SF03_TerminalMarketSource.mqh`.
- No live-order authority tokens exist in Phase 03.
- Obsidian links and machine-readable registries are valid.

Mandatory local evidence:

- `SF03_MarketServicesSelfTest.mq5` compiles with **0 errors**.
- Self-test returns `INIT_SUCCEEDED`.
- Diagnostic EA successfully refreshes one single-symbol series.
- Diagnostic EA successfully validates a synchronized two-symbol case on the intended broker.
- At least one prefixed or suffixed broker symbol is accepted.
- Broker UTC offset configuration is explicitly verified.

## Definition of failure

The phase is not accepted if a future anatomy must implement any of the following itself:

```text
new-bar detection
broker-to-UTC conversion
New York DST
session boundaries
CopyRates coordination
missing-bar policy
symbol-spec normalization
multi-symbol close alignment
```
