---
title: "Keep the Runtime Registry in MQL5"
status: accepted
phase: 04
---

# Keep the Runtime Registry in MQL5

## Context

The Strategy Factory must accept many future anatomy engines without allowing dynamic ambiguity, duplicate infrastructure or live authority drift.

## Decision

Python mirrors descriptors and validators for research and CI but does not own live plugin selection.

## Consequences

- Reproducible startup and replay.
- More explicit registration work for each new plugin.
- Faster failure discovery.
- Smaller and more deterministic live path.
- Legacy systems must be wrapped rather than copied into the core.

## Revisit trigger

Revisit only if MetaTrader gains a safe, deterministic and testable native plugin-loading mechanism that preserves exact version and authority guarantees.
