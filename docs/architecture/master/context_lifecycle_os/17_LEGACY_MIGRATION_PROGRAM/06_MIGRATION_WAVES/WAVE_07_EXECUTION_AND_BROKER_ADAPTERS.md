---
title: "Wave 07 — Execution and Broker Adapters"
status: proposed-reference
version: 1.0.0
updated: 2026-07-18
tags: [acl-os, lcm, legacy-migration]
---
# Wave 07 — Execution and Broker Adapters

Migrate E0001–E0011, CG/STC execution, Astro order shell and other broker-capable modules last. Context and Setup consumers must already be canonical. Order adapters are capability-gated, dry-run by default and reviewed for spread, volume, stop distance, session, duplicate-decision, reconciliation, kill switch and rollback behavior.
