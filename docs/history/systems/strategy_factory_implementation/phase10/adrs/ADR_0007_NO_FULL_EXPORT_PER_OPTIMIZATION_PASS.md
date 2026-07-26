---
title: "No Full Export Per Optimization Pass"
status: accepted
phase: 10
---
# No Full Export Per Optimization Pass

## Decision

Full pass exports are prohibited during broad optimization to preserve performance and cloud compatibility.

## Consequences

The rule is enforced by the MQL5 research harness, schemas, tests and operating runbook. Any exception requires a new ADR and a versioned contract change.
