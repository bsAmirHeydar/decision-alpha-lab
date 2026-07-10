# Phase 14 Hotfix 001 — Signal Source Direct Dependency

## Failure

MetaEditor rejected `CGX_SignalSource.mqh` at the `CCGC_ConfirmationField` member declaration because the module declared and used the concrete class without directly including its defining header.

## Root cause

`CGX_SignalSource.mqh` included `CGT_Time.mqh` and `CGX_Types.mqh`, but neither header is the authority that defines `CCGC_ConfirmationField`. The module therefore depended on an accidental transitive include that was not present in the Phase 14 compile path.

## Fix

The signal-source module now directly includes:

```text
IntermarketDivergenceExecution/CG/CGC_ConfirmationField.mqh
```

The include is placed before the `CCGX_SignalSource` class declaration and before the `CCGC_ConfirmationField m_confirmation_field` member.

## Scope

No signal, freshness, execution, risk, stop, target, sizing, routing, or lifecycle behavior changes. This is a compile-contract correction only.

## Regression guard

The Phase 14 contract test now asserts that the defining header is explicitly present and ordered before the signal-source class declaration.
