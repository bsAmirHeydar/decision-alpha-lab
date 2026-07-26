---
title: RTHP MT5 Automatic M1 Data Acquisition and One-Click Train — MOC
status: implemented-real-mt5-smoke-proven
version: 1.1.0
updated: 2026-07-23
tags: [rthp, mt5, m1, data-acquisition, train-activation, roadmap]
---

# RTHP MT5 Automatic M1 Data Acquisition and One-Click Train

## Mission

Define the complete context-owned implementation roadmap that allows an operator to select only the two broker symbols and then delegate the remaining workflow to an automated, read-only MetaTrader 5 acquisition and RTHP train-activation shell.

The delivery is deliberately outside the central Strategy Factory, SAED, UCEE, ACL, dataset, trainer, validation, promotion, and runtime engines. It supplies source data and run configuration to those engines without changing their semantics.

## Canonical production data floor

- Source resolution: **closed M1 bars**.
- Sub-M1 bars and raw ticks: **excluded from the canonical research path**.
- Higher timeframes: derived deterministically from M1.
- Intrabar order: never inferred from M1 OHLC.
- Incomplete current M1 bar: never admitted.

## Navigation

- [[01_Current_State_and_Gap_Map]]
- [[02_Mission_Boundary_and_Authority]]
- [[03_Target_Operator_Experience]]
- [[04_Architecture_and_End_to_End_Data_Flow]]
- [[05_MT5_Terminal_Discovery_Connection_and_Health]]
- [[06_Symbol_Discovery_Alias_Resolution_and_Metadata_Freeze]]
- [[07_M1_Canonical_Data_Floor_and_Sub_M1_Exclusion]]
- [[08_M1_Bar_Semantics_Touch_Precision_and_Ambiguity]]
- [[09_Historical_Acquisition_Paging_Coverage_and_Retry]]
- [[10_UTC_New_York_DST_and_Trading_Calendar_Normalization]]
- [[11_Session_Aware_Gap_Duplicate_and_Cross_Symbol_Quality_Gates]]
- [[12_Canonical_Landing_Zone_Provenance_Hashing_and_Immutability]]
- [[13_RTHP_Materialization_and_Existing_Train_Activation_Handoff]]
- [[14_One_Click_Orchestration_State_Machine_Resume_and_Idempotency]]
- [[15_Security_Entitlements_Secrets_and_No_Trade_Sandbox]]
- [[16_Observability_Reports_Receipts_and_Operator_Diagnostics]]
- [[17_Test_Strategy_Acceptance_Matrix_and_Definition_of_Done]]
- [[18_Implementation_Phases_Critical_Path_and_Release_Gates]]
- [[19_Repository_File_Tree_and_Ownership_Map]]
- [[20_Open_Decisions_Assumptions_and_Non_Goals]]

## Atomic concepts

- [[../../13_ATOMIC_CONCEPTS/RTHP_MT5_AUTOMATION/01_M1_Is_The_Canonical_Source_Floor|M1 Is the Canonical Source Floor]]
- [[../../13_ATOMIC_CONCEPTS/RTHP_MT5_AUTOMATION/02_MT5_Acquisition_Is_An_Adapter_Not_Engine_Logic|MT5 Acquisition Is an Adapter, Not Engine Logic]]
- [[../../13_ATOMIC_CONCEPTS/RTHP_MT5_AUTOMATION/03_Bar_Known_Time_Is_The_Close_Cut|Bar Known Time Is the Close Cut]]
- [[../../13_ATOMIC_CONCEPTS/RTHP_MT5_AUTOMATION/04_No_Intrabar_Order_Inference_From_M1|No Intrabar Order Inference from M1]]
- [[../../13_ATOMIC_CONCEPTS/RTHP_MT5_AUTOMATION/05_Symbol_Selection_Is_Run_Configuration|Symbol Selection Is Run Configuration]]
- [[../../13_ATOMIC_CONCEPTS/RTHP_MT5_AUTOMATION/06_Missing_Bar_Is_Not_Automatically_Missing_Data|Missing Bar Is Not Automatically Missing Data]]

## Lifecycle boundary

This roadmap is a context-owned delivery. It is **not a replacement or renumbering of ACL-07**, whose existing responsibility remains Unified Validation. It is also not a new central-engine phase.

- [[21_Implementation_Release_and_Operator_Command]]
- [[22_M1_Materializer_Parity_and_Interval_Censoring]]
- [[23_Read_Only_MT5_API_and_No_Trade_Authority]]
- [[24_First_Real_Terminal_Run_Checklist]]
- [[25_Latest_Closed_M1_History_Warmup_Hotfix]]
- [[26_Provider_Closed_Bar_Authority_and_Workstation_Clock_Skew_Hotfix]]

- [[27_Holiday_and_Session_Aware_Gap_Classification]]
- [[28_Cross_Platform_Governance_Hardening]]
- [[29_Real_MT5_Smoke_Train_Evidence]]
