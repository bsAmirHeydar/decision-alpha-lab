# NDS F2 Waist-Break Point-2 Limit — Audit Report

## Scope

This patch corrects the dedicated F2 Strategy Tester setup and formalizes it as a separate canonical execution contract.

## Final contract

```text
Complete unconfirmed F2 two-leg body
→ F2 Waist = Point 1
→ stage limit strictly beyond F2 Waist
→ fill = executable Point 2
→ stop strictly beyond direct parent F1 Waist
→ target = F2 Leg2 endpoint / end of F2 flag
```

## Critical correction

The previous implementation waited for `F2.confirm`. That was incorrect. In the waist-break branch, confirmation occurs only after price returns to and re-breaks F2 Leg2. F2 Leg2 is this setup's target, so confirmed F2 is necessarily too late for entry.

The corrected trigger is the first non-lookahead bar on which the complete F2 body and its Leg2 endpoint are observable.

## Existing Canon reused

- `FLAG_COUNTING_SEQUENCE_CONTRACT_V3`: F2 waist-break branch maps `1 = F2 Waist`, `2 = node that breaks F2 Waist`.
- `FLAG_COUNTING_STATE_MACHINE_V3`: F2 waist break is valid while F2 Origin remains intact.
- `ZONE-AF-0008`: F2 waist contact can become Point 1 and the following hit/extension becomes Point 2.
- Phoenix canonical rates, nodes, F1 lifecycle, F2 body builder and direct-parent resolution.
- Phase-52 symbol normalization, sizing, broker preflight and accepted-retcode helpers.

## New execution authorization

The direct test profile now has an explicit stable risk contract:

```text
risk edge = direct parent F1 Waist
completion edge = F2 Leg2
```

This does not change the general Zone doctrine for unrelated F2 contexts.

## Runtime changes

### Trigger

Before:

```text
confirmed F2 → order
```

After:

```text
complete unconfirmed F2 body → order
```

### Entry

- Bullish: Buy Limit at least one trade tick below F2 Waist.
- Bearish: Sell Limit at least one trade tick above F2 Waist.

The strict penetration means equality remains Point 1 and fill beyond it is Point 2.

### Stop

- Bullish: at least one trade tick below direct parent F1 Waist.
- Bearish: at least one trade tick above direct parent F1 Waist.

No fallback stop is invented.

### Target

Exactly `f2.leg2.price`.

### Pending lifecycle

If F2 Leg2 is touched while the order remains pending, the target has been consumed without entry and the pending order is removed. The full detector is not rebuilt on the pending path.

### F2 extension

A pre-entry Leg2 extension creates a new F2 body version and target identity. The old pending is cancelled after its target is consumed, and the extended body may arm on a later bar.

## Performance correction

The previous fast detector still delegated to `FP_DetectScale`, which internally constructed Hook branches. The new detector directly reuses:

```text
canonical node builder
→ raw-origin F1 chains
→ F1 lifecycle
→ F2 body/lifecycle
```

It does not call Hook construction, the general detector, F3, ownership, renderer, CSV or diagnostics.

## Files changed

### MQL5

- `mql5/Experts/FlagCounting/NDSF2WaistLimitBacktest.mq5`
- `mql5/Include/FlagCountingPhoenix/FP_NDSF2FastDetector.mqh`
- `mql5/Include/FlagCountingPhoenix/FP_NDSF2WaistBreakSetupRules.mqh`
- `mql5/Include/FlagCountingPhoenix/FP_NDSF2WaistTradeTypes.mqh`
- `mql5/Include/FlagCountingPhoenix/FP_NDSF2WaistTradeRules.mqh`
- `mql5/Include/FlagCountingPhoenix/FP_NDSF2WaistTradeEngine.mqh`
- `mql5/Include/FlagCountingPhoenix/FP_NDSF2WaistBacktestEngine.mqh`

### Documentation

- detailed setup package under `docs/contexts/legacy/nds/entry/f2_waist_break_point2_limit/`;
- corrected Obsidian setup and runtime notes;
- updated entry MOC and architecture indexes.

### QA

- corrected legacy F2 backtest QA;
- added dedicated waist-break Point-2 contract QA.

## Validation results

```text
NDS F2 waist-break Point-2 contract QA: PASS
Legacy F2 fast backtest QA updated: PASS
Project include resolution: 0 missing project includes
MQL lexical balance: PASS
Engineering policy: 0 errors, 0 warnings
MQL5 compatibility: 0 errors, 0 warnings
Repository layout: 0 missing directories
```

## Environment limitation

MetaEditor and Strategy Tester are not available in the build environment. Final MQL5 compilation and real-tick tester execution must be confirmed locally.
