---
title: "Keep Capital Authority Outside Anatomy Plugins"
status: accepted
phase: 04
---

# Keep Capital Authority Outside Anatomy Plugins

## Context

The Strategy Factory must accept many future anatomy engines without allowing dynamic ambiguity, duplicate infrastructure or live authority drift.

## Decision

Plugins can describe market events only. Candidate, model, risk and broker authority remain downstream.

## Consequences

- Reproducible startup and replay.
- More explicit registration work for each new plugin.
- Faster failure discovery.
- Smaller and more deterministic live path.
- Legacy systems must be wrapped rather than copied into the core.

## Revisit trigger

Revisit only if MetaTrader gains a safe, deterministic and testable native plugin-loading mechanism that preserves exact version and authority guarantees.
