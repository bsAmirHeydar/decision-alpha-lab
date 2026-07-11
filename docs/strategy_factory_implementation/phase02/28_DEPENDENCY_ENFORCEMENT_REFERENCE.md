---
title: "Dependency Enforcement Reference"
---

# Dependency Enforcement Reference

The dependency guard scans MQL5 includes and live-authority tokens.

## Layer Rules

```text
Contracts → Contracts only
Core → Contracts + Core
Ports → Contracts + Core + Ports
Runtime → Contracts + Core + Ports + Runtime
Adapters → Contracts + Core + Ports + Adapters
Testing → all non-live Phase 02 layers
```

## Why Runtime Does Not Import Adapters

Runtime depends on interfaces. The Host or a later composition factory binds concrete adapters. This preserves replacement, fixture testing and no-send operation.

## Why Core Does Not Import Ports

Core types such as state, config and event envelopes are reusable and do not need service interfaces. This avoids circular dependencies.

## Enforcement Limits

The static scanner is an engineering guard, not a full compiler. MetaEditor remains authoritative for MQL5 syntax. The scanner complements, rather than replaces, compile and fixture tests.
