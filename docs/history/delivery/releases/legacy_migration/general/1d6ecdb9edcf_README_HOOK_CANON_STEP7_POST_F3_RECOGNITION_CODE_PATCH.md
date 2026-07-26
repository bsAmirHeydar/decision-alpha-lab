# Hook Canon Step 7 — Post-F3 Recognition Code Patch

## Purpose

The previous code could identify F3 events but selected the post-F3 Hook too narrowly: mostly only a Hook whose origin price exactly matched the F3 terminal endpoint.

This patch implements the wider Canon:

1. Direct structural Hook from the F3 terminal side.
2. Direct geometric 80% Hook from the F3 terminal side.
3. Delayed/rebound structural Hook inside the post-F3 ownership window.
4. Delayed/rebound geometric 80% Hook inside the post-F3 ownership window.

## New inputs

```mql5
InpHookPostF3RecognitionMode
InpHookPostF3SelectionPriority
InpHookPostF3AllowDirectTerminalHook
InpHookPostF3AllowDelayedReboundHook
InpHookPostF3MaxSearchBars
InpHookPostF3TerminalToleranceBars
InpHookPostF3TerminalTolerancePricePoints
InpHookPostF3GeometricMinCompletionPct
```

## Visible labels

- `F3H-D-S` = direct structural
- `F3H-D80` = direct geometric 80
- `F3H-R-S` = delayed/rebound structural
- `F3H-R80` = delayed/rebound geometric 80
- `HH` = Hook-after-Hook
- `PARENT` = required companion of HH

## Scope

Hook Phase02 post-F3 validity annotation, labels, colors, CSV, and documentation only. No execution or broker behavior is changed.
