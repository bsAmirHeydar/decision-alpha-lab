# 08 - Remaining Open Questions Before Implementation

Most core strategy ambiguities have been resolved by the owner. The remaining questions are implementation-level and reporting-level.

## Q1 - Exact touch operator

Owner decision: no tolerance.

Remaining implementation detail:

Should exact equality count as touch?

Recommended implementation:

- High hunt: high >= reference_high.
- Low hunt: low <= reference_low.

This is still no tolerance; it only defines equality behavior.

## Q2 - Backtest entry price wording

Owner approved next-bar open after check-candle close as good.

Implementation should document the exact convention:

- research/backtest: next check-bar open after confirmation;
- live: market order immediately after confirmation close.

Confirm whether this should be fixed or remain an input.

## Q3 - SL/TP intrabar ambiguity in coarse backtests

Owner accepted using the same check candle path for backtest at this stage.

Remaining detail:

If a single backtest candle touches both SL and TP, should the report assume:

- conservative SL-first;
- TP-first;
- ambiguous/excluded?

Recommended:

- conservative SL-first unless lower timeframe path is available.

## Q4 - Multiple reference selection mode

Owner approved closest reference by time and also allowed smallest-stop reference as an option.

Remaining detail:

Which should be the default production mode?

Recommended:

- Default: closest-by-time, strict SRS/owner rule.
- Research input: smallest-stop.

## Q5 - Event recording when simultaneous buy/sell occurs

Owner decision: do not trade.

Remaining detail:

Should the ambiguous event be marked consumed or can it be reconsidered on a later check candle if only one side remains?

Recommended:

- record ambiguous no-trade event;
- do not open trade;
- do not consume the underlying one-sided divergence permanently unless it remains ambiguous at its own confirmation close.

## Q6 - Live broker volume behavior

Owner decision: no strategy max-volume cap, but respect broker min/max.

Remaining detail:

If calculated volume exceeds broker max, should live execution:

- clamp to broker max and trade;
- reject/skip the trade;
- split into multiple orders?

Recommended first implementation:

- clamp to broker max only if explicitly enabled;
- otherwise skip and journal `BROKER_VOLUME_LIMIT`.

## Q7 - Entry OFF audit depth

Owner decision: scan and record, but do not trade.

Remaining detail:

Should Entry OFF record only confirmed signals or also raw/intrabar divergence states?

Recommended:

- record confirmed signals and skipped trade reason `ENTRY_OFF`.

## Q8 - Symbol mapping for CME vs broker execution

Owner decision: logic applies equally to SPX/NDX, ES/NQ, NAS100 equivalents.

Remaining detail:

For this specific STC EA, should Symbol1/Symbol2 be both data and execution symbols, or should we support separate data symbols and execution symbols?

Recommended first implementation:

- Symbol1/Symbol2 are both data and execution symbols.
- Add a later optional `DataSymbol -> ExecutionSymbol` mapping layer for CME-driven CFD execution.

## Q9 - Cost model details

Owner decision: add spread and commission.

Remaining detail:

Use fixed inputs, broker-reported spread, or both?

Recommended:

- report gross results;
- report net results using input spread points, slippage points, and commission per lot/contract.

## Q10 - Early close calendar

Owner decision: if data is missing or market is closed, do not trade.

Remaining detail:

Do we need an explicit holiday/early-close calendar in v1?

Recommended:

- v1: data-driven no-trade when bars are missing.
- v2: explicit calendar module.
