---
id: UCPS-N1-02-RUNBOOK
title: "UC04-W1B-N1 One-Click Windows Runbook"
type: runbook
status: canonical
domain: unified-consolidation-platform-seal
version: 1.0.0
created: 2026-07-28
updated: 2026-07-28
tags:
  - consolidation
  - uc04
  - windows
  - metaeditor
  - mt5
---
# UC04-W1B-N1 One-Click Windows Runbook

## Preconditions

- The W1B-N1 patch is committed.
- The tracked working tree is clean.
- The repository is located under the intended MetaTrader terminal data folder or `-TerminalDataPath` is supplied.
- The matching `terminal64.exe` is closed.
- Python 3 is available.
- The runtime symbol exists in the target terminal. The script does not read market data, but MetaTrader needs a chart symbol to launch a startup script.

## Command

From repository root:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "tools/consolidation/uc04w1bn1/Invoke-UC04W1BNativeHostQualification.ps1" -RepositoryRoot (Get-Location).Path -RuntimeSymbol "#USSPX500"
```

For a different broker symbol, replace only `-RuntimeSymbol`. Explicit path parameters remain available:

- `-MetaEditorPath`
- `-TerminalPath`
- `-TerminalDataPath`
- `-TerminalCommonFilesPath`

## Outputs

All run products are written outside the repository under:

`%LOCALAPPDATA%\AlphaLab\runs\uc04w1b\native_host_qualification\<UTC_RUN_ID>`

A successful run ends with:

- `native_acceptance_receipt.json`
- `independent_native_review.json`
- compile logs and EX5 copies
- runtime CSV
- sanitized evidence ZIP
- optional non-apply cutover candidate under the sibling `cutover_candidates` directory

## Failure behavior

Any missing target, stale compile artifact, compile warning, runtime timeout, failed fixture, duplicate runtime CSV, hash mismatch, running terminal, dirty tracked tree or repository mutation terminates the run. Temporary terminal files are restored in `finally`.
