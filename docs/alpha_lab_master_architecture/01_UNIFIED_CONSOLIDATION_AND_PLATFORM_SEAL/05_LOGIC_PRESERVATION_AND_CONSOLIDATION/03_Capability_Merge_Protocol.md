---
id: UCPS-4414564867E6
title: "Capability Merge Protocol"
type: workflow
status: canonical
domain: unified-consolidation-platform-seal
version: 1.0.0
created: 2026-07-23
updated: 2026-07-23
tags:
  - consolidation
  - platform-seal
---
# Capability Merge Protocol

## Protocol

1. Define the capability and semantic boundary.
2. Enumerate all implementations and consumers.
3. Select the canonical implementation using evidence.
4. Port behavior missing from the canonical implementation.
5. Represent valid semantic differences as named strategies or policies.
6. Add characterization, differential and property tests.
7. Rewrite consumers to the public canonical interface.
8. Run dual execution only when it produces meaningful parity evidence.
9. Retire compatibility paths after telemetry reaches zero.
10. Issue a logic-preservation certificate and remove the duplicate.

## Selection criteria

Correctness, known-time safety, contract clarity, deterministic behavior, testability, operational maturity, performance, security and maintenance cost. File age or phase number is not sufficient.

## Prohibition

Copying all old implementations into one new directory is not consolidation. Wrapping duplicates behind a facade without retirement criteria is not consolidation.
