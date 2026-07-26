---
title: "ADR-004 — Checkpoint Is a Cache"
tags: [exp0019, faerie-protocol, fp-i13, indicator-release, obsidian]
status: implemented
experiment: EXP0019
context_id: FP-CONTEXT-001
phase_id: FP-I13
phase_version: 1.0.0
last_updated: 2026-07-13
language: en
---
# ADR-004 — Checkpoint Is a Cache

## Decision

Invalid checkpoints are rejected and rebuilt from accepted evidence.

## Consequences

The decision is versioned in FP-I13, covered by tests, and included in the handoff to FP-I14. Any reversal requires a new ADR and replay rebaseline.
