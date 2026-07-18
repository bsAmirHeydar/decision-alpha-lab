---
title: Acl12 Migration And Rollback
status: accepted-reference
version: 1.0.0
updated: 2026-07-18
tags: [acl-os, acl-12, security]
---
# Acl12 Migration And Rollback

## Purpose

Defines versioned migration and rollback for future security-control changes.

## Authority boundary

This contract may assess, classify and preserve evidence. It may not access production signing keys, manufacture runtime candidates, activate a runtime, submit orders or authorize capital.

## Inputs

- immutable `ACL11_TO_ACL12` handoff;
- exact ACL-11 manifest, receipt and digest-bound artifacts;
- ACL-12 authority permit;
- closed control and threat registries.

## Invariants

- UNKNOWN blocks production readiness;
- reference evidence is not production attestation;
- zero runtime candidates remains zero;
- no key material is written to the repository or generated package;
- every result has reason codes and immutable lineage.

## Failure semantics

Integrity mismatch, unregistered control, authority escalation, scan finding, unresolved path, symlink, forged digest or publication conflict fails closed.

## Evidence

Machine contracts live under `registry/acl_os/acl_12`. Reference evidence lives under `lab/11_strategy_factory/acl_os/fixtures/acl_12/reference_security_hardening`.

## Related

- [[ACL12_SECURITY_HARDENING_RUNTIME]]
- [[ACL12_SECURITY_READINESS_DECISION]]
- [[ACL12_ACL13_HANDOFF]]
