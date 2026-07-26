---
title: "UCE-I18 — Micro-live is explicitly bounded"
tags: [strategy-factory, uce-i18, production-qualification, atomic-concept]
status: implemented_reference_external_evidence_pending
doc_version: 1.0.0
last_updated: 2026-07-15
---
# Micro-live is explicitly bounded

## Normative decision

Micro-live requires human approval, expiry, risk cap, broker/account identity, rollback generation and automatic kill conditions.

## Invariant

The gate is fail-closed, identity-relevant, replayable and independently auditable. Missing evidence is `pending`; contradictory or unsafe evidence is `fail`; neither state grants execution authority.

## Required evidence

- source and environment identity;
- event and availability time;
- machine-readable result and reason code;
- immutable hashes for inputs, outputs and logs;
- owner, expiry and rollback reference.

## Negative test

Remove or corrupt the evidence, reorder the event stream, change the environment fingerprint, or exceed the hard budget. Qualification must become blocked without changing any market or treatment semantics.

## Related

- [[00_UCE_I18_DELIVERY_MOC|UCE-I18 Delivery MOC]]
- [[43_ACCEPTANCE_EVIDENCE_MATRIX|Acceptance Evidence Matrix]]
- [[47_LIMITATIONS_RESIDUAL_RISK_AND_POST_I18_HANDOFF|Limitations and Handoff]]
