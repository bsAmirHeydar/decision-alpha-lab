# NDS Phase 52 Hotfix 01 — Strategy Tester OnInit Audit Report

## Incident

```text
2026.07.10 20:31:29.906 Core 1 tester stopped because OnInit returns non-zero code 1
```

## Source diagnosis

The central EA had a single `INIT_FAILED` return in `OnInit()`:

```mql5
if(!FP_EnsureOfflineLicense(true))
   return INIT_FAILED;
```

`FP_LoadOfflineLicenseConfig()` forced the offline distribution license to:

- enabled;
- fail-closed;
- account-bound;
- server-bound;
- password-required;
- hidden-gates-required;
- expiry-required.

The signed token is carried through `InpPhaseModelProfile`. Its default is an
empty string. `InpRenderMemo` and all hidden gate seeds also default to empty or
zero. A default Strategy Tester run therefore reaches
`license_token_parse_failed`, returns false from `FP_EnsureOfflineLicense()`,
and stops before `FP_Run()` or the Phase 52 trade engine executes.

## Root cause classification

```text
Runtime authority defect
not Hook detection
not limit-entry geometry
not F123 exit
not broker order rejection
```

The live EX5 distribution license was applied unchanged to local historical
research. Tester agents need a distinct, explicit authority path.

## Implemented fix

The EA now checks MQL runtime properties before invoking the signed license:

```text
MQL_OPTIMIZATION + InpLicenseAllowOptimizationBypass
→ optimization bypass

MQL_TESTER + InpLicenseAllowStrategyTesterBypass
→ Strategy Tester bypass

otherwise
→ original signed offline license
```

The bypass builds a positive runtime license report so downstream safety gates
see a coherent authorized research state. It does not change the live license
engine or its fail-closed behavior.

## Inputs

```text
InpLicenseAllowStrategyTesterBypass = true
InpLicenseAllowOptimizationBypass = true
InpPrintLicenseTesterBypass = true
```

## Expected tester log

```text
FP_LICENSE status=tester_bypass context=strategy_tester live_license_enforcement=unchanged
```

Visual mode uses `context=visual_strategy_tester`; optimization uses
`context=optimization`.

## Security boundary

A normal chart does not report `MQL_TESTER` or `MQL_OPTIMIZATION`, so the bypass
branch is unreachable there. Live runtime still requires the signed token,
passphrase, account/server match, expiry, signature, and hidden gates.

## Version

```text
FlagCountingPhoenixExperiment.mq5 = 18.41
```

## Validation

- Phase 52.1 tester OnInit contract QA: PASS
- Phase 52 Hook trade contract QA: PASS
- Phase 51 Entry contract QA: PASS
- NDS Hook contract QA: PASS
- Engineering policy: 0 errors, 0 warnings
- MQL5 compatibility scan: 0 errors, 0 warnings
- Repository layout: 0 missing directories
- Engineering OS vault: 0 errors, 0 warnings
- MQL lexical balance: PASS

MetaEditor is unavailable in the build environment. Final compilation and one
visual Strategy Tester run remain required on the operator terminal.
