---
title: "Phase 02 MQL5 API Reference"
---

# Phase 02 MQL5 API Reference

## Runtime Configuration

`SF02_RuntimeConfig` is the immutable startup description of one Host generation. It identifies the strategy, strategy version, run, runtime generation, run mode, strictness, timer cadence, event-drain budget and audit-bus policy.

### Required Fields

| Field | Meaning | Validation |
|---|---|---|
| `strategy_id` | Stable strategy identity | ASCII safe identifier |
| `strategy_version` | Canon or implementation version | ASCII safe identifier |
| `run_id` | One reproducible run identity | ASCII safe identifier |
| `generation_id` | Runtime generation | Positive integer |
| `run_mode` | Operational mode | Enumerated |
| `strict_fail_closed` | Whether invalid downstream state fails the runtime | Boolean |
| `timer_period_ms` | Timer cadence | 10–60,000 ms |
| `max_events_per_cycle` | Bounded work budget | 1–10,000 |
| `audit_bus_capacity` | Fixed audit capacity | 8–1,000,000 |

The runtime configuration is validated once during initialization. Later phases may compile a richer manifest into this structure, but the fast path never parses configuration files.

## Runtime State Machine

`CSF02RuntimeStateMachine` exposes:

```cpp
ENUM_SF02_RUNTIME_STATE State() const;
ENUM_SF02_RUNTIME_STATE Previous() const;
long LastTransitionUtcMsc() const;
string Reason() const;
bool Transition(next, now_utc_msc, reason, error);
```

Every transition is explicit. A failed transition returns false and leaves the current state unchanged.

## Typed Event Bus

`CSF02TypedEventBus` provides:

```cpp
bool Initialize(capacity, overflow_policy, error);
bool Publish(event, error);
bool Poll(event);
int Count() const;
int Capacity() const;
long Dropped() const;
```

Published events receive sequence numbers inside the bus. Producers must not invent sequence identity.

## Runtime Orchestrator

`CSF02StrategyRuntime` is the central phase-owned class. It binds ports, validates startup, initializes services, drains events and builds snapshots.

### Binding

```cpp
runtime.BindClock(&clock);
runtime.BindAnatomy(&anatomy);
runtime.BindFeatures(&features);
runtime.BindSink(&sink);
runtime.BindExecutionBoundary(&no_send);
```

### Lifecycle

```cpp
runtime.Initialize(config, error);
runtime.Start(error);
runtime.OnTick(tick, error);
runtime.OnTimer(error);
runtime.Stop(error);
runtime.Shutdown();
```

### Diagnostics

```cpp
runtime.State();
runtime.ProcessedEvents();
runtime.RejectedEvents();
runtime.CreatedSnapshots();
runtime.DroppedAuditEvents();
runtime.LastError();
```

The runtime deliberately does not expose candidate, model, risk or broker methods in Phase 02.

## Port Contracts

### Clock Port

Provides UTC wall-clock and monotonic process timing. Phase 03 replaces the terminal-clock adapter with a full broker/UTC time kernel.

### Anatomy Provider

Receives ticks and timers, owns strategy-specific lifecycle, and emits canonical `SF01_AnatomyEvent` records through `PopEvent`.

### Feature Provider

Builds a causal `CSF01FeatureSnapshot` for one accepted anatomy event. It may not use information later than the snapshot time.

### Result Sink

Persists or displays accepted events and snapshots. Production sinks must become append-only and versioned in Phase 05.

### Execution Boundary

Exists now only to make authority explicit. The only Phase 02 implementation reports no live-order authority.
