---
title: RTHP MT5 Automation — Open Decisions, Assumptions, and Non-Goals
status: roadmap-approved-for-implementation
version: 1.0.0
updated: 2026-07-22
tags: [rthp, decisions, assumptions, non-goals]
---

# Open Decisions, Assumptions, and Non-Goals

## Resolved by this roadmap

- M1 is the canonical production floor.
- Sub-M1 and tick history are excluded from canonical acquisition.
- No synthetic tick reconstruction.
- Direct MT5 Python integration is the primary source path.
- The delivery is context-owned and does not modify shared engines.
- Operator input is reduced to two symbol selections under the default profile.

## Decisions to freeze during implementation

1. Default minimum common-history threshold.
2. Default maximum lookback under the Context Discovery profile.
3. Broker alias registry ownership.
4. Exact accepted classification for no-quote/no-bar intervals.
5. Storage codec for large immutable M1 artifacts.
6. Whether the terminal may be launched automatically or must already be open.
7. Secret-provider integration for non-default account sessions.
8. Versioned contract-roll policies for expiring instruments.

## Assumptions

- MetaTrader 5 and the official Python integration are installed on Windows.
- The selected account is entitled to the requested history.
- The terminal server provides M1 history for both symbols.
- Existing RTHP train-activation and shared trainer engines remain available.

## Non-goals

- Tick-level microstructure research.
- Sub-second or sub-minute signal reconstruction.
- HFT or latency research.
- Broker execution automation.
- Live trading, order placement, or capital activation.
- Silent semantic amendment of RTHP.
