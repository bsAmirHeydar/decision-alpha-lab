---
title: ACL-03 Context Compiler and Onboarding — MOC
status: accepted-reference
version: 1.0.0
updated: 2026-07-17
tags: [acl-os, acl-03, moc]
---
# ACL-03 Context Compiler and Onboarding

## Control flow

`ACL-02 semantic package → frozen source snapshot → authority and approval binding → compiler plan → detector / occurrence / known-time / feature IR → adapter contracts → generated schemas → golden replay → onboarding matrix → bounded ACL-04 handoff`

## Canonical artifacts

- Python: `tools/strategy_factory/acl_os/acl_03/`
- Policies and schemas: `registry/acl_os/acl_03/`
- Tests: `lab/11_strategy_factory/acl_os/tests_acl_03/`
- Reference fixtures: `lab/11_strategy_factory/acl_os/fixtures/acl_03/`
- MQL5 static mirror: `lab/11_strategy_factory/mql5/Include/AlphaLab/ACL_OS/ACL03/`
- Phase status: [[ACL_03_STATUS]]
- Atomic concepts: [[00_MOC|ACL-03 Atomic Concepts MOC]]

## Phase documentation

- [[01_01_MISSION_SCOPE_AND_NON_CLAIMS]]
- [[02_02_ACL_00_AUTHORITY_BINDING]]
- [[03_03_ACL_01_IDENTITY_LOCATOR_BINDING]]
- [[04_04_ACL_02_SEMANTIC_INPUT_BINDING]]
- [[05_05_COMPILER_ARCHITECTURE]]
- [[06_06_SOURCE_FREEZE_AND_SNAPSHOT]]
- [[07_07_COMPILATION_PLAN_DAG]]
- [[08_08_DETECTOR_IR]]
- [[09_09_GUARD_DSL_AND_EXECUTION_PROHIBITION]]
- [[10_10_STATE_MACHINE_DETERMINISM]]
- [[11_11_OCCURRENCE_IDENTITY_IR]]
- [[12_12_OCCURRENCE_DEDUPLICATION_AND_REVISION]]
- [[13_13_KNOWN_TIME_GUARD_IR]]
- [[14_14_LATE_DATA_AND_CORRECTION_POLICY]]
- [[15_15_FEATURE_BINDING_IR]]
- [[16_16_FEATURE_ORDER_AND_SCHEMA_FREEZE]]
- [[17_17_DATA_ADAPTER_CONTRACTS]]
- [[18_18_CALENDAR_ADAPTER_CONTRACT]]
- [[19_19_FEATURE_VIEW_ADAPTER_CONTRACT]]
- [[20_20_CAPABILITY_SANDBOX]]
- [[21_21_GENERATED_SCHEMA_EMISSION]]
- [[22_22_GOLDEN_CASE_COMPILATION]]
- [[23_23_DETERMINISTIC_GOLDEN_REPLAY]]
- [[24_24_REPLAY_TRACE_AND_DIAGNOSTICS]]
- [[25_25_GENERATED_FILE_POLICY]]
- [[26_26_ATOMIC_OUTPUT_PUBLICATION]]
- [[27_27_OUTPUT_ARTIFACT_MANIFEST]]
- [[28_28_COMPILATION_RECEIPT]]
- [[29_29_ONBOARDING_GATE_MATRIX]]
- [[30_30_OPEN_OBLIGATIONS_AND_ALLOWED_ACTIONS]]
- [[31_31_ACL_04_HANDOFF_ENVELOPE]]
- [[32_32_EXTENSION_POINTS]]
- [[33_33_PLUGIN_CONFORMANCE]]
- [[34_34_SECURITY_THREAT_MODEL]]
- [[35_35_SOURCE_TAMPER_AND_APPROVAL_INVALIDATION]]
- [[36_36_PATH_SYMLINK_AND_OUTPUT_SAFETY]]
- [[37_37_TEST_STRATEGY]]
- [[38_38_MUTATION_AND_NEGATIVE_TESTS]]
- [[39_39_MQL5_STATIC_MIRROR]]
- [[40_40_CLI_AND_OPERATOR_WORKFLOW]]
- [[41_41_CLEAN_CHECKOUT_REPRODUCTION]]
- [[42_42_MIGRATION_AND_VERSIONING]]
- [[43_43_OBSERVABILITY_REASON_CODES]]
- [[44_44_DEFINITION_OF_DONE]]
- [[45_45_HANDOFF_TO_ACL_04]]

## Upstream and downstream

- Upstream: [[ACL_02_CONTEXT_STANDARD_AND_INTAKE]]
- Downstream: [[ACL_04_DUAL_SETUP_FACTORY]]
- Kernel authority: [[ACL_00_CONSTITUTION_AND_AUTHORITY]]
- Identity and locator: [[ACL_01_REPOSITORY_IDENTITY_AND_LOCATOR]]
