# 11 - Algorithm Layers

This document decomposes the STC strategy into independent algorithms.

## Layer 1: Time normalization

Inputs:

- Broker server time.
- Broker UTC offset input.
- Optional UTC timestamps from external data.

Outputs:

- New York timestamp.
- STC trading-day ID.
- M context.
- W context.
- Check-candle context.
- Hard-close status.

Algorithm:

1. Convert all timestamps into UTC.
2. Convert UTC into New York time with DST support.
3. Compute STC trading-day start and end.
4. Reject signal processing outside the active STC day.
5. Assign M, W, gap, and check-candle state.

## Layer 2: Data completeness

Inputs:

- Symbol1 bars.
- Symbol2 bars.
- Expected interval.

Outputs:

- Complete/incomplete flag.
- Missing count.
- Audit reason.

Algorithm:

1. For each interval required by the signal engine, load bars for both symbols.
2. Verify both symbols have complete coverage.
3. If either side is incomplete, reject signal logic for that interval.
4. Still write audit output.

## Layer 3: W builder

Inputs:

- Complete bars for a W interval.

Outputs:

- W high.
- W low.
- W open/close if needed for audit.
- Data coverage status.

Algorithm:

1. Collect bars inside W start inclusive and W end exclusive.
2. W high = maximum bar high.
3. W low = minimum bar low.
4. Mark complete only if required data exists for both symbols.

## Layer 4: Reference matrix

Inputs:

- Current W ID.
- Current M ID.
- W records for current STC day.

Outputs:

- Eligible reference W list.

Algorithm:

1. If W1, return empty list.
2. If W2, return W1.
3. If W3, return W2 and W1.
4. If W4, return W3, W2, and W1.
5. Exclude incomplete references.
6. Exclude references outside current M.
7. Exclude references from previous STC day.

## Layer 5: Hunt detector

Inputs:

- Completed check candle.
- Reference W high/low.

Outputs:

- high_hunted.
- low_hunted.

Algorithm:

1. high_hunted = check_candle.high >= reference.high.
2. low_hunted = check_candle.low <= reference.low.
3. Use no tolerance.
4. Do not require close beyond level.

## Layer 6: SMT detector

Inputs:

- Symbol1 hunt state.
- Symbol2 hunt state.
- Side.
- Reference W.

Outputs:

- SMT candidate or no candidate.

Algorithm:

1. If both hunted, no SMT.
2. If neither hunted, no SMT.
3. If Symbol1 hunted and Symbol2 did not, clean symbol is Symbol2.
4. If Symbol2 hunted and Symbol1 did not, clean symbol is Symbol1.
5. If side is high, setup side is sell.
6. If side is low, setup side is buy.

## Layer 7: Reference selector

Inputs:

- Candidate references.
- Clean traded symbol.
- Side.
- Entry price estimate.

Outputs:

- Selected reference.

Algorithm:

1. For each candidate reference, compute stop distance on clean symbol.
2. Select the candidate with largest stop distance.
3. If tie, select nearest in time.
4. If still tie, select deterministic W order: W3, then W2, then W1.

## Layer 8: Confirmation filter

Inputs:

- Candidate list at check-candle close.

Outputs:

- Confirmed trade intents.
- Rejected candidates.

Algorithm:

1. Reject if current check candle is final for M.
2. Reject if data incomplete.
3. Reject if clean symbol also hunted.
4. Discard if buy and sell both confirm in same check candle.
5. Resolve multiple references by largest stop.
6. Reject duplicates from consumed-signal journal.
7. Reject if Entry STC OFF, but audit.
8. Reject if M trade limit full.
9. Reject if direction lock disallows side.
10. Pass remaining intents to execution.

## Layer 9: Execution/risk

Inputs:

- Confirmed trade intent.
- Equity.
- Risk percent.
- Tick value / contract size.
- Broker volume limits.

Outputs:

- Entry price.
- SL.
- TP.
- Volume or split-order plan.

Algorithm:

1. Entry = next check-candle open in backtest, market after close in live.
2. SL = selected reference high/low on trade symbol.
3. Risk distance = abs(entry - SL).
4. TP = entry +/- FinalReward * risk distance.
5. Compute risk money.
6. Compute theoretical volume.
7. Normalize or split by broker constraints.
8. Skip if below broker minimum.

## Layer 10: Position management

Inputs:

- Open STC positions.
- Current time.
- Current/check candle prices.

Outputs:

- TP/SL/partial/hard-close actions.

Algorithm:

1. Always manage open positions, including gaps.
2. Evaluate outcome using check candles in backtest.
3. Mark both SL and TP in same candle as AMBIGUOUS.
4. At W4 end of M1/M2, perform partial if due.
5. At 15:30, perform hard close.
6. If partial/hard close missed, recover on restart.

## Layer 11: Persistence

Inputs:

- Signals.
- Trades.
- Position actions.
- Runtime state.

Outputs:

- Daily journal files.

Algorithm:

1. Write every signal and rejection reason.
2. Write every consumed signal.
3. Write every order attempt.
4. Write every position-management action.
5. On restart, load current STC day journals and open magic-number positions.

## Layer 12: Visualization

Inputs:

- Cycle records.
- W levels.
- Candidates.
- Trades.
- Position actions.

Outputs:

- Chart drawings.

Algorithm:

1. Draw M/W zones.
2. Draw W high/low reference levels.
3. Draw hunt markers.
4. Draw SMT confirmation markers.
5. Draw rejected/ambiguous markers.
6. Draw entry, SL, TP.
7. Draw partial and hard-close markers.
8. Keep drawings under one safe object prefix.
