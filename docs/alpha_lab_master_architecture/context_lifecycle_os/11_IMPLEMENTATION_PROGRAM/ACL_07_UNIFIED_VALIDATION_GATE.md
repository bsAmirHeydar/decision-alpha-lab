---
title: ACL-07 — Unified Validation Gate
status: proposed-reference
version: 1.0.0
updated: 2026-07-18
tags: [acl-os, acl-06]
---
# ACL-07 — Unified Validation Gate

## Accepted ACL-06 dependency contract

ACL-07 starts only from a byte-valid `ACL06_TO_ACL07` handoff. It must resolve the exact research run, DAG, result bundle, task receipt set, resource accounting, run object index, event ledger and provenance graph. Every candidate result remains descriptive and `NOT_VALIDATED` until ACL-07 applies the full validation battery.

ACL-07 may verify research evidence, apply unified validation gates and issue a non-promotional validation decision. It may not mutate the frozen Batch, rewrite research results, promote the diagnostic lane, infer alpha without gates, authorize execution or activate capital.

## Minimum intake checks

- exact ACL-06 output manifest and receipt;
- complete successful task receipt set;
- resource usage within the ACL-05 frozen budget;
- candidate and segment lineage to the frozen Batch;
- diagnostic-lane non-selectability;
- known-time and split evidence;
- event-chain and provenance completeness;
- no order or capital authority.

## Required ACL-07 outputs

ACL-07 must produce gate-level reason codes, support/effect evidence, leakage and data-quality results, overfit controls, distributional and temporal robustness evidence, multiple-testing controls and a decision that remains separate from execution authority.

## Claim ceiling

Receiving a completed research run does not establish alpha or promotion eligibility.

## Related

[[ACL_06_RESEARCH_DAG_ORCHESTRATION]], [[UNIFIED_STATISTICAL_GATE]], [[PROMOTION_DECISION_POLICY]]
