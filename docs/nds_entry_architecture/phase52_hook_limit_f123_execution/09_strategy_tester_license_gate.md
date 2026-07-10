---
title: Strategy Tester License Gate
status: implemented
version: 1.0.0
updated: 2026-07-10
---
# Strategy Tester License Gate

## Defect

The central Phoenix EA entered `OnInit()` through the offline distribution
license before any structural or execution module. The default research inputs
do not contain a signed account/server-bound token, passphrase, or hidden gate
values. Therefore `FP_EnsureOfflineLicense(true)` returned `false`, and
`OnInit()` returned `INIT_FAILED` before the Strategy Tester could begin.

The Phase 52 order engine was not the source of the failure. The failure was an
authority-boundary mismatch between live EX5 licensing and local historical
research.

## Contract

```text
Live chart / live terminal
→ signed offline license remains mandatory and fail-closed

Strategy Tester
→ optional explicit tester bypass
→ OnInit continues
→ normal Hook/entry/F123 logic runs

Optimization
→ optional explicit optimization bypass
→ each agent can initialize without account/server-bound research credentials
```

## Inputs

```text
InpLicenseAllowStrategyTesterBypass = true
InpLicenseAllowOptimizationBypass = true
InpPrintLicenseTesterBypass = true
```

The bypass is accepted only when the runtime itself reports `MQL_TESTER` or
`MQL_OPTIMIZATION`. The same inputs cannot bypass licensing on a normal chart.

## Audit message

One line is emitted per EA instance:

```text
FP_LICENSE status=tester_bypass context=visual_strategy_tester live_license_enforcement=unchanged
```

Possible contexts:

- `strategy_tester`
- `visual_strategy_tester`
- `optimization`

## Fail-closed preservation

When both bypass inputs are false, Strategy Tester follows the same signed
license path as live runtime. On a live chart, tester flags are false and the
original license engine is always used.
