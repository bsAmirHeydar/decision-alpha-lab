---
title: Execution Digital Twin — Map of Content
status: implemented-reference
phase: SAED_V4_09
version: 1.0.0
created: '2026-07-15'
updated: '2026-07-15'
capability_tier: core-production-reference
authority: reference-only
tags:
  - saed-v4
  - v4-09
  - execution-digital-twin
---

# Execution Digital Twin — Map of Content

## Institutional intent

The canonical map for the complete V4-09 implementation, evidence, operations, and V4-10 handoff. The implementation is subordinate to immutable Context truth, the V4-08 Executable Path Outcome Cube, protected evidence roles, UCEE promotion, hard risk, portfolio governance, runtime compilation, and I18 production qualification.

## Contract and invariants

- Every artifact is exact-versioned, content-addressed, and reproducible from frozen inputs.
- Every source outcome row is preserved by `source_row_id`, `source_row_hash`, `node_id`, and `node_hash`.
- Every configured scenario produces exactly one projection for every source row; missing, duplicate, or unexpected pairs fail closed.
- Skip and Abstain remain non-order outcomes in every scenario.
- Unknown fields, unsupported evidence roles, invalid probabilities, negative costs, and authority escalation are rejected.
- V4-09 adds execution assumptions and incremental execution costs; it never rewrites V4-08 outcomes.

## Scientific and execution semantics

The reference implementation starts with deliberately simple monotone components: bounded latency realization, queue uncertainty, exponential fill-hazard decay, linear plus square-root impact, and explicit adverse-selection penalties. Complexity is not accepted merely because it fits historical fills. Any learned point-process, queue-reactive, agent-based, or broker-specific challenger must declare support, censoring, calibration, drift, transport limits, and protected evaluation evidence.

Reference-synthetic scenarios are watermarked. They can reject fragile ideas, expose sensitivity, and define engineering boundaries, but they cannot create positive alpha, promotion, prospective, shadow, broker-parity, or production claims. The digital twin is not a substitute for prospective paper, shadow operation, micro-live qualification, or recovery drills.

## Failure behavior

Failures resolve to reject, quarantine, or explicit non-order state. No implicit fallback may create a fill, change a source row, delete a scenario, rank a treatment, allocate capital, activate runtime, or send an order. Incidents retain source identity, reason code, detail, and a false recovery-authority flag.

## Evidence required

1. Closed schema validation and negative fixtures.
2. Deterministic golden build, replay, semantic diff, and Merkle receipt.
3. Complete row-by-scenario exposure accounting.
4. Python unit, mutation, property, and authority tests.
5. MQL5 static diagnostics with MetaEditor compilation separately classified.
6. Explicit limitations and unresolved external qualification gates.

## Operational review

Reviewers must verify that nominal and stress profiles are exact, source identities are untouched, incremental cost is non-negative, partial fills preserve quantity, lifecycle chains are monotone, synthetic watermarking cannot be removed, and all output authority flags remain false. Any mismatch blocks the V4-10 handoff.

## Navigation

