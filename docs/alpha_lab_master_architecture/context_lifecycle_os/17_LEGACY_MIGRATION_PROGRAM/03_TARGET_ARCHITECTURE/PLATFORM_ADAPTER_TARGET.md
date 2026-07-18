---
title: "Platform Adapter Target"
status: proposed-reference
version: 1.0.0
updated: 2026-07-18
tags: [acl-os, lcm, legacy-migration]
---
# Platform Adapter Target

Adapters translate platform data and lifecycle events into canonical contracts. They validate CopyRates, CopyBuffer, history synchronization, array direction, symbol selection and time mapping. They fail closed on incomplete data and never invent a domain default.

Legacy wrappers live under Compatibility and forward to canonical implementations while preserving public include paths during dual run.
