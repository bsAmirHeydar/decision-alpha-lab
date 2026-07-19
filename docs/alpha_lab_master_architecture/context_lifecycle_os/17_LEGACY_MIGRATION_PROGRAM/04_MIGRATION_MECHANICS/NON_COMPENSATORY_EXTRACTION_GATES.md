---
title: "Non Compensatory Extraction Gates"
status: implemented-reference
version: 1.0.0
updated: 2026-07-19
tags: [acl-os, lcm, lcm-07, shared-engine]
phase_id: LCM-07
---
# Non Compensatory Extraction Gates

Every extraction gate is mandatory; UNKNOWN and BLOCKED are not compensable by other evidence.

## Invariants

- source bytes and behavior remain unchanged;
- UNKNOWN remains blocking;
- static equality is not runtime parity;
- target paths remain proposals;
- execution, live-order and capital authority remain false.
