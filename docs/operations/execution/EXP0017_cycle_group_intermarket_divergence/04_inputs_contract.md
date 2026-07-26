# 04 — Inputs Contract

## 1. Purpose

This document defines the MQL5 input surface for the independent CG Intermarket Divergence EA.

The input design must keep the system modular. Every cycle group has independent trade/draw/color settings so that research and live execution can isolate which CGs are allowed to act.

## 2. Symbol inputs

```cpp
input string InpSymbolA = "SPXUSD";
input string InpSymbolB = "NDXUSD";
```

Rules:

- Both symbols must be selected in Market Watch.
- Both symbols must provide bars for the chart timeframe used by the EA.
- Both symbols must be tradable if trade inputs are enabled.
- The expert should fail safely if either symbol is missing.

## 3. Time conversion inputs

```cpp
input int InpBrokerUtcOffsetHours  = 3;
input int InpNewYorkUtcOffsetHours = -4;
```

Rationale:

- User requested broker default UTC+3.
- New York offset changes by season.
- MQL5 does not provide a universal broker-independent New York session clock by default.
- Manual inputs are explicit and auditable.

Alternative future input:

```cpp
input int InpBrokerMinusNewYorkOffsetHours = 7;
```

But the preferred design is to keep broker UTC and NY UTC offset separate.

## 4. Risk inputs

Baseline:

```cpp
input double InpRiskPercentEquity = 1.0;
```

Recommended safety inputs:

```cpp
input bool   InpEnableTrading = true;
input int    InpMagicNumber   = 170017;
input int    InpSlippagePoints = 50;
input bool   InpOnePositionPerSymbol = true;
```

These are implementation safety controls, not strategy rules.

## 5. Drawing global inputs

Recommended:

```cpp
input bool InpEnableDrawing = true;
input int  InpDrawLineWidth = 1;
input ENUM_LINE_STYLE InpDrawLineStyle = STYLE_SOLID;
```

Per-CG draw inputs remain separate.

## 6. Per-cycle-group inputs

Every CG requires:

```cpp
input bool  InpCG_<duration>_Trade = true;
input bool  InpCG_<duration>_Draw  = true;
input color InpCG_<duration>_Color = clrBlack;
```

The requested default is:

```text
Trade: ON
Draw:  ON
Color: Black
```

## 7. Full input list

```cpp
// Symbols
input string InpSymbolA = "SPXUSD";
input string InpSymbolB = "NDXUSD";

// Time conversion
input int InpBrokerUtcOffsetHours  = 3;
input int InpNewYorkUtcOffsetHours = -4;

// Risk and execution
input bool   InpEnableTrading = true;
input double InpRiskPercentEquity = 1.0;
input int    InpMagicNumber = 170017;
input int    InpSlippagePoints = 50;
input bool   InpOnePositionPerSymbol = true;

// Drawing
input bool InpEnableDrawing = true;
input int  InpDrawLineWidth = 1;
input ENUM_LINE_STYLE InpDrawLineStyle = STYLE_SOLID;

// cg_3m
input bool  InpCG_3m_Trade = true;
input bool  InpCG_3m_Draw  = true;
input color InpCG_3m_Color = clrBlack;

// cg_5m
input bool  InpCG_5m_Trade = true;
input bool  InpCG_5m_Draw  = true;
input color InpCG_5m_Color = clrBlack;

// cg_9m
input bool  InpCG_9m_Trade = true;
input bool  InpCG_9m_Draw  = true;
input color InpCG_9m_Color = clrBlack;

// cg_10m
input bool  InpCG_10m_Trade = true;
input bool  InpCG_10m_Draw  = true;
input color InpCG_10m_Color = clrBlack;

// cg_15m
input bool  InpCG_15m_Trade = true;
input bool  InpCG_15m_Draw  = true;
input color InpCG_15m_Color = clrBlack;

// cg_18m
input bool  InpCG_18m_Trade = true;
input bool  InpCG_18m_Draw  = true;
input color InpCG_18m_Color = clrBlack;

// cg_20m
input bool  InpCG_20m_Trade = true;
input bool  InpCG_20m_Draw  = true;
input color InpCG_20m_Color = clrBlack;

// cg_24m
input bool  InpCG_24m_Trade = true;
input bool  InpCG_24m_Draw  = true;
input color InpCG_24m_Color = clrBlack;

// cg_30m
input bool  InpCG_30m_Trade = true;
input bool  InpCG_30m_Draw  = true;
input color InpCG_30m_Color = clrBlack;

// cg_40m
input bool  InpCG_40m_Trade = true;
input bool  InpCG_40m_Draw  = true;
input color InpCG_40m_Color = clrBlack;

// cg_45m
input bool  InpCG_45m_Trade = true;
input bool  InpCG_45m_Draw  = true;
input color InpCG_45m_Color = clrBlack;

// cg_60m
input bool  InpCG_60m_Trade = true;
input bool  InpCG_60m_Draw  = true;
input color InpCG_60m_Color = clrBlack;

// cg_72m
input bool  InpCG_72m_Trade = true;
input bool  InpCG_72m_Draw  = true;
input color InpCG_72m_Color = clrBlack;

// cg_90m
input bool  InpCG_90m_Trade = true;
input bool  InpCG_90m_Draw  = true;
input color InpCG_90m_Color = clrBlack;

// cg_120m
input bool  InpCG_120m_Trade = true;
input bool  InpCG_120m_Draw  = true;
input color InpCG_120m_Color = clrBlack;

// cg_150m
input bool  InpCG_150m_Trade = true;
input bool  InpCG_150m_Draw  = true;
input color InpCG_150m_Color = clrBlack;

// cg_180m
input bool  InpCG_180m_Trade = true;
input bool  InpCG_180m_Draw  = true;
input color InpCG_180m_Color = clrBlack;

// cg_240m
input bool  InpCG_240m_Trade = true;
input bool  InpCG_240m_Draw  = true;
input color InpCG_240m_Color = clrBlack;

// cg_300m
input bool  InpCG_300m_Trade = true;
input bool  InpCG_300m_Draw  = true;
input color InpCG_300m_Color = clrBlack;

// cg_360m
input bool  InpCG_360m_Trade = true;
input bool  InpCG_360m_Draw  = true;
input color InpCG_360m_Color = clrBlack;

// cg_720m
input bool  InpCG_720m_Trade = true;
input bool  InpCG_720m_Draw  = true;
input color InpCG_720m_Color = clrBlack;
```

## 8. Internal config object

Inputs should be copied into an internal array of structs:

```cpp
struct CG_Config
{
   string name;
   int    duration_minutes;
   bool   trade_enabled;
   bool   draw_enabled;
   color  draw_color;
};
```

This prevents duplicated strategy logic for 21 CGs.

The EA should not contain separate detection code for each CG. It should iterate through a `CG_Config configs[]` array.

## 9. Required validation

On initialization:

- Symbol A and Symbol B must be non-empty.
- Symbol A and Symbol B must not be equal.
- Risk percent must be positive.
- Broker UTC offset must be reasonable, for example between -12 and +14.
- NY UTC offset must be either -4 or -5, or at least within a safe range if kept generic.
- At least one CG must have trade or draw enabled.

## 10. Default implementation mode

Recommended default:

```text
Trading enabled: true
All CG trade enabled: true
All CG draw enabled: true
All CG draw color: black
Risk: 1% equity
Broker UTC: +3
New York UTC: -4
```

