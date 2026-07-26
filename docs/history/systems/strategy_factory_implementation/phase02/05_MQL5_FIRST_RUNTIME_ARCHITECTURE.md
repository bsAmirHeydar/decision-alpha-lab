# MQL5-First Runtime Architecture

## Runtime Ownership

The runtime owns orchestration, not strategy meaning. Its responsibilities are limited to lifecycle, dependency binding, event draining, contract validation, snapshot construction, result routing and audit emission.

## Dependency Direction

```text
Contracts
↑
Core
↑
Ports
↑
Runtime
↑
Host composition
```

Adapters implement ports. Anatomy plugins will later implement the anatomy port. Runtime never imports a concrete strategy.

## Fail-Closed Rule

In strict mode, an invalid event, invalid snapshot, sink failure or missing required port moves the runtime to `FAILED`. In permissive research mode, individual invalid rows may be rejected and counted, but all rejections remain auditable.
