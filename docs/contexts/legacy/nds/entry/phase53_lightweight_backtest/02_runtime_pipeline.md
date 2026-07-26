# Runtime Pipeline

## Production expert

The central production expert historically executes structural detection and then a large set of visual, audit, release, paper, broker-dry-run, normalization, and health layers. Those layers are useful for engineering and inspection but are not required to simulate the current executable strategy.

## Lightweight expert

On each new bar only:

1. Load one canonical closed-bar window.
2. Build the selected scale list.
3. Run `FP_DetectAllScales` once.
4. When no managed position is open, rebuild the Hook Phase 02 snapshot through `FP_RunHookPhase02DetectionCore`.
5. Run `FP_RunNDSHookLimitF123ExecutionCore`.
6. Record only in-memory timing counters unless a meaningful trade transition occurs.

## No duplicate node scan

The production path previously ran Hook Phase 01 and then Phase 02, while Phase 02 rebuilt its own node source. The lightweight path calls Phase 02's detection core directly, so the separate Phase 01 runtime pass is omitted.

## New-bar authority

`OnTick` returns immediately while the current chart bar has not changed. The structural engine therefore runs once per bar rather than once per tick.
