---
title: "Lcm07 Reference Fixture Strategy"
status: implemented-reference
version: 1.0.0
updated: 2026-07-19
tags: [acl-os, lcm, lcm-07, shared-engine]
phase_id: LCM-07
---
# Lcm07 Reference Fixture Strategy

Metamorphic fixtures test static-normalization behavior while explicitly denying runtime-parity claims.

## Invariants

- source bytes and behavior remain unchanged;
- UNKNOWN remains blocking;
- static equality is not runtime parity;
- target paths remain proposals;
- execution, live-order and capital authority remain false.
