# 16 - Implementation Checklist

## Phase 0: Documentation and test fixtures

- Confirm documentation is applied.
- Add deterministic synthetic data fixtures.
- Add expected output CSV samples.

## Phase 1: Core types

Create types for:

- STC day.
- M cycle.
- W cycle.
- Check candle.
- W reference.
- SMT candidate.
- Signal intent.
- Trade plan.
- Position action.
- Journal row.

## Phase 2: Time and cycle engine

Implement:

- New York conversion.
- STC day ID.
- M assignment.
- W assignment.
- Gap detection.
- Check-candle anchoring from 20:00.
- Final check candle detection.
- Hard-close time detection.

## Phase 3: Data and aggregation

Implement:

- Symbol1/Symbol2 data loader.
- Check-candle aggregator.
- W high/low builder.
- Completeness detector.
- Current-day data restriction.

## Phase 4: SMT detector

Implement:

- W reference matrix.
- Touch-only hunt detector.
- High/low SMT candidate builder.
- Clean/hunted symbol selector.
- Side mapper.
- Largest-stop reference selector.

## Phase 5: Confirmation and filtering

Implement:

- Check-candle close confirmation.
- Clean symbol late hunt invalidation.
- Final check candle expiration.
- Buy/sell ambiguity discard.
- Duplicate consumed signal filter.
- Entry STC audit-only filter.
- M trade limit filter.
- Hedging direction lock filter.

## Phase 6: Risk and trade planning

Implement:

- Entry price model.
- SL/TP calculation.
- Final Reward R multiple.
- Risk money.
- Tick value use.
- Contract Size fallback.
- Volume split plan.
- Below-min-volume skip.

## Phase 7: Research backtest

Implement:

- Chronological check-candle loop.
- Simulated entries at next check-candle open.
- SL/TP outcome with check candles.
- AMBIGUOUS outcome.
- Partial and hard close simulation.
- Gross and net reporting.

## Phase 8: Journals and restart persistence

Implement:

- Cycle audit.
- Check candle audit.
- SMT candidate audit.
- Signal journal.
- Trade journal.
- Position action journal.
- Daily summary.
- Consumed signal persistence.
- Restart reconstruction.

## Phase 9: Drawing

Implement:

- Cycle zones.
- W levels.
- Hunt markers.
- Signal markers.
- Trade lines.
- Partial/hard close markers.
- Dashboard.

## Phase 10: Paper live

Implement:

- OnTimer scheduler.
- Live data refresh.
- Paper trade creation.
- Paper position management.
- No delayed entry.
- Delayed partial/hard-close recovery.

## Phase 11: Auto trade

Implement only after research and paper validation:

- Market order send.
- Magic number ownership.
- Broker volume splitting.
- Order failure consumption.
- Close retry.
- Hard close recovery.

## Phase 12: Validation gates

Before live trading:

- All time/cycle tests pass.
- All W/reference tests pass.
- All SMT tests pass.
- All ambiguity tests pass.
- All risk tests pass.
- Restart tests pass.
- Duplicate instance tests pass.
- Hard close tests pass.
