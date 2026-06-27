# FlagCounting Phoenix

Phoenix is a clean rebuild of the Flag Counting engine. It intentionally does not include, reuse, or depend on any earlier `FlagCounting`, `FlagCountingVNext`, or `FlagCountingV6` implementation.

## Core principles

1. Node logic is copied conceptually from the original project rule: a node is a candle high/low level that has at least `L` candles on both sides that do not reach that price.
2. Equality is not a break. Equal highs/lows form one plateau node.
3. Open, close, candle body, and candle color are ignored by the structural logic.
4. A flag body is always `Origin -> Leg1 -> Waist -> Leg2`.
5. F1, F2, and F3 share the same two-leg body shape; they differ in post-flag semantics.
6. F2 and F3 use backfilled origins from the deepest adverse correction after their parent flag.
7. Hook/ND is rendered and exposed as a first-class structure.
8. Renderer is non-authoritative. It draws only engine-emitted structures.

## Files

- `FP_Types.mqh`: model types and contract helpers.
- `FP_NodeEngine.mqh`: L-based high/low node extraction with plateau handling.
- `FP_HookEngine.mqh`: branch-based ND/hook detection.
- `FP_FlagBodyEngine.mqh`: two-leg flag body construction.
- `FP_InternalCountEngine.mqh`: internal 1/2/3/4 and post-flag correction scanning.
- `FP_SequenceEngine.mqh`: F1 -> F2 -> F3 orchestration.
- `FP_Renderer.mqh`: chart drawing.
- `FP_Audit.mqh`: logs and diagnostics.

## Expert

Compile:

```text
mql5/Experts/FlagCounting/FlagCountingPhoenixExperiment.mq5
```

## Recommended first run

Keep the initial settings inspectable rather than over-strict:

```text
InpRequireF1PhaseBoundary = true
InpAllowF1FailOpenWhenNoHook = true
InpEnforceSingleChainPerDirectionScale = false
InpEnforceSingleChainPerDirectionGlobal = false
InpDrawHooks = true
InpDetailedLabels = true
InpShowParentIds = true
```

After Hook/ND coverage is verified, you can tighten:

```text
InpAllowF1FailOpenWhenNoHook = false
InpEnforceSingleChainPerDirectionScale = true
InpEnforceSingleChainPerDirectionGlobal = true
```
