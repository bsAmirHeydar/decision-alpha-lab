---
title: MOC V4-06 Treatment DSL V4
status: implemented
version: 1.0.0
phase: V4-06
created: '2026-07-15'
updated: '2026-07-15'
capability_tier: core-production-context-plane
tags: [saed-v4, v4-06, treatment-dsl]
---

# V4-06 Treatment DSL V4

## Mission

Freeze a finite, exact-versioned, strongly typed Treatment declaration language on top of the immutable V4-05 semantic-temporal hypergraph. The phase converts governed Treatment intent into deterministic canonical programs, validates their structure and authority, binds externally approved graph descriptors, and emits an integrity-protected handoff to V4-07.

## Institutional invariant

A V4-06 Treatment program is a declaration. It is not a prediction, recommendation, selected action, risk allocation, runtime bundle, broker instruction or order. UCEE remains authority of record. The implementation denies graph mutation, arbitrary action generation, lattice solving, model training, Treatment selection, capital allocation, runtime activation, network access and order submission.

## Delivered reference surface

- 20 exact-versioned primitives across 13 semantic kinds.
- First-class Skip and Abstain system actions.
- Closed parameter types, units, ranges, enum domains and monotonic metadata.
- Closed source grammar, canonical AST and content-derived identities.
- Static validation for registry, policy, capabilities, constraints, feature references and state DAGs.
- Exact descriptor binding to the V4-05 graph and handoff.
- Integrity, replay, semantic diff, deterministic partitioning, telemetry and exposure accounting.
- Closed JSON schemas, golden and negative fixtures, Python implementation, diagnostic-only MQL5 mirror and bounded V4-07 handoff.

## Delivery map

- [[01_Executive_Intent]] — Executive Intent
- [[02_Phase_Scope_And_Non_Goals]] — Phase Scope And Non-Goals
- [[03_Authority_And_UCEE_Boundary]] — Authority And UCEE Boundary
- [[04_V4_05_Input_Contract]] — V4-05 Input Contract
- [[05_Finite_Action_Constitution]] — Finite Action Constitution
- [[06_Primitive_Ontology]] — Primitive Ontology
- [[07_Action_Skip_And_Abstain]] — Action Skip And Abstain
- [[08_Payoff_Primitives]] — Payoff Primitives
- [[09_Direction_Primitives]] — Direction Primitives
- [[10_Entry_Primitives]] — Entry Primitives
- [[11_Trigger_Primitives]] — Trigger Primitives
- [[12_Stop_Primitives]] — Stop Primitives
- [[13_Target_And_Exit_Primitives]] — Target And Exit Primitives
- [[14_Trail_Primitives]] — Trail Primitives
- [[15_Management_Primitives]] — Management Primitives
- [[16_Time_Primitives]] — Time Primitives
- [[17_Cost_And_Economics_Boundary]] — Cost And Economics Boundary
- [[18_Capability_Profiles]] — Capability Profiles
- [[19_Parameter_Type_System]] — Parameter Type System
- [[20_Units_And_Normalization]] — Units And Normalization
- [[21_Exact_Version_Registry]] — Exact Version Registry
- [[22_Closed_Program_Grammar]] — Closed Program Grammar
- [[23_Canonical_Abstract_Syntax_Tree]] — Canonical Abstract Syntax Tree
- [[24_Program_Identity]] — Program Identity
- [[25_Component_Identity]] — Component Identity
- [[26_Static_Type_Checking]] — Static Type Checking
- [[27_Constraint_Declaration_Grammar]] — Constraint Declaration Grammar
- [[28_Feature_Reference_Grammar]] — Feature Reference Grammar
- [[29_Known_Time_And_Evidence_Roles]] — Known-Time And Evidence Roles
- [[30_Descriptor_Binding]] — Descriptor Binding
- [[31_Semantic_Label_Reconciliation]] — Semantic Label Reconciliation
- [[32_State_Machine_Declaration]] — State Machine Declaration
- [[33_Cycle_Rejection_And_Reachability]] — Cycle Rejection And Reachability
- [[34_Capability_Compatibility]] — Capability Compatibility
- [[35_Budgets_And_Explosion_Controls]] — Budgets And Explosion Controls
- [[36_Prohibited_Sizing_And_Capital_Semantics]] — Prohibited Sizing And Capital Semantics
- [[37_Fail_Closed_Skip_Abstain_Fallback]] — Fail-Closed Skip And Abstain Fallback
- [[38_Deterministic_Builder_Pipeline]] — Deterministic Builder Pipeline
- [[39_Integrity_Receipt]] — Integrity Receipt
- [[40_Deterministic_Replay]] — Deterministic Replay
- [[41_Semantic_Diff]] — Semantic Diff
- [[42_Deterministic_Partitioning]] — Deterministic Partitioning
- [[43_Telemetry_And_Exposure_Ledger]] — Telemetry And Exposure Ledger
- [[44_Service_And_CLI]] — Service And CLI
- [[45_Python_Reference_Implementation]] — Python Reference Implementation
- [[46_MQL5_Diagnostic_Mirror]] — MQL5 Diagnostic Mirror
- [[47_Closed_Schema_Catalog]] — Closed Schema Catalog
- [[48_Golden_Negative_And_Conformance_Fixtures]] — Golden Negative And Conformance Fixtures
- [[49_Test_Strategy_And_Mutation_Coverage]] — Test Strategy And Mutation Coverage
- [[50_Security_And_Threat_Model]] — Security And Threat Model
- [[51_Quarantine_Incident_And_Recovery]] — Quarantine Incident And Recovery
- [[52_Operational_Runbook]] — Operational Runbook
- [[53_Performance_And_Compute_Economics]] — Performance And Compute Economics
- [[54_Release_Rollback_And_Recovery]] — Release Rollback And Recovery
- [[55_Acceptance_Criteria]] — Acceptance Criteria
- [[56_Evidence_And_Claim_Ledger]] — Evidence And Claim Ledger
- [[57_Limitations_And_Residual_Risk]] — Limitations And Residual Risk
- [[58_V4_07_Action_Lattice_Handoff]] — V4-07 Action Lattice Handoff
- [[59_Implementation_Checklist]] — Implementation Checklist

