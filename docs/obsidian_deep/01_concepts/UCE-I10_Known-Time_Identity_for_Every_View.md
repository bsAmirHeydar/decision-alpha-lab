---
title: "UCE-I10 Known-Time Identity for Every View"
tags: [strategy-factory, uce-i10, concept]
status: canonical
doc_version: 1.0.0
last_updated: 2026-07-13
---
# UCE-I10 Known-Time Identity for Every View

A representation is identified by both payload and decision cut. context_observation_id and known_time_ms prevent legal past artifacts from being confused with later or leaked artifacts.

## Consequence

Violating this rule invalidates the affected artifact and blocks promotion. The rule is represented in Python contracts/tests, closed JSON schemas, and the UCE-I10 acceptance evidence.

## Links

- [[../../strategy_factory_universal_context_exploitation_engine/implementation_program/phase_deliveries/uce_i10/00_UCE_I10_DELIVERY_MOC|UCE-I10 Delivery MOC]]
- [[../../strategy_factory_universal_context_exploitation_engine/implementation_program/phase_deliveries/uce_i10/19_TEST_STRATEGY_GOLDEN_NEGATIVE_AND_CHAOS|I10 Test Strategy]]
