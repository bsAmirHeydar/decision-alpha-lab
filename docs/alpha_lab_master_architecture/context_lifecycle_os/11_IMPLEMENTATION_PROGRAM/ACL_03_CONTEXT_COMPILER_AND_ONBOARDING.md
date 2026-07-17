---
title: ACL-03 Context Compiler and Onboarding
status: accepted-reference-implementation
version: 1.0.0
updated: 2026-07-17
tags: [acl-os, implementation-program, acl-03]
---
# ACL-03 Context Compiler and Onboarding

ACL-03 consumes only an ACL-02 Context package whose exact source snapshot is approved by the semantic owner and an independent reviewer under ACL-00 authority. It freezes the source, compiles deterministic detector, occurrence, known-time and feature-binding IR, emits least-privilege adapter contracts and closed schemas, executes golden replay, publishes an onboarding matrix and creates a bounded ACL-04 handoff.

## Delivered reference implementation

- `tools/strategy_factory/acl_os/acl_03/`
- `registry/acl_os/acl_03/`
- `lab/11_strategy_factory/acl_os/tests_acl_03/`
- `lab/11_strategy_factory/acl_os/fixtures/acl_03/`
- `lab/11_strategy_factory/mql5/Include/AlphaLab/ACL_OS/ACL03/`
- [[00_00_EXECUTIVE_DELIVERY_INDEX]]

## Authority boundary

ACL-03 may compile and project approved semantics. It may not create Setup search authority, train models, establish statistical eligibility, generate unrestricted executable code, submit orders, activate capital or authorize production. Adapter implementations remain obligations until separately qualified.

## Next phase

[[ACL_04_DUAL_SETUP_FACTORY]] consumes only the signed, immutable ACL-03 handoff and is forbidden from altering Context semantics or known-time guards.
