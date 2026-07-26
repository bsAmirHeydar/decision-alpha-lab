---
title: "Failure Semantics and Recovery"
---

# Failure Semantics and Recovery

## Failure Classes

### Configuration Failure

Examples: invalid strategy ID, invalid timer period, missing required port. The runtime fails during initialization and never enters READY.

### Service Initialization Failure

A bound service may reject configuration or report unavailable resources. The failing service ID is prefixed to the error. Runtime transitions to FAILED.

### Contract Failure

An anatomy event or snapshot violates schema, identity or time semantics. In strict mode the runtime fails. In non-strict research mode the item is rejected and counted.

### Sink Failure

If an accepted event cannot be written to the result sink, the runtime fails. Losing accepted research truth is not treated as a harmless warning.

### Audit Overflow

Audit overflow follows the configured policy. The dropped count always increases. In later phases, critical event types may force degradation or failure even if low-priority telemetry is droppable.

### Clock Failure

Phase 02 uses a simple terminal clock. Phase 03 must distinguish unavailable wall time, unstable broker offset and stale synchronization.

## Recovery Policy

Automatic recovery is intentionally absent in Phase 02. A FAILED runtime cannot transition directly back to RUNNING. Recovery must occur through an explicit teardown and reinitialization so partial state is not reused accidentally.

Production hardening will later define restart checkpoints, replay positions, sink offsets and broker reconciliation. Until then, fail closed and require operator-visible reinitialization.
