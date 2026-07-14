---
title: V4-00 Program Constitution MOC
status: implemented
version: 1.0.0
phase: V4-00
created: '2026-07-13'
updated: '2026-07-13'
capability_tier: core-production-control-plane
tags:
  - saed-v4
  - v4-00
  - program-constitution
---

# V4-00 Program Constitution MOC

> **Focus:** Navigation, deliverable topology and acceptance map.

## Phase map

- [[01_Executive_Delivery_Summary]]
- [[02_Phase_Mission_And_Non_Goals]]
- [[03_Constitutional_Kernel_Architecture]]
- [[04_UCEE_I01_I18_Crosswalk]]
- [[05_Authority_Matrix_And_Denial_By_Default]]
- [[06_Evidence_Role_Firewall]]
- [[07_Objective_Freeze_And_Baseline_Obligations]]
- [[08_Two_Person_Integrity_And_Reviewer_Independence]]
- [[09_Amendment_Protocol]]
- [[10_Waiver_Sunset_Protocol]]
- [[11_Complete_Exposure_Accounting]]
- [[12_Hidden_Evaluation_Query_Budget]]
- [[13_External_Evidence_Classification]]
- [[14_Deterministic_Identity_And_Canonicalization]]
- [[15_Tamper_Evident_Ledger]]
- [[16_Signature_And_Key_Management_Boundary]]
- [[17_Core_Engine_Additive_Boundary]]
- [[18_Program_Manifest_And_Registry]]
- [[19_Constitutional_Incident_Model]]
- [[20_Fail_Closed_State_Machine]]
- [[21_Agent_Authority_Envelope]]
- [[22_Model_Risk_Three_Lines_Of_Defense]]
- [[23_Security_Threat_Model]]
- [[24_Python_Reference_Implementation]]
- [[25_MQL5_Mirror_Contract]]
- [[26_JSON_Schema_Catalog]]
- [[27_Golden_Negative_And_Mutation_Fixtures]]
- [[28_Conformance_Vector_Program]]
- [[29_Test_Strategy_And_Coverage]]
- [[30_CLI_And_Operator_Workflows]]
- [[31_Release_And_Integrity_Pipeline]]
- [[32_Installation_And_Repository_Integration]]
- [[33_Operational_Runbook]]
- [[34_Failure_And_Escalation_Runbook]]
- [[35_Acceptance_Evidence]]
- [[36_Known_Limitations_And_Deferred_Evidence]]
- [[37_Handoff_To_V4_01]]
- [[38_Persian_Implementation_Overview]]

## Institutional invariant

The phase-zero control plane is **subordinate** to canonical UCEE truth. It does not infer a Context, select a Treatment, sign a promotion, allocate capital, activate a runtime generation, access a broker, or place an order. Its job is to decide whether a research action, evidence use, process amendment or release claim is constitutionally admissible.

```text
Request
→ Closed contract validation
→ Known-time and lineage validation
→ Authority evaluation
→ Evidence-role firewall
→ Objective/baseline gate
→ Independence and budget gate
→ Deterministic constitutional decision
→ Tamper-evident ledger
```

## Hard properties

1. **Deny by default.** An actor receives only authorities listed in the exact-version authority matrix.
2. **No autonomous promotion.** Research agents and researchers cannot sign promotion or activate runtime.
3. **Protected evidence never trains.** Locked-final, prospective, shadow, micro-live and live evidence cannot feed training or adaptive search.
4. **Synthetic evidence is asymmetric.** It may reject or stress a candidate but cannot create positive promotion evidence.
5. **No retroactive governance.** Amendments apply only to programs created after their effective time.
6. **Complete exposure accounting.** Trials, queries, charts, narratives and agent suggestions are counted.
7. **External evidence is typed.** Static checks are never represented as actual MetaEditor compile, parity, shadow or live evidence.
8. **UCEE remains authoritative.** Every I01–I18 crosswalk entry is read-only from SAED.

## Required artifacts

- Active research constitution and SHA-256 hash.
- Exact-version authority matrix.
- Evidence-role policy.
- Objective and mandatory-baseline policy.
- Program manifest with owners and budgets.
- UCEE I01–I18 crosswalk.
- Exposure ledger and budget.
- Constitutional decision ledger.
- Core-boundary snapshot.
- Explicit limitations and external-evidence classification.

## Failure semantics

| Failure | Constitutional result | Required next action |
|---|---|---|
| Unknown field or malformed contract | Reject | Repair contract; never infer defaults |
| Research actor requests hard authority | Reject | Record incident if attempted escalation is material |
| Protected evidence used for training | Reject and quarantine | Invalidate affected trials and lineage |
| Synthetic result used to promote | Reject | Reclassify as stress-only evidence |
| Objective changes without amendment | Require review | Freeze family and submit amendment |
| Reviewer is proposer or same unit | Reject | Assign independent reviewers |
| Exposure budget exhausted | Reject | Stop the hypothesis family |
| Core UCEE snapshot changes | Reject patch | Split work and restore core boundary |
| Static evidence claimed as actual | Reject claim | Correct evidence class and requalify |
| Ledger/hash mismatch | Quarantine | Treat as integrity incident |

## Scale behavior

The kernel is stateless and deterministic. It can run in CI, a research-control service, an air-gapped hidden-evaluation service, or a local CLI. State is kept in immutable registries and hash-chained ledgers. Work can be sharded by program, hypothesis family, Context Cell and evidence role without weakening the constitution.

## Reference implementation

Python package:

```text
lab/11_strategy_factory/python/saed_v4_constitution/
```

The package separates pure policy evaluation from I/O. `ConstitutionKernel` composes the authority matrix and evidence firewall. Amendment, waiver, review, exposure, registry, ledger, bundle, crosswalk and core-boundary modules remain independently testable.

MQL5 mirror:

```text
mql5/Include/AlphaLab/StrategyFactory/SAEDV4Constitution/
```

The mirror exists only to verify that runtime-side diagnostics preserve the same denial semantics. It has no order-management implementation and static validation rejects trading/network tokens.

## Acceptance checklist

- [ ] All closed schemas validate under JSON Schema Draft 2020-12.
- [ ] Golden examples validate and negative examples fail for the intended reason.
- [ ] Research actors cannot obtain order, broker, network, risk, portfolio, runtime, promotion or context-mutation authority.
- [ ] Protected evidence cannot train or tune.
- [ ] Synthetic stress cannot positively promote.
- [ ] Objective drift requires a prospective amendment.
- [ ] Two independent approvals are mandatory.
- [ ] Non-waivable rules remain non-waivable.
- [ ] Exposure budget exhaustion stops the family.
- [ ] Decision replay is deterministic.
- [ ] Ledger tampering is detected.
- [ ] UCEE crosswalk has no mutation permission.
- [ ] Static MQL5 evidence is labeled `pending_local_windows` for actual compile.
- [ ] Patch file index changes only additive phase-zero paths.
