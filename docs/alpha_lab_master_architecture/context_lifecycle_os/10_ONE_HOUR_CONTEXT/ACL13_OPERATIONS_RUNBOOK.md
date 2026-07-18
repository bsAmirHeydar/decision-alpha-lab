---
title: ACL-13 Operations Runbook
status: accepted-reference
version: 2.0.0
updated: 2026-07-18
tags: [acl-os, acl-13, one-hour-assessment]
---
# ACL-13 Operations Runbook

## Purpose

Provides build, verify, replay and failure-recovery procedures.

## Responsibility boundary

This contract owns bounded research triage only. It does not validate alpha, authorize a real pilot, generate runtime code, submit orders or activate capital.

## Required inputs

- exact `ACL12_TO_ACL13` handoff and immutable ACL-12 package;
- action-bound ACL-13 authority permit;
- exact Context identity, version and owners;
- explicit doctrine summary without invented market semantics;
- known-time-safe observation slice or explicit UNKNOWN;
- predeclared bounded setup families;
- frozen one-hour budget profile.

## Invariants

- ACL-12 production-not-ready status is preserved;
- zero runtime candidates remains zero;
- synthetic evidence is visibly classified and cannot become real evidence;
- deterministic baselines replace unstable randomness;
- triage evidence never becomes validation or capital authority;
- generated projections are not sources of truth.

## Failure behavior

Integrity mismatch, unknown identity, future-data leakage, budget breach, unregistered family, path escape, destination conflict or authority escalation stops publication.

## Evidence and verification

Machine contracts live under `registry/acl_os/acl_13`; reference tests and replay fixtures live under `lab/11_strategy_factory/acl_os`. The phase requires deterministic replay, schema validation, security-negative tests and clean-overlay delivery validation.

## Claim ceiling

`RESEARCH_TRIAGE_REFERENCE_ONLY`

## Related

- [[ACL_13_ONE_HOUR_ASSESSMENT_PRODUCT]]
- [[ACL13_ACL14_HANDOFF]]
- [[ADR_011_ONE_HOUR_ASSESSMENT_IS_TRIAGE]]
