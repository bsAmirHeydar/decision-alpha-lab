---
id: UCPS-A030B010C1C5
title: "One CLI, Operator UI and Explainability"
type: interface
status: canonical
domain: unified-consolidation-platform-seal
version: 1.0.0
created: 2026-07-23
updated: 2026-07-23
tags:
  - consolidation
  - platform-seal
---
# One CLI, Operator UI and Explainability

## CLI surface

```text
alpha context create
alpha context validate
alpha context compile
alpha context acquire
alpha context materialize
alpha context train
alpha context discover
alpha context evaluate
alpha context paper
alpha context status
alpha context explain
alpha context resume
alpha verify repository
```

## Design rules

- commands are stable and versioned;
- every command supports machine-readable output;
- destructive actions require explicit scope and dry-run;
- resumable work has run identity and checkpoint semantics;
- errors use reason codes rather than only stack traces;
- environment and configuration are explicit.

## Operator UI

A lightweight UI consumes the same APIs and presents Context Builder, validation errors, lifecycle status, run history, evidence, blocked reasons and next action. It contains no independent business logic.

## Lowering expertise requirements

Ordinary users select approved options and provide market semantics. Advanced programming is required only for new extension behavior, not for normal Context lifecycle operation.
