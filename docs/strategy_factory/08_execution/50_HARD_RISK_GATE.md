---
type: strategy-factory-document
status: canonical
title: "Hard Risk Gate"
tags:
  - strategy-factory
---

# Hard Risk Gate

The risk gate is deterministic, independent of model confidence, and authoritative over every execution intent.

## Limits

Per-intent dollars/R, daily reserved risk, daily realized loss, open portfolio risk, strategy risk, symbol risk, correlated cluster risk, concurrent positions, session and symbol allowlists, stale decision time, and kill switch.

## One thesis, one risk unit

Multiple candidates, symbols, or cycle groups derived from the same market-event cluster share a risk budget. The gate prevents apparently separate strategies from multiplying one exposure.

## Reservation lifecycle

Risk is reserved before broker submission, adjusted on partial fill, released on cancellation or close, and reconstructed after restart from broker state. Inconsistent state stops new orders.

## Scaling

Scaling changes policy version and promotion state. No model probability can exceed the hard ceiling. Initial micro-live risk remains deliberately small until execution and calibration evidence accumulate.

