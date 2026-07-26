---
title: "Service Composition Reference"
---

# Service Composition Reference

## Phase 02 Composition

```text
Terminal Clock
Null Anatomy Provider
Null Feature Provider
Print Result Sink
No-Send Execution Boundary
        ↓
CSF02StrategyRuntime
        ↓
SF02_StrategyHost
```

This composition proves startup, lifecycle and authority boundaries without pretending a strategy is integrated.

## Test Composition

```text
Fixture Clock
Fixture Anatomy Provider
Fixture Feature Provider
Fixture Sink
No-Send Boundary
        ↓
Runtime Self-Test
```

One deterministic tick emits one event and one feature snapshot.

## Future Production Composition

After Phase 03 and Phase 04:

```text
Shared Time Kernel
Shared Market Cache
Shared Symbol Specs
Selected Anatomy Adapter
Registered Feature Providers
Versioned Result Sink
No-Send or Paper Execution Adapter
        ↓
Compiled Runtime Generation
```

The Host should not know the concrete type of the selected strategy. A composition factory or static registry will construct the service graph during startup.
