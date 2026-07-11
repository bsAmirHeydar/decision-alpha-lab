---
title: "Late Frames Are Drained"
status: accepted
phase: 10
---
# Late Frames Are Drained

## Decision

OnTesterDeinit performs a final FrameNext drain to avoid losing delayed optimization frames.

## Consequences

The rule is enforced by the MQL5 research harness, schemas, tests and operating runbook. Any exception requires a new ADR and a versioned contract change.
