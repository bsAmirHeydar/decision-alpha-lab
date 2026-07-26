---
title: "Prove the SDK with a Fixture Before Migration"
status: accepted
phase: 04
---

# Prove the SDK with a Fixture Before Migration

## Context

The Strategy Factory must accept many future anatomy engines without allowing dynamic ambiguity, duplicate infrastructure or live authority drift.

## Decision

A deterministic synthetic anatomy validates the platform before any old strategy is integrated.

## Consequences

- Reproducible startup and replay.
- More explicit registration work for each new plugin.
- Faster failure discovery.
- Smaller and more deterministic live path.
- Legacy systems must be wrapped rather than copied into the core.

## Revisit trigger

Revisit only if MetaTrader gains a safe, deterministic and testable native plugin-loading mechanism that preserves exact version and authority guarantees.
