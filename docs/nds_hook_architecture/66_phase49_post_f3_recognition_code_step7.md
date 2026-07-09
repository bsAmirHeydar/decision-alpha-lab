# Phase 49 — Post-F3 Recognition Code

## Problem

F3 detection was correct, but the Hook selected after F3 was not always the intended Hook. The old logic effectively recognized only the immediate structural Hook whose origin matched an F3 terminal endpoint. It missed two important practical cases:

1. A near-death geometric Hook that reaches 80% completion but has not produced a full structural sequence.
2. A delayed/rebound Hook that forms slightly after the market touches the terminal side of F3.

## Canon implemented

A post-F3 Hook belongs to one of four families:

| Family | Meaning |
|---|---|
| `F3H_DIRECT_STRUCTURAL` | The Hook starts directly from the F3 terminal side and has a full structural sequence. |
| `F3H_DIRECT_GEOMETRIC_80` | The Hook starts directly from the F3 terminal side and has at least 80% cycle completion. |
| `F3H_DELAYED_STRUCTURAL` | Price reaches the F3 terminal side, rebounds, then a full structural Hook forms inside the ownership window. |
| `F3H_DELAYED_GEOMETRIC_80` | Price reaches the F3 terminal side, rebounds, then an 80% geometric Hook forms inside the ownership window. |

## Ownership window

An F3 does not validate every later Hook. It owns only candidates whose origin time is inside:

```text
F3 terminal time <= Hook origin time <= F3 terminal time + InpHookPostF3MaxSearchBars
```

## Direct vs delayed

Direct is determined by both price and time proximity to the F3 terminal endpoint:

```text
abs(Hook.origin_price - F3.terminal_price) <= InpHookPostF3TerminalTolerancePricePoints
Hook.origin_time - F3.terminal_time <= InpHookPostF3TerminalToleranceBars
```

If a candidate is not direct but is inside the ownership window, it is delayed/rebound.

## Structural vs geometric 80

Structural requires:

```text
- valid sequence
- not failed
- confirmed terminal
- valid crown
- x_count >= 2
```

Geometric 80 requires:

```text
- valid candidate
- valid crown
- retracement_ratio * 100 >= InpHookPostF3GeometricMinCompletionPct
```

## Selection priority

`STRUCTURAL_FIRST` is the default:

1. Prefer structural candidates.
2. If structural candidates do not exist, allow geometric 80 candidates.
3. Prefer direct over delayed when rank is equal.
4. Prefer earliest origin time.

## Labels

| Label | Meaning |
|---|---|
| `F3H-D-S` | Direct structural post-F3 Hook |
| `F3H-D80` | Direct 80% geometric post-F3 Hook |
| `F3H-R-S` | Delayed/rebound structural post-F3 Hook |
| `F3H-R80` | Delayed/rebound 80% geometric post-F3 Hook |

## Limitation

This patch classifies Phase02 candidates that already exist. It does not yet synthesize pure geometric Hook objects directly from raw candles when no Phase02 candidate row exists.
