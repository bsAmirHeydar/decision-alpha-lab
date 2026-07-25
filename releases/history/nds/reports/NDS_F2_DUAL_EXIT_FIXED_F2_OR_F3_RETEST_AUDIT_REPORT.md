# NDS F2 Dual Exit — Fixed F2 End or F3 Flag Retest

## Scope

This patch extends the dedicated lightweight `NDSF2WaistLimitBacktest` expert with two explicit exit modes while preserving the existing F2 Waist-Break Point-2 entry, F1-waist stop, minimum-RR repricing, overlap arbitration, hedge policy, and parallel-context ownership.

## Canonical interpretation

### Mode 1 — Fixed F2 Flag End

The existing behavior is unchanged:

1. Build the complete, not-yet-confirmed F2 two-leg body.
2. Place the Point-2 limit behind the F2 waist.
3. Place the stop behind the direct parent F1 waist.
4. Attach broker TP at the original F2 Leg2 endpoint.

### Mode 2 — F3 Flag Retest

The original F2 Leg2 endpoint remains the economic reference target used for:

- minimum reward/risk filtering;
- reward/risk entry repricing;
- pending target-consumption cancellation before fill.

It is not attached as broker TP.

After the position opens:

1. Wait for the exact source F2 to confirm.
2. Capture the F2 confirmation node. In the canonical NDS chain, this node is the F3 Leg1 node.
3. Wait for price to correct away from that node by the configured minimum number of ticks.
4. Arm TP at the captured confirmation/F3-Leg1 node.
5. Exit when price retests that node, which is the executable F3-flag-hit exit.
6. If the target is already reached before the broker TP can be attached, optionally close the exact position at market.

## Why RR is unchanged

The F3 retest target does not exist at setup creation. Using it for pre-entry RR would introduce future information. Therefore:

```text
RR reference = original F2 Leg2 endpoint
Actual dynamic exit = later F2-confirm / F3-Leg1 retest node
```

This preserves causal entry filtering.

## Runtime architecture

```text
Per new bar:
Canonical closed bars
→ F1/F2 fast detector
→ source-F2 confirmation matching
→ candidate and order processing

Per tick:
Dynamic context lookup only
→ pending consumption check
→ position binding
→ correction detection
→ TP arm / market-close fallback
```

The dynamic mode does not load the full F3 scanner. It reuses the canonical equivalence already present in the NDS anatomy: the F2 confirmation node is the first F3-leg node. This keeps the Strategy Tester runtime lightweight.

## Position ownership

Dynamic contexts are bound by:

1. accepted pending-order ticket;
2. order `POSITION_ID` / open position `POSITION_IDENTIFIER`;
3. broker comment as a fallback;
4. symbol, magic number, direction, timeframe, scale, source F2 origin/waist, source parent F1 waist.

This prevents one context from modifying another context's TP in hedging mode.

## Safety behavior

- Dynamic orders are initially submitted with `TP = 0`.
- If dynamic-context registration fails, the accepted pending order is removed.
- The original stop remains attached to the order and position.
- No full F3 detector, renderer, CSV, timer, chart object, AI, CG, or runtime print was added.
- Mode 1 remains backward-compatible.

## Inputs

```text
InpF2BTExitMode
InpF2BTF3ExitCorrectionTicks
InpF2BTCloseAtMarketIfF3TargetAlreadyReached
```

Default mode remains:

```text
FP_NDS_F2_EXIT_FIXED_F2_FLAG_END
```

## Version

```text
Expert: 1.50
Contract: NDS-F2-WAIST-BREAK-06
Schema: nds_f2_waist_break_point2_v6
```

## Validation performed

- Dual-exit contract QA: PASS
- Existing F2 Waist-Break Point-2 QA: PASS
- RR / parallel-context QA: PASS
- overlap-wider / RR-reprice QA: PASS
- lightweight backtest QA: PASS
- MQL5 compatibility: 0 errors, 0 warnings
- repository layout: 0 missing directories
- engineering policy: 0 errors, 0 warnings
- AI Engineering OS vault: 0 errors, 0 warnings
- project include resolution: PASS
- changed-MQL lexical balance: PASS
- ZIP integrity and manifest hashes: PASS

MetaEditor is not available in the patch-build environment. Final MQL5 compilation and real-tick Strategy Tester execution must be confirmed locally.
