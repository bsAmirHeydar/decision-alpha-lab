---
title: "Instances share semantics, not mutable state"
tags: [exp0019, faerie-protocol, fp-i13, indicator-release, obsidian]
status: implemented
experiment: EXP0019
context_id: FP-CONTEXT-001
phase_id: FP-I13
phase_version: 1.0.0
last_updated: 2026-07-13
language: en
---
# Instances share semantics, not mutable state

Concurrent charts may share semantic truth but never namespace, checkpoint, export, alert, or preference state.

This invariant is implemented by FP-I13 contracts, Python reference tests, MQL5 release modules, and acceptance evidence. It is normative for the FP-I14 differential-validation handoff.
