---
title: "Require Declarative Market Resources"
status: accepted
phase: 04
---

# Require Declarative Market Resources

## Context

The Strategy Factory must accept many future anatomy engines without allowing dynamic ambiguity, duplicate infrastructure or live authority drift.

## Decision

Every plugin declares symbols, timeframes, lookback, staleness and synchronization before startup.

## Consequences

- Reproducible startup and replay.
- More explicit registration work for each new plugin.
- Faster failure discovery.
- Smaller and more deterministic live path.
- Legacy systems must be wrapped rather than copied into the core.

## Revisit trigger

Revisit only if MetaTrader gains a safe, deterministic and testable native plugin-loading mechanism that preserves exact version and authority guarantees.
