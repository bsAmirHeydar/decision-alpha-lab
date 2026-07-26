---
title: "FP-I01 Local Acceptance Runbook"
tags: [exp0019, faerie-protocol, fp-i01, compatibility, adapter-contracts]
status: normative
phase: FP-I01
phase_version: 1.0.0
doc_version: 1.0.0
last_updated: 2026-07-13
language: en
---

# FP-I01 Local Acceptance Runbook

## Preconditions

- Run from the Decision Alpha Lab repository root.
- FP-I00 patch and Implementation Program are already committed.
- The FP-I01 patch has been expanded.
- MetaTrader 5 and MetaEditor are installed for the compile gate.

## Automated checks

```powershell
& .\lab_infrastructure\EXP0019_faerie_protocol\phase_i01\powershellun_exp0019_fp_i01_checks.ps1 -RepoRoot $PWD
```

## Compile gate

```powershell
& .\lab_infrastructure\EXP0019_faerie_protocol\phase_i01\powershell\compile_exp0019_fp_i01_compatibility.ps1 -RepoRoot $PWD
```

Inspect every generated log for `0 errors`. Preserve logs outside the patch-owned source tree or attach them to the local evidence folder before updating phase status.

## Source-control review

```powershell
git status --short
git diff --check
git diff --stat
git diff -- mql5/Include/IntermarketDivergenceExecution/CG
git diff -- mql5/Include/DayeTrader/EXP0018
```

The two final diff commands must be empty for FP-I01.

## Acceptance outcome

- `PASS`: all Python/static checks pass, previous entry points exist, dependency hashes match, and MetaEditor logs contain zero errors.
- `PENDING_LOCAL_METAEDITOR`: repository/static evidence passes but compile logs are not available.
- `BLOCKED`: any pin, adapter, authority, previous-context, or compile check fails.
