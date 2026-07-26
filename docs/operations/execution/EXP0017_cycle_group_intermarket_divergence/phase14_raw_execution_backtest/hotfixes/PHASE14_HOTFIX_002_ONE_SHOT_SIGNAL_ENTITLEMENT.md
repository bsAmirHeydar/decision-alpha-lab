# Phase 14 Hotfix 002 — One-Shot Signal Entitlement

## Defect

A confirmed divergence can remain valid across several lower-timeframe closed candles. Treating each observation as an independent entry event can create repeated trades from one underlying divergence anatomy.

The earlier signal-ID registry reduced duplicates but did not formalize the identity boundary, symbol-order invariance, terminal no-retry semantics, or dedicated duplicate audit contract.

## Resolution

Hotfix002 introduces a mandatory, versioned `CGX_ONCE_V1` trade-entitlement identity and a terminal first-observation gate.

The key is based on:

- canonical symbol pair;
- CG;
- New York trading day;
- current cycle;
- reference cycle;
- divergence side.

The key excludes lower-candle confirmation time and all execution configuration.

## Runtime order

```text
signal observation
→ canonical entitlement key
→ consume first observation
→ planner
→ router
```

A duplicate observation is suppressed before planning. A planner or router failure does not rearm the signal.

## Restart behavior

Current-day closed boundaries are replayed during startup to reconstruct consumed entitlements without historical order transport.

## Observability

- Main execution audit now carries `trade_entitlement_key` and uses the V3 default filename.
- Duplicate observations are written to the derived `_OneShot_Gate.csv` audit.
- Order comments hash the entitlement key instead of the candle-scoped observation identity.

## Preserved behavior

- no change to divergence detection;
- no change to SPX/NDX freshness;
- no change to CG definitions;
- no change to entry, stop, target, volume, hedge, or visual settings;
- `cg_3m` remains the only enabled default CG.

## Related documents

- [[../PHASE14_ONE_SHOT_SIGNAL_EXECUTION_CONTRACT]]
- [[../PHASE14_ONE_SHOT_STATE_MACHINE]]
- [[../PHASE14_ONE_SHOT_VALIDATION_PLAN]]
