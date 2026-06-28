# 04 - SMT Divergence Rules

## Core principle

SMT divergence is defined structurally between two symbols.

Each symbol has its own W highs and lows. The strategy does not compare the absolute price level of Symbol1 with the absolute price level of Symbol2.

Instead, it compares whether each symbol has hunted the corresponding W reference of its own structure.

## Eligible references

Only previous W cycles inside the same M are eligible.

W1 produces no signal.

W2 can only use W1.

W3 can use W2 or W1.

W4 can use W3, W2, or W1.

## Hunt definition

Hunt is touch-only.

No candle close beyond the reference is required.

No tolerance is applied. Equality still counts as touch.

High hunt occurs when the active price high is greater than or equal to the selected reference W high.

Low hunt occurs when the active price low is less than or equal to the selected reference W low.

## High-side divergence

A high-side SMT divergence exists when:

- exactly one symbol hunts an eligible previous W high;
- the other symbol does not hunt its corresponding previous W high;
- both references belong to the same W index inside the same M structure;
- the divergence remains valid until the check-candle close.

Trade direction: sell.

Trade symbol: the symbol that did not hunt.

## Low-side divergence

A low-side SMT divergence exists when:

- exactly one symbol hunts an eligible previous W low;
- the other symbol does not hunt its corresponding previous W low;
- both references belong to the same W index inside the same M structure;
- the divergence remains valid until the check-candle close.

Trade direction: buy.

Trade symbol: the symbol that did not hunt.

## Confirmation

Raw divergence can form intrabar.

The strategy waits until the active configured check candle closes.

At check-candle close:

- if only one symbol has hunted, the divergence is confirmed;
- if both symbols have hunted, the divergence is invalid;
- if neither symbol has hunted, there is no divergence.

The same active check candle is sufficient. A full additional check candle is not required.

## Clean-symbol invalidation

If the initially clean symbol hunts the corresponding reference before check-candle close, the divergence is invalid and no trade is opened.

If the clean symbol hunts after the trade has already been opened, the old divergence does not produce a new entry. The open position is managed through normal SL/TP/partial/daily-close rules.

## Duplicate prevention

Each divergence can be traded only once.

Suggested divergence ID components:

- trading day;
- M id;
- current W id;
- reference W id;
- side: high or low;
- hunted symbol;
- clean/traded symbol;
- check-candle close time.

If the same divergence remains true on later check candles, no new entry is allowed.

## Multiple eligible references

When multiple eligible references are hunted, the default selected reference is the closest eligible W by time.

Example:

If W4 is current and W3, W2, and W1 references are all touched, W3 is selected by default because it is closest.

The purpose is to keep the stop-loss smaller.

Optional research mode:

- choose the eligible reference that produces the smallest stop distance on the trade symbol.

This optional mode must be explicitly labelled in reports because it is not the strict default.

## Simultaneous buy and sell

If buy-side and sell-side divergences are both confirmed in the same check candle, no trade is opened.

The event should be recorded as ambiguous/no-trade.

If buy and sell signals occur on separate check candles and hedging is enabled, both may be traded subject to max-trade-per-M limits.

## No-entry moments

No new entry is allowed:

- during M gaps;
- on the last check candle of an M;
- after 15:30 New York;
- when required symbol data is missing;
- when the market is closed.

## Reference selection

If multiple eligible previous W references are valid for the same side and clean/traded symbol, the selected reference is the one that creates the largest stop distance for the clean/traded symbol.

Multiple eligible references in the same check candle resolve into one signal per side/trade-symbol after reference selection. They must not create duplicate trades by themselves.
