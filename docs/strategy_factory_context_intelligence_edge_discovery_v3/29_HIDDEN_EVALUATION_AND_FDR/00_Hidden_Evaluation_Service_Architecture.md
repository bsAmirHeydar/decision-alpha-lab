---
title: Hidden Evaluation Service Architecture
status: canonical
version: 3.0.0
created: '2026-07-13'
updated: '2026-07-13'
capability_tier: core-production
tags:
  - saed-v3
---

# Mission

Provide a physically and logically separated evaluation service that scores frozen candidates without exposing protected labels or granular outcomes to researchers or agents.

## Why this component exists

- None declared.

## Authority and safety boundary

- This component may estimate, rank, simulate, challenge, or recommend only inside a declared research scope.
- It cannot create canonical Context truth, modify protected evidence roles, sign promotion, change portfolio risk, activate runtime generations, access live credentials, or place orders.
- Unsupported, stale, contradictory, OOD, hash-mismatched, uncalibrated, or incomplete paths resolve to **Skip**, **Abstain**, **Manual fallback**, **Reject**, or **Quarantine**.
- Every result is subordinate to UCEE I12 promotion admission, I13 authority/fallback, I14 immutable runtime, I17 portfolio/risk, and I18 release qualification.

## Input contracts

- Signed candidate bundle.
- Evaluation request with predeclared metrics.
- Protected dataset role.

## Output contracts

- Minimal signed scorecard.
- Pass/fail and bounded diagnostics.
- Exposure event.

## Algorithmic design

- One-way submission interface.
- Candidate executed in isolated environment.
- Return only predeclared aggregate metrics, uncertainty, and gate reasons.
- Granular predictions/outcomes remain sealed until campaign closure or retirement.
- Rate-limit submissions by hypothesis and institution-wide FDR budget.


## Data and known-time semantics

- None declared.

## Anti-overfit and model-risk controls

- Researchers cannot inspect evaluation code, labels, or row-level residuals.
- Agents cannot adaptively query the service.
- Submission hashes immutable.
- Human access is dual-controlled.

## Measurement system

- Submissions per campaign.
- Protected exposure count.
- Query adaptivity score.
- Hidden-test reuse age.

## Scalability and operating model

- None declared.

## Adversarial failure modes

- Leaderboard overfitting through repeated queries.
- Scorecard reveals enough subgroup data to reverse engineer labels.
- Candidate changes after evaluation.

## UCEE integration

- None declared.

## Required tests and evidence

- Adaptive query simulation.
- Side-channel scan.
- Candidate hash mismatch.
- Evaluation environment escape.

## Implementation slices

- None declared.

## Decision record

- None declared.

## Acceptance gate

The component is accepted only when its contracts are closed and versioned, all lineage and role boundaries are reconstructible, protected evaluation remains unexposed, negative and mutation tests pass, simpler baselines remain available, and an independent reviewer can reproduce the decision-equivalent result from immutable hashes.

## Related notes

- [[Online_False_Discovery_Control]]
- [[Protected_Evidence_Access_And_Blinding]]
