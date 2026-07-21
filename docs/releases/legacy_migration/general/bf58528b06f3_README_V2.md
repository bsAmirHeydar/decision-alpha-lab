# Strategy Factory V2

V2 adds the compiled online decision layer to the original shared research factory.

## Python packages

- `plugins/` — versioned interfaces, descriptors, registry, and built-ins.
- `context/` — dependency graph, incremental cache, providers, and fixed vectors.
- `decision/` — calibration, model routing, scoring, abstention, and envelopes.
- `optimization/` — plan compiler, immutable plans, pruning, and spec loading.
- `serving/` — precompiled candidate factory, fast decision engine, fallback, and benchmark.
- `runtime/` — latency, telemetry, event bus, idempotency, and atomic generations.
- `testing/` — reusable metamorphic and deterministic boundary helpers.

## V2 commands

```text
scaffold-v2
compile-v2
decide-v2
benchmark-v2
```

The old V1 batch/research commands remain available.
