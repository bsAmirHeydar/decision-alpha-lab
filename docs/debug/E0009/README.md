# E0009 — Multi-Level Monotonic Swing Hook Executor

Release 109 reorganizes E0009 into four independent levels.

## Compact default logic

```text
H4: 4 falling lows -> only BUY
M15: 4 falling lows -> BUY setup
M1: buy every eligible LOW hook
H4: 3 rising highs -> BUY TP at latest high

H4: 4 rising highs -> only SELL
M15: 4 rising highs -> SELL setup
M1: sell every eligible HIGH hook
H4: 3 falling lows -> SELL TP at latest low
```

## Input groups

### 00. Symbol / Execution
Controls symbol, real trading switch, magic, logging, and initial run.

### 01. Macro Mode Level
`InpMacroModeTF`, `InpMacroModeNodeCount`, `InpMacroModeL`, `InpMacroModeBars`, `InpMacroModeMaxAgeBars`.

Default macro mode is H4 with 4 nodes. Four falling lows allow BUY only. Four rising highs allow SELL only.

### 02. Middle Setup Level
`InpSetupTF`, `InpSetupNodeCount`, `InpSetupL`, `InpSetupBars`, `InpSetupMaxAgeBars`.

Default setup is M15 with 4 nodes. It must agree with macro if `InpRequireSetupAgreesWithMacro=true`.

### 03. M1 Entry Hooks
`InpExecutionTF`, `InpExecutionL`, hook age, hook candidates, duplicate ledger, and order mode.

BUY mode trades LOW hooks. SELL mode trades HIGH hooks.

### 04. Micro-Only Entry Filter
Rejects large hooks by setup amplitude, M1 average range, or fixed points.

### 05. Exit Level
Default exit is H4 with 3 nodes. BUY TP is the newest high of 3 rising highs. SELL TP is the newest low of 3 falling lows. Exit is independent from entry time.

### 06. Spread / Risk / Exposure
Risk cash, commission, spread multipliers, and side caps.


## Release 110 — nearest-live monotonic sequence scan

Release 109 only checked the latest `N` nodes of a type. That was too strict.

Example:

```text
latest high is lower than the previous high
but the four highs before it were rising
```

Release 109 rejected SELL macro mode.  
Release 110 fixes this.

New detector behavior:

```text
For highs:
    collect all confirmed HIGH nodes
    scan from live edge backwards
    find the nearest consecutive window where:
        High1 < High2 < High3 < High4

For lows:
    collect all confirmed LOW nodes
    scan from live edge backwards
    find the nearest consecutive window where:
        Low1 > Low2 > Low3 > Low4

If both a high-window and a low-window exist:
    choose the one whose newest node is closer to live.
```

This applies to macro, setup, and exit pattern detection because they all use the same monotonic detector.

So a single newest failed high/low no longer invalidates the earlier nearest valid sequence.


## Release 111 — organized input titles and missing ZoneRatio fix

Release 111 fixes the compile error:

```text
undeclared identifier 'InpZoneRatio'
```

The missing input is now under the Entry Hook section:

```text
InpZoneRatio = 0.90
```

Inputs are also grouped with visible string section titles:

```text
InpSection00 = ===== 00 | SYMBOL / EXECUTION =====
InpSection01 = ===== 01 | MACRO MODE: H4 DEFAULT =====
InpSection02 = ===== 02 | SETUP: M15 DEFAULT =====
InpSection03 = ===== 03 | ENTRY: M1 HOOKS =====
InpSection04 = ===== 04 | MICRO-ONLY FILTER =====
InpSection05 = ===== 05 | EXIT: INDEPENDENT TF PATTERN =====
InpSection06 = ===== 06 | SPREAD / RISK / EXPOSURE =====
```

These title strings are only visual labels and are not used by the logic.
