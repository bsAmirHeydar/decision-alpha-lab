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
