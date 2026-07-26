---
title: Phase 55 No-Trade Root Cause and Engine Integration Fix
status: implemented_reference_pending_metaeditor
version: 1.1.0
updated: 2026-07-16
---
# 17 — No-Trade Root Cause and Engine Integration Fix

## Incident statement

The first Phase 55 delivery could compile statically and pass synthetic geometry tests while a Strategy Tester run still produced zero trades. The problem was not one isolated threshold. It was a chain of integration defects that collectively hid the intended setup from the executable path.

## Confirmed causes

### 1. Wrong dedicated tester default

`NDSHookLimitF123Backtest` still defaulted to the legacy `TERMINAL_F123` profile. The 86.4 profile existed in code but was not the active profile unless the correct input was changed manually.

The actual tester input is:

```text
InpBTTradeProfile
```

It is not `InpNDSHookTradeProfile`; that name belongs to the central Phoenix expert. Phase 55 v1.1 makes the dedicated backtest default explicit:

```text
InpBTTradeProfile = HOOK_864_CYCLE_R1
```

### 2. Sparse FAST scan for a low-frequency setup

The old dedicated tester default used the FAST profile: 1200 bars and L scales 2/3/5/8. A valid Hook family that also has x-count 3 or 4, a confirmed terminal, a canonical X closure, remains alive, and has not consumed its first 86.4 arrival can be rare. A zero result from a short scan was therefore ambiguous.

The dedicated tester now defaults to PARITY:

```text
5000 closed bars
L = 2, 3, 5, 8, 13, 21, 34, 55
```

FAST is still available for performance checks, but it is no longer the diagnostic default for this setup.

### 3. Phase02 terminal was mistaken for cycle closure

The v1.0 adapter used `FP_HookP02SequenceCycleClosed(seq)` as the setup's cycle-close proof. That helper proves Phase02 terminal availability. The Hook architecture, however, has a separate canonical lifecycle engine:

```text
Phase02 sequence
→ Phase03 Y-axis reference
→ Phase04 50% X-closure lifecycle
```

The setup now consumes `FP_HookPhase04Lifecycle.x_closed` and `origin_return_penetrated` from the existing Phase03/04 engines. No second node detector, Hook builder, Y extractor, or closure algorithm was created.

### 4. First-arrival gate used the wrong field

`seq.retracement_ratio` describes Phase02 terminal geometry. It does not prove whether market price touched the 86.4 limit after the Phase04 closure was known. Using it as the first-arrival gate could reject valid candidates or accept a temporally impossible order.

The corrected bridge scans the same canonical closed `MqlRates[]` supplied by the engine. It starts at the Phase04 closure candle and records the first positive low or negative high that reaches 86.4.

The closure candle is intentionally included. If closure and 86.4 occur in the same closed candle, the order could not have been placed after observing the closure, so the first arrival is consumed and the setup fails closed.

### 5. Zero-trade reports had no gate funnel

The prior run report exposed only a final “no eligible sequence” reason. It could not distinguish:

- no Phase02 sequences;
- no valid family;
- no x3/x4 sequence;
- no Phase04 evidence;
- no X closure;
- all cycles dead;
- first 86.4 already consumed;
- broker/execution rejection.

The run and session reports now publish a deterministic funnel:

```text
total
→ canonical valid
→ valid family
→ family allowed
→ confirmed terminal
→ valid crown
→ x3/x4
→ mature/capped
→ Phase04 evidence found
→ Phase04 X closed
→ alive after closure
→ first 86.4 untouched
→ execution ready
```

The first zero counter is reported as `dominant_blocker`.

## Corrected authority path

```text
Canonical timebase
→ existing F/Rally detector
→ existing Hook Phase02 sequence snapshot
→ existing Hook Phase03 Y records
→ existing Hook Phase04 lifecycle records
→ read-only 86.4 first-arrival evidence bridge
→ existing Hook trade selector
→ existing broker capability/risk/one-exposure adapter
```

The bridge has no order, network, file, chart, or secret authority. It cannot create a Hook or change node count. It only binds Phase04 lifecycle evidence and closed-price arrival evidence to the exact Phase02 sequence identity.

## Tester behavior after fix

On initialization, the Journal must show:

```text
trade_profile=HOOK_864_CYCLE_R1
runtime_profile=PARITY
```

Each scheduled report prints Phase02, Phase03, Phase04, funnel, action, and reason. At deinitialization, the session report aggregates closure, evidence, untouched, ready, paper-ready, sent, pending, held, cancelled, and blocked counts.

## Remaining external proof

Repository QA cannot prove that MetaEditor accepts every include, that a broker allows a particular pending distance, or that the tested history contains a qualifying setup. Windows MetaEditor compilation and MT5 Strategy Tester logs remain required external evidence.
