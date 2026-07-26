---
id: SAED-68620FDA3C
title: "Entry Mechanisms — Breakout, Market, and Pullback Limit"
type: architecture
status: canonical
domain: strategy-factory-setup-ai-edge-discovery
version: 1.0.0
created: 2026-07-13
updated: 2026-07-13
tags:
  - strategy-factory
  - setup-factory
  - ai-training
  - entry-mechanism
---

# Entry Mechanisms — Breakout, Market, and Pullback Limit

## E1 — Breakout / With-Move Entry

Buys confirmation in exchange for worse price, slippage and possible exhaustion. Models follow-through probability, false-break probability, remaining destination, breakout compression and immediate pullback.

## E2 — Immediate Market Entry

Buys immediacy and fill certainty in exchange for no price improvement. Models opportunity decay, immediate MAE, expected pullback and cost of waiting.

## E3 — Pullback / Counter-Move Limit Entry

Buys better price and stop geometry in exchange for non-fill and adverse selection. Requires separate models for:

1. probability and time of fill before expiry;
2. outcome conditional on fill;
3. opportunity cost when not filled;
4. whether fill itself signals Context deterioration.

## Premium Interpretation

| Mechanism | Premium purchased | Cost paid |
|---|---|---|
| Breakout | confirmation | worse price, slippage, false break |
| Market | immediacy | no price improvement |
| Limit | price improvement | non-fill, adverse selection |

The learner estimates which premium is economically worth paying for the current Context.
