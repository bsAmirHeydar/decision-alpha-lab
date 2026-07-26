---
title: Submit to Hidden Evaluation
status: canonical
version: 3.0.0
created: '2026-07-13'
updated: '2026-07-13'
capability_tier: canonical
tags:
  - saed-v3
  - runbook
  - operations
---

# Mission

Score a frozen candidate in a sealed service with minimal disclosure and query-budget control.

## Entry conditions

- Signed candidate bundle.
- Remaining query/FDR budget.
- Predeclared scorecard.

## Mandatory roles and separation of duties

- Research owner.
- Hidden evaluation custodian.
- Independent statistician.

## Procedure

1. Validate bundle completeness and signatures.
2. Check near-duplicate history.
3. Run isolated evaluation.
4. Compute predeclared metrics and uncertainty.
5. Return bounded scorecard.
6. Record exposure and budget spend.

## Mandatory outputs

- Submission receipt.
- Signed hidden scorecard.
- Exposure/budget event.

## Stop and escalation conditions

- Budget exhausted.
- Partial/mismatched bundle.
- Adaptive duplicate.
- Evaluation environment anomaly.

## Evidence retained

- Submission hash.
- Environment hash.
- Sealed detailed results.

## Completion gate

The runbook is complete only when all required artifacts are content-addressed, all exposures and deviations are recorded, an independent reviewer signs the completion state, and the downstream UCEE gate accepts the exact immutable bundle rather than a narrative summary.

## Related notes

- [[Hidden_Evaluation_Service_Architecture]]
- [[Blinded_Submission_Protocol]]
