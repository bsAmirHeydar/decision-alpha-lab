---
title: "Implementation Program Charter and Delivery Principles"
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
# Implementation Program Charter and Delivery Principles

## Program mission

The implementation program turns the frozen Faerie Protocol context specification into a production-grade, modular MQL5 subsystem while preserving the already validated intermarket-divergence cores. The program delivers **two first-class products from one engine**:

1. a complete visual and analytical **Faerie Protocol Indicator**;
2. a staged **Diagnostic → Paper → Live Expert Advisor** path.

The indicator is not a thin drawing wrapper around an EA and the EA is not allowed to contain a second private detector. Both consume the same immutable context engine, the same signal ledger, the same IDs, and the same lifecycle state.

## Product doctrine

```text
Shared stable divergence cores
        ↓
Faerie Protocol context engine
        ├── Indicator projection product
        ├── Diagnostic/replay product
        ├── Paper execution product
        └── Live execution product after final gate
```

## Mandatory delivery principles

1. **One semantic engine.** Detection, confirmation, WW resolution, suppression, quota eligibility, and identity are implemented once.
2. **Indicator before execution.** The complete indicator must pass replay and restart parity before the paper EA may use the engine.
3. **No monolithic file.** A single large `FP 101.mq5`-style implementation is prohibited.
4. **Core reuse through adapters.** Context-specific behavior wraps the shared time/reference/hunt/divergence/identity/risk surfaces.
5. **Contracts precede engines.** Every phase freezes types, IDs, reason codes, inputs, and state transitions before behavior code.
6. **Historical and live parity.** M1 replay and incremental live processing must produce identical semantic events from identical data.
7. **Rendering is a projection.** Chart objects never become source-of-truth state.
8. **Suppression is not deletion.** WW, quota, missing-data, and execution policies change eligibility/style, not raw signal existence.
9. **Open decisions fail closed.** `FP-DEC-012` blocks canonical live quota consumption but does not block the indicator or detection engine.
10. **Every phase is independently releasable.** Each phase has entry gates, code, tests, documentation, QA evidence, a patch index, and rollback scope.

## Delivery profiles

| Profile | Contains | Order authority |
|---|---|---:|
| `FP_CORE_DIAGNOSTIC` | Contracts, time, windows, references, detection, ledger | None |
| `FP_INDICATOR_FULL` | Full core + visuals + panel + alerts + export | None |
| `FP_EA_DIAGNOSTIC` | Full core + runtime diagnostics and differential checks | None |
| `FP_EA_PAPER` | Full core + quota/risk + simulated execution | Simulated only |
| `FP_EA_LIVE` | Full core + authorized broker adapter | Blocked until final gates |

## Definition of done

The program is complete only when:

- all seven relation families are replayable and observable;
- the indicator is complete, responsive, restart-safe, and timeframe-invariant for detection;
- the same signal IDs appear in indicator, diagnostic EA, and paper EA;
- no previous divergence context regresses;
- all open decisions required for live execution are frozen;
- MetaEditor compilation, Strategy Tester replay, and controlled forward tests are attached as evidence.
