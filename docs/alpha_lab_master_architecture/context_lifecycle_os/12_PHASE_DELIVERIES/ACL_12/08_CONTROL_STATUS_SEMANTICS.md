---
title: ACL-12 Delivery — Control Status Semantics
status: accepted-reference
version: 1.0.0
updated: 2026-07-18
tags: [acl-os, acl-12, phase-delivery]
---
# Control Status Semantics

## Contract

This delivery unit belongs to ACL-12 Security Hardening. It is versioned, digest-bound, root-relative and non-production.

## Required behavior

- consume only verified ACL-11 evidence;
- preserve zero runtime candidates and zero key material;
- use registered controls, threats, reason codes and statuses;
- fail closed on UNKNOWN where production readiness is concerned;
- emit immutable machine evidence and an Obsidian projection.

## Acceptance

The unit is accepted only when direct tests, ACL-11 regression, static validation, deterministic replay, clean overlay validation and manifest verification pass.

## Non-claims

No production security attestation, runtime activation, broker safety, live order permission or capital authorization is implied.

## Related

- [[ACL12_SECURITY_HARDENING_RUNTIME]]
- [[ACL12_DEFINITION_OF_DONE]]
