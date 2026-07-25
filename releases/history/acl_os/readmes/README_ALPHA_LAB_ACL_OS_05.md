---
title: Alpha Lab ACL-OS 05 — Immutable Batch and Artifact Store
status: accepted-reference
version: 1.0.0
updated: 2026-07-18
tags: [acl-os, acl-05, release]
---

# Alpha Lab ACL-OS 05 — Immutable Batch and Artifact Store

ACL-05 is the reference implementation that freezes accepted ACL-04 Setup Candidates and all research-defining contracts into one immutable, content-addressed Batch. It validates the full upstream manifest and receipts, preserves candidate behavior, segregates diagnostics, binds dataset known-time cuts, label maturity, purged walk-forward splits, environment and budgets, emits a byte-addressed object store and hands a non-promotional contract to ACL-06.

## Claim ceiling

`RESEARCH_BATCH_FREEZE_REFERENCE_ONLY`

This delivery does not run research, prove alpha, compile MetaTrader code, establish broker parity, submit orders or authorize capital.

## Main paths

- Python: `tools/strategy_factory/acl_os/acl_05`
- Schemas/policies: `registry/acl_os/acl_05`
- Tests: `lab/11_strategy_factory/acl_os/tests_acl_05`
- Fixtures and generated reference: `lab/11_strategy_factory/acl_os/fixtures/acl_05`
- MQL5 static mirror: `lab/11_strategy_factory/mql5/Include/AlphaLab/ACL_OS/ACL05`
- Canonical Obsidian notes: `docs/alpha_lab_master_architecture/context_lifecycle_os/05_RESEARCH_BATCH`
- Phase evidence: `docs/alpha_lab_master_architecture/context_lifecycle_os/12_PHASE_DELIVERIES/ACL_05`
- Atomic concepts: `docs/alpha_lab_master_architecture/context_lifecycle_os/13_ATOMIC_CONCEPTS/ACL_05`

## Verification

Run the ACL-05 tests, ACL-04 regression tests, Python compilation and full QA module. MetaEditor compilation remains a separate environment-specific obligation.
