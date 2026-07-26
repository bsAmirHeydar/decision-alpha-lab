---
title: Acl14 Real Data Source Contract
status: accepted-reference
version: 1.0.0
updated: 2026-07-18
tags: [acl-os, acl-14, first-real-context-pilot]
---
# Acl14 Real Data Source Contract

## Purpose

Defines source ownership, data reality classification, schema, timezone and source digest requirements.

## Responsibility boundary

ACL-14 authors and assesses a precommitted non-capital pilot contract. It does not treat design artifacts as prospective evidence, execute the pilot, validate alpha, generate runtime code, connect to a broker, submit orders or activate capital.

## Required evidence

Exact ACL-13 identity and digests, approved Context identity, independent owners, doctrine, real-data classification, versioned mapping, known-time availability semantics, precommitted period, frozen evaluation rules, frozen setup families, support targets, stop/failure conditions and the non-capital boundary.

## Invariants

- UNKNOWN mandatory evidence blocks readiness.
- Reference or synthetic evidence cannot be relabeled as real.
- Post-outcome rule or search-space changes require a new pilot version.
- Every decision is deterministic, reason-coded and replayable.
- Generated projections are not the source of truth.

## Failure behavior

Integrity, identity, approval, future-data, search expansion, operator conflict, security or authority failures stop publication or produce an explicit non-ready decision. No permissive default is used.

## Claim ceiling

`FIRST_REAL_CONTEXT_PILOT_REFERENCE_ONLY`

## Related

- [[ACL14_FIRST_REAL_CONTEXT_PILOT_RUNTIME]]
- [[ACL14_READINESS_GATE_REGISTRY]]
- [[ACL14_ACL15_HANDOFF]]
