# CG Implementation Checklist

## Inputs

- [ ] Symbol A input default `SPXUSD`.
- [ ] Symbol B input default `NDXUSD`.
- [ ] Broker UTC offset input default `3`.
- [ ] New York UTC offset input default `-4` or manually configurable.
- [ ] Risk percent input default `1.0`.
- [ ] Global trading enabled input.
- [ ] Global drawing enabled input.
- [ ] Per-CG trade ON/OFF for all 21 CGs.
- [ ] Per-CG draw ON/OFF for all 21 CGs.
- [ ] Per-CG color for all 21 CGs default black.

## Calendar

- [ ] Day starts at 18:00 NY.
- [ ] Day ends at 17:00 NY.
- [ ] Cycle index calculated from minutes after 18:00.
- [ ] Final incomplete cycles end at 17:00.
- [ ] First cycle has no reference cycle.

## Detection

- [ ] Use only closed chart candle.
- [ ] High hunt uses `>=`.
- [ ] Low hunt uses `<=`.
- [ ] Equal high/low counts as hunt.
- [ ] One high hunt only creates sell divergence.
- [ ] One low hunt only creates buy divergence.
- [ ] Both hunt = no divergence.
- [ ] Neither hunt = no divergence.

## Execution

- [ ] Trade clean symbol.
- [ ] Buy SL = clean reference low.
- [ ] Sell SL = clean reference high.
- [ ] Risk = 1% equity.
- [ ] Volume normalized to broker constraints.
- [ ] Exit scheduled at current cycle end.
- [ ] Duplicate signal keys prevented.

## Drawing

- [ ] Draw from hunter hunted level to confirmation close time.
- [ ] Use CG color input.
- [ ] Object names deterministic.
- [ ] No duplicate object creation.
- [ ] Avoid drawing wrong-symbol price levels on mismatched chart scale.

## Safety

- [ ] Missing symbol data skips signal.
- [ ] Invalid stop geometry skips trade.
- [ ] Near-cycle-end signal policy defined.
- [ ] Same-day registry resets at new 18:00 NY day.
- [ ] Open positions are closed at scheduled cycle end after restart.

