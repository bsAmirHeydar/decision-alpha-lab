---
title: "ADR-001 — One Reducer for All Replay Modes"
tags: [exp0019, faerie-protocol, fp-i13, indicator-release, obsidian]
status: implemented
experiment: EXP0019
context_id: FP-CONTEXT-001
phase_id: FP-I13
phase_version: 1.0.0
last_updated: 2026-07-13
language: en
---
# ADR-001 — One Reducer for All Replay Modes

## Decision

Full, incremental, and restart modes use one reducer to prevent test-only semantic branches.

## Consequences

The decision is versioned in FP-I13, covered by tests, and included in the handoff to FP-I14. Any reversal requires a new ADR and replay rebaseline.
