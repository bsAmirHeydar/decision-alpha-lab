---
title: "Proposal Review and Architecture Comparison"
---

# Proposal Review and Architecture Comparison

The uploaded MQL5-first proposal was reviewed as an architectural input. Its strongest decisions were accepted, while event-bus, multi-strategy, runtime configuration and UI recommendations were constrained to protect latency, determinism and implementation closure.

## Areas of Strong Agreement

The proposal correctly identifies the central problem: separate research and execution implementations create semantic drift. It also correctly places live market, anatomy, candidate, risk and broker truth in MQL5 while assigning offline statistics and training to Python.

The following ideas are adopted as canonical:

1. One MQL5-first Strategy Operating System.
2. One canonical event language after anatomy.
3. One candidate contract across historical research, Strategy Tester, paper and live.
4. A central Strategy Host.
5. Shared market, clock and symbol-specification services.
6. MQL5-native Strategy Tester integration.
7. ONNX inference inside MQL5 after offline validation.
8. A hard deterministic risk authority above model confidence.
9. Replayable ledgers and fixture-driven testing.
10. No large external UI before the first complete loop closes.

## Main Architectural Corrections

### Event Bus

A fully generic event bus is useful for audit, replay and low-frequency notifications, but it should not become the only control-flow mechanism. Hidden event routing can make latency, ownership and failure propagation difficult to reason about. Therefore the fast path uses direct typed method calls through ports. A bounded typed bus records important lifecycle events asynchronously.

### Strategy Host

The Host is accepted only as a thin composition root. It must not contain strategy selection switches that grow into a monolith. The current phase binds null adapters. Later a static plugin registry will bind one selected anatomy plugin. Multi-strategy portfolio hosting is deferred until single-strategy parity is proven.

### Python Scope

Python remains essential, but it does not recreate market anatomy, candidate geometry or execution transitions. It receives canonical MQL5 artifacts and performs advanced statistics, anti-overfit tests, model training and reporting.

### Runtime Configuration

The runtime does not parse arbitrary JSON or dynamically discover code on every decision. Configuration is validated at startup and compiled into a runtime generation. The hot path is allocation-light and deterministic.
