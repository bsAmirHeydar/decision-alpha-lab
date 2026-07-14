---
title: Runbook — Independent Statistical Challenge and Promotion Dossier
status: canonical
version: 4.0.0
created: '2026-07-13'
updated: '2026-07-13'
tags:
- saed-v4
- runbook
- operations
---

# Purpose

Challenge finalists under multiplicity, clustering, transport, cost, brittleness and model-risk tests, then produce a signed promote/challenge/reject recommendation.

# Entry conditions

- Finalist artifacts and full trial/exposure ledger are frozen.
- Independent validator owns challenge execution.
- Locked final role has not been consumed beyond registered accesses.

# Roles and separation of duties

| Role | Responsibility |
|---|---|
| Independent Validator | Runs challenge and owns verdict. |
| Statistical Adversary | Reconstructs multiplicity and nulls. |
| Execution Auditor | Challenges costs/fills/path. |
| Causal Auditor | Challenges identification claims. |
| Model Risk Committee | Signs admission recommendation. |

# Procedure

## Step 1 — Reconstruct science

**Action**

Rebuild dataset, folds, preprocessing, candidate universe and predictions from source artifacts.

**Mandatory output**

- Independent reconstruction report.

**Stop conditions**

- Any material artifact cannot be reproduced.

## Step 2 — Audit leakage and known-time

**Action**

Run lineage, timestamp, future-suffix, fold and preprocessing mutation tests.

**Mandatory output**

- Leakage certification.

**Stop conditions**

- Any decision-time leakage or role contamination is unresolved.

## Step 3 — Quantify selection bias

**Action**

Reconstruct all trials/exposures and apply multiplicity, PBO/CSCV, deflated and reality-check diagnostics.

**Mandatory output**

- Multiplicity report.

**Stop conditions**

- Trial universe is incomplete or evidence collapses after adjustment.

## Step 4 — Run destructive stresses

**Action**

Remove best trades/clusters/periods, perturb parameters/features/treatments and stress cost/delay/fill/path.

**Mandatory output**

- Brittleness and execution report.

**Stop conditions**

- Utility becomes negative or risk constraints fail within plausible stress.

## Step 5 — Run transport and subgroup challenge

**Action**

Test symbols, feeds, regimes, sessions, support buckets and context versions.

**Mandatory output**

- Transport report.

**Stop conditions**

- Critical subgroup is unsupported or aggregate hides collapse.

## Step 6 — Score model risk

**Action**

Assess complexity, opacity, support, data dependence, security, runtime and monitoring.

**Mandatory output**

- Model risk scorecard.

**Stop conditions**

- Residual risk exceeds capability tier.

## Step 7 — Assemble promotion dossier

**Action**

Bind evidence, limitations, support, policy scope, fallback, monitoring, runtime dependencies and kill criteria.

**Mandatory output**

- Signed dossier recommendation.

**Stop conditions**

- Any mandatory evidence or owner is absent.

## Step 8 — Issue verdict

**Action**

Return promote-to-paper, challenge, reject or quarantine; never direct live promotion.

**Mandatory output**

- Admission decision record.

**Stop conditions**

- Committee conflict or unsigned waiver exists.

# Completion gates

- [ ] Independent reconstruction passes.
- [ ] No unresolved leakage.
- [ ] Multiplicity-adjusted evidence remains meaningful.
- [ ] Plausible execution and transport stress survive.
- [ ] Scope/fallback/kill criteria are explicit.

# Evidence retained

- `reconstruction_report`
- `leakage_certification`
- `multiplicity_report`
- `stress_report`
- `transport_report`
- `model_risk_scorecard`
- `promotion_dossier`
- `admission_decision`

# Failure and escalation matrix

| Condition | Required response |
|---|---|
| Locked evidence overexposed | Downgrade evidence; create new prospective challenge. |
| Critical finding disputed | Preserve dissent; escalate to committee; no promotion while open. |
| Waiver proposed | Require scoped signed expiry and compensating control. |
| Model author modifies artifact | Restart challenge on a new version. |

# Exit state

Successful candidate is admitted only to prospective paper/shadow scope.

# Related architecture

- [[00_Home]]
- [[End_To_End_Reference_Architecture]]
- [[Adversarial_Anti_Overfit_Red_Team]]
- [[Failure_Modes_Kill_Criteria_And_Recovery]]
