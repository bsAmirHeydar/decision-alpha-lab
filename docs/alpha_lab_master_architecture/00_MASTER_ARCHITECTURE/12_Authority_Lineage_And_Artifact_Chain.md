---
id: ALMA-3C6C5011B3
title: "Authority, Lineage and Artifact Chain"
type: architecture
status: canonical
domain: alpha-lab-master-architecture
version: 1.0.0
created: 2026-07-13
updated: 2026-07-13
tags:
  - alpha-lab
  - master-architecture
---
# Authority, Lineage and Artifact Chain

## 1. Single-Owner Principle

Every mutable state has one authoritative writer.

| Concern | Authority |
|---|---|
| market meaning | human doctrine owner |
| context occurrence and lifecycle | context engine |
| treatment construction | manual policy or treatment compiler |
| research plan and trial registry | experiment compiler |
| evidence eligibility | deterministic evidence gate |
| explanatory interpretation | AI analyst, non-authoritative |
| capital limits | capital and portfolio governance |
| broker action | execution layer after risk gate |
| live activation | deployment governance |
| emergency shutdown | hard risk/operator authority |

## 2. Canonical Artifact Chain

```text
Doctrine
→ ContextSpec
→ ContextEvents
→ ContextSnapshots
→ TreatmentInventory
→ Outcomes
→ Dataset + Folds
→ TrialLedger + Predictions
→ Statistics + AntiOverfit
→ AnalystReport
→ EvidenceDecision
→ CapitalPolicy
→ PortfolioAdmission
→ RuntimeGeneration
→ Decision / Order / Fill Ledger
→ Monitoring / Incident / Retirement
```

## 3. Required Identity Chain

Every final claim binds:

- source inventory;
- code and build;
- doctrine/context versions;
- schema and feature order;
- treatment and cost profile;
- dataset and fold plan;
- experiment and trial;
- model, calibration and threshold;
- evidence policy;
- capital/portfolio policy;
- runtime generation;
- approvals.

A result that cannot be reconstructed through this chain is exploratory only.

## 4. Versioning

Major version changes meaning or compatibility. Minor adds backward-compatible capability. Patch fixes wording or defects without semantic reclassification.

When a context definition changes historical classification, prior evidence remains attached to the old lineage.

## 5. Promotion and Waivers

Promotion gates cover context, research integrity, statistical evidence, economics, prospective parity, portfolio admission and production readiness.

A waiver may temporarily relax a noncritical requirement but must identify scope, reason, tighter controls, expiry and remediation. Critical leakage, artifact corruption and hard risk limits cannot be waived.

## 6. Audit Questions

The architecture must answer:

- What did the system know at decision time?
- Which doctrine created the context?
- Which alternatives were searched?
- Which data selected the winner?
- Why was it promoted?
- What risk was requested and approved?
- What order was expected and filled?
- Which assumption changed before reduction or retirement?