## Atomic concepts

- [[V4_06_Exact_Primitive_Key]]
- [[V4_06_Treatment_DSL_Registry]]
- [[V4_06_Treatment_Program_Source]]
- [[V4_06_Canonical_Treatment_Program]]
- [[V4_06_Canonical_Component]]
- [[V4_06_First_Class_Skip]]
- [[V4_06_First_Class_Abstain]]
- [[V4_06_Parameter_Unit]]
- [[V4_06_Capability_Profile]]
- [[V4_06_Constraint_Declaration]]
- [[V4_06_Feature_Reference]]
- [[V4_06_State_DAG]]
- [[V4_06_Descriptor_Binding]]
- [[V4_06_Evidence_Role_Isolation]]
- [[V4_06_Program_Hash]]
- [[V4_06_Source_Artifact_Hash]]
- [[V4_06_Package_Lineage_Root]]
- [[V4_06_Static_Rejection]]
- [[V4_06_Exposure_Ledger]]
- [[V4_06_Non_Executing_MQL5_Mirror]]
- [[V4_06_Bounded_V4_07_Handoff]]
- [[V4_06_No_Sizing_Authority]]

## Upstream and downstream

- Upstream: [[00_MOC_V4_05_Semantic_And_Temporal_Hypergraph]]
- Canonical roadmap: [[V4_06_Treatment_DSL_V4]]
- Downstream: [[V4_07_Constraint_Solver_And_Action_Lattice]]

## Claim boundary

This reference implementation claims deterministic finite DSL construction and validation only. It does not claim MetaEditor compilation, research/runtime parity, real-market feasibility, learned policy value, real alpha, prospective acceptance, production authorization or live execution.
