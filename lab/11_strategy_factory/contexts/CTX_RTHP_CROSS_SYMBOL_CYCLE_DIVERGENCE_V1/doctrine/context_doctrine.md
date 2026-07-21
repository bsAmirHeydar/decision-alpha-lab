---
title: RTHP Cross-Symbol Cycle Divergence Context Doctrine
status: semantically-validated
version: 1.0.0
---
# RTHP Context Doctrine

## Intended market relationship
Two symbols are evaluated through corresponding High or Low levels derived independently from the same versioned cycle relationship. A relationship occurrence exists when one symbol touches its own corresponding level while the paired symbol has not touched its own corresponding level by the common M15 evaluation cut.

## Observable definition
A confirmed RTHP occurrence requires a registered symbol pair, one signal family, one active-cycle identity, one reference-cycle identity, one level side, equal price-basis labels, synchronized non-stale observations for both symbols, and an exclusive-or touch state at the confirmation close. Low-side occurrences receive the `BULLISH_DIVERGENCE` context label and High-side occurrences receive the `BEARISH_DIVERGENCE` context label.

## Falsification conditions
No confirmed occurrence is produced when both symbol-local levels are touched, neither level is touched, either observation is missing or stale at the common cut, price-basis labels differ, no reference cycle is available, the scoped reference is exhausted, or a duplicate immutable event identity already exists.

## Economic hypothesis — non-authoritative
The polarity labels may correlate with future directional changes over research-defined horizons. This statement is an unverified research hypothesis and is not a reversal guarantee, trade instruction, profit claim, or permission to alter the Context definition.

## Non-goals
This package excludes Entry, Treatment, Execution, Stop, Target, Risk, Position Sizing, order submission, capital activation, profitability classification, and win-rate claims.
