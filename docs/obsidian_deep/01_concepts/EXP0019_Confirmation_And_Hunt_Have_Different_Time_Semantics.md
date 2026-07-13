---
title: "EXP0019 Confirmation And Hunt Have Different Time Semantics"
tags: [atomic-concept, exp0019, faerie-protocol]
status: canonical
experiment: EXP0019
context_id: FP-CONTEXT-001
doc_version: 1.0.0
last_updated: 2026-07-13
---
# EXP0019 Confirmation And Hunt Have Different Time Semantics

## Definition

Hunt با high/low intrabar رخ می‌دهد، اما validity فقط در closed-candle boundary تعیین می‌شود.

## Consequence

- در contract به‌صورت explicit field/enum ثبت شود.
- در identity و test coverage منعکس شود.
- failure آن به‌عنوان reason-coded evidence باقی بماند.

## Links

- [[docs/execution/EXP0019_faerie_protocol_contextual_divergence/00_EXP0019_MOC]]
