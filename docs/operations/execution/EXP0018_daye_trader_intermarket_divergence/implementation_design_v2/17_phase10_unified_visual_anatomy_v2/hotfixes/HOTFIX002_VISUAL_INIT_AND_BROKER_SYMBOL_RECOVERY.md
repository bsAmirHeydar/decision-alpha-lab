# EXP0018 P10 Hotfix002 — Visual Initialization and Broker-Symbol Recovery

## Incident

`EXP0018_Daye_Visual_Anatomy` could terminate from `OnInit` with `INIT_FAILED` when the default broker symbols `SPXUSD` and `NDXUSD` did not exist on the active broker. On terminals where those names happened to exist but the attached chart used a different broker alias such as `#USNDAQ100`, initialization could succeed while the visual target resolver found no matching chart, resulting in no drawings.

The temporal visual suite was also coupled to the paired divergence pipeline. Therefore any pair-source initialization problem—symbol alias, old checkpoint, unavailable counterpart, or delayed history—blocked Daily, Session, Subcycle, 22.5-minute, GAP, TDO, and TWO drawings even though those layers only require the attached symbol.

## Root causes

1. Hard-coded broker-facing defaults were treated as universal symbol names.
2. Chart targeting required exact equality with configured source symbols.
3. P10 initialization failed when the optional P08/P07 paired divergence dependency failed.
4. P10 had no single-symbol period fallback for temporal drawings.
5. Object-creation failures were counted but did not emit actionable diagnostics.
6. The P07 self-test still contained the reserved MQL5 identifier `protected` in the pre-hotfix source chain.

## Corrected architecture

### Broker-symbol resolution

The chart-facing Expert now resolves broker aliases before building the paired source configuration.

Resolution order:

1. Prefer the current chart when it is a high-confidence alias for the requested canonical identity.
2. Use the exact configured broker symbol when it exists.
3. Scan all terminal symbols and rank known SPX/NDX aliases and symbol descriptions.
4. Refuse low-confidence or same-symbol pair resolution.

Known NDX families include `#USNDAQ100`, `NASDAQ100`, `NAS100`, `US100`, `USTEC`, `NDX`, and `NQ100` variants. Known SPX families include `#USSPX500`, `SPXUSD`, `US500`, `SP500`, `SPX500`, and `USA500` variants.

Canonical identities remain unchanged. Alias resolution changes only broker symbol names.

### Fail-soft paired source

P10 visual initialization no longer fails merely because the paired divergence source cannot initialize, unless strict pair initialization is explicitly enabled.

- Paired source ready: divergence plus temporal anatomy.
- Paired source unavailable: attached-chart temporal anatomy remains active.
- Strict mode: previous fail-fast behavior remains available as an input.

### Single-symbol temporal fallback

When no paired periods are exportable or the attached chart is not one of the paired source symbols, P10 loads closed bars for the attached chart symbol, aggregates local Daily/Session/Subcycle periods through the same P01/P03 contracts, and renders the temporal anatomy on that chart.

This fallback has no hunt, divergence, lifecycle, direction, or execution authority.

### Diagnostics

Initialization now logs:

- configured and resolved symbol names;
- resolution reasons and scores;
- current chart symbol and timeframe;
- paired-source readiness;
- local fallback readiness or exact bar/history failure reason;
- chart-object kind, name, chart ID, geometry, price, and terminal error code when object creation fails.

## Preserved invariants

- SPX and NDX price scales remain separate.
- Divergence lines still require the paired P01–P07 source pipeline.
- Temporal fallback cannot fabricate divergence evidence.
- No forward fill or nearest-timestamp matching is introduced.
- All objects remain deterministic and prefix-owned.
- No order, position, risk, network, model, or execution authority is introduced.

## New inputs

- `InpAutoResolveBrokerSymbols = true`
- `InpPreferCurrentChartSymbol = true`
- `InpFailInitIfPairPipelineUnavailable = false`
- `InpAllowSingleSymbolTimeFallback = true`
- `InpLocalVisualMinimumBars = 60`
- `InpPrintDetailedInitDiagnostics = true`

## Runtime acceptance

On a `#USNDAQ100` chart:

1. The resolver must identify the chart as the NDX-side broker symbol.
2. It should locate a high-confidence SPX counterpart when available.
3. If no counterpart exists, the Expert must still initialize.
4. Daily, A/L/N/P, a1–p4, micro-quarter, GAP, TDO, and TWO layers must render from the attached chart history.
5. The log must state that divergence projection is unavailable until both symbols resolve.

## Rollback

Restore the previous four P10 files and remove `DAYE_SymbolResolver.mqh`. The previous behavior will again require exact configured broker symbols and a fully initialized paired source.
