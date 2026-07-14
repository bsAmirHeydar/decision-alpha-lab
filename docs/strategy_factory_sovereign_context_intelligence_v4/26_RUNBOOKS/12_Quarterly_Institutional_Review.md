---
title: Runbook — Quarterly Institutional AI and Edge Review
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

Review the complete research, model-risk, portfolio, runtime and memory system to reallocate capital, retire weak assets and update the institutional roadmap.

# Entry conditions

- Quarterly evidence snapshot is closed.
- Research, validation, risk, operations and finance packets are prepared.
- Incidents, waivers, authorizations and active generations are reconciled.

# Roles and separation of duties

| Role | Responsibility |
|---|---|
| Executive Sponsor | Sets strategic capital and risk appetite. |
| Research Council | Reviews programs and evidence pipeline. |
| Model Risk Committee | Reviews findings, waivers and capability tiers. |
| Portfolio/Risk | Reviews dependence, capacity and capital. |
| Operations | Reviews runtime health and incidents. |
| Platform/Finance | Reviews compute economics and roadmap. |

# Procedure

## Step 1 — Review edge inventory

**Action**

Classify proposed, research, paper, shadow, live, reduced, quarantined and retired edges.

**Mandatory output**

- Edge inventory decision table.

**Stop conditions**

- Status/evidence mismatch exists.

## Step 2 — Review scientific quality

**Action**

Assess falsification rate, multiplicity, replication, prospective outcomes and negative evidence.

**Mandatory output**

- Scientific health report.

**Stop conditions**

- Programs rely on exposed/weak evidence.

## Step 3 — Review model risk and technology tiers

**Action**

Evaluate advanced models, agents, foundation/world/RL uses, open findings and fallbacks.

**Mandatory output**

- Capability-tier review.

**Stop conditions**

- Research-only component has de facto production authority.

## Step 4 — Review portfolio and capital

**Action**

Assess marginal value, dependence, capacity, concentration, drawdown and edge decay.

**Mandatory output**

- Portfolio research report.

**Stop conditions**

- Unknown dependence or capacity risk is hidden.

## Step 5 — Review operations and security

**Action**

Assess incidents, compile/parity, authorization, rollback, SBOM, drift and recovery drills.

**Mandatory output**

- Operational readiness report.

**Stop conditions**

- Critical control remains untested or waiver expired.

## Step 6 — Review compute and organization

**Action**

Evaluate cost per evidence, bottlenecks, staffing, validation capacity and reuse.

**Mandatory output**

- Resource allocation report.

**Stop conditions**

- Compute growth lacks evidence value.

## Step 7 — Set next-quarter portfolio

**Action**

Promote research priorities, pause/retire programs, fund platform gaps and freeze milestones.

**Mandatory output**

- Signed quarterly plan.

**Stop conditions**

- Decision rights or budgets are ambiguous.

## Step 8 — Update memory and roadmap

**Action**

Record decisions, rationale, dissent, assumptions and kill criteria.

**Mandatory output**

- Quarterly memory packet.

**Stop conditions**

- Decisions cannot be traced to evidence.

# Completion gates

- [ ] Every active edge has current evidence/support/owner.
- [ ] Research-only capabilities remain bounded.
- [ ] Open critical findings block expansion.
- [ ] Capital/compute allocation links to evidence value.
- [ ] Retirement and falsification are explicit outcomes.

# Evidence retained

- `edge_inventory`
- `scientific_health_report`
- `capability_tier_review`
- `portfolio_report`
- `operational_report`
- `resource_allocation`
- `quarterly_plan`
- `quarterly_memory_packet`

# Failure and escalation matrix

| Condition | Required response |
|---|---|
| Live edge lacks current qualification | Reduce/pause/quarantine immediately. |
| Expired waiver/authorization | Revoke until renewed qualification. |
| Research pipeline overexposed | Reset evidence strategy and prospective plan. |
| Systemic incident trend | Commission architecture-level root-cause review. |

# Exit state

A signed, budgeted and risk-bounded quarterly operating plan is active.

# Related architecture

- [[00_Home]]
- [[End_To_End_Reference_Architecture]]
- [[Adversarial_Anti_Overfit_Red_Team]]
- [[Failure_Modes_Kill_Criteria_And_Recovery]]
