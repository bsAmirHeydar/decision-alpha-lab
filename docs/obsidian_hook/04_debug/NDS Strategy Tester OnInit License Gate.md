---
title: NDS Strategy Tester OnInit License Gate
aliases:
  - NDS OnInit Code 1
  - Phoenix Tester License Bypass
status: implemented
updated: 2026-07-10
---
# NDS Strategy Tester OnInit License Gate

## Symptom

`tester stopped because OnInit returns non-zero code 1`

## Diagnosis

The only `INIT_FAILED` path in the central Phoenix expert was
`FP_EnsureOfflineLicense(true)`. Default research parameters do not carry the
signed live-distribution license payload, so the tester stopped before market
structure or execution logic ran.

## Fixed contract

```text
MQL_TESTER or MQL_OPTIMIZATION
+ matching bypass input enabled
→ tester_bypass report
→ OnInit succeeds

normal chart runtime
→ original offline signed license
→ fail-closed
```

## Inputs

- `InpLicenseAllowStrategyTesterBypass`
- `InpLicenseAllowOptimizationBypass`
- `InpPrintLicenseTesterBypass`

## Expected Journal line

```text
FP_LICENSE status=tester_bypass context=visual_strategy_tester live_license_enforcement=unchanged
```

## Related

- [[../03_architecture/Phase 52 NDS Hook Limit F123 Execution]]
- [[../../nds_entry_architecture/phase52_hook_limit_f123_execution/09_strategy_tester_license_gate|Strategy Tester License Gate]]
