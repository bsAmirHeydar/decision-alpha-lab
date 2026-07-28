---
id: UCPS-UC04COMP-NATIVE-SEAL
title: "UC-04 Native Seal Runbook"
type: runbook
status: active
domain: unified-consolidation-platform-seal
version: 1.0.0
created: 2026-07-28
updated: 2026-07-28
tags:
  - consolidation
  - uc04
  - mql5
  - native-seal
---
# UC-04 Native Seal Runbook

The native seal is performed by `Invoke-UC04CompleteNativeSeal.ps1` on the installation host. It compiles every target in the canonical contract inside an isolated workspace, requires zero errors and zero warnings, executes the shared-primitives self-test with live trading and DLL imports disabled, independently reviews all hashes and may then materialize the accepted UC-04 exit.

Evidence is written outside the repository under `%LOCALAPPDATA%/AlphaLab/runs/uc04_complete/native_seal`. The runner must prove that tracked source files are unchanged before acceptance records are written.

The `-FinalizeRepository` switch is valid only after compile and runtime PASS. It creates `uc04_acceptance.json` and `uc05_handoff_decision.json`; it does not authorize UC-05 implementation or any trading authority.
