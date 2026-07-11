---
type: strategy-factory-document
status: canonical
title: "Live Execution and Broker Bridge"
tags:
  - strategy-factory
---

# Live Execution and Broker Bridge

The live bridge translates approved intents into broker-specific requests and reconciles the broker as source of truth for actual positions.

## Preflight

Symbol selection, session status, tick size, point value, volume step, min/max volume, stops level, freeze level, margin, account mode, duplicate order, price freshness, expiry, and risk reservation.

## Request trace

Persist intended prices, normalized prices, request time, response time, retcode, broker order/deal/position IDs, fills, slippage, rejection, modifications, and final close. Every trace maps to one intent.

## Failure behavior

Timeouts and ambiguous responses trigger reconciliation before retry. Never blindly resend. Partial fills update exposure. Repeated rejects activate a strategy or global circuit breaker.

## Deployment boundary

The supplied patch defines the bridge interface and paper broker but intentionally contains no live `OrderSend`, `OrderCheck`, or `CTrade`. A live adapter is a separately reviewed and promoted patch.

