---
id: UCPS-0C8E3F75B291
title: "UC04-W1B Windows Runbook"
type: runbook
status: canonical
domain: unified-consolidation-platform-seal
version: 1.0.0
created: 2026-07-27
updated: 2026-07-27
tags:
  - consolidation
  - uc04
  - w1b
  - windows
  - mt5
---
# UC04-W1B Windows Runbook

## Preconditions

- W0 and W1A patches are applied and committed.
- MetaEditor 64-bit and its matching MetaTrader 5 terminal are installed.
- The target terminal is closed.
- Python 3 is available as `python` or `py -3`.
- The repository working tree is not modified by the runner.

## Execution

Run from the repository root:

`powershell -ExecutionPolicy Bypass -File tools/consolidation/uc04w1b/Invoke-UC04W1BQualification.ps1`

Optional path parameters are available for broker-specific MetaTrader installations:

- `-MetaEditorPath`
- `-TerminalPath`
- `-TerminalDataPath`
- `-RuntimeSymbol`

The runner resolves the terminal data folder from `origin.txt` when possible and refuses ambiguous resolution.

## Outputs

The run creates an evidence directory under `.alpha/runs/uc04w1b/native_qualification`. A successful run contains compile logs, EX5 copies, the runtime CSV, `native_acceptance_receipt.json`, and `independent_native_review.json`. Unless disabled, it also generates a non-apply cutover candidate under `.alpha/runs/uc04w1b/cutover_candidates`.

## Failure handling

Any missing target, nonzero MetaEditor exit, warning, compile error, runtime timeout, missing CSV, failed fixture, hash mismatch, or pre-existing running terminal stops the process. Temporary terminal files are restored in all cases.

## Navigation

- [[01_UNIFIED_CONSOLIDATION_AND_PLATFORM_SEAL/15_UC04_W1B_NATIVE_QUALIFICATION/00_MOC|W1B records MOC]]
