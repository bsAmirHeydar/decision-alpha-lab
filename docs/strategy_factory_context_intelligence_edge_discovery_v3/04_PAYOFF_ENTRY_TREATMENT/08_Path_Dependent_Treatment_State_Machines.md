---
title: Path-Dependent Treatment State Machines
status: canonical
version: 3.0.0
created: '2026-07-13'
updated: '2026-07-13'
tags:
- saed-v3
- gap-closure
- canonical
---

# Scope

Formalize trail, partial, break-even, re-entry, time-stop and context-invalidated exits as deterministic event-sourced state machines.

# Canonical states

`candidate → armed → triggered → partially_filled → active → protected → trailing → partially_exited → closed | cancelled | expired | invalidated`

# Requirements

- Transition guards are known-time safe.
- Event ordering and intrabar ambiguity policy are explicit.
- Trail reference, activation, ratchet, giveback and gap behavior are versioned.
- Restart reconstructs the same state from the event ledger.
- A state machine cannot widen risk beyond hard authorization.

# Path labels

Capture activation time, high/low sequence, MFE/MAE path, pullback depths, trail moves, giveback, premature exit, re-entry eligibility and captured-tail ratio.

# Tests

Golden paths, same-bar stop/target ambiguity, gaps, partial fills, delayed quotes, duplicate events, restart and future-suffix mutation.
