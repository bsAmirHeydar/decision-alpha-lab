---
id: UCPS-4D89C177A2F0
title: "UC04-W1B Native Qualification Execution Contract"
type: execution-contract
status: canonical
domain: unified-consolidation-platform-seal
version: 1.0.0
created: 2026-07-27
updated: 2026-07-27
tags:
  - consolidation
  - uc04
  - w1b
  - mql5
  - metaeditor
---
# UC04-W1B Native Qualification Execution Contract

## Purpose

UC04-W1B-Q closes the operational gap left intentionally by W1A. It provides one deterministic Windows runner that captures native MetaEditor compilation and MetaTrader runtime evidence without modifying tracked production sources.

## Native matrix

The runner compiles the ten frozen consumers, the W1A Expert self-test, and the W1B script runner. Every target must produce an EX5 and a log containing zero errors and zero warnings. Source, log, and EX5 SHA-256 values are bound into the native receipt.

## Runtime contract

The runtime program is a test-only MQL5 script. It executes thirteen frozen datetime vectors, compares the historical helper body with the W1A reference implementation byte-for-byte, writes one CSV under MT5 Common Files, and exits. Live trading and DLL import remain disabled.

## Isolation

- compilation occurs in `.alpha/runs/uc04w1b/native_qualification/<run>/compile_workspace`;
- the terminal receives only a temporary test EX5;
- any pre-existing EX5 at the test location is backed up and restored;
- tracked repository sources are never compiled in place;
- terminal test files are removed or restored in `finally`;
- the target terminal must be closed before execution.

## Accepted output

A native receipt is acceptable only when all twelve compile targets are clean, all thirteen runtime rows pass, the summary row is PASS, and all authority fields remain false.

## Evidence

- `tools/consolidation/uc04w1b/Invoke-UC04W1BQualification.ps1`
- `mql5/Tests/Scripts/UC04/UC04W1B_DeterministicDateTimeFormatNativeRunner.mq5`
- `registry/consolidation/uc04/w1b/native_execution_contract.json`

## Navigation

- [[01_UNIFIED_CONSOLIDATION_AND_PLATFORM_SEAL/15_UC04_W1B_NATIVE_QUALIFICATION/00_MOC|W1B records MOC]]
