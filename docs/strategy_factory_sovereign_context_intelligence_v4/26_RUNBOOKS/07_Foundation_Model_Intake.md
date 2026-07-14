---
title: Runbook — Time-Series Foundation Model Intake and Challenge
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

Evaluate external or internally pretrained foundation models as bounded representation/forecasting challengers without granting them semantic, promotion or runtime authority.

# Entry conditions

- Model source, license, weights and documentation are available.
- Capability tier is Research-Only or Governed Challenger.
- Approved sandbox and safe serialization path exist.

# Roles and separation of duties

| Role | Responsibility |
|---|---|
| Foundation Model Owner | Owns intake and comparisons. |
| Security/Supply Chain | Scans code, weights, license and SBOM. |
| Data Governance | Approves pretraining/evaluation data use. |
| Independent Validator | Runs leakage, transport and baseline challenge. |

# Procedure

## Step 1 — Verify provenance and license

**Action**

Record source, authorship, license, version, hashes, training-data claims and restrictions.

**Mandatory output**

- Intake provenance card.

**Stop conditions**

- Unknown/forbidden license, unsafe origin or unverifiable weights.

## Step 2 — Sandbox and scan

**Action**

Use isolated loader, inspect serialization/code/dependencies and generate SBOM.

**Mandatory output**

- Security intake report.

**Stop conditions**

- Arbitrary code execution, unresolved vulnerability or secret/network access.

## Step 3 — Define adapter modes

**Action**

Predeclare zero-shot, frozen embedding, linear probe, parameter-efficient and full fine-tune modes allowed.

**Mandatory output**

- Adapter experiment plan.

**Stop conditions**

- Unbounded fine-tuning or direct live use is proposed.

## Step 4 — Build fair baselines

**Action**

Match data, horizon, folds, economics, context features and compute where possible.

**Mandatory output**

- Comparison manifest.

**Stop conditions**

- Foundation model receives protected data or richer labels than baselines.

## Step 5 — Evaluate support and calibration

**Action**

Test context-conditioned performance, OOD, uncertainty, subgroup transport and failure cases.

**Mandatory output**

- Support/calibration report.

**Stop conditions**

- Aggregate gain hides critical subgroup loss.

## Step 6 — Run ablations and contamination checks

**Action**

Compare frozen/random embeddings, timestamp/label nulls and suspected benchmark overlap.

**Mandatory output**

- Ablation/contamination report.

**Stop conditions**

- Potential contamination cannot be bounded.

## Step 7 — Decide capability tier

**Action**

Reject, research-only, governed challenger or approved component with fallback.

**Mandatory output**

- Intake decision.

**Stop conditions**

- Incremental value is not stable or operational cost unsupported.

# Completion gates

- [ ] Provenance/license/security pass.
- [ ] No direct semantic or trading authority.
- [ ] Fair baseline and role isolation.
- [ ] Stable protected incremental value.
- [ ] Fallback and export/runtime feasibility exist.

# Evidence retained

- `foundation_model_provenance`
- `sbom_manifest`
- `security_scan_report`
- `adapter_experiment_plan`
- `comparison_report`
- `support_audit`
- `intake_decision`

# Failure and escalation matrix

| Condition | Required response |
|---|---|
| New upstream version | Treat as a new model; no silent replacement. |
| License changes | Quarantine affected artifacts and deployments. |
| Contamination suspected | Downgrade evidence; require new data/period. |
| Export unsupported | Keep research-only regardless of offline performance. |

# Exit state

Model is rejected, research-only or admitted to a tightly scoped challenger role.

# Related architecture

- [[00_Home]]
- [[End_To_End_Reference_Architecture]]
- [[Adversarial_Anti_Overfit_Red_Team]]
- [[Failure_Modes_Kill_Criteria_And_Recovery]]
