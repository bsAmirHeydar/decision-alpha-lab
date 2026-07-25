---
title: CTX_RTHP_CROSS_SYMBOL_CYCLE_DIVERGENCE_V1 ACL-03 Onboarding Report
status: generated
context_id: CTX_RTHP_CROSS_SYMBOL_CYCLE_DIVERGENCE_V1
context_version: 1.0.2
report_digest: sha256:4f328ce14246ba492921120031b55c8cb331146911c0d504110f08410fee855f
---
# ACL-03 Onboarding Report

> [!warning] Generated evidence
> This file is generated from machine-readable artifacts. Do not edit it manually. It does not prove alpha, external data quality, runtime parity, security hardening or capital authorization.

## Decision

- Decision: `COMPILED_WITH_OBLIGATIONS`
- Highest state: `CONTEXT_COMPILED`
- Claim ceiling: `CONTEXT_COMPILATION_REFERENCE_ONLY`

## Gate matrix

| Gate | Status | Reason codes |
|---|---|---|
| source_frozen | PASS | — |
| authority_bound | PASS | — |
| ir_compiled | PASS | — |
| golden_replay | PASS | — |
| adapter_contracts | PASS | — |
| adapter_implementation | BLOCKED | ACL03_ADAPTER_IMPLEMENTATION_REQUIRED |
| external_data_qualification | BLOCKED | ACL14_REAL_CONTEXT_EVIDENCE_REQUIRED |
| research_entry | BLOCKED | ACL04_SETUP_FACTORY_REQUIRED, ACL05_IMMUTABLE_BATCH_REQUIRED |
| live_activation | BLOCKED | ACL11_RUNTIME_PARITY_REQUIRED, ACL12_SECURITY_HARDENING_REQUIRED, ACL14_CAPITAL_AUTHORIZATION_REQUIRED |

## Open obligations

- `ACL03_ADAPTER_IMPLEMENTATION_REQUIRED`
- `ACL04_DUAL_SETUP_FACTORY_REQUIRED`
- `ACL05_IMMUTABLE_BATCH_REQUIRED`

## Allowed next actions

- `IMPLEMENT_REGISTERED_ADAPTERS`
- `ADD_DOMAIN_GOLDEN_CASES`
- `REQUEST_ACL04_SETUP_SEARCH_AUTHORITY`
