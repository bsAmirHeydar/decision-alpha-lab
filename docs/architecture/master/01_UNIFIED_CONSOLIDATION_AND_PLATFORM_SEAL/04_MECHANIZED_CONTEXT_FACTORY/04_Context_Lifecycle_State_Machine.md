---
id: UCPS-49E7CCAB55E2
title: "Context Lifecycle State Machine"
type: architecture
status: canonical
domain: unified-consolidation-platform-seal
version: 1.0.0
created: 2026-07-23
updated: 2026-07-23
tags:
  - consolidation
  - platform-seal
---
# Context Lifecycle State Machine

## Canonical states

```text
DRAFT
→ VALIDATED
→ COMPILED
→ REPLAY_VERIFIED
→ DATA_READY
→ MATERIALIZED
→ RESEARCH_READY
→ TRAINED
→ EVIDENCE_COMPLETE
→ PAPER_ELIGIBLE
→ SHADOW_ELIGIBLE
→ CAPITAL_REVIEW
→ RUNTIME_ELIGIBLE
```

## Transition authority

A transition occurs only through a command that validates required evidence and writes a reason-coded event. Folder presence, a green local test or an AI statement cannot change state.

## Regressions

Contract changes, data revisions, failed monitoring assumptions or reproducibility loss may move an artifact backward, quarantine it or create a new version. Previous evidence remains immutable.

## Abstention

The system supports `NO_TRADE`, `NO_MODEL`, `NO_PROMOTION` and `INSUFFICIENT_EVIDENCE` outcomes as first-class results.

## Explainability

For every blocked transition the status service reports current state, missing evidence, failing policy, relevant artifacts and allowed next commands.
