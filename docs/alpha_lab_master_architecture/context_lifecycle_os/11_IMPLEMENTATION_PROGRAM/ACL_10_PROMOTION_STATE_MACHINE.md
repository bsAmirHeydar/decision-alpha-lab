---
title: ACL-10 — Promotion State Machine
status: proposed-reference
version: 2.0.0
updated: 2026-07-18
tags: [acl-os, acl-10, promotion]
---
# ACL-10 — Promotion State Machine

ACL-10 consumes `ACL09_TO_ACL10`, verifies the complete memory/planner package and evaluates promotion prerequisites without inferring eligibility from planner priority or memory admission.

## ACL-09 dependency contract

Required actions:
- `VERIFY_MEMORY_AND_PLANNER_PACKAGE`
- `EVALUATE_PROMOTION_PREREQUISITES`
- `ISSUE_NON_PROMOTIONAL_STATE_DECISION`

Forbidden actions:
- execute a research proposal;
- mutate memory history;
- promote without validated and policy-approved evidence;
- authorize execution or activate capital.

The ACL-09 reference fixture contains zero reporting-eligible candidates. ACL-10 must therefore demonstrate the non-promotional path of its state machine.
