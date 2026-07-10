# Phase 53 — Lightweight Backtest Runtime

Phase 53 separates the executable Strategy Tester path from the production visual expert.

## Shared rule path

```text
FP_DetectAllScales
→ FP_RunHookPhase02DetectionCore
→ FP_RunNDSHookLimitF123ExecutionCore
```

The production Hook and trade engines now wrap those same cores with optional visual and CSV sinks. The backtest expert calls the cores directly.

## New executable

```text
mql5/Experts/FlagCounting/NDSHookLimitF123Backtest.mq5
```

## Performance controls

- once-per-new-bar execution;
- FAST / PARITY / CUSTOM profiles;
- no rendering, timer, chart event, license, validation, or research pipeline;
- no CSV by default;
- Hook reconstruction skipped while a managed position is open;
- deterministic one-attempt registry reset for each tester run.

Full documentation:

```text
docs/nds_entry_architecture/phase53_lightweight_backtest/README.md
```
