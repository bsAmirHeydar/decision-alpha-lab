---
title: ACL-10 — Promotion State Machine
status: accepted-reference
version: 3.0.0
updated: 2026-07-18
tags: [acl-os, acl-10, promotion]
---
# ACL-10 — Promotion State Machine

ACL-10 consumes `ACL09_TO_ACL10`, verifies the complete memory and planner package, evaluates a closed prerequisite matrix, and issues deterministic non-executing promotion-state decisions.

## Reference result

The ACL-09 fixture contains zero reporting-eligible candidates. ACL-10 therefore produces four baseline-reference states, one diagnostic-quarantine state and seven research-hold states. It creates no approval request, executes no transition, and emits an empty runtime-candidate manifest.

## Required controls

- closed state, transition and prerequisite registries;
- explicit SATISFIED, UNSATISFIED, UNKNOWN and NOT_APPLICABLE semantics;
- UNKNOWN blocks promotion;
- baseline and diagnostic isolation;
- two-person human approval boundary and self-approval prohibition;
- append-only transition, dissent, revocation and retirement records;
- atomic publication, event ledger and provenance;
- explicit ACL-11 handoff without runtime authority.

## Claim ceiling

`PROMOTION_STATE_DECISION_REFERENCE_ONLY`
