# Runtime State Machine

```text
CREATED
→ INITIALIZING
→ READY
→ RUNNING
↔ DEGRADED
→ STOPPING
→ STOPPED
```

Any initialization or runtime failure may transition to `FAILED`. `FAILED` is terminal in Phase 02. Recovery orchestration is deferred to production hardening.

Illegal transitions are rejected. This prevents partial startup, duplicate start, silent restart and shutdown from an unknown state.
