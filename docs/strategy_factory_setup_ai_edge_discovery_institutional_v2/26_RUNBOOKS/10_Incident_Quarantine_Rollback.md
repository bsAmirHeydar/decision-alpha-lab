---
title: Runbook — Incident, Quarantine, Revocation and Rollback
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

Move the system to a safe state, preserve evidence, identify impacted artifacts and recover without duplicate decisions or hidden state divergence.

# Entry conditions

- Incident signal or credible critical finding exists.
- Kill/quarantine authority and communication path are available.
- Current generation, account and portfolio state can be identified.

# Roles and separation of duties

| Role | Responsibility |
|---|---|
| Incident Commander | Owns timeline and decisions. |
| Operations | Executes pause/kill/rollback. |
| Risk | Controls exposure and reservations. |
| Engineering | Diagnoses data/runtime/artifact fault. |
| Independent Validator | Determines requalification scope. |
| Security | Handles compromise and revocation. |

# Procedure

## Step 1 — Declare and classify

**Action**

Open incident, severity, scope, affected accounts/symbols/generations and initial evidence.

**Mandatory output**

- Incident record.

**Stop conditions**

- Scope cannot be bounded—treat as highest severity.

## Step 2 — Reach safe state

**Action**

Pause, kill, de-risk, revoke authorization or isolate service according to kill matrix.

**Mandatory output**

- Safe-state confirmation.

**Stop conditions**

- Orders/positions/reservations remain unreconciled.

## Step 3 — Preserve forensics

**Action**

Snapshot logs, artifacts, market/broker data, journals, credentials and clocks.

**Mandatory output**

- Forensic evidence manifest.

**Stop conditions**

- Evidence is mutable or retention unavailable.

## Step 4 — Trace dependency impact

**Action**

Use lineage graph to identify affected datasets, models, dossiers and generations.

**Mandatory output**

- Impact graph.

**Stop conditions**

- Unknown dependencies remain.

## Step 5 — Rollback or contain

**Action**

Activate last admitted generation or management-only mode; reconcile positions/decisions.

**Mandatory output**

- Rollback/reconciliation record.

**Stop conditions**

- Rollback target is incompatible or unqualified.

## Step 6 — Remediate and challenge

**Action**

Fix root cause, add regression/adversarial tests and independent review.

**Mandatory output**

- Remediation package.

**Stop conditions**

- Cause or control effectiveness is unresolved.

## Step 7 — Requalify and resume

**Action**

Run scoped mandatory gates, sign authorization and monitor heightened state.

**Mandatory output**

- Resume authorization.

**Stop conditions**

- Any critical gate or evidence remains open.

## Step 8 — Close and institutionalize

**Action**

Publish post-mortem, failure signature, memory and control changes.

**Mandatory output**

- Incident closure dossier.

**Stop conditions**

- Owner, follow-up or prevention evidence absent.

# Completion gates

- [ ] Safe state reached and confirmed.
- [ ] Forensic artifacts preserved.
- [ ] Dependency impact complete.
- [ ] Rollback/reconciliation passes.
- [ ] Independent requalification and authorization precede resume.

# Evidence retained

- `incident_record`
- `safe_state_confirmation`
- `forensic_manifest`
- `impact_graph`
- `rollback_record`
- `remediation_package`
- `requalification_report`
- `closure_dossier`

# Failure and escalation matrix

| Condition | Required response |
|---|---|
| Kill path fails | Escalate to manual broker/account containment. |
| Evidence store compromised | Use secondary immutable archive; treat as security incident. |
| Rollback mismatch | Stay paused/management-only; rebuild reconciliation. |
| Repeated incident | Increase severity; consider retirement and architecture review. |

# Exit state

System is safely resumed under new authorization, remains quarantined, or is retired.

# Related architecture

- [[00_Home]]
- [[End_To_End_Reference_Architecture]]
- [[Adversarial_Anti_Overfit_Red_Team]]
- [[Failure_Modes_Kill_Criteria_And_Recovery]]
