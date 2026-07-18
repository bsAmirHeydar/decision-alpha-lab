---
title: ACL-11 — Runtime Parity and Handoff
status: proposed-reference
version: 2.0.0
updated: 2026-07-18
tags: [acl-os, acl-11, runtime]
---
# ACL-11 — Runtime Parity and Handoff

ACL-11 consumes `ACL10_TO_ACL11`, verifies the complete promotion-state package and evaluates runtime-parity prerequisites without generating runtime artifacts for ineligible subjects.

## ACL-10 dependency contract

Required actions:
- `VERIFY_PROMOTION_STATE_PACKAGE`
- `ASSESS_RUNTIME_PARITY_PREREQUISITES`
- `ISSUE_NON_EXECUTABLE_RUNTIME_CUSTODY_DECISION`

Forbidden actions:
- generate runtime for an ineligible subject;
- mutate ACL-10 state decisions;
- bypass parity, signing or custody gates;
- authorize live orders;
- activate capital.

The ACL-10 reference fixture contains zero runtime candidates. ACL-11 must therefore prove the no-runtime-handoff path.