- [[01_Executive_Intent|Executive Intent]]
- [[02_Phase_Scope_And_Non_Goals|Phase Scope and Non-Goals]]
- [[03_Authority_And_UCEE_Boundary|Authority and UCEE Boundary]]
- [[04_V4_08_Input_Contract|V4-08 Input Contract]]
- [[05_Execution_Twin_Constitution|Execution Twin Constitution]]
- [[06_Order_Lifecycle_Ontology|Order Lifecycle Ontology]]
- [[07_Latency_And_Jitter_Profile|Latency and Jitter Profile]]
- [[08_Queue_Position_Uncertainty|Queue Position Uncertainty]]
- [[09_Fill_Hazard_Baseline|Fill Hazard Baseline]]
- [[10_Marked_Point_Process_Boundary|Marked Point Process Boundary]]
- [[11_Spread_And_Liquidity_State|Spread and Liquidity State]]
- [[12_Market_Impact_Surface|Market Impact Surface]]
- [[13_Adverse_Selection_Model|Adverse Selection Model]]
- [[14_Broker_Profile_Contract|Broker Profile Contract]]
- [[15_Broker_Constraint_Solver|Broker Constraint Solver]]
- [[16_Partial_Fill_Semantics|Partial Fill Semantics]]
- [[17_Cancel_Replace_And_Expiry|Cancel, Replace, and Expiry]]
- [[18_Rejection_Model_And_Stress|Rejection Model and Stress]]
- [[19_Scenario_Matrix_Contract|Scenario Matrix Contract]]
- [[20_Nominal_Scenario|Nominal Scenario]]
- [[21_Latency_Stress|Latency Stress]]
- [[22_Spread_Stress|Spread Stress]]
- [[23_Queue_And_Partial_Fill_Stress|Queue and Partial-Fill Stress]]
- [[24_Combined_Severe_Stress|Combined Severe Stress]]
- [[25_Source_Row_Identity_Preservation|Source Row Identity Preservation]]
- [[26_Complete_Scenario_Exposure|Complete Scenario Exposure]]
- [[27_Incremental_Execution_Cost|Incremental Execution Cost]]
- [[28_Adjusted_Outcome_Projection|Adjusted Outcome Projection]]
- [[29_Skip_And_Abstain_Preservation|Skip and Abstain Preservation]]
- [[30_Synthetic_Watermarking|Synthetic Watermarking]]
- [[31_Calibration_Claim_Tiers|Calibration Claim Tiers]]
- [[32_Digital_Twin_Does_Not_Replace_Shadow|Digital Twin Does Not Replace Shadow]]
- [[33_Deterministic_Identity_And_Hashing|Deterministic Identity and Hashing]]
- [[34_Lifecycle_Event_Hash_Chain|Lifecycle Event Hash Chain]]
- [[35_Twin_Row_Merkle_Root|Twin Row Merkle Root]]
- [[36_Deterministic_Replay|Deterministic Replay]]
- [[37_Semantic_Diff|Semantic Diff]]
- [[38_Budget_And_Explosion_Control|Budget and Explosion Control]]
- [[39_Telemetry_And_Observability|Telemetry and Observability]]
- [[40_Quarantine_And_Incident_Handling|Quarantine and Incident Handling]]
- [[41_Service_And_CLI|Service and CLI]]
- [[42_Python_Reference_Implementation|Python Reference Implementation]]
- [[43_MQL5_Diagnostic_Mirror|MQL5 Diagnostic Mirror]]
- [[44_Closed_Schema_Catalog|Closed Schema Catalog]]
- [[45_Golden_Fixtures|Golden Fixtures]]
- [[46_Negative_Fixtures|Negative Fixtures]]
- [[47_Conformance_Vectors|Conformance Vectors]]
- [[48_Mutation_And_Property_Tests|Mutation and Property Tests]]
- [[49_Broker_Transport_Limitations|Broker Transport Limitations]]
- [[50_Security_Threat_Model|Security Threat Model]]
- [[51_Operational_Runbook|Operational Runbook]]
- [[52_Release_And_Rollback|Release and Rollback]]
- [[53_Independent_Reproduction|Independent Reproduction]]
- [[54_MetaEditor_Qualification|MetaEditor Qualification]]
- [[55_Broker_Calibration_Qualification|Broker Calibration Qualification]]
- [[56_Cross_Broker_Transport|Cross-Broker Transport]]
- [[57_Execution_Twin_To_I18|Execution Twin to I18 Qualification]]
- [[58_Acceptance_Criteria|Acceptance Criteria]]
- [[59_Evidence_And_Claim_Ledger|Evidence and Claim Ledger]]
- [[60_Limitations_And_Residual_Risk|Limitations and Residual Risk]]
- [[61_V4_10_Baseline_Manual_Handoff|V4-10 Baseline and Manual Program Handoff]]
- [[62_Implementation_Checklist|Implementation Checklist]]
- [[63_File_Inventory_And_Hash_Ledger|File Inventory and Hash Ledger]]
- [[64_Architecture_Decisions|Architecture Decisions]]
- [[65_Review_Guide|Review Guide]]
- [[66_Test_Evidence|Test Evidence]]
- [[67_Change_Log|Change Log]]

## Related architecture

- [[V4_09_Execution_Digital_Twin]]
- [[Execution_Digital_Twin_Charter]]
- [[ADR_V4_014_Execution_Digital_Twin_Does_Not_Replace_Shadow]]
