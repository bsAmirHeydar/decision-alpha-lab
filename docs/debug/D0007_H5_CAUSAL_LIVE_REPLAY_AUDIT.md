# D0007 — H5 Causal Live Replay Audit

D0007 is the root live-validity validator for H0005.  It exists because the old
`DAL_M0005_FINAL_*` report is a structural path report, not a live execution
proof.

## Contract

D0007 enforces four rules:

1. **Prefix-only decision data** — at every simulated decision step the engine
   loads only closed candles up to that cursor.
2. **Known-time regime state** — regime is not ordered by arbitrary sample id or
   entry order.  Samples that become known on the same candle are processed as a
   single batch.
3. **Same-candle batch policy** — if a candle confirms several highs/lows, those
   events are simultaneous.  If the batch contains both reversal and continuation
   labels, the regime is ambiguous and can be skipped.
4. **Post-entry measurement only** — future candles are used only after a causal
   candidate is activated and after a touch/break entry is triggered.

## Why this matters

In M0004/H0004 and H0005, several highs/lows can be confirmed on the same candle.
If the code sorts them by `id`, `entry_index`, or some incidental order, it can
invent a fake sequence such as `REVERSAL -> CONTINUATION -> REVERSAL` even though
all of those labels became knowable at the exact same candle.  D0007 treats this
as a batch.  Mixed-energy batches are counted as ambiguous rather than forced
into a false sequence.

## Families audited

D0007 can audit:

- reversal: regime energy is REVERSAL, candidate entry is later zone touch;
- continuation: regime energy is CONTINUATION, candidate entry is later node/zone
  break by close or intrabar high/low, depending on input;
- both.

## Key outputs

Look for:

```text
DAL_D0007_SUMMARY
```

Important fields:

```text
sameBarBatchSteps
ambiguousEnergySteps
mixedDirectionSteps
reversalRegimeSteps
continuationRegimeSteps
reversalCandidates
continuationCandidates
entered
entryRatePct
rewardHitPct
stopHitPct
expectancyR
profitFactor
```

`ambiguousEnergySteps` is especially important.  It shows how often the old
sequence-based reports might be pretending that simultaneous confirmations had a
clean order.
