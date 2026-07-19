---
title: "Shared Engine Discovery Architecture"
status: implemented-reference
version: 1.0.0
updated: 2026-07-19
tags: [acl-os, lcm, lcm-07, shared-engine]
phase_id: LCM-07
---
# Shared Engine Discovery Architecture

Deterministic function-level discovery over non-protected MQL assets, bound to source hashes and LCM-06 authority.

## Invariants

- source bytes and behavior remain unchanged;
- UNKNOWN remains blocking;
- static equality is not runtime parity;
- target paths remain proposals;
- execution, live-order and capital authority remain false.
