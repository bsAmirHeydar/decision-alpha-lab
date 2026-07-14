---
title: Service Boundaries and APIs
status: canonical
version: 4.0.0
created: '2026-07-13'
updated: '2026-07-13'
tags:
- saed-v4
- enterprise
---

# Thesis

Institutional scale requires explicit service contracts rather than shared in-process assumptions.

## Architectural design

### Core services

Context registry, event store, feature service, treatment compiler, outcome service, dataset registry, experiment orchestrator, model registry, evidence service, policy compiler.

### API style

Versioned schemas, idempotency keys, bounded payloads, deadlines, retry semantics, and typed errors.

### Consistency

Strong consistency for promotion and reservation state; eventual consistency only for non-authoritative analytics.

## Machine contracts

- `api_version`
- `request_id`
- `idempotency_key`
- `deadline`
- `artifact_reference`
- `error_code`

## Validation and evidence

- Contract tests across versions.
- Retry does not duplicate artifacts or decisions.
- Partial service outages fail closed for authority-bearing operations.

## Failure modes and mandatory response

- **Silent schema coercion:** Reject request.
- **Non-idempotent retry:** Critical operational defect.
- **Analytics cache used as authority:** Architecture violation.

## UCEE handoff

All outputs bind to exact upstream context, feature, data-role, treatment-universe, and economics hashes. Promotion and runtime authority remain in UCEE I12–I18.

## Related notes

- [[02_Master_System_Map]]
