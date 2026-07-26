---
type: strategy-factory-document
status: canonical
title: "Known-Time and Causality Contract"
tags:
  - strategy-factory
---

# Known-Time and Causality Contract

Every official feature and decision answers one question: what was actually knowable at this exact timestamp?

## Three times

`event_time_utc` marks when the underlying market action occurred. `known_time_utc` marks when the event could first be determined under the approved closed-bar or intrabar rule. `confirmation_time_utc` marks when the event becomes eligible for candidate creation. These may be equal, but they must never be conflated implicitly.

## Feature availability

Every feature stores its own known time. A snapshot rejects any feature whose known time exceeds the decision time. Daily high, final session range, future F-count completion, eventual zone validity, outcome rank, or any post-event aggregation are forbidden unless computed causally from data available then.

## Same-time events

Events that become known on the same candle are simultaneous. Sorting them by outcome, source file order, object ID, or price creates artificial sequence. The cluster and batch contracts must preserve ambiguity rather than invent a regime transition.

## Label horizon purge

Training observations whose outcomes extend into a test period are removed. Embargo alone is not enough. The last time used to construct a label is part of the sample contract and must be materialized.

