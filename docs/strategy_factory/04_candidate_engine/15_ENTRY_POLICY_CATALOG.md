---
type: strategy-factory-document
status: canonical
title: "Entry Policy Catalog"
tags:
  - strategy-factory
---

# Entry Policy Catalog

Entry policies define when and at what price exposure begins. They must be causal, fillable, and reproducible.

## Core families

Market-on-confirmation tests immediate execution. Reference or zone-edge limits test location and optionality. Fractional retracements test pullback efficiency. Breakout stops test continuation. First-pullback and displacement-return policies can be added when their trigger and expiry are mechanical.

## Fill semantics

Every policy specifies eligible time, expiry, bid/ask side, gap behavior, touch rules, order type, and whether the creation bar may fill. Historical fills are rejected when required quotes are unavailable. A limit order is not assumed filled merely because the candle range crosses the price if sequence ambiguity changes the result; the ambiguity policy must be explicit.

## Entry research

Compare fill rate, opportunity cost, conditional outcome after fill, missed winners, adverse selection, and latency sensitivity. A better average R with a 5% fill rate may be economically inferior to a robust market entry.

