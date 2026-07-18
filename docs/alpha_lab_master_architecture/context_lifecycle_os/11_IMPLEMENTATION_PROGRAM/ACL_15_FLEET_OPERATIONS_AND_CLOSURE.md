---
title: ACL-15 — Fleet Operations and Closure
status: dependency-contract
version: 2.0.0
updated: 2026-07-18
tags: [acl-os, acl-15, fleet-operations, closure]
---
# ACL-15 — Fleet Operations and Closure

ACL-15 consumes `ACL14_TO_ACL15` and closes the reference lifecycle with governed fleet registration, package status, surveillance/retention contracts and explicit non-capital closure.

## Required actions

- `VERIFY_FIRST_REAL_CONTEXT_PILOT_PACKAGE`
- `REGISTER_FLEET_OPERATIONS_CONTRACT`
- `ISSUE_NON_CAPITAL_CLOSURE_DECISION`

## Mandatory behavior

- preserve the exact ACL-14 readiness and execution state;
- distinguish authored pilot design from observed prospective evidence;
- register lifecycle ownership, retention, surveillance and closure status;
- preserve failures, UNKNOWNs and unexecuted states;
- expose only policy-approved reopen or migration actions.

## Forbidden actions

- invent pilot outcomes;
- treat a reference contract as real prospective evidence;
- bypass ACL-07 validation or ACL-10 promotion;
- generate or activate runtime;
- authorize live orders or capital.

## Claim ceiling

Only environment-specific evidence can establish real pilot completion, validation, runtime parity, production security, broker behavior or capital authorization.
