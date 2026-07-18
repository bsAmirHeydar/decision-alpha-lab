---
title: ACL-13 — One-Hour Assessment Product
status: dependency-contract
version: 2.0.0
updated: 2026-07-18
tags: [acl-os, acl-13, assessment-product]
---
# ACL-13 — One-Hour Assessment Product

ACL-13 consumes `ACL12_TO_ACL13` and constructs a bounded one-hour assessment product from immutable architecture, security-readiness and evidence contracts.

## Required actions

- `VERIFY_SECURITY_READINESS_PACKAGE`
- `BUILD_ONE_HOUR_ASSESSMENT_PRODUCT`
- `ISSUE_NON_CAPITAL_ASSESSMENT_RESULT`

## Forbidden actions

- invent production security evidence;
- access production signing keys;
- authorize runtime activation or live orders;
- activate capital;
- reinterpret `REFERENCE_SECURITY_HARDENED_PRODUCTION_NOT_READY` as production readiness.

The ACL-12 reference package is non-production and contains zero runtime candidates. ACL-13 must preserve those facts.
