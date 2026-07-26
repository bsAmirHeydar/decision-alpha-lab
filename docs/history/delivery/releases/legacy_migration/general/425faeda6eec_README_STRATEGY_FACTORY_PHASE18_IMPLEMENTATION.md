# Strategy Factory Phase 18 — Live Broker Adapter and Hard Safety

Phase 18 introduces the first broker mutation authority in the Strategy Factory. The authority is intentionally narrow: `OrderCheck` and `OrderSend` exist only in `SF18_Mql5BrokerAdapter.mqh`. Every other component is a typed release, authorization, safety, request, ledger, reconciliation or conformance component.

The default operational posture is locked. `SF18_MicroLiveHost.mq5` starts with micro-live disabled and the kill switch engaged. Attaching the host to a chart does not synthesize or submit a trade. A governed Phase 16 intent, exact Phase 18 release, short-lived authorization, matching account/server/symbol, fresh account and quote snapshots, all hard risk gates, successful broker `OrderCheck`, and an explicit coordinator call are required before a synchronous `OrderSend` can occur.

Python is an offline conformance implementation. It contains no live broker port and cannot send an order.
