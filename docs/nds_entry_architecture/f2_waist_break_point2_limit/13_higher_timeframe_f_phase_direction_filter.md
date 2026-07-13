# 13 — Higher-Timeframe F-Phase Direction Filter

## 1. Purpose

This filter restricts the lower-timeframe F2 Waist-Break Point-2 setup to the direction of the current canonical F phase on a configurable higher timeframe.

Default:

```text
Higher timeframe = H1
Filter enabled = true
```

The filter is not a moving-average trend filter, candle-color filter, swing-slope approximation, or generic momentum filter. It reuses the canonical Phoenix F1/F2/F3 and Hook/ND architecture.

## 2. Direction contract

```text
Higher timeframe in bullish F phase
→ lower timeframe may create Buy setups only

Higher timeframe in bearish F phase
→ lower timeframe may create Sell setups only

Higher timeframe in Hook/ND phase
→ no new lower-timeframe setup

Higher timeframe ambiguous, unavailable, or without canonical F
→ no new lower-timeframe setup
```

The gate has higher authority than the parallel-context and hedge switches. For example:

```text
HTF bullish F
+ opposite-direction hedge enabled
→ new Sell setup is still blocked
```

The hedge switch controls coexistence of already-authorized lower-timeframe contexts. It cannot override higher-timeframe directional authorization.

## 3. Canonical phase classification

The higher-timeframe classifier loads closed bars only and runs the existing Phoenix sequence engine with:

```text
scan_hooks = true
scan_f1 = true
scan_f2 = true
scan_f3 = true
strict canonical ownership = true
```

It selects the most recent visible canonical F event using this deterministic order:

1. latest observable structural timestamp;
2. highest final canonical rank;
3. highest ownership rank;
4. highest F level;
5. larger scale;
6. later event id.

A canonical F event must:

- be visible on the main semantic stream;
- be F1, F2, or F3;
- have a valid bullish or bearish direction;
- not be invalidated;
- contain a complete `Origin → Leg1 → Waist → Leg2` body;
- have a renderable semantic state.

## 4. F versus Hook ownership

The classifier also finds the latest visible Hook/ND context.

```text
latest Hook/ND time >= latest canonical F time
→ current phase = Hook/ND
→ gate closed

latest canonical F time > latest Hook/ND time
→ current phase = F
→ direction inherited from selected F event
```

Equality is fail-closed. A Hook/ND context appearing on the same structural timestamp as the latest F prevents a new entry until a later canonical F reclaims phase authority.

This rule is intentionally stricter than simply reading the direction of the last F label. It enforces the user requirement that the higher timeframe must currently be in F, not merely have a historical F somewhere behind the present Hook phase.

## 5. Closed-bar and no-lookahead contract

The filter excludes the live higher-timeframe bar.

```text
H1 open bar = not used
latest closed H1 structure = decision authority
```

The snapshot is refreshed only when the higher-timeframe open-bar timestamp changes. Therefore the full canonical higher-timeframe pass runs once per new H1 bar, not on every lower-timeframe bar or tick.

If higher-timeframe history is temporarily unavailable, the filter retries on subsequent lower-timeframe cycles and remains fail-closed until a valid snapshot exists.

## 6. Pending-order lifecycle

Default:

```text
InpF2BTCancelPendingWhenHigherTimeframeDisallows = true
```

On each higher-timeframe phase refresh:

- bullish F keeps managed Buy pending orders and cancels managed Sell pending orders;
- bearish F keeps managed Sell pending orders and cancels managed Buy pending orders;
- Hook/ND, ambiguous, no-F, or data-not-ready cancels all managed pending orders.

Only still-unfilled orders are cancelled. Existing positions are not force-closed by an HTF phase change. They continue under their original SL and selected exit mode.

This separation is deliberate:

```text
HTF filter = entry authorization
SL / fixed F2 exit / dynamic F3 retest = position exit authority
```

## 7. Interaction with existing controls

The processing order is:

```text
HTF phase gate
→ lower-timeframe F2 setup construction
→ RR filter and entry repricing
→ overlap arbitration
→ same-direction / hedge context policy
→ broker preflight and order send
```

Consequences:

- disallowed directions are removed before RR and overlap work;
- overlap arbitration compares only directionally authorized candidates;
- same-direction multiple contexts remain allowed by their own input;
- opposite-direction hedge is possible only when both directions have independently been authorized over time and existing positions remain open;
- a currently bullish HTF snapshot cannot generate a new Sell order.

## 8. Inputs

```text
InpF2BTUseHigherTimeframeFPhaseFilter = true
InpF2BTHigherTimeframe = PERIOD_H1
InpF2BTUseHigherTimeframeF1ToF2ConfirmationWindow = true
InpF2BTCancelPendingWhenHigherTimeframeDisallows = true
```

The higher-timeframe detector uses an internal cached canonical profile:

```text
closed bars = 900 requested / 180 minimum
scales = 2, 3, 5, 8, 13
max events = 2400
max hooks = 2400
```

These values are not exposed in the first operational version to avoid unnecessary optimization degrees of freedom. They can be promoted to inputs later only if profiling or parity evidence requires it.

## 9. State model

```text
DISABLED
DATA_NOT_READY
NO_CANONICAL_F
HOOK_OR_ND
AMBIGUOUS
F_BULLISH
F_BEARISH
```

The bullish and bearish F states open the phase-direction layer. When the optional F1-to-F2 confirmation-window input is enabled, the selected count must additionally be in `OPEN` lifecycle-window state. See [16 — Higher-Timeframe F1-to-F2 Confirmation Window](16_higher_timeframe_f1_to_f2_confirmation_window.md).

## 10. Performance contract

The lower-timeframe execution path remains lightweight:

- F1/F2-only entry detector;
- no lower-timeframe Hook build;
- no renderer;
- no CSV;
- no timer;
- no custom print.

The heavier F/Hook classifier exists only on the selected higher timeframe and is cached by higher-timeframe bar. With the default H1 filter, it runs at most once per hour of tester time.

## 11. Acceptance cases

### Bullish authorization

```text
H1 latest phase = bullish F
M1/M5 bullish F2 Point-2 setup = allowed
M1/M5 bearish F2 Point-2 setup = blocked
```

### Bearish authorization

```text
H1 latest phase = bearish F
M1/M5 bearish setup = allowed
M1/M5 bullish setup = blocked
```

### Hook block

```text
H1 latest canonical F exists
but newer/equal H1 Hook/ND exists
→ both Buy and Sell entries blocked
```

### Pending reconciliation

```text
H1 bullish F → Buy Limit exists
H1 changes to bearish F before fill
→ Buy Limit cancelled
→ existing filled Buy position, if any, remains managed
```

### Missing data

```text
H1 history not ready
→ no new entry
→ retry later
```

## 12. Optional F1-to-F2 lifecycle window

The phase selector and lifecycle-window filter use the same selected canonical HTF sequence. With the window enabled, direction alone is insufficient:

```text
selected HTF F1 confirmed
AND exact direct-child HTF F2 not confirmed
→ selected HTF direction may authorize entries
```

Before F1 confirmation and at/after F2 confirmation, the gate is closed. The window is optional and enabled by default. The full contract is in [16 — Higher-Timeframe F1-to-F2 Confirmation Window](16_higher_timeframe_f1_to_f2_confirmation_window.md).

## 13. Non-goals

This filter does not:

- close a live position on HTF phase reversal;
- change Stop, Target, RR, overlap, or wider-context selection;
- choose the best higher-timeframe scale by AI;
- use CG context;
- infer trend from price alone;
- use the live incomplete H1 candle.
