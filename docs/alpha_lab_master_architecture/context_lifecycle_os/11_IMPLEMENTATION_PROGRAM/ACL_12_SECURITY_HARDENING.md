---
title: ACL-12 — Security Hardening
status: dependency-contract
version: 2.0.0
updated: 2026-07-18
tags: [acl-os, acl-12, security]
---
# ACL-12 — Security Hardening

ACL-12 consumes `ACL11_TO_ACL12` and hardens identity, signature verification, key custody interfaces, supply-chain controls, trusted-computing-base constraints, revocation, incident handling and operator separation.

## Required actions

- `VERIFY_RUNTIME_CUSTODY_PACKAGE`
- `HARDEN_SECURITY_BOUNDARIES`
- `ISSUE_SECURITY_READINESS_DECISION`

## Forbidden actions

- invent a runtime candidate;
- bypass runtime parity or signing gates;
- access production key material in reference mode;
- authorize live orders;
- activate capital.

The ACL-11 reference package is non-executable and contains zero runtime candidates. Security hardening must preserve that fact.
