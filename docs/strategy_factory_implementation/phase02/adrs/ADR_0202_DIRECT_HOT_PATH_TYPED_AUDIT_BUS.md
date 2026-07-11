# ADR 0202 — Direct Hot Path with Typed Audit Bus

The main runtime uses direct typed port calls. The event bus is bounded and used for audit and notification, not as the only control-flow mechanism. This preserves determinism, traceability and low latency.