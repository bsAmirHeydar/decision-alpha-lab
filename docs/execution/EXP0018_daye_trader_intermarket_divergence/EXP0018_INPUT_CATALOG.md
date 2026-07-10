# کاتالوگ ورودی‌های EXP0018

## Symbols

- `InpSymbolA = SPXUSD`
- `InpSymbolB = NDXUSD`

## Time

- `InpNewYorkTimeMode = AUTO_DST | MANUAL`
- `InpBrokerUtcOffset`
- `InpManualNewYorkUtcOffset`

## Lookback

- `InpLookbackWeeks = 2`

## Divergence drawings

- `InpDrawDivergenceLines = true`
- `InpDivergenceLineColor`
- نیازمند تصمیم: line width/style

## Signal switches

22 input مستقل، یکی برای هر signal type. عبارت 21 در منبع به‌عنوان تناقض ثبت شده است.

## Session boxes

- A color
- L color
- N color
- P color
- نیازمند تصمیم: on/off جداگانه، opacity، border style

## TWO

- show
- width
- color

## TDO

- show
- width
- color

## ورودی‌هایی که فعلاً نباید اضافه شوند

- trade/risk/lot/order inputs
- statistical filters
- EXP0017 CG controls
- AI/model controls

این Expert در scope فعلی drawing-only است.
