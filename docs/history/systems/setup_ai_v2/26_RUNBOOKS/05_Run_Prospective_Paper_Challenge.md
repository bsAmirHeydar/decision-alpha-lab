---
title: Runbook — Prospective Paper and Shadow Challenge
status: canonical
version: 2.0.0
created: '2026-07-13'
updated: '2026-07-13'
tags:
- saed-v2
- runbook
- operations
---

# Purpose

Collect untouched forward evidence for a frozen candidate while prohibiting tuning, retraining, selective omission and silent artifact replacement.

# Entry conditions

- Signed admission to paper/shadow exists.
- Runtime generation and monitoring contract are frozen.
- Start/end rules, sample/event targets and invalidation policy are predeclared.

# Roles and separation of duties

| Role | Responsibility |
|---|---|
| Paper Operator | Runs generation without model modification. |
| Operations Observer | Monitors data/runtime health. |
| Independent Validator | Owns final comparison and deviations. |
| Release Authority | Can pause/revoke; cannot tune candidate. |

# Procedure

## Step 1 — Activate frozen generation

**Action**

Verify hashes, signatures, account/environment and no-send authority.

**Mandatory output**

- Activation record.

**Stop conditions**

- Any component differs from admitted dossier.

## Step 2 — Capture every opportunity

**Action**

Record contexts, candidates, scores, Skip/Abstain, expected decisions and expiration.

**Mandatory output**

- Prospective opportunity ledger.

**Stop conditions**

- Opportunities can be hidden or manually removed.

## Step 3 — Capture execution truth

**Action**

In paper/shadow, record executable quotes, simulated/observed fills, spread, latency, rejects and broker specifications.

**Mandatory output**

- Prospective execution ledger.

**Stop conditions**

- Mid-price substitutes for executable observations.

## Step 4 — Monitor assumptions

**Action**

Track support, calibration, OOD, missing views, drift, cost, capacity and runtime health.

**Mandatory output**

- Monitoring stream and incidents.

**Stop conditions**

- Critical assumption or runtime integrity fails.

## Step 5 — Prevent adaptation

**Action**

Block retraining, threshold edits, treatment changes, model swaps and selective restart.

**Mandatory output**

- Change-control audit.

**Stop conditions**

- Any unadmitted adaptive change occurs.

## Step 6 — Close challenge by rule

**Action**

Stop only at predeclared time/event boundary or critical kill condition.

**Mandatory output**

- Closure record.

**Stop conditions**

- Early stop is based on favorable/unfavorable performance without rule.

## Step 7 — Evaluate expected versus observed

**Action**

Compare decision, fill, cost, utility, calibration, support, tail, capacity and incidents.

**Mandatory output**

- Prospective evidence report.

**Stop conditions**

- Missing or inconsistent evidence prevents reconstruction.

## Step 8 — Issue next-stage recommendation

**Action**

Recommend reject, extend, requalify or no-send rehearsal; no automatic live step.

**Mandatory output**

- Prospective verdict.

**Stop conditions**

- Evidence target or assumptions are not met.

# Completion gates

- [ ] Frozen artifact remained unchanged.
- [ ] Every opportunity and abstention is retained.
- [ ] Execution observations are reconstructible.
- [ ] No tuning or selective stopping occurred.
- [ ] Expected/observed divergence is within declared bounds.

# Evidence retained

- `activation_record`
- `prospective_opportunity_ledger`
- `prospective_execution_ledger`
- `monitoring_stream`
- `change_control_audit`
- `closure_record`
- `prospective_evidence_report`
- `prospective_verdict`

# Failure and escalation matrix

| Condition | Required response |
|---|---|
| Critical data/runtime failure | Pause or quarantine; preserve state; follow incident runbook. |
| Authorization or signature expires | Disable operation immediately. |
| Manual intervention | Record exact action/reason; segment evidence; possibly invalidate challenge. |
| Insufficient occurrence count | Close as inconclusive or extend only under predeclared rule. |

# Exit state

Candidate may proceed to bounded runtime/no-send qualification only after independent prospective approval.

# Related architecture

- [[00_Home]]
- [[End_To_End_Reference_Architecture]]
- [[Adversarial_Anti_Overfit_Red_Team]]
- [[Failure_Modes_Kill_Criteria_And_Recovery]]
