---
title: "Use a Static Exact-Version Registry"
status: accepted
phase: 04
---

# Use a Static Exact-Version Registry

## Context

The Strategy Factory must accept many future anatomy engines without allowing dynamic ambiguity, duplicate infrastructure or live authority drift.

## Decision

Runtime discovery and latest-version selection are rejected. Factories are registered in source and resolved by exact plugin ID and exact semantic version.

## Consequences

- Reproducible startup and replay.
- More explicit registration work for each new plugin.
- Faster failure discovery.
- Smaller and more deterministic live path.
- Legacy systems must be wrapped rather than copied into the core.

## Revisit trigger

Revisit only if MetaTrader gains a safe, deterministic and testable native plugin-loading mechanism that preserves exact version and authority guarantees.
