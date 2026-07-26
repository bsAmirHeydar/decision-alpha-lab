# Strategy Factory Phase 18 — Live Broker Adapter and Hard Safety

## Status

Phase 18 introduces a deliberately narrow broker-mutation boundary. Live authority is present in exactly one MQL5 adapter, disabled by default, protected by a startup-engaged kill switch, exact release and authorization lineage, mandatory `OrderCheck`, bounded micro-live limits, a circuit breaker and an append-only ledger.

## Navigation

- [[docs/strategy_factory_implementation/phase18/00_PHASE_18_MOC|Phase 18 implementation MOC]]
- [[docs/strategy_factory_implementation/phase18/02_LIVE_AUTHORITY_BOUNDARY|Live authority boundary]]
- [[docs/strategy_factory_implementation/phase18/06_MICRO_LIVE_RELEASE|Micro-live release]]
- [[docs/strategy_factory_implementation/phase18/08_LIVE_AUTHORIZATION|Live authorization]]
- [[docs/strategy_factory_implementation/phase18/17_KILL_SWITCH|Kill switch]]
- [[docs/strategy_factory_implementation/phase18/19_CIRCUIT_BREAKER|Circuit breaker]]
- [[docs/strategy_factory_implementation/phase18/44_ORDER_CHECK|Mandatory OrderCheck]]
- [[docs/strategy_factory_implementation/phase18/45_ORDER_SEND|Isolated OrderSend]]
- [[docs/strategy_factory_implementation/phase18/72_MICRO_LIVE_RUNBOOK|Micro-live runbook]]
- [[docs/strategy_factory_implementation/phase18/84_PHASE19_HANDOFF|Phase 19 handoff]]

## Hard boundary

The MQL5 file `SF18_Mql5BrokerAdapter.mqh` is the only Phase 18 source that may contain `OrderCheck(` or `OrderSend(`. No asynchronous broker send exists. The default host cannot generate an intent and therefore cannot trade by being attached to a chart alone.
