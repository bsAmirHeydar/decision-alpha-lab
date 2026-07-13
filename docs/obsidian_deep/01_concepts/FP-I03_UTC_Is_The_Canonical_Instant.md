---
title: "FP-I03 UTC Is The Canonical Instant"
tags: [exp0019, faerie-protocol, fp-i03, time-calendar, obsidian]
status: normative
phase: FP-I03
phase_version: 1.0.0
doc_version: 1.0.0
last_updated: 2026-07-13
language: en
---
# FP-I03 UTC Is The Canonical Instant

## Definition

Every semantic time fact begins as a UTC instant. New York and broker values are projections, preventing server or chart timezone drift.

## Operational rule

- Preserve the exact FP-I03 configuration and registry hash.
- Use UTC before constructing New York ownership.
- Test the boundary and failure path.
- Carry the resulting IDs into FP-I04 and later evidence.

## Why it matters

A one-second or one-offset disagreement can change reference windows, hunt ordering, confirmation deadlines, WW context, quota ownership, drawing, and execution. Time semantics therefore belong to the stable core, not product projection.

## Related

- [[../../execution/EXP0019_faerie_protocol_contextual_divergence/implementation_program/phase_deliveries/fp_i03/00_FP_I03_DELIVERY_MOC|FP-I03 Delivery MOC]]
